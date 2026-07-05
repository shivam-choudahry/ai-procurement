"""
Recommendation Agent — generates evidence-backed vendor shortlisting recommendations.

All nodes are async; LLM calls use ainvoke via acall_llm,
json.dumps on large payloads is offloaded with asyncio.to_thread.
Observability handled automatically by Langfuse CallbackHandler.

Uses output_schema=BuyerRecommendation with method="json_schema" so the LLM
is constrained to the Pydantic model schema — no manual JSON parsing needed.
"""

import asyncio
import json
import logging
from datetime import datetime

from src.schemas.comparison import BuyerRecommendation
from src.prompts.prompt_library import RECOMMENDATION_SYSTEM_PROMPT, RECOMMENDATION_USER_PROMPT
from src.utils.llm import acall_llm, has_api_key, parse_json_response
from langfuse import observe

logger = logging.getLogger(__name__)

@observe
async def generate_recommendation(
    extractions: list,
    validations: list = None,
    comparison: dict = None,
) -> dict:
    """
    Generate per-vendor shortlisting recommendations.

    Args:
        extractions: List of VendorExtraction dicts
        validations: List of ValidationResult dicts
        comparison:  ComparisonMatrix dict

    Returns:
        BuyerRecommendation dict
    """
    if not has_api_key():
        return await asyncio.to_thread(_demo_recommendation, extractions)

    payload = {
        "extractions": extractions,
        "validations": validations or [],
        "comparison_summary": comparison or {},
    }
    payload_json = await asyncio.to_thread(json.dumps, payload, indent=2)
    user_prompt = RECOMMENDATION_USER_PROMPT.format(data_json=payload_json[:8000])

    # Primary: structured output via BuyerRecommendation Pydantic schema
    result = await acall_llm(
        system_prompt=RECOMMENDATION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_schema=BuyerRecommendation,
        temperature=0.2,
        step_name="recommendation",
    )

    # Fallback: if structured output fails, retry as plain text + manual parse
    if result is None:
        logger.warning("recommendation: structured output failed, retrying with method=None")
        raw = await acall_llm(
            system_prompt=RECOMMENDATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            method=None,
            temperature=0.2,
            step_name="recommendation_fallback",
        )
        result = parse_json_response(raw)

    if result is None or (isinstance(result, dict) and "error" in result):
        logger.warning(f"Recommendation failed: {(result or {}).get('error', 'LLM call failed')}")
        return await asyncio.to_thread(_demo_recommendation, extractions)

    if "recommendation_timestamp" not in result:
        result["recommendation_timestamp"] = datetime.now().isoformat()

    logger.info(f"Recommendations generated for {len(extractions)} vendors")
    return result


def _demo_recommendation(extractions: list) -> dict:
    """Generate a basic rule-based demo recommendation."""
    vendors = []
    for ex in extractions:
        vid        = ex.get("vendor_id", "")
        vname      = ex.get("vendor_name", "Unknown")
        quality    = ex.get("overall_data_quality", "LOW")
        risks      = ex.get("risks", [])
        high_risks = [r for r in risks if r.get("severity") == "high"]
        conflicts  = ex.get("conflicting_info", [])
        missing    = ex.get("missing_info", [])

        score = {"HIGH": 80, "MEDIUM": 55, "LOW": 35}.get(quality, 40)
        score -= len(high_risks) * 10
        score -= len(conflicts) * 15
        score -= len(missing) * 3
        score  = max(0, min(100, score))

        if score >= 65 and not high_risks:
            rec = "shortlist"
        elif score >= 40 or (high_risks and not conflicts):
            rec = "conditional"
        else:
            rec = "reject"

        risk_level = "HIGH" if high_risks or conflicts else ("MEDIUM" if missing else "LOW")

        vendors.append({
            "vendor_id": vid,
            "vendor_name": vname,
            "recommendation": rec,
            "confidence_score": score,
            "pros": [f"Data quality: {quality}"] + (["No critical conflicts detected"] if not conflicts else []),
            "cons": (
                ([f"{len(high_risks)} high-severity risks identified"] if high_risks else []) +
                ([f"{len(conflicts)} internal contradictions"] if conflicts else []) +
                ([f"{len(missing)} missing required fields"] if missing else [])
            ),
            "risk_level": risk_level,
            "conditions": (
                [f"Resolve {len(missing)} missing information gaps before final decision"]
                if rec == "conditional" else []
            ),
            "evidence_citations": [],
            "buyer_decision_notes": (
                "Based on rule-based analysis of extracted data. "
                "Enable AI recommendations (add OPENAI_API_KEY) for evidence-backed analysis."
            ),
        })

    return {
        "recommendation_id": "REC-DEMO-001",
        "recommendation_timestamp": datetime.now().isoformat(),
        "rfq_reference": "RFQ-MKT-2025-NKL-001",
        "vendors": vendors,
        "overall_summary": (
            f"Rule-based shortlisting across {len(vendors)} vendors. "
            "Add OPENAI_API_KEY for AI-powered evidence-backed recommendations."
        ),
        "next_steps": [
            "Resolve all HIGH-priority buyer flags before shortlisting",
            "Send clarification questions to vendors with MEDIUM/HIGH risk",
            "Schedule presentation slots for shortlisted vendors",
        ],
        "disclaimer": (
            "This recommendation is based solely on the information provided in vendor proposals. "
            "Final decision rests with the buyer."
        ),
    }
