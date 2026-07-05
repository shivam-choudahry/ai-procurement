"""
Comparator Agent — vendor comparison using extracted data.

All nodes are async; LLM calls use ainvoke via acall_llm,
json.dumps on large payloads is offloaded with asyncio.to_thread.
Observability handled automatically by Langfuse CallbackHandler.

Uses output_schema=ComparisonMatrix with method="json_schema" so the LLM
is constrained to the Pydantic model schema — no manual JSON parsing needed.
"""

import asyncio
import json
import logging
from datetime import datetime

from src.schemas.comparison import ComparisonMatrix
from src.prompts.prompt_library import COMPARISON_SYSTEM_PROMPT, COMPARISON_USER_PROMPT
from src.utils.llm import acall_llm, has_api_key, parse_json_response
from langfuse import observe

logger = logging.getLogger(__name__)

@observe
async def compare_vendors(extractions: list) -> dict:
    """
    Compare vendors using their extracted data.

    Args:
        extractions: List of VendorExtraction dicts

    Returns:
        ComparisonMatrix dict
    """
    if not has_api_key():
        from data.comparison_data import COMPARISON_DATA
        return COMPARISON_DATA

    extraction_dict = {e.get("vendor_id", f"V{i}"): e for i, e in enumerate(extractions)}
    extractions_json = await asyncio.to_thread(json.dumps, extraction_dict, indent=2)

    user_prompt = COMPARISON_USER_PROMPT.format(vendor_extractions_json=extractions_json)

    # Primary: structured output via ComparisonMatrix Pydantic schema
    result = await acall_llm(
        system_prompt=COMPARISON_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_schema=ComparisonMatrix,
        temperature=0.1,
        step_name="comparison",
    )

    # Fallback: if structured output fails, retry as plain text + manual parse
    if result is None:
        logger.warning("comparison: structured output failed, retrying with method=None")
        raw = await acall_llm(
            system_prompt=COMPARISON_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            method=None,
            temperature=0.1,
            step_name="comparison_fallback",
        )
        result = parse_json_response(raw)

    if result is None or (isinstance(result, dict) and "error" in result):
        logger.warning(f"Comparison failed: {(result or {}).get('error', 'LLM call failed')}")
        from data.comparison_data import COMPARISON_DATA
        return COMPARISON_DATA

    if "comparison_timestamp" not in result:
        result["comparison_timestamp"] = datetime.now().isoformat()

    logger.info(f"Comparison complete for {len(extractions)} vendors")
    return result
