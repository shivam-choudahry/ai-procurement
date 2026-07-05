"""
Pydantic V2 models for Vendor Extraction and Validation.
5-value status taxonomy: present | partial | missing | unclear | conflicting
"""

from __future__ import annotations
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    present = "present"
    partial = "partial"
    missing = "missing"
    unclear = "unclear"
    conflicting = "conflicting"


class RiskSeverity(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class FieldValue(BaseModel):
    """A single extracted field with status + evidence."""
    value: Optional[str] = None
    status: StatusEnum = StatusEnum.missing
    evidence: Optional[str] = None

    model_config = {"use_enum_values": True}


class ScopeLineItemExtraction(BaseModel):
    id: int
    name: str
    covered: Any = None  # true/false/"partial"
    detail: str = ""
    status: StatusEnum = StatusEnum.missing
    evidence: Optional[str] = None
    flags: list[str] = Field(default_factory=list)

    model_config = {"use_enum_values": True}


class ScopeCoverage(BaseModel):
    line_items: list[ScopeLineItemExtraction] = Field(default_factory=list)
    overall_coverage_score: str = "0"
    uncovered_items: list[str] = Field(default_factory=list)


class PricingLineItem(BaseModel):
    item: str
    cost: str
    status: str = "missing"


class PricingExtraction(BaseModel):
    total_stated: Optional[str] = None
    currency: Optional[str] = None
    includes_gst: Optional[bool] = None
    itemized: list[PricingLineItem] = Field(default_factory=list)
    itemized_total: Optional[str] = None
    consistency_check: str = "UNKNOWN"  # PASS|FAIL|PARTIAL|UNKNOWN
    consistency_note: str = ""
    status: StatusEnum = StatusEnum.missing
    evidence: Optional[str] = None
    flags: list[str] = Field(default_factory=list)

    model_config = {"use_enum_values": True}


class CommercialTermsExtraction(BaseModel):
    payment_terms: FieldValue = Field(default_factory=FieldValue)
    proposal_validity: FieldValue = Field(default_factory=FieldValue)
    gst_treatment: FieldValue = Field(default_factory=FieldValue)
    escalation_clause: FieldValue = Field(default_factory=FieldValue)
    flags: list[str] = Field(default_factory=list)


class TimelineExtraction(BaseModel):
    proposed_kickoff: FieldValue = Field(default_factory=FieldValue)
    campaign_go_live: FieldValue = Field(default_factory=FieldValue)
    total_duration: FieldValue = Field(default_factory=FieldValue)
    consistency_check: str = "UNKNOWN"
    consistency_note: str = ""
    flags: list[str] = Field(default_factory=list)


class PersonnelItem(BaseModel):
    role: str
    name: str
    experience: str = ""


class TeamAndExperience(BaseModel):
    key_personnel: list[PersonnelItem] = Field(default_factory=list)
    team_size_claimed: FieldValue = Field(default_factory=FieldValue)
    kids_category_experience: FieldValue = Field(default_factory=FieldValue)
    relevant_clients: list[str] = Field(default_factory=list)
    flags: list[str] = Field(default_factory=list)


class ComplianceFieldValue(BaseModel):
    value: Optional[str] = None
    status: StatusEnum = StatusEnum.missing
    evidence: Optional[str] = None
    detail_level: str = "none"  # high|medium|low|none

    model_config = {"use_enum_values": True}


class ComplianceExtraction(BaseModel):
    asci_kids_code: ComplianceFieldValue = Field(default_factory=ComplianceFieldValue)
    fssai_health_claims: ComplianceFieldValue = Field(default_factory=ComplianceFieldValue)
    platform_policies: FieldValue = Field(default_factory=FieldValue)
    compliance_reviewer_named: bool = False
    flags: list[str] = Field(default_factory=list)


class Assumptions(BaseModel):
    listed: list[str] = Field(default_factory=list)
    status: StatusEnum = StatusEnum.missing
    count: int = 0

    model_config = {"use_enum_values": True}


class Exclusions(BaseModel):
    listed: list[str] = Field(default_factory=list)
    hidden_costs_detected: list[str] = Field(default_factory=list)
    status: StatusEnum = StatusEnum.missing

    model_config = {"use_enum_values": True}


class Risk(BaseModel):
    """A risk identified in vendor extraction."""
    risk: str
    severity: RiskSeverity = RiskSeverity.medium
    category: str = "commercial"
    evidence: str = ""

    model_config = {"use_enum_values": True}


class ConflictInfo(BaseModel):
    area: str
    statement_1: str
    statement_2: str
    buyer_impact: str = ""


class Evidence(BaseModel):
    """Evidence citation for a claim."""
    quoted_text: str
    source_reference: str = ""
    field_supported: str = ""


class VendorExtraction(BaseModel):
    """Full structured extraction per vendor."""
    vendor_id: str
    vendor_name: str
    extraction_timestamp: str = ""

    scope_coverage: ScopeCoverage = Field(default_factory=ScopeCoverage)
    pricing: PricingExtraction = Field(default_factory=PricingExtraction)
    commercial_terms: CommercialTermsExtraction = Field(default_factory=CommercialTermsExtraction)
    timeline: TimelineExtraction = Field(default_factory=TimelineExtraction)
    team_and_experience: TeamAndExperience = Field(default_factory=TeamAndExperience)
    compliance: ComplianceExtraction = Field(default_factory=ComplianceExtraction)
    assumptions: Assumptions = Field(default_factory=Assumptions)
    exclusions: Exclusions = Field(default_factory=Exclusions)
    risks: list[Risk] = Field(default_factory=list)
    missing_info: list[str] = Field(default_factory=list)
    unclear_info: list[str] = Field(default_factory=list)
    conflicting_info: list[ConflictInfo] = Field(default_factory=list)
    overall_data_quality: str = "LOW"
    buyer_flags: list[str] = Field(default_factory=list)
    clarification_questions: list[str] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class ValidationIssue(BaseModel):
    issue_type: str  # missing|contradiction|unsupported|hallucination_risk
    field: str
    description: str
    severity: str = "medium"
    evidence: Optional[str] = None


class ValidationResult(BaseModel):
    """Validation output per vendor extraction."""
    vendor_id: str
    vendor_name: str
    validation_timestamp: str = ""
    passed: bool = False
    issues: list[ValidationIssue] = Field(default_factory=list)
    missing_required: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    unsupported_claims: list[str] = Field(default_factory=list)
    overall_quality_score: int = 0  # 0-100
    validation_summary: str = ""

