"""
UI Agent — generates buyer-journey optimized UI structure recommendations.

All nodes are async; LLM calls use ainvoke via acall_llm.
Observability handled automatically by Langfuse CallbackHandler.
"""

import logging

from src.prompts.prompt_library import UIUX_GENERATION_PROMPT
from src.utils.llm import acall_llm, has_api_key
from langfuse import observe

logger = logging.getLogger(__name__)

@observe
async def generate_ui_structure(context: dict = None) -> dict:
    """
    Generate buyer-facing UI structure with UX rationale.

    Args:
        context: Optional workflow context

    Returns:
        UI structure dict with screen definitions
    """
    if not has_api_key():
        return _default_ui_structure()

    system_prompt = (
        "You are a Senior Product Designer for B2B procurement tools. "
        "Output JSON only. No prose outside JSON."
    )

    result = await acall_llm(
        system_prompt=system_prompt,
        user_prompt=UIUX_GENERATION_PROMPT,
        temperature=0.3,
        step_name="ui_generation",
    )

    if result is None or (isinstance(result, dict) and "error" in result):
        return _default_ui_structure()

    return result


def _default_ui_structure() -> dict:
    """Default UI structure for demo mode."""
    return {
        "screens": [
            {"screen_name": "RFQ Overview", "icon": "🏠",
             "purpose": "Display the full RFQ including scope, timeline, compliance, and questionnaire",
             "primary_question": "What did we ask vendors to respond to?",
             "components": ["metrics", "tabs", "expanders", "dataframe"]},
            {"screen_name": "Vendor Responses", "icon": "📄",
             "purpose": "View all vendor proposals with quality indicators",
             "primary_question": "What proposals did we receive?",
             "components": ["cards", "badges", "flags", "full-text viewer"]},
            {"screen_name": "Upload", "icon": "📤",
             "purpose": "Upload new vendor documents for parsing and extraction",
             "primary_question": "How do I add a new vendor proposal?",
             "components": ["file_uploader", "form", "progress_bar"]},
            {"screen_name": "Extraction Review", "icon": "🔍",
             "purpose": "Per-vendor structured extraction with flags and evidence",
             "primary_question": "What did each vendor actually say?",
             "components": ["tabs", "badges", "evidence_boxes", "conflict_boxes", "dataframe"]},
            {"screen_name": "Vendor Comparison", "icon": "📊",
             "purpose": "Scorecard, comparison matrix, and key differentiators",
             "primary_question": "How do vendors compare?",
             "components": ["scorecard", "dataframe", "risk_matrix", "expanders"]},
            {"screen_name": "Risks", "icon": "⚠️",
             "purpose": "Buyer Risk Dashboard — traffic-light risk system per vendor",
             "primary_question": "What are the key risks and how do vendors compare on risk?",
             "components": ["risk_badges", "traffic_light", "confidence_bars", "recommendation_cards"]},
            {"screen_name": "Prompt Trace", "icon": "📝",
             "purpose": "Full AI audit trail — prompts, outputs, token usage",
             "primary_question": "How did the AI make its decisions?",
             "components": ["prompt_viewer", "trace_entries", "code_blocks"]},
        ]
    }
