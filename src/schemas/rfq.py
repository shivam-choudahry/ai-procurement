"""
Pydantic V2 models for RFQ (Request for Quotation).
All LLM outputs must use these models — never parse markdown or tables.
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class TimelineItem(BaseModel):
    rfq_issue_date: str = ""
    clarification_deadline: str = ""
    submission_deadline: str = ""
    shortlisting_notification: str = ""
    presentation_dates: str = ""
    award_date: str = ""
    project_kickoff: str = ""
    campaign_go_live: str = ""
    campaign_end_date: str = ""


class Deliverable(BaseModel):
    description: str


class ScopeLineItem(BaseModel):
    line_item_id: int
    name: str
    description: str
    deliverables: list[str] = Field(default_factory=list)
    volume: str = ""
    quality_standards: str = ""
    dependencies: str = ""


class CommercialExpectation(BaseModel):
    pricing_format: str = ""
    payment_terms: str = ""
    budget_range: str = ""
    cost_transparency_requirements: str = ""


class EvaluationCriterion(BaseModel):
    criterion: str
    weight: str
    description: str


class QuestionnaireItem(BaseModel):
    q_id: str
    question: str
    guidance: str = ""


class Compliance(BaseModel):
    area: str
    requirement: str
    documentation_required: str = ""


class Issuer(BaseModel):
    company: str = ""
    department: str = ""
    contact_name: str = ""
    contact_email: str = ""
    contact_phone: str = ""


class SubmissionInstructions(BaseModel):
    format: str = ""
    deadline: str = ""
    contact: str = ""
    page_limit: str = ""


class Timeline(BaseModel):
    rfq_issue_date: str = ""
    clarification_deadline: str = ""
    submission_deadline: str = ""
    shortlisting_notification: str = ""
    presentation_dates: str = ""
    award_date: str = ""
    project_kickoff: str = ""
    campaign_go_live: str = ""
    campaign_end_date: str = ""


class RFQ(BaseModel):
    """Full RFQ document structure."""
    rfq_id: str
    title: str
    issuer: Issuer = Field(default_factory=Issuer)
    brand: str = ""
    brand_description: str = ""
    market: str = ""
    issue_date: str = ""
    timelines: Timeline = Field(default_factory=Timeline)
    overview: str = ""
    scope_of_work: list[ScopeLineItem] = Field(default_factory=list)
    commercial_expectations: CommercialExpectation = Field(default_factory=CommercialExpectation)
    vendor_questionnaire: list[QuestionnaireItem] = Field(default_factory=list)
    compliance_requirements: list[Compliance] = Field(default_factory=list)
    evaluation_criteria: list[EvaluationCriterion] = Field(default_factory=list)
    submission_instructions: Optional[SubmissionInstructions] = None

    model_config = {"populate_by_name": True}

