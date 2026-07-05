"""
Pydantic V2 models for Comparison Matrix and Buyer Recommendation.
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class VendorScore(BaseModel):
    score: Optional[str] = "N/A"  # 1-5 or "N/A"
    rationale: str = ""
    key_gaps: list[str] = Field(default_factory=list)


class DimensionScores(BaseModel):
    description: str = ""
    scores: dict[str, VendorScore] = Field(default_factory=dict)
    winner: str = "CANNOT DETERMINE"
    comparability_note: str = ""
    total_costs: dict[str, dict] = Field(default_factory=dict)  # for pricing_clarity


class KeyDifferentiator(BaseModel):
    dimension: str
    finding: str
    vendors_affected: list[str] = Field(default_factory=list)
    buyer_implication: str = ""


class CannotCompare(BaseModel):
    area: str
    reason: str
    vendors_affected: list[str] = Field(default_factory=list)
    resolution: str = ""


class CriticalConflict(BaseModel):
    vendor: str
    conflict: str
    impact: str = ""
    recommended_action: str = ""


class BuyerAttentionPoint(BaseModel):
    priority: str  # HIGH|MEDIUM|LOW
    point: str
    vendor: str = "ALL"
    action_required: str = ""


class VendorRiskSummary(BaseModel):
    risk_level: str = "UNKNOWN"
    top_risks: list[str] = Field(default_factory=list)
    missing_before_decision: list[str] = Field(default_factory=list)


class ComparisonMatrix(BaseModel):
    """Full vendor comparison output."""
    comparison_id: str = "CMP-001"
    comparison_timestamp: str = ""
    vendors_compared: list[str] = Field(default_factory=list)
    rfq_reference: str = ""
    dimension_scores: dict[str, DimensionScores] = Field(default_factory=dict)
    key_differentiators: list[KeyDifferentiator] = Field(default_factory=list)
    cannot_compare_because: list[CannotCompare] = Field(default_factory=list)
    critical_conflicts_detected: list[CriticalConflict] = Field(default_factory=list)
    buyer_attention_points: list[BuyerAttentionPoint] = Field(default_factory=list)
    clarification_questions_per_vendor: dict[str, list[str]] = Field(default_factory=dict)
    overall_risk_summary: dict[str, VendorRiskSummary] = Field(default_factory=dict)
    comparison_limitations: list[str] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class VendorRecommendation(BaseModel):
    vendor_id: str
    vendor_name: str
    recommendation: str  # shortlist | conditional | reject
    confidence_score: int = 0  # 0-100
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)
    risk_level: str = "UNKNOWN"
    conditions: list[str] = Field(default_factory=list)  # if conditional
    evidence_citations: list[str] = Field(default_factory=list)
    buyer_decision_notes: str = ""


class BuyerRecommendation(BaseModel):
    """Per-vendor recommendation with confidence scores."""
    recommendation_id: str = "REC-001"
    recommendation_timestamp: str = ""
    rfq_reference: str = ""
    vendors: list[VendorRecommendation] = Field(default_factory=list)
    overall_summary: str = ""
    next_steps: list[str] = Field(default_factory=list)
    disclaimer: str = "This recommendation is based solely on the information provided in vendor proposals. Final decision rests with the buyer."

    model_config = {"populate_by_name": True}

