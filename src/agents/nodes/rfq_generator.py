"""
RFQ Generator Agent — generates structured RFQ from a procurement brief.

All nodes are async; LLM calls use ainvoke via acall_llm.
Observability: handled automatically by Langfuse CallbackHandler.
"""

import logging

from src.schemas.rfq import RFQ
from src.prompts.prompt_library import RFQ_GENERATION_PROMPT
from src.utils.llm import acall_llm, parse_json_response
from langfuse import observe

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "You are a Senior Procurement Manager generating a formal RFQ document. "
    "Fill every field with realistic, specific procurement content. "
    "Do not leave fields empty or use placeholder text."
)

@observe
async def generate_rfq_from_brief(brief: str = "") -> dict:
    """
    Generate a structured RFQ from a procurement brief.

    Args:
        brief: Optional additional context/brief text

    Returns:
        RFQ dict or {"error": "..."} on failure
    """
    user_prompt = RFQ_GENERATION_PROMPT.format(
        brief=f"Additional brief context:\n{brief}" if brief.strip() else ""
    )

    # Try structured output via Pydantic schema first
    result = await acall_llm(
        system_prompt=_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_schema=RFQ,
        step_name="rfq_generation",
    )

    # Fallback: plain text output → parse JSON (handles models that ignore function_calling schema)
    if result is None:
        logger.warning("rfq_generation: structured output failed, retrying with method=None")
        raw = await acall_llm(
            system_prompt=_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            method=None,
            step_name="rfq_generation_fallback",
        )
        result = parse_json_response(raw)

    if result is None:
        return {"error": "No API key configured or LLM call failed. Set OPENAI_API_KEY / AZURE_API_KEY in .env."}

    logger.info(f"RFQ generated: {result.get('rfq_id', 'unknown')}")
    return result
