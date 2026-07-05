"""
Validation Agent — validates extraction quality.

All nodes are async; LLM calls use ainvoke via acall_llm,
json.dumps on large payloads is offloaded with asyncio.to_thread.
Observability handled automatically by Langfuse CallbackHandler.

Uses output_schema=ValidationResult with method="json_schema" so the LLM
is constrained to the Pydantic model schema — no manual JSON parsing needed.
"""

import asyncio
import json
import logging
from datetime import datetime

from src.schemas.extraction import ValidationResult
from src.prompts.prompt_library import VALIDATION_SYSTEM_PROMPT, VALIDATION_USER_PROMPT
from src.utils.llm import acall_llm, has_api_key, parse_json_response
from langfuse import observe

logger = logging.getLogger(__name__)

@observe
async def validate_extraction(extraction: dict) -> dict:
    """
    Validate a vendor extraction for completeness and consistency.

    Args:
        extraction: VendorExtraction dict from extraction agent

    Returns:
        ValidationResult dict
    """
    vendor_id   = extraction.get("vendor_id", "unknown")
    vendor_name = extraction.get("vendor_name", "Unknown")

    if not has_api_key():
        return await asyncio.to_thread(_rule_based_validation, extraction)

    extraction_json = await asyncio.to_thread(json.dumps, extraction, indent=2)
    user_prompt = VALIDATION_USER_PROMPT.format(
        vendor_id=vendor_id,
        vendor_name=vendor_name,
        extraction_json=extraction_json,
    )

    # Primary: structured output via ValidationResult Pydantic schema
    result = await acall_llm(
        system_prompt=VALIDATION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_schema=ValidationResult,
        temperature=0.1,
        step_name="validation",
    )

    # Fallback: if structured output fails, retry as plain text + manual parse
    if result is None:
        logger.warning(f"validation [{vendor_id}]: structured output failed, retrying with method=None")
        raw = await acall_llm(
            system_prompt=VALIDATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            method=None,
            temperature=0.1,
            step_name="validation_fallback",
        )
        result = parse_json_response(raw)

    if result is None or (isinstance(result, dict) and "error" in result):
        return await asyncio.to_thread(_rule_based_validation, extraction)

    if "validation_timestamp" not in result:
        result["validation_timestamp"] = datetime.now().isoformat()

    logger.info(f"Validation for {vendor_name}: passed={result.get('passed')}, score={result.get('overall_quality_score')}")
    return result


def _rule_based_validation(extraction: dict) -> dict:
    """
    Rule-based validation without LLM — used in demo mode.
    Checks required fields and obvious contradictions.
    """
    vendor_id   = extraction.get("vendor_id", "unknown")
    vendor_name = extraction.get("vendor_name", "Unknown")

    issues        = []
    missing_required = []
    contradictions   = []
    score = 100

    pricing = extraction.get("pricing", {})
    if not pricing.get("total_stated"):
        missing_required.append("pricing.total_stated")
        score -= 20
    if not pricing.get("currency"):
        missing_required.append("pricing.currency")
        score -= 10

    timeline = extraction.get("timeline", {})
    duration = timeline.get("total_duration", {})
    if not duration.get("value"):
        missing_required.append("timeline.total_duration")
        score -= 10

    compliance = extraction.get("compliance", {})
    if compliance.get("asci_kids_code", {}).get("status") == "missing":
        missing_required.append("compliance.asci_kids_code")
        score -= 15
    if compliance.get("fssai_health_claims", {}).get("status") == "missing":
        missing_required.append("compliance.fssai_health_claims")
        score -= 15

    if pricing.get("consistency_check") == "FAIL":
        contradictions.append("Pricing: stated total does not match itemized total")
        score -= 15
    if timeline.get("consistency_check") == "FAIL":
        contradictions.append("Timeline: stated duration contradicts detailed phase plan")
        score -= 15

    for field in missing_required:
        issues.append({"issue_type": "missing", "field": field,
                       "description": f"Required field '{field}' is missing from vendor response",
                       "severity": "high"})
    for contradiction in contradictions:
        issues.append({"issue_type": "contradiction", "field": "multiple",
                       "description": contradiction, "severity": "high"})

    score  = max(0, score)
    passed = score >= 60 and not any(i.get("severity") == "high" for i in issues)

    return {
        "vendor_id": vendor_id,
        "vendor_name": vendor_name,
        "validation_timestamp": datetime.now().isoformat(),
        "passed": passed,
        "issues": issues,
        "missing_required": missing_required,
        "contradictions": contradictions,
        "unsupported_claims": [],
        "overall_quality_score": score,
        "validation_summary": (
            f"Rule-based validation: {len(issues)} issues found. "
            f"Quality score: {score}/100. "
            f"{'PASSED' if passed else 'FAILED'} minimum threshold."
        ),
    }
