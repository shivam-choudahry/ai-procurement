"""
LangGraph workflow definition for RFQ AI Procurement Copilot.

All nodes are async; LLM calls use ainvoke via acall_llm,
other sync I/O uses asyncio.to_thread.

Workflow:
START → [route_rfq_workflow] → generate_rfq → generate_vendors → parse_documents
      → extract_information → validate_extraction → compare_vendors
      → generate_recommendation → END

Each potentially-skippable node has a dedicated router function that is called
AFTER the preceding node to decide whether to RUN the next node or SKIP it.
All routing decisions are logged explicitly:
  ▶  [RUN ]  — node will execute
  ⏭  [SKIP]  — node bypassed, jumping ahead

Observability: all LLM calls are automatically traced via Langfuse CallbackHandler
attached in LLMFactory.get_model() — no manual prompt_trace node needed.
"""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime

from src.agents.state import RFQWorkflowState

from langfuse import observe

logger = logging.getLogger(__name__)


# ─── Router functions ────────────────────────────────────────────────────────
# Each router is called by add_conditional_edges AFTER the preceding node.
# Returns "run" to execute the next node, or "skip" to jump past it.

def route_rfq_workflow(state: RFQWorkflowState) -> str:
    """
    Entry-point router called from START.
    Cascades through all skip checks to find the first node that needs to run.
    """
    # ── Check 1: generate_rfq ───────────────────────────────────────────────
    if not state.get("rfq"):
        logger.info("▶  [RUN ] generate_rfq        — no RFQ found in state")
        return "generate_rfq"
    logger.info("⏭  [SKIP] generate_rfq        — RFQ already seeded in state")

    # ── Check 2: generate_vendors ───────────────────────────────────────────
    if not state.get("vendor_responses"):
        logger.info("▶  [RUN ] generate_vendors    — no vendor responses in state")
        return "generate_vendors"
    logger.info(f"⏭  [SKIP] generate_vendors    — {len(state['vendor_responses'])} vendor(s) already in state")

    # ── Check 3: parse_documents ────────────────────────────────────────────
    if state.get("uploaded_documents"):
        logger.info(f"▶  [RUN ] parse_documents     — {len(state['uploaded_documents'])} uploaded doc(s) to parse")
        return "parse_documents"
    logger.info("⏭  [SKIP] parse_documents     — no uploaded_documents in state")

    # ── Check 4: extract_information ────────────────────────────────────────
    vendors     = state.get("vendor_responses", [])
    existing_ids = {e.get("vendor_id") for e in state.get("vendor_extractions", [])}
    pending     = [v for v in vendors if (v.get("vendor_id") or v.get("id", "")) not in existing_ids]
    if pending:
        logger.info(f"▶  [RUN ] extract_information — {len(pending)} vendor(s) pending extraction")
        return "extract_information"
    logger.info(f"⏭  [SKIP] extract_information — all {len(vendors)} vendor(s) already extracted")

    # All pre-work done — jump straight to validation
    logger.info("▶  [RUN ] validate_extraction  — proceeding to validation")
    return "validate_extraction"


def route_after_rfq(state: RFQWorkflowState) -> str:
    """After generate_rfq: run or skip generate_vendors."""
    if not state.get("vendor_responses"):
        logger.info("▶  [RUN ] generate_vendors    — no vendor responses in state")
        return "run"
    logger.info(f"⏭  [SKIP] generate_vendors    — {len(state['vendor_responses'])} vendor(s) already in state")
    return "skip"


def route_after_vendors(state: RFQWorkflowState) -> str:
    """After generate_vendors: run or skip parse_documents."""
    if state.get("uploaded_documents"):
        logger.info(f"▶  [RUN ] parse_documents     — {len(state['uploaded_documents'])} uploaded doc(s) to parse")
        return "run"
    logger.info("⏭  [SKIP] parse_documents     — no uploaded_documents in state")
    return "skip"


def route_after_parse(state: RFQWorkflowState) -> str:
    """After parse_documents: run or skip extract_information."""
    vendors      = state.get("vendor_responses", [])
    existing_ids = {e.get("vendor_id") for e in state.get("vendor_extractions", [])}
    pending      = [v for v in vendors if (v.get("vendor_id") or v.get("id", "")) not in existing_ids]
    if pending:
        logger.info(f"▶  [RUN ] extract_information — {len(pending)} vendor(s) pending extraction")
        return "run"
    logger.info(f"⏭  [SKIP] extract_information — all {len(vendors)} vendor(s) already extracted")
    return "skip"


# ─── Node functions (all async) ─────────────────────────────────────────────
# Nodes no longer contain skip guards — routing is handled exclusively by
# the router functions above. Nodes focus only on their core work.

@observe
async def node_generate_rfq(state: RFQWorkflowState) -> RFQWorkflowState:
    """Generate RFQ document via LLM or load from static data."""
    from src.utils.llm import has_api_key, acall_llm, parse_json_response
    from data.rfq_data import RFQ_DATA
    from src.prompts.prompt_library import RFQ_GENERATION_PROMPT

    logger.info("Node: generate_rfq — executing")

    if has_api_key():
        raw = await acall_llm(
            system_prompt="You are a procurement expert. Output JSON only.",
            user_prompt=RFQ_GENERATION_PROMPT,
            method=None,
            step_name="rfq_generation",
        )
        result = parse_json_response(raw)
        rfq = result if result and "error" not in result else RFQ_DATA
    else:
        rfq = RFQ_DATA

    return {**state, "rfq": rfq}


@observe
async def node_generate_vendors(state: RFQWorkflowState) -> RFQWorkflowState:
    """Generate vendor responses via LLM or load from static data."""
    from src.utils.llm import has_api_key, acall_llm, parse_json_response
    from data.vendor_data import VENDOR_RESPONSES
    from src.prompts.prompt_library import VENDOR_RESPONSE_GENERATION_PROMPT

    logger.info("Node: generate_vendors — executing")

    if has_api_key():
        rfq_json    = await asyncio.to_thread(json.dumps, state.get("rfq", {}), indent=2)
        user_prompt = f"RFQ Context:\n{rfq_json[:2000]}\n\n{VENDOR_RESPONSE_GENERATION_PROMPT}"
        raw = await acall_llm(
            system_prompt="You are simulating vendor responses. Output JSON array only.",
            user_prompt=user_prompt,
            method=None,
            step_name="vendor_generation",
        )
        result = parse_json_response(raw)
        if result and not (isinstance(result, dict) and "error" in result):
            vendors = result if isinstance(result, list) else result.get("vendors", list(VENDOR_RESPONSES))
        else:
            vendors = list(VENDOR_RESPONSES)
    else:
        vendors = list(VENDOR_RESPONSES)

    return {**state, "vendor_responses": vendors}


@observe
async def node_parse_documents(state: RFQWorkflowState) -> RFQWorkflowState:
    """Parse uploaded documents into plain text."""
    from parser import parse_document

    logger.info("Node: parse_documents — executing")
    uploaded        = state.get("uploaded_documents", [])
    parsed_existing = state.get("parsed_documents", [])
    already_parsed_ids = {p["vendor_id"] for p in parsed_existing}

    new_parsed = list(parsed_existing)
    for doc in uploaded:
        if doc["vendor_id"] in already_parsed_ids:
            continue
        raw  = doc.get("raw_bytes") or b""
        text = await asyncio.to_thread(parse_document, doc["filename"], raw) if raw else ""
        new_parsed.append({
            "vendor_id":    doc["vendor_id"],
            "vendor_name":  doc["vendor_name"],
            "filename":     doc["filename"],
            "text":         text,
            "parse_method": doc.get("file_type", "unknown"),
        })

    logger.info(f"Node: parse_documents — parsed {len(new_parsed) - len(parsed_existing)} new doc(s)")
    return {**state, "parsed_documents": new_parsed}


@observe
async def node_extract_information(state: RFQWorkflowState) -> RFQWorkflowState:
    """Run extraction agent concurrently on all pending vendor responses."""
    from src.agents.nodes.extractor import extract_vendor_response

    logger.info("Node: extract_information — executing")
    vendors              = state.get("vendor_responses", [])
    parsed_docs          = state.get("parsed_documents", [])
    existing_extractions = state.get("vendor_extractions", [])
    existing_ids         = {e.get("vendor_id") for e in existing_extractions}

    to_extract = [
        (v.get("vendor_id") or v.get("id", ""), v.get("vendor_name", "Unknown"), v.get("response_text", ""))
        for v in vendors if (v.get("vendor_id") or v.get("id", "")) not in existing_ids
    ] + [
        (d.get("vendor_id", ""), d.get("vendor_name", "Unknown"), d.get("text", ""))
        for d in parsed_docs
        if d.get("vendor_id", "") not in existing_ids
        and not any(e.get("vendor_id") == d.get("vendor_id") for e in existing_extractions)
    ]

    logger.info(f"Node: extract_information — extracting {len(to_extract)} vendor(s) concurrently")
    new_results = await asyncio.gather(*[
        extract_vendor_response(vendor_id=vid, vendor_name=name, response_text=text)
        for vid, name, text in to_extract
    ])

    return {**state, "vendor_extractions": list(existing_extractions) + list(new_results)}


@observe
async def node_validate_extraction(state: RFQWorkflowState) -> RFQWorkflowState:
    """Run validation agent concurrently on all extractions."""
    from src.agents.nodes.validator import validate_extraction

    logger.info("Node: validate_extraction — executing")
    extractions          = state.get("vendor_extractions", [])
    existing_validations = state.get("validation_results", [])
    validated_ids        = {v.get("vendor_id") for v in existing_validations}

    to_validate = [e for e in extractions if e.get("vendor_id", "") not in validated_ids]
    logger.info(f"Node: validate_extraction — validating {len(to_validate)} extraction(s) concurrently")

    new_results = await asyncio.gather(*[
        validate_extraction(extraction=e) for e in to_validate
    ])

    return {**state, "validation_results": list(existing_validations) + list(new_results)}


@observe
async def node_compare_vendors(state: RFQWorkflowState) -> RFQWorkflowState:
    """Run comparison agent across all vendor extractions."""
    from src.agents.nodes.comparator import compare_vendors

    logger.info("Node: compare_vendors — executing")
    extractions = state.get("vendor_extractions", [])

    if not extractions:
        logger.warning("Node: compare_vendors — no extractions available, skipping")
        return state

    comparison = await compare_vendors(extractions=extractions)
    return {**state, "comparison": comparison}


@observe
async def node_generate_recommendation(state: RFQWorkflowState) -> RFQWorkflowState:
    """Run recommendation agent."""
    from src.agents.nodes.recommendation import generate_recommendation

    logger.info("Node: generate_recommendation — executing")
    extractions = state.get("vendor_extractions", [])
    validations = state.get("validation_results", [])
    comparison  = state.get("comparison", {})

    if not extractions:
        logger.warning("Node: generate_recommendation — no extractions available, skipping")
        return state

    recommendation = await generate_recommendation(
        extractions=extractions,
        validations=validations,
        comparison=comparison,
    )
    return {**state, "recommendation": recommendation, "workflow_status": "complete"}


# ─── Graph construction ──────────────────────────────────────────────────────

def build_graph():
    """Build and compile the LangGraph workflow with conditional routing."""
    try:
        from langgraph.graph import StateGraph, START, END

        graph = StateGraph(RFQWorkflowState)

        # Register all nodes
        graph.add_node("generate_rfq",           node_generate_rfq)
        graph.add_node("generate_vendors",        node_generate_vendors)
        graph.add_node("parse_documents",         node_parse_documents)
        graph.add_node("extract_information",     node_extract_information)
        graph.add_node("validate_extraction",     node_validate_extraction)
        graph.add_node("compare_vendors",         node_compare_vendors)
        graph.add_node("generate_recommendation", node_generate_recommendation)

        # ── Entry point: cascade-skip to the first node that needs to run ──
        graph.add_conditional_edges(
            START,
            route_rfq_workflow,
            {
                "generate_rfq":           "generate_rfq",
                "generate_vendors":       "generate_vendors",
                "parse_documents":        "parse_documents",
                "extract_information":    "extract_information",
                "validate_extraction":    "validate_extraction",
            },
        )

        # ── After generate_rfq: run or skip generate_vendors ───────────────
        graph.add_conditional_edges(
            "generate_rfq",
            route_after_rfq,
            {"run": "generate_vendors", "skip": "parse_documents"},
        )

        # ── After generate_vendors: run or skip parse_documents ────────────
        graph.add_conditional_edges(
            "generate_vendors",
            route_after_vendors,
            {"run": "parse_documents", "skip": "extract_information"},
        )

        # ── After parse_documents: run or skip extract_information ─────────
        graph.add_conditional_edges(
            "parse_documents",
            route_after_parse,
            {"run": "extract_information", "skip": "validate_extraction"},
        )

        # ── Remaining nodes always execute ─────────────────────────────────
        graph.add_edge("extract_information",     "validate_extraction")
        graph.add_edge("validate_extraction",     "compare_vendors")
        graph.add_edge("compare_vendors",         "generate_recommendation")
        graph.add_edge("generate_recommendation", END)

        return graph.compile()

    except ImportError:
        logger.warning("LangGraph not available — workflow will run sequentially")
        return None


def graph_png(graph):
    """Generate PNG for workflow graph."""
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        output_path = "graph_output.png"
        with open(output_path, "wb") as f:
            f.write(png_data)
        logging.info(f"Image saved to {output_path}")
        return png_data
    except Exception as exp_write:
        logging.error(f"Graph export failed: {exp_write}")
        return None


@observe
async def rfq_workflow(initial_state: dict | None = None) -> RFQWorkflowState:
    """
    Run the NourishKids RFQ procurement workflow asynchronously.

    Args:
        initial_state: Optional partial state to seed the workflow (existing
                       rfq, vendor_responses, vendor_extractions are skipped
                       by their respective nodes if already populated).

    Returns:
        Final RFQWorkflowState
    """
    state: RFQWorkflowState = {
        "rfq": None,
        "uploaded_documents": [],
        "parsed_documents": [],
        "vendor_responses": [],
        "vendor_extractions": [],
        "validation_results": [],
        "comparison": None,
        "recommendation": None,
        "workflow_id": f"WF-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "workflow_status": "running",
        "errors": [],
    }
    if initial_state:
        state.update(initial_state)

    app = build_graph()
    graph_png(app)
    if app:
        return await app.ainvoke(state)

    # ── Sequential fallback when LangGraph is unavailable ──────────────────
    # Mirror the same skip logic as the router functions so behaviour is
    # identical whether LangGraph is present or not.
    logger.warning("Running sequential fallback — LangGraph graph not available")

    skip_to = route_rfq_workflow(state)
    ordered_nodes = [
        ("generate_rfq",           node_generate_rfq),
        ("generate_vendors",       node_generate_vendors),
        ("parse_documents",        node_parse_documents),
        ("extract_information",    node_extract_information),
        ("validate_extraction",    node_validate_extraction),
        ("compare_vendors",        node_compare_vendors),
        ("generate_recommendation",node_generate_recommendation),
    ]
    executing = False
    for name, node_fn in ordered_nodes:
        if name == skip_to:
            executing = True
        if not executing:
            logger.info(f"⏭  [SKIP] {name} (sequential fallback)")
            continue
        try:
            state = await node_fn(state)
        except Exception as e:
            logger.error(f"Node {name} failed: {e}")
            state["errors"] = state.get("errors", []) + [f"{name}: {str(e)}"]

    return state
