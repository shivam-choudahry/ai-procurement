"""
Pydantic V2 models for Vendor Responses.
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class PricingSummary(BaseModel):
    total_stated: Optional[str] = None
    currency: str = "INR"
    includes_gst: Optional[bool] = None


class VendorResponse(BaseModel):
    """A vendor's raw proposal response."""
    vendor_id: str
    vendor_name: str
    tagline: str = ""
    submission_date: str = ""
    pricing_summary: PricingSummary = Field(default_factory=PricingSummary)
    response_text: str = ""
    persona: str = ""  # premium | cheap | messy | conflicting | incomplete

    model_config = {"populate_by_name": True}


class VendorResponseList(BaseModel):
    """
    Wrapper model for LLM structured output returning multiple vendor responses.

    json_schema / function_calling structured output requires a JSON object at the
    top level — a bare JSON array is not supported. This wrapper holds the list
    so the Pydantic schema can be passed as output_schema to acall_llm.
    """
    vendors: list[VendorResponse] = Field(default_factory=list)


