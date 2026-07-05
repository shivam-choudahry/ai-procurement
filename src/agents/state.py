"""
RFQWorkflowState — LangGraph TypedDict state.
Flows through every node in the workflow graph.

Observability is handled automatically by Langfuse — no prompt_trace field needed.
"""

from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from typing_extensions import TypedDict

if TYPE_CHECKING:
    from src.schemas.rfq import RFQ
    from src.schemas.vendor import VendorResponse
    from src.schemas.extraction import VendorExtraction, ValidationResult
    from src.schemas.comparison import ComparisonMatrix, BuyerRecommendation


class UploadedDoc(TypedDict):
    vendor_id: str
    vendor_name: str
    filename: str
    file_type: str  # pdf|docx|txt|md
    raw_bytes: Optional[bytes]


class ParsedDoc(TypedDict):
    vendor_id: str
    vendor_name: str
    filename: str
    text: str
    parse_method: str  # pdfplumber|python-docx|plaintext


class RFQWorkflowState(TypedDict, total=False):
    """Central state object flowing through all LangGraph nodes."""
    # Core procurement document
    rfq: Optional[dict]

    # Vendor data
    uploaded_documents: list[UploadedDoc]
    parsed_documents: list[ParsedDoc]
    vendor_responses: list[dict]

    # Extraction pipeline
    vendor_extractions: list[dict]
    validation_results: list[dict]

    # Comparison & recommendation
    comparison: Optional[dict]
    recommendation: Optional[dict]

    # Workflow metadata
    workflow_id: Optional[str]
    workflow_status: Optional[str]   # pending|running|complete|error
    errors: list[str]
