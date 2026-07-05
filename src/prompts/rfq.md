# RFQ Generation Prompt

## Role
You are a Senior Procurement Manager at NourishPlus Foods India Ltd., a large FMCG company.

## Task
Generate a REALISTIC, DETAILED RFQ (Request for Quotation) for marketing services to launch a new children's nutrition brand called NourishKids — a range of fortified fruit-and-vegetable snacks.

## Context
- Brand: NourishKids — fortified snacks for children aged 4–12 years, zero artificial colours, 12 essential vitamins
- Market: India — metros (Mumbai, Delhi, Bengaluru, Chennai, Hyderabad) + Tier 1 cities
- Regulatory: ASCI Chapter III (Advertising to Children), FSSAI nutrition and health claims
- Target go-live: September 2025

## Required Sections

### 1. General Information
- Event ID, issue date, submission deadline, contact details
- Brand background with specific positioning
- Evaluation criteria (price, capability, compliance, experience) with weights

### 2. Timelines
- RFQ issue date, clarification deadline, submission deadline
- Shortlisting notification, presentation dates, award date
- Project kickoff (March 2025) and campaign go-live (September 2025)

### 3. Scope of Work — 8 Line Items
For each line item provide: detailed deliverables, volume/quantity, quality standards, dependencies.

1. Strategy and creative development
2. TVC development (Hindi + English)
3. TVC production (broadcast quality)
4. Social organic content (60 posts/month minimum)
5. Social paid media planning
6. Social paid media buying and optimization
7. Kids advertising and claims compliance review (ASCI + FSSAI mandatory)
8. Launch program management

### 4. Commercial Expectations
- Pricing format: itemized per line item, INR, excluding GST
- Payment terms expectations (30-40-30 structure preferred)
- Budget indicative range
- Cost structure transparency requirements

### 5. Vendor Questionnaire (minimum 10 questions)
- Capability, experience, team composition, financial stability
- Kids advertising compliance process
- TVC production track record
- Sub-contractor disclosure requirements

### 6. Compliance Requirements
- ASCI Kids Advertising Code compliance (Chapter III)
- FSSAI health and nutrition claims regulations
- Platform-specific policies (YouTube Kids, Meta under-13)
- POSH policy, data protection, financial vetting

## Output Format

```json
{
  "rfq_id": "string",
  "title": "string",
  "issuer": { "company": "", "department": "", "contact_name": "", "contact_email": "", "contact_phone": "" },
  "brand": "string",
  "brand_description": "string",
  "market": "string",
  "issue_date": "string",
  "timelines": { "rfq_issue_date": "", "clarification_deadline": "", "submission_deadline": "",
                 "shortlisting_notification": "", "presentation_dates": "", "award_date": "",
                 "project_kickoff": "", "campaign_go_live": "", "campaign_end_date": "" },
  "overview": "string",
  "scope_of_work": [
    { "line_item_id": 1, "name": "", "description": "", "deliverables": [], "volume": "", "quality_standards": "", "dependencies": "" }
  ],
  "commercial_expectations": { "pricing_format": "", "payment_terms": "", "budget_range": "", "cost_transparency_requirements": "" },
  "vendor_questionnaire": [ { "q_id": "", "question": "", "guidance": "" } ],
  "compliance_requirements": [ { "area": "", "requirement": "", "documentation_required": "" } ],
  "evaluation_criteria": [ { "criterion": "", "weight": "", "description": "" } ],
  "submission_instructions": { "format": "", "deadline": "", "contact": "", "page_limit": "" }
}
```

## Hallucination Controls
- Ground all content in real Indian market context (ASCI, FSSAI, INR)
- Specify actual deliverable counts, not vague quantities
- Use real regulatory references, not placeholder text
- Commercial terms must reflect standard Indian FMCG procurement practice

