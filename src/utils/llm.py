from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from pydantic import BaseModel

# Load .env so os.getenv() can see all vars (AZURE_API_KEY, etc.)
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env", override=False)

logger = logging.getLogger(__name__)


# ── Langfuse observability ────────────────────────────────────────────────────

class LangfuseHelper:
    """
    Initialise Langfuse tracing.

    Observability is handled automatically by the Langfuse CallbackHandler
    attached to the LLM in LLMFactory.get_model() — no manual trace_entry needed.
    """

    @staticmethod
    def setup():
        """Initialize and return a Langfuse client. Returns None if not configured."""
        public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
        secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")
        host       = os.getenv("LANGFUSE_HOST", None)

        if not public_key or not secret_key:
            return None

        try:
            from langfuse import Langfuse
            client = Langfuse(public_key=public_key, secret_key=secret_key, host=host)
            logger.info("Langfuse client initialised")
            return client
        except ImportError:
            logger.debug("langfuse package not installed — tracing disabled")
            return None
        except Exception as e:
            logger.exception(f"Langfuse initialisation failed: {e}")
            return None


# ── LLM Factory ───────────────────────────────────────────────────────────────

class LLMFactory:
    """
    Factory to initialize and manage LLM instances.

    - llm_env()            : set OPENAI / Azure env vars from .env
    - get_model()          : init_chat_model with optional Langfuse callbacks
    - get_singleton_model(): cached singleton for repeated agent calls
    """

    _llm_instance = None

    def __init__(self):
        self.langfuse_enabled = bool(
            os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")
        )
        self.llm_env()

    @staticmethod
    def llm_env():
        """Set LLM environment variables."""
        os.environ["OPENAI_API_VERSION"]      = os.getenv("AZURE_API_VERSION", "")
        os.environ["AZURE_OPENAI_DEPLOYMENT"] = os.getenv("AZURE_DEPLOYMENT", "")
        os.environ["AZURE_OPENAI_ENDPOINT"]   = os.getenv("AZURE_API_BASE", "")
        os.environ["AZURE_OPENAI_API_KEY"]    = os.getenv("AZURE_API_KEY", "")
        os.environ["AZURE_OPENAI_API_TYPE"]   = "azure"

    def get_model(self, model_name: str | None = None, streaming: bool = False):
        """
        Initialize and return a chat model.

        Attaches Langfuse CallbackHandler when credentials are configured so that
        every LLM invocation is automatically traced — no manual trace_entry needed.
        """
        self.llm_env()

        model_name    = model_name or os.getenv("OPENAI_MODEL", "gpt-5.4")
        openai_key    = os.getenv("OPENAI_API_KEY", "")
        azure_key     = os.getenv("AZURE_API_KEY", "") or os.getenv("AZURE_OPENAI_API_KEY", "")

        if not openai_key and not azure_key:
            return None

        if openai_key and openai_key.startswith("sk-..."):
            return None

        if self.langfuse_enabled:
            LangfuseHelper.setup()
            try:
                from langfuse.langchain import CallbackHandler
                langfuse_handler = CallbackHandler()
            except Exception as exe:
                langfuse_handler = None
                logger.info(f"LangFuse initialisation failed: {exe}")
        else:
            langfuse_handler = None

        temperature = 1 if model_name == "gpt-5-mini" else 0

        logger.info(f"Initialising LLM: azure_openai:{model_name}")
        try:
            from langchain.chat_models import init_chat_model
            return init_chat_model(
                f"azure_openai:{model_name}",
                temperature=temperature,
                azure_deployment="gpt-5-chat",
                streaming=streaming,
                callbacks=[langfuse_handler] if langfuse_handler else None,
            )
        except Exception as e:
            logger.exception(f"Error creating chat model: {e}")
            raise

    @classmethod
    def get_singleton_model(cls, model_name: str | None = None):
        """Return a cached singleton LLM instance."""
        if cls._llm_instance is None:
            logger.info("Creating singleton LLM instance")
            instance = cls().get_model(model_name)
            cls._llm_instance = instance
        return cls._llm_instance

    @classmethod
    def reset_singleton(cls):
        """Force recreation of the singleton (useful after env changes)."""
        cls._llm_instance = None


# ── Prompt / message helpers ──────────────────────────────────────────────────

def _build_prompt(system_prompt, user_prompt):
    """
    Build a ChatPromptTemplate from static system + human content.

    By passing LangGraph Message objects (not string tuples), LangChain treats
    the content as completely static — JSON examples with { } are never parsed
    as template variables.  The chain is then invoked with an empty dict: {}.

    Pattern (mirrors rfq_generator.py):
        chain = _build_prompt(sys, usr) | llm
        response = chain.invoke({})

    Accepts str or PromptTemplate for both arguments; PromptTemplate objects
    are coerced to their raw template string so Pydantic validation passes.
    """
    from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
    from langchain_core.messages import SystemMessage, HumanMessage

    def _to_str(p) -> str:
        if isinstance(p, PromptTemplate):
            return p.template
        return str(p) if p is not None else ""

    return ChatPromptTemplate.from_messages([
        SystemMessage(content=_to_str(system_prompt)),
        HumanMessage(content=_to_str(user_prompt)),
    ])

# ── call_llm — structured output / plain text response ───────────────────────

def call_llm(
    system_prompt: str,
    user_prompt: str,
    inputs: Dict[str, Any] | None = None,
    output_schema: Optional[Any] = None,
    model: str | None = None,
    method: str | None = "json_schema",
    temperature: float | None = None,
    step_name: str = "llm_call",
) -> dict | str | None:
    """
    Call an LLM with optional structured output.

    - method=None          → plain LLM, returns raw string
    - method set, no schema → generic schema → raw dict
    - method set, schema    → schema.model_json_schema() → raw dict
    """
    llm = LLMFactory.get_singleton_model(model)
    if llm is None:
        logger.warning(f"[{step_name}] No LLM available.")
        return None

    if temperature is not None:
        llm = llm.bind(temperature=temperature)

    prompt = _build_prompt(system_prompt, user_prompt)

    if method is None:
        chain = prompt | llm
    else:
        schema = (
            output_schema.model_json_schema()
            if output_schema is not None
            else {"title": "Response", "type": "object", "additionalProperties": True}
        )
        chain = prompt | llm.with_structured_output(schema, method=method)

    prompt_vars = set(getattr(prompt, "input_variables", (inputs or {}).keys()))
    filtered = {k: v for k, v in (inputs or {}).items() if k in prompt_vars and v is not None}

    try:
        response = chain.invoke(filtered)

        if method is None:
            if hasattr(response, "content"):
                return response.content
            if isinstance(response, BaseModel):
                return response.model_dump(mode="json", exclude_none=True)
            return response

        if isinstance(response, dict):
            json_res = response
        elif isinstance(response, BaseModel):
            json_res = response.model_dump(mode="json", exclude_none=True)
        elif isinstance(response, str):
            json_res = json.loads(response)
        else:
            raise TypeError(f"Unexpected structured output type: {type(response)}")

        if output_schema is not None:
            validated = output_schema.model_validate(json_res)
            return validated.model_dump(mode="json", exclude_none=True)

        return json_res

    except Exception as e:
        logger.exception(f"[{step_name}] LLM call failed: {e}")
        return None


# ── acall_llm — async variant (uses ainvoke) ──────────────────────────────────

async def acall_llm(
    system_prompt: str,
    user_prompt: str,
    inputs: Dict[str, Any] | None = None,
    output_schema: Optional[Any] = None,
    model: str | None = None,
    method: str | None = "json_schema",
    temperature: float | None = None,
    step_name: str = "acall_llm",
) -> dict | str | None:
    """
    Async version of call_llm — identical behavior but uses chain.ainvoke.

    - method=None          → plain LLM, returns raw string
    - method set, no schema → generic schema → raw dict
    - method set, schema    → schema.model_json_schema() → raw dict
    """
    llm = LLMFactory.get_singleton_model(model)
    if llm is None:
        logger.warning(f"[{step_name}] No LLM available.")
        return None

    if temperature is not None:
        llm = llm.bind(temperature=temperature)

    prompt = _build_prompt(system_prompt, user_prompt)

    if method is None:
        chain = prompt | llm
    else:
        schema = (
            output_schema.model_json_schema()
            if output_schema is not None
            else {"title": "Response", "type": "object", "additionalProperties": True}
        )
        chain = prompt | llm.with_structured_output(schema, method=method)

    prompt_vars = set(getattr(prompt, "input_variables", (inputs or {}).keys()))
    filtered = {k: v for k, v in (inputs or {}).items() if k in prompt_vars and v is not None}

    try:
        response = await chain.ainvoke(filtered)

        if method is None:
            if hasattr(response, "content"):
                return response.content
            if isinstance(response, BaseModel):
                return response.model_dump(mode="json", exclude_none=True)
            return response

        if isinstance(response, dict):
            json_res = response
        elif isinstance(response, BaseModel):
            json_res = response.model_dump(mode="json", exclude_none=True)
        elif isinstance(response, str):
            json_res = json.loads(response)
        else:
            raise TypeError(f"Unexpected structured output type: {type(response)}")

        if output_schema is not None:
            validated = output_schema.model_validate(json_res)
            return validated.model_dump(mode="json", exclude_none=True)

        return json_res

    except Exception as e:
        logger.exception(f"[{step_name}] Async LLM call failed: {e}")
        return None


# ── JSON response parser ──────────────────────────────────────────────────────

def parse_json_response(response) -> dict | list | None:
    """
    Parse a JSON result from an LLM response.

    Handles three cases:
    - Already a dict/list (structured output path): returned as-is
    - A plain string: tries json.loads, then markdown code-block extraction,
      then first-brace heuristic
    - None: returns None

    Use this after acall_llm(method=None) where the model returns the JSON
    schema embedded in the prompt as raw text.
    """
    import re

    if response is None:
        return None
    if isinstance(response, (dict, list)):
        return response
    if not isinstance(response, str):
        return None

    text = response.strip()

    # 1. Direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. Markdown code block  ```json … ```
    match = re.search(r"```(?:json)?\s*(\{.*?}|\[.*?])\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # 3. First-brace / first-bracket heuristic
    for start_char, end_char in [("{", "}"), ("[", "]")]:
        start = text.find(start_char)
        end   = text.rfind(end_char)
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass

    logger.warning("parse_json_response: could not parse LLM response as JSON")
    return None


# ── Convenience helpers ───────────────────────────────────────────────────────

def has_api_key() -> bool:
    """Return True if usable LLM credentials are configured."""
    from src.config import get_settings
    return get_settings().has_api_key
