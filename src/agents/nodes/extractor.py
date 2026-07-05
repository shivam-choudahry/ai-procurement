"""
Extraction Agent — structured extraction of vendor responses.

All nodes are async; LLM calls use ainvoke via acall_llm,
heavy sync I/O (json.dumps) is offloaded with asyncio.to_thread.
Observability handled automatically by Langfuse CallbackHandler.

Uses output_schema=VendorExtraction with method="json_schema" so the LLM
is constrained to the Pydantic model schema — no manual JSON parsing needed.
"""

import asyncio
import logging
from datetime import datetime

from src.schemas.extraction import VendorExtraction
from src.prompts.prompt_library import EXTRACTION_SYSTEM_PROMPT, EXTRACTION_USER_PROMPT
from src.utils.llm import acall_llm, has_api_key, parse_json_response
from langfuse import observe

logger = logging.getLogger(__name__)

@observe
async def extract_vendor_response(
    vendor_id: str,
    vendor_name: str,
    response_text: str,
) -> dict:
    """
    Run the extraction agent on a single vendor response.
    Returns extraction dict (or error dict).
    """
    if not has_api_key():
        from data.extracted_data import EXTRACTED_DATA
        demo = EXTRACTED_DATA.get(vendor_id)
        if demo:
            logger.info(f"Demo mode: returning cached extraction for {vendor_id}")
            return demo
        return {
            "error": "No API key configured",
            "vendor_id": vendor_id,
            "vendor_name": vendor_name,
        }

    user_prompt = EXTRACTION_USER_PROMPT.format(
        vendor_id=vendor_id,
        vendor_name=vendor_name,
        vendor_response_text=response_text,
    )

    # Primary: structured output via VendorExtraction Pydantic schema
    result = await acall_llm(
        system_prompt=EXTRACTION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_schema=VendorExtraction,
        temperature=0.1,
        step_name="extraction",
    )

    # Fallback: if structured output fails, retry as plain text + manual parse
    if result is None:
        logger.warning(f"extraction [{vendor_id}]: structured output failed, retrying with method=None")
        raw = await acall_llm(
            system_prompt=EXTRACTION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            method=None,
            temperature=0.1,
            step_name="extraction_fallback",
        )
        result = parse_json_response(raw)

    if result is None or (isinstance(result, dict) and "error" in result):
        return {"error": (result or {}).get("error", "LLM call failed"), "vendor_id": vendor_id, "vendor_name": vendor_name}

    if "extraction_timestamp" not in result:
        result["extraction_timestamp"] = datetime.now().isoformat()

    logger.info(f"Extraction complete for {vendor_name}: quality={result.get('overall_data_quality', 'unknown')}")
    return result


async def extract_all_vendors(vendors: list) -> dict:
    """
    Run extraction concurrently on a list of vendor dicts.
    Returns dict mapping vendor_id -> extraction result.
    """
    async def _extract(vendor: dict) -> tuple[str, dict]:
        vid = vendor.get("vendor_id") or vendor.get("id", "")
        result = await extract_vendor_response(
            vendor_id=vid,
            vendor_name=vendor.get("vendor_name", "Unknown"),
            response_text=vendor.get("response_text", ""),
        )
        return vid, result

    pairs = await asyncio.gather(*[_extract(v) for v in vendors])
    return dict(pairs)
