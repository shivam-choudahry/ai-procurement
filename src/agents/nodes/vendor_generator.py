"""
Vendor Generator Agent — generates 5 distinct vendor persona responses.

All nodes are async; LLM calls use ainvoke via acall_llm,
json.dumps on large payloads is offloaded with asyncio.to_thread.
Observability handled automatically by Langfuse CallbackHandler.

Uses output_schema=VendorResponseList with method="json_schema". The wrapper
model is required because json_schema structured output requires a JSON object
at the top level — a bare JSON array is not supported.
"""

import asyncio
import json
import logging

from src.schemas.vendor import VendorResponseList
from src.prompts.prompt_library import VENDOR_RESPONSE_GENERATION_PROMPT
from src.utils.llm import acall_llm, parse_json_response
from langfuse import observe

logger = logging.getLogger(__name__)

@observe
async def generate_vendor_responses(rfq_context: dict = None) -> list:
    """
    Generate 5 distinct vendor responses with deliberate personas.

    Args:
        rfq_context: RFQ dict for context

    Returns:
        List of vendor response dicts
    """
    system_prompt = (
        "You are simulating realistic vendor proposal responses for the NourishKids "
        "brand launch RFQ. Generate all vendor responses in the 'vendors' array."
    )

    rfq_snippet = ""
    if rfq_context:
        rfq_json = await asyncio.to_thread(json.dumps, rfq_context, indent=2)
        rfq_snippet = f"RFQ Context (for grounding):\n{rfq_json[:2000]}"

    user_prompt = VENDOR_RESPONSE_GENERATION_PROMPT.format(rfq_context=rfq_snippet)

    # Primary: structured output via VendorResponseList Pydantic schema
    result = await acall_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        output_schema=VendorResponseList,
        temperature=0.7,
        step_name="vendor_generation",
    )

    # Fallback: if structured output fails, retry as plain text + manual parse
    if result is None:
        logger.warning("vendor_generation: structured output failed, retrying with method=None")
        raw = await acall_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            method=None,
            temperature=0.7,
            step_name="vendor_generation_fallback",
        )
        result = parse_json_response(raw)

    if result is None:
        logger.warning("Vendor generation failed: LLM call returned None")
        return []

    if isinstance(result, dict) and "error" in result:
        logger.warning(f"Vendor generation failed: {result.get('error', 'unknown error')}")
        return []

    # VendorResponseList schema returns {"vendors": [...]}
    vendors = (
        result.get("vendors", [])
        if isinstance(result, dict)
        else result  # fallback path may return a bare list
    )
    if not isinstance(vendors, list):
        vendors = []

    logger.info(f"Generated {len(vendors)} vendor responses")
    return vendors
