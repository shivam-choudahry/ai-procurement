"""
FastAPI Backend — RFQ AI Procurement Copilot
REST API layer exposing the LangGraph workflow to the Streamlit frontend.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import traceback
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.config import get_settings

logger = logging.getLogger(__name__)

# ─── App init ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="RFQ AI Procurement Copilot",
    description="Multi-agent LangGraph system for vendor evaluation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Request/Response models ─────────────────────────────────────────────────

class GenerateRFQRequest(BaseModel):
    brief: Optional[str] = None
    use_demo: bool = False


class GenerateVendorsRequest(BaseModel):
    rfq_context: Optional[dict] = None
    count: int = 5
    use_demo: bool = False


class ExtractRequest(BaseModel):
    vendor_id: str
    vendor_name: str
    response_text: str


class CompareRequest(BaseModel):
    vendor_extractions: list[dict]


class RunWorkflowRequest(BaseModel):
    use_demo: bool = False
    vendor_responses: Optional[list[dict]] = None


# ─── Endpoints ───────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    """Health check endpoint."""
    settings = get_settings()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_key_configured": settings.has_api_key,
        "demo_mode": not settings.has_api_key,
    }


@app.post("/generate-rfq")
async def generate_rfq(request: GenerateRFQRequest):
    """Run RFQ Generator agent — returns structured RFQ JSON."""
    settings = get_settings()
    from data.rfq_data import RFQ_DATA

    if request.use_demo or not settings.has_api_key:
        return {"status": "demo", "rfq": RFQ_DATA}

    from src.agents.nodes.rfq_generator import generate_rfq_from_brief
    try:
        rfq = await generate_rfq_from_brief(brief=request.brief or "")
        if "error" in rfq:
            return {"status": "error", "error": rfq["error"], "rfq": RFQ_DATA}
        _save_generated("rfq.json", rfq)
        return {"status": "success", "rfq": rfq}
    except Exception as e:
        logger.error(f"generate_rfq error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-vendors")
async def generate_vendors(request: GenerateVendorsRequest):
    """Run Vendor Generator agent — returns 5 vendor personas."""
    settings = get_settings()
    from data.vendor_data import VENDOR_RESPONSES

    if request.use_demo or not settings.has_api_key:
        return {"status": "demo", "vendors": list(VENDOR_RESPONSES)}

    from src.agents.nodes.vendor_generator import generate_vendor_responses
    try:
        vendors = await generate_vendor_responses(rfq_context=request.rfq_context or {})
        if isinstance(vendors, dict) and "error" in vendors:
            return {"status": "error", "error": vendors["error"], "vendors": list(VENDOR_RESPONSES)}
        _save_generated("vendors/vendors.json", vendors)
        return {"status": "success", "vendors": vendors}
    except Exception as e:
        logger.error(f"generate_vendors error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-vendor")
async def upload_vendor(
    file: UploadFile = File(...),
    vendor_name: str = Form(...),
    vendor_id: str = Form(...)
):
    """Accept file upload, parse it, and run extraction."""
    settings = get_settings()

    content  = await file.read()
    filename = file.filename or "upload.txt"

    from parser import parse_document
    text = await asyncio.to_thread(parse_document, filename, content)

    if not settings.has_api_key:
        return {
            "status": "parsed_only",
            "vendor_id": vendor_id,
            "vendor_name": vendor_name,
            "filename": filename,
            "text_preview": text[:500],
            "extraction": None,
            "message": "Add OPENAI_API_KEY to run extraction.",
        }

    from src.agents.nodes.extractor import extract_vendor_response
    extraction = await extract_vendor_response(
        vendor_id=vendor_id,
        vendor_name=vendor_name,
        response_text=text,
    )
    _save_generated(f"extractions/{vendor_id}.json", extraction)

    return {
        "status": "success",
        "vendor_id": vendor_id,
        "vendor_name": vendor_name,
        "filename": filename,
        "text_preview": text[:500],
        "extraction": extraction,
    }


@app.post("/extract")
async def extract(request: ExtractRequest):
    """Run Extraction + Validation agents on a single vendor."""
    from src.agents.nodes.extractor import extract_vendor_response
    from src.agents.nodes.validator import validate_extraction

    extraction = await extract_vendor_response(
        vendor_id=request.vendor_id,
        vendor_name=request.vendor_name,
        response_text=request.response_text,
    )
    if "error" in extraction:
        return {"status": "error", "error": extraction["error"], "extraction": extraction}

    validation = await validate_extraction(extraction=extraction)
    _save_generated(f"extractions/{request.vendor_id}.json", extraction)

    return {
        "status": "success",
        "extraction": extraction,
        "validation": validation,
    }


@app.post("/compare")
async def compare(request: CompareRequest):
    """Run Comparison + Recommendation agents across all vendors."""
    from src.agents.nodes.comparator import compare_vendors
    from src.agents.nodes.recommendation import generate_recommendation

    comparison = await compare_vendors(extractions=request.vendor_extractions)
    if isinstance(comparison, dict) and "error" in comparison:
        return {"status": "error", "error": comparison["error"]}

    recommendation = await generate_recommendation(
        extractions=request.vendor_extractions,
        validations=[],
        comparison=comparison,
    )
    _save_generated("comparison.json", comparison)
    _save_generated("recommendation.json", recommendation)

    return {
        "status": "success",
        "comparison": comparison,
        "recommendation": recommendation,
    }


@app.post("/run-workflow")
async def run_workflow(request: RunWorkflowRequest):
    """Run the full LangGraph workflow end-to-end."""
    from src.agents.graph import rfq_workflow

    initial = {}
    if request.vendor_responses:
        initial["vendor_responses"] = request.vendor_responses

    try:
        final_state = await rfq_workflow(initial_state=initial if initial else None)
        return {
            "status": final_state.get("workflow_status", "unknown"),
            "workflow_id": final_state.get("workflow_id"),
            "rfq": final_state.get("rfq"),
            "vendors_count": len(final_state.get("vendor_responses", [])),
            "extractions_count": len(final_state.get("vendor_extractions", [])),
            "comparison": final_state.get("comparison"),
            "recommendation": final_state.get("recommendation"),
            "errors": final_state.get("errors", []),
        }
    except Exception as e:
        logger.error(f"Workflow error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _save_generated(relative_path: str, data: dict | list) -> None:
    """Save data to the generated/ directory."""
    try:
        settings  = get_settings()
        full_path = os.path.join(settings.generated_dir, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    except Exception as e:
        logger.warning(f"Could not save generated file {relative_path}: {e}")


# ─── Run directly ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.api:app", host="0.0.0.0", port=8000, reload=True)
