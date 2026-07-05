"""
PROMPT LIBRARY — NourishKids RFQ Procurement System
=====================================================
All prompts used in the AI workflow, with rationale annotations.

Design Principles:
1. Role assignment  — give the model a clear expert persona
2. Output schema    — always specify JSON structure to prevent hallucination drift
3. Constraint rules — explicit "if missing, say MISSING" prevents confabulation
4. Evidence anchoring — require quoting source text to keep outputs grounded
5. Separation of extraction vs. inference — extraction only, no gap-filling
"""

import textwrap
from datetime import datetime

from langchain_core.prompts import PromptTemplate

# ─────────────────────────────────────────────
# UTILITY
# ─────────────────────────────────────────────
def wrap(text: str) -> str:
    """Strip leading indentation and surrounding whitespace from multiline strings."""
    return textwrap.dedent(text).strip()


def _current_date() -> str:
    """Full human-readable date for prose context — e.g. 'July 03, 2026'."""
    return datetime.now().strftime("%B %d, %Y")


def _current_year() -> str:
    """Year only, for use in document IDs — e.g. '2026'."""
    return str(datetime.now().year)


def _submission_date() -> str:
    """Vendor submission deadline: ~3 weeks from today in ISO format — e.g. '2026-07-24'."""
    from datetime import timedelta
    return (datetime.now() + timedelta(weeks=3)).strftime("%Y-%m-%d")


# ─────────────────────────────────────────────
# PROMPT 1: RFQ GENERATION
# ─────────────────────────────────────────────
# Purpose: Generate a realistic, complete RFQ for marketing services
# Structure: Role + Context + Specific requirements + Output format
# Hallucination control: Anchored to real Indian market context (ASCI, FSSAI, INR)
# ─────────────────────────────────────────────
RFQ_GENERATION_PROMPT = PromptTemplate(
    input_variables=["brief"],
    partial_variables={"current_date": _current_date, "current_year": _current_year},
    template=wrap("""
        {brief}

        You are a Senior Procurement Manager at NourishPlus Foods India Ltd., a large FMCG company.
        You are issuing a formal RFQ (Request for Quotation) for marketing services to launch a new
        children's nutrition brand called NourishKids — a range of fortified fruit-and-vegetable snacks.
        Today's date is {current_date}. Generate all timeline dates realistically relative to today.

        Generate a REALISTIC, DETAILED RFQ document. This should feel like an actual corporate procurement
        document, not a textbook template. Include market-specific detail (India, ASCI, FSSAI, INR pricing).

        The RFQ must cover ALL of the following sections with specific, realistic content:

        1. GENERAL INFORMATION
           - Unique RFQ event ID, issue date, submission deadline, issuer contact details
           - Brand background: NourishKids — fortified fruit-and-vegetable snacks for children aged 4–12
             launching across India metros and Tier 1 cities
           - Evaluation criteria covering price, capability, compliance, and relevant experience

        2. TIMELINES (all dates must be realistic and sequential)
           - RFQ issue date, clarification deadline, submission deadline
           - Shortlisting notification, presentation dates, award date
           - Project kickoff and campaign go-live (target: approximately 6–7 months from today), campaign end date

        3. SCOPE OF WORK — provide detailed content for ALL 8 line items:
           1. Strategy and creative development
              — deliverables, volume, quality standards, dependencies
           2. TVC development
              — script formats (30s/20s/10s), storyboards, language versions, deliverable counts
           3. TVC production
              — shoot, post-production, talent, format masters, rights documentation
           4. Social organic content
              — platform mix, post volume (minimum 60/month), reels, community management
           5. Social paid media planning
              — audience strategy, platform selection, KPI framework, budget phasing
           6. Social paid media buying and optimization
              — campaign execution, reporting cadence, optimization process, platform certifications
           7. Kids advertising and claims compliance review
              — ASCI Chapter III review, FSSAI claims validation, platform policy review, sign-off process
           8. Launch program management
              — project governance, critical path, stakeholder reporting, risk register

        4. COMMERCIAL EXPECTATIONS
           - Itemized pricing per line item in INR excluding GST
           - Payment milestone structure (e.g. 20/30/25/15/10 split)
           - Indicative budget range (INR crore)
           - Full transparency requirements: mark-ups, rebates, third-party costs

        5. VENDOR QUESTIONNAIRE (minimum 10 questions covering)
           - Agency profile, FMCG and kids category experience
           - ASCI and FSSAI compliance process with named reviewer
           - TVC production capability and track record
           - Paid media platform certifications
           - Team structure and seniority for this assignment
           - Financial stability, sub-contractor disclosure, POSH and data protection policies

        6. COMPLIANCE REQUIREMENTS (with documentation required for each)
           - ASCI Kids Advertising Code (Chapter III)
           - FSSAI Health and Nutrition Claims Regulations 2018
           - Platform policies: YouTube Kids, Meta under-13 targeting restrictions
           - POSH compliance, child safety in production, data protection, anti-bribery

        Make every field SPECIFIC and REALISTIC — use actual deliverable counts, concrete Indian market
        references, real regulatory citations, and commercially credible terms a senior FMCG buyer would use.
        Do not use placeholder text. Every field must contain substantive content.
    """),
)

# ─────────────────────────────────────────────
# PROMPT 2: VENDOR RESPONSE GENERATION
# ─────────────────────────────────────────────
# Purpose: Generate 3 diverse, realistic vendor responses with deliberate complexity
# Structure: Role + 3 vendor personas + specific mess instructions per vendor
# Why: Real vendor responses are never uniform — this simulates that reality
# Hallucination control: Personas are bounded (each vendor has a fixed profile)
# ─────────────────────────────────────────────
VENDOR_RESPONSE_GENERATION_PROMPT = PromptTemplate(
    input_variables=["rfq_context"],
    partial_variables={
        "current_date": _current_date,
        "current_year": _current_year,
        "submission_date": _submission_date,
    },
    template=wrap("""
        {rfq_context}

        You are simulating realistic vendor responses to a marketing services RFQ for the NourishKids
        brand launch (RFQ-MKT-{current_year}-NKL-001, issued by NourishPlus Foods India Ltd.).
        Today's date is {current_date}. Generate all dates realistically relative to today.

        Generate responses from 3 different agencies. Each response should feel like a REAL agency
        proposal — with marketing fluff, inconsistencies, and varying levels of professionalism.
        Do NOT make all responses equally good or equally bad.

        ---

        VENDOR 1: Apex Creative Co. (Full-service, 18-year-old agency)
        Profile: Established, well-regarded FMCG agency. Comprehensive proposal. Mostly clear.
        Complexity to include:
        - Detailed itemized pricing in INR, consistent totals
        - Minor assumption: media buying commission (10%) is EXCLUDED from proposal total
        - Good compliance section referencing ASCI and FSSAI
        - Clear timeline (28 weeks) with per-phase breakdown
        - One ambiguity: English TVC is "adapted" from Hindi, not independently produced
        - All 8 line items covered with clear deliverables

        VENDOR 2: Spark Digital Agency (Digital-first boutique, 6 years old)
        Profile: Performance-led digital agency, strong on paid social but weak on TVC.
        Complexity to include:
        - TVC production cost listed as "TBD — estimated INR 80-120 lakhs, subject to production house RFQ"
        - Kids compliance section: only a vague statement, recommends external specialist
        - Influencer fees priced in USD (currency inconsistency with INR RFQ)
        - Timeline: "10-12 weeks for digital deliverables, TVC timeline TBD" — vague
        - Social organic content: covers 50 posts/month (RFQ asks for 60) — gap not acknowledged
        - Line Item 6 (paid media buying) coverage present but commission is 12% net vs. RFQ expectation
        - Line 2/3 covers online video only, explicitly NOT broadcast TVC
        - Vendor questionnaire: skips financial stability question

        VENDOR 3: Brandsmith Group (Full-service, 12 years, mid-market)
        Profile: Claims full-service but proposal has internal conflicts and suspicious claims.
        Complexity to include:
        - CRITICAL CONFLICT: Executive summary states "INR 3,90,00,000 all-inclusive" but
          itemized line items total INR 3,64,00,000 — unexplained INR 26L discrepancy
        - SECOND CONFLICT: Intro says "campaign live in 6-8 weeks" but detailed timeline
          plan shows 15-16 weeks
        - Line Item 6 (paid media buying): first says "included in all-inclusive package"
          then adds a SEPARATE line item of INR 35L for it — contradictory
        - TVC scope: covers 2x30s in Hindi only (English is "extra INR 8L") — RFQ asked for Hindi+English
        - Compliance: claims "ASCI compliant" with no process detail, no named reviewer
        - Kids category experience: cites Haldirams Snacks which targets families, not specifically kids
        - "Dedicated team of 15 specialists" claimed in intro, but only 8 people listed in team section
        - One exclusion buried in fine print: "travel outside Mumbai at actuals"
        - Social posts: 45/month (RFQ asks 60, Vendor claims they recommend this lower volume)

        ---

        For each vendor, write the response as a long-form markdown document (~800-1200 words)
        that feels like a real agency proposal letter with:
        - Professional header and introduction
        - Marketing language and self-promotion
        - Structured sections for each line item
        - A pricing table
        - A timeline section
        - Team details
        - Questionnaire answers
        - Assumptions and exclusions

        Return all 3 vendor responses in the "vendors" array. For each vendor set:
        vendor_id (V001/V002/V003), vendor_name, tagline, submission_date ({submission_date}),
        response_text (the full markdown proposal), and pricing_summary with total_stated,
        currency, and includes_gst.
    """),
)

# ─────────────────────────────────────────────
# PROMPT 3: MESSY/COMPLEX DATA GENERATION
# ─────────────────────────────────────────────
# Purpose: Inject real-world edge cases into vendor data for testing extraction robustness
# Structure: Enumerates specific exception types — prevents generic output
# Why separate from Prompt 2: Allows targeted injection of specific test cases
# ─────────────────────────────────────────────
MESSY_DATA_GENERATION_PROMPT = PromptTemplate(
    input_variables=[],
    template=wrap("""
        You are generating edge-case complexity for vendor proposal test data in a procurement system.

        For the NourishKids marketing services RFQ, generate ADDITIONAL complexity scenarios that
        real-world proposals exhibit. These will be injected into or appended to existing proposals.

        Generate examples of the following real-world mess types:

        1. BUNDLED PRICING: A vendor who says "TVC development and production are bundled at INR 2.5Cr,
           we don't break these out separately" — making line-by-line comparison impossible.

        2. CURRENCY INCONSISTENCY: Mix INR and USD across different line items without explanation
           (e.g., social tools at "$1,200/month platform fee" embedded in an otherwise INR proposal).

        3. VAGUE COMPLIANCE CLAIM: "We are fully compliant with all applicable regulations" — no
           specifics, no documentation offered, no named compliance owner.

        4. CONDITIONAL PRICING: "All prices are valid subject to: (a) client approving brief within 5
           days, (b) no scope changes after Week 2, (c) media budget minimum of INR 80L/month."

        5. ASSUMPTION BURIED IN LEGAL: Key scope exclusion (e.g., "Post-production colour grading
           is excluded from TVC production cost") mentioned only in a legal disclaimer footer.

        6. CONFLICTING TIMELINE: Project summary says "8 weeks" but dependency table shows Phase 3
           alone takes 6 weeks, making the total impossible.

        7. MISSING SECTION WITH DEFLECTION: For Line Item 7 (Kids compliance), vendor writes
           "Our team is well-versed in all content guidelines and will ensure full compliance"
           without any specifics about ASCI or FSSAI.

        8. UNVERIFIABLE CLAIM: "We have cleared 50+ ASCI compliance reviews" — no case study,
           no client reference, no verifiable detail.

        9. SCOPE CREEP INDICATOR: Proposal includes "phase 2 digital amplification" and
           "influencer seeding program" without pricing — implying additional scope beyond RFQ.

        10. PAYMENT RISK: Payment terms that conflict with standard terms (e.g., "75% advance,
            25% on final delivery" vs. typical 30-40-30 structure).

        For each scenario, output:
        {{
          "scenario_id": string,
          "type": string,
          "description": string,
          "example_text": string,
          "extraction_challenge": string,
          "buyer_risk": string,
          "handling_instruction": string
        }}
    """),
)

# ─────────────────────────────────────────────
# PROMPT 4: UI/UX GENERATION
# ─────────────────────────────────────────────
# Purpose: Generate buyer-facing UI structure and UX copy
# Structure: Role as product designer + buyer journey framing
# ─────────────────────────────────────────────
UIUX_GENERATION_PROMPT = PromptTemplate(
    input_variables=[],
    template=wrap("""
        You are a Senior Product Designer at a B2B SaaS company that builds procurement tools for
        enterprise buyers. You are designing the buyer-facing UI for an AI-powered RFQ analysis system.

        The buyer is a Procurement Manager at an FMCG company evaluating vendor responses to an RFQ
        for marketing services. The buyer needs to:
        1. Understand the RFQ they issued
        2. Review vendor responses
        3. See extracted and structured information from each vendor
        4. Compare vendors across multiple dimensions
        5. Identify risks, missing info, and clarification needs
        6. Make a shortlisting decision

        Design the full UI/UX for this tool. For each screen, provide:
        - Screen name and purpose
        - Primary user question the screen answers
        - Key information hierarchy (what the buyer sees first, second, third)
        - Components to use (tables, cards, badges, charts, expanders)
        - UX copy (labels, empty states, tooltips, warning messages)
        - Design decisions rationale (why this layout helps the buyer)

        Screens to design:
        1. RFQ Overview — What did we ask vendors to respond to?
        2. Vendor Upload — How do I input vendor proposals?
        3. Extraction Review — What did each vendor actually say?
        4. Vendor Comparison — How do vendors compare to each other?
        5. Prompt Trace — How does the AI work?

        Special attention to:
        - How to display MISSING information (don't hide it — surface it prominently)
        - How to display CONFLICTING information (badge + expandable evidence)
        - How to display RISK levels (traffic light system)
        - How to show AI confidence vs. uncertainty
        - What a buyer sees when they land on the comparison page
        - How to avoid misleading the buyer through false equivalence

        Output as structured JSON with one object per screen, including components and UX copy.
    """),
)

# ─────────────────────────────────────────────
# PROMPT 5: EXTRACTION AGENT
# ─────────────────────────────────────────────
# Purpose: Extract structured procurement info from a single vendor response
# Structure: Strict JSON schema + explicit status taxonomy + evidence requirement
# Hallucination control: "DO NOT infer missing info" + MISSING flag required
# Evidence anchoring: Evidence field required for each extracted value
# ─────────────────────────────────────────────
EXTRACTION_SYSTEM_PROMPT = PromptTemplate(
    input_variables=[],
    template=wrap("""
        You are a precision procurement extraction agent. Your role is to extract structured
        procurement information from vendor proposal documents.

        CRITICAL RULES:
        1. Extract ONLY information explicitly stated in the vendor response. Never infer, assume,
           or fill in gaps.
        2. For every extracted field, assign one of these status values:
           - "present": Information is clearly stated
           - "partial": Information is present but incomplete or ambiguous
           - "missing": Information is not present in the document
           - "unclear": Information is present but cannot be reliably interpreted
           - "conflicting": Multiple statements in the document contradict each other
        3. For any "present" or "partial" field, provide an exact quote (evidence) from the source.
        4. For "conflicting" fields, quote BOTH conflicting statements.
        5. Never hallucinate commercial figures, timelines, or compliance claims.
        6. Flag assumptions, exclusions, and hidden costs explicitly.
    """),
)

EXTRACTION_USER_PROMPT = PromptTemplate(
    input_variables=["vendor_response_text", "vendor_id", "vendor_name"],
    partial_variables={"current_date": _current_date, "current_year": _current_year},
    template=wrap("""
        Extract procurement information from the following vendor response to an RFQ for
        marketing services (NourishKids brand launch, RFQ-MKT-{current_year}-NKL-001).
        Today's date is {current_date}.
        Vendor ID: {vendor_id} | Vendor Name: {vendor_name}

        RFQ CONTEXT — the vendor must respond to all 8 line items:
        1. Strategy and creative development
        2. TVC development
        3. TVC production
        4. Social organic content (60 posts/month requested)
        5. Social paid media planning
        6. Social paid media buying and optimization
        7. Kids advertising and claims compliance review (ASCI Chapter III + FSSAI required)
        8. Launch program management

        VENDOR RESPONSE:
        {vendor_response_text}

        EXTRACTION INSTRUCTIONS:
        - scope_coverage: For each of the 8 line items, determine covered/partial/missing,
          detail what is offered, assign status, and include an evidence quote. Compute an
          overall_coverage_score 0-100.
        - pricing: Extract total_stated, currency, GST inclusion, itemized line costs, compute
          itemized_total, run a consistency_check (PASS/FAIL/PARTIAL/UNKNOWN), and note any
          discrepancy. Flag hidden costs and ambiguous line items.
        - commercial_terms: Extract payment terms, proposal validity, GST treatment, and any
          escalation clause — each with status and evidence quote.
        - timeline: Extract proposed kickoff, campaign go-live, and total duration. Run a
          consistency_check across all timeline statements in the document.
        - team_and_experience: Extract named personnel, team size claimed, kids category
          experience, and relevant client references.
        - compliance: Extract ASCI Kids Code and FSSAI Health Claims coverage with detail_level
          (high/medium/low/none). Note whether a named compliance reviewer is provided.
        - assumptions: List all stated assumptions.
        - exclusions: List all stated exclusions and any hidden costs detected.
        - risks: List all identified risks with severity (high/medium/low) and evidence quote.
        - conflicting_info: For every pair of contradictory statements, quote both and note
          buyer impact.
        - buyer_flags: Top issues the buyer must review before shortlisting.
        - clarification_questions: Specific questions the buyer should send to this vendor.
        - overall_data_quality: HIGH (all key fields present, no conflicts) |
          MEDIUM (some gaps or one conflict) | LOW (multiple missing fields or conflicts).

        IMPORTANT: If any field cannot be determined from the vendor response, set status to
        "missing" and value to null. Do not guess. Do not interpolate. Do not fill gaps.
    """),
)

# ─────────────────────────────────────────────
# PROMPT 6: COMPARISON AGENT
# ─────────────────────────────────────────────
# Purpose: Compare multiple vendors using ONLY their extracted data
# Structure: Strict grounding rule + comparison schema + incomparability flagging
# Hallucination control: "Only use extracted data" + flags for "cannot compare"
# ─────────────────────────────────────────────
COMPARISON_SYSTEM_PROMPT = PromptTemplate(
    input_variables=[],
    template=wrap("""
        You are a procurement comparison agent helping a buyer evaluate vendor responses.

        CRITICAL RULES:
        1. Base ALL comparisons on the extracted data provided. Do not introduce external knowledge.
        2. When two vendors cannot be fairly compared (e.g., one has pricing, one doesn't),
           explicitly state "NOT COMPARABLE — {{reason}}" rather than making a forced comparison.
        3. Assign scores (1-5) only when sufficient data exists. Use "N/A" otherwise.
        4. Surface buyer risks and decision points clearly.
        5. Do not recommend a vendor — present information for buyer decision-making.
        6. Flag all conflicts, gaps, and ambiguities that affect comparability.
    """),
)

COMPARISON_USER_PROMPT = PromptTemplate(
    input_variables=["vendor_extractions_json"],
    partial_variables={"current_date": _current_date, "current_year": _current_year},
    template=wrap("""
        Compare the following vendors based on their extracted procurement data.
        RFQ: NourishKids Brand Launch (RFQ-MKT-{current_year}-NKL-001) | Today: {current_date}

        VENDOR EXTRACTIONS:
        {vendor_extractions_json}

        Produce a structured vendor comparison across these 6 dimensions:

        1. scope_coverage — How completely each vendor covers all 8 RFQ line items. Score each
           vendor 1-5, identify key gaps, and note the winner (or CANNOT DETERMINE).

        2. pricing_clarity — How clear, complete, and comparable the pricing is. For each vendor
           compute a comparable_total (or mark INCOMPLETE with a note explaining why). Score 1-5.

        3. commercial_completeness — Completeness of payment terms, validity, assumptions,
           exclusions. Score 1-5.

        4. timeline_quality — Realism, clarity, and detail of proposed timelines. Flag any
           timeline conflicts within a vendor's own proposal. Score 1-5.

        5. compliance_quality — Depth and credibility of compliance coverage (ASCI Chapter III,
           FSSAI health claims, platform policies). Named reviewer is a positive signal. Score 1-5.

        6. risk_level — Overall risk profile based on gaps, conflicts, and assumptions.
           Score 1-5 where lower = higher risk.

        Also provide:
        - key_differentiators: The most important differences between vendors and their buyer
          implication.
        - cannot_compare_because: Any dimension where fair comparison is not possible, with the
          reason and what the buyer should request to resolve it.
        - critical_conflicts_detected: Internal conflicts within any single vendor's proposal.
        - buyer_attention_points: The highest-priority issues the buyer must resolve, ranked
          HIGH/MEDIUM/LOW.
        - clarification_questions_per_vendor: Specific questions for each vendor keyed by
          vendor_id.
        - overall_risk_summary: Per vendor — risk_level (HIGH/MEDIUM/LOW), top_risks list, and
          missing_before_decision list.
        - comparison_limitations: What this comparison cannot tell us and why.

        Set comparison_id to "CMP-{current_year}-NKL-001" and rfq_reference to
        "RFQ-MKT-{current_year}-NKL-001".

        Remember: Only compare on data that exists. Flag incomparabilities. Do not pick a winner.
        Help the buyer understand what they know, what they don't, and what to ask next.
    """),
)

# ─────────────────────────────────────────────
# PROMPT 6B: VALIDATION AGENT
# ─────────────────────────────────────────────
VALIDATION_SYSTEM_PROMPT = PromptTemplate(
    input_variables=[],
    template=wrap("""
        You are a procurement data validation specialist. Your role is to validate the quality and
        completeness of vendor extraction outputs.

        CRITICAL RULES:
        1. Validate against extracted data only — do NOT re-read the original proposal
        2. Flag every missing required field explicitly
        3. Detect contradictions across fields within the same vendor
        4. Flag unsupported claims — any claim without evidence in the extraction
        5. Score objectively: start at 100, deduct for each issue found

        Required fields that MUST be present:
        - pricing.total_stated
        - pricing.currency
        - pricing.consistency_check
        - timeline.total_duration
        - compliance.asci_kids_code
        - compliance.fssai_health_claims
        - scope_coverage.overall_coverage_score
    """),
)

VALIDATION_USER_PROMPT = PromptTemplate(
    input_variables=["vendor_id", "vendor_name", "extraction_json"],
    template=wrap("""
        Validate the following vendor extraction for completeness and consistency.

        Vendor ID: {vendor_id}
        Vendor Name: {vendor_name}

        EXTRACTION DATA:
        {extraction_json}

        VALIDATION INSTRUCTIONS:
        - Check every required field listed in the system prompt. Mark each missing one.
        - Detect contradictions: any two fields within the extraction that state incompatible values
          (e.g., pricing total vs. itemized total, timeline summary vs. phase detail).
        - Flag unsupported claims: any claim in the extraction that lacks an evidence quote.
        - Compute overall_quality_score starting at 100:
            deduct 20 per missing required field
            deduct 15 per contradiction
            deduct 10 per unsupported claim
            deduct 5 per minor gap
            minimum 0
        - passed = true if score >= 60 AND no high-severity issues.
        - Write a concise validation_summary (1-2 sentences) stating the outcome.

        Set vendor_id to "{vendor_id}" and vendor_name to "{vendor_name}".
    """),
)

# ─────────────────────────────────────────────
# PROMPT 6C: RECOMMENDATION AGENT
# ─────────────────────────────────────────────
RECOMMENDATION_SYSTEM_PROMPT = PromptTemplate(
    input_variables=[],
    template=wrap("""
        You are a procurement advisory specialist generating evidence-backed vendor shortlisting recommendations.

        CRITICAL RULES:
        1. All pros and cons MUST be evidence-backed — cite specific data from extractions
        2. Confidence scores MUST be justified with reasoning
        3. Recommendation options: shortlist | conditional | reject only
        4. Do NOT pick a single winner — provide per-vendor recommendations
        5. Buyer decision authority is preserved — always include disclaimer
        6. Risk level must be grounded in specific risks/missing fields
    """),
)

RECOMMENDATION_USER_PROMPT = PromptTemplate(
    input_variables=["data_json"],
    partial_variables={"current_date": _current_date, "current_year": _current_year},
    template=wrap("""
        Generate evidence-backed shortlisting recommendations for all vendors.
        Today's date is {current_date}.

        DATA (extractions, validations, comparison summary):
        {data_json}

        RECOMMENDATION INSTRUCTIONS:
        - For each vendor produce: recommendation (shortlist/conditional/reject), confidence_score
          (0-100 with justification), pros (evidence-backed), cons (evidence-backed), risk_level
          (HIGH/MEDIUM/LOW), conditions (if conditional: what must be resolved before shortlisting),
          and evidence_citations (exact quotes from extraction data supporting each judgement).
        - base every pro, con, and condition on specific data from the extraction — no generic claims.
        - overall_summary: 2-3 sentence cross-vendor summary for the buyer.
        - next_steps: Ordered list of actions the buyer should take.
        - disclaimer: Must state that the final decision rests with the buyer.
        - Set recommendation_id to "REC-{current_year}-NKL-001" and
          rfq_reference to "RFQ-MKT-{current_year}-NKL-001".
    """),
)

# ─────────────────────────────────────────────
# PROMPT 7: EXCEPTION HANDLING & CLARIFICATION
# ─────────────────────────────────────────────
# Purpose: Generate targeted clarification questions for specific issues
# Structure: Context-specific + actionable question format
# ─────────────────────────────────────────────
CLARIFICATION_PROMPT = PromptTemplate(
    input_variables=["issues_json"],
    template=wrap("""
        You are a procurement specialist generating precise clarification questions for vendor proposals.

        Based on the following extraction issues identified in a vendor proposal, generate targeted,
        professionally-worded clarification questions that a buyer would send to the vendor.

        EXTRACTION ISSUES:
        {issues_json}

        For each issue, generate a clarification question that:
        1. Cites the specific discrepancy or ambiguity from the proposal
        2. Asks for a specific, answerable response (not open-ended)
        3. States the deadline or format for the response
        4. Is professionally worded for B2B vendor communication

        Format each question as:
        {{
          "issue_type": "missing|unclear|conflicting|incomplete",
          "area": string,
          "question": string,
          "what_buyer_needs": string,
          "deadline": "Please respond by [DATE]",
          "priority": "HIGH|MEDIUM|LOW"
        }}

        Output as JSON array. Generate questions only for issues that genuinely need vendor input.
        Do not generate questions for information the buyer already has.
    """),
)

# ─────────────────────────────────────────────
# PROMPT PACK METADATA
# ─────────────────────────────────────────────
PROMPT_PACK = {
    "RFQ Generation": {
        "prompt": RFQ_GENERATION_PROMPT,
        "purpose": "Generate a realistic, complete RFQ document for marketing services procurement",
        "why_structured_this_way": (
            "Role assignment (Senior Procurement Manager) anchors the model to professional vocabulary. "
            "Specific brand context (NourishKids, India, FSSAI, ASCI) prevents generic output. "
            "JSON schema removed from prompt — enforced via Pydantic RFQ model with function_calling "
            "structured output, so the model fills content rather than re-specifying structure."
        ),
        "hallucination_controls": [
            "Grounded in real regulatory context (ASCI, FSSAI, INR)",
            "Specific deliverable counts required per line item",
            "Pydantic RFQ schema enforced via model.with_structured_output(method='function_calling')",
            "Pydantic model_validate() re-validates response before returning",
        ],
    },
    "Vendor Response Generation": {
        "prompt": VENDOR_RESPONSE_GENERATION_PROMPT,
        "purpose": "Generate 3 diverse, realistic vendor responses with deliberate messy data",
        "why_structured_this_way": (
            "Each vendor has a fixed profile (age, specialty, quality level) preventing homogeneous output. "
            "Specific mess instructions per vendor (e.g., 'currency inconsistency', 'conflicting total') "
            "ensure test data exercises all extraction edge cases. "
            "Long-form markdown output simulates real agency proposals."
        ),
        "hallucination_controls": [
            "Fixed vendor profiles prevent drift",
            "Specific conflict types listed explicitly",
            "JSON wrapper for consistent parsing",
        ],
    },
    "Messy Data Generation": {
        "prompt": MESSY_DATA_GENERATION_PROMPT,
        "purpose": "Generate specific edge-case complexity types for testing extraction robustness",
        "why_structured_this_way": (
            "Enumerates 10 specific mess types rather than asking for 'complex data'. "
            "Each scenario includes extraction_challenge and buyer_risk — driving test quality. "
            "Separated from main vendor generation for modularity."
        ),
        "hallucination_controls": [
            "Bounded to 10 specific scenario types",
            "Each scenario has a handling_instruction for the extraction agent",
        ],
    },
    "UI/UX Generation": {
        "prompt": UIUX_GENERATION_PROMPT,
        "purpose": "Generate buyer-facing UI structure with product thinking rationale",
        "why_structured_this_way": (
            "Frames designer as B2B procurement product expert — not generic UI designer. "
            "Buyer journey framing ('what question does each screen answer?') forces information "
            "hierarchy thinking. Explicit attention to MISSING and CONFLICTING data display "
            "prevents UI that hides uncertainty."
        ),
        "hallucination_controls": [
            "Constrained to 5 specific screens",
            "UX copy requirements prevent abstract output",
        ],
    },
    "Extraction Agent": {
        "system_prompt": EXTRACTION_SYSTEM_PROMPT,
        "user_prompt": EXTRACTION_USER_PROMPT,
        "purpose": "Extract structured procurement information from vendor responses with evidence anchoring",
        "why_structured_this_way": (
            "Two-prompt design: system prompt sets strict rules once; user prompt provides variable content. "
            "5-value status taxonomy (present/partial/missing/unclear/conflicting) covers all real-world cases. "
            "Evidence field requirement forces model to quote source text — prevents confabulation. "
            "Consistency checks (pricing total vs. itemized) catch internal contradictions automatically."
        ),
        "hallucination_controls": [
            "CRITICAL RULES block explicitly forbids inference",
            "Evidence quotation required for all present/partial fields",
            "Conflicting info requires quoting BOTH statements",
            "MISSING is a valid, expected output — model rewarded for flagging",
        ],
    },
    "Comparison Agent": {
        "system_prompt": COMPARISON_SYSTEM_PROMPT,
        "user_prompt": COMPARISON_USER_PROMPT,
        "purpose": "Compare vendors across 6 dimensions using only extracted data, with buyer decision support",
        "why_structured_this_way": (
            "Grounding rule ('base ALL comparisons on extracted data') prevents external knowledge injection. "
            "'NOT COMPARABLE' as an explicit output option prevents forced false comparisons. "
            "Score schema with 'N/A' option handles asymmetric data (some vendors have info, others don't). "
            "Buyer attention points are structured by priority — helping buyers focus. "
            "Explicitly does NOT recommend a winner — preserves buyer decision authority."
        ),
        "hallucination_controls": [
            "Rule 2: 'NOT COMPARABLE' required when data is asymmetric",
            "Rule 5: No vendor recommendation — information presentation only",
            "comparison_limitations field documents what the comparison cannot tell us",
        ],
    },
    "Clarification/Exception Handling": {
        "prompt": CLARIFICATION_PROMPT,
        "purpose": "Generate precise, professional clarification questions for specific extraction issues",
        "why_structured_this_way": (
            "Context-specific structure (cites exact discrepancy) prevents generic 'please clarify' questions. "
            "what_buyer_needs field ensures questions drive actionable responses. "
            "Priority field helps buyer manage follow-up workload."
        ),
        "hallucination_controls": [
            "Input-constrained to specific issues from extraction output",
            "Instruction not to generate questions for info buyer already has",
        ],
    },
    "Validation Agent": {
        "system_prompt": VALIDATION_SYSTEM_PROMPT,
        "user_prompt": VALIDATION_USER_PROMPT,
        "purpose": "Validate extraction completeness, detect contradictions and unsupported claims",
        "why_structured_this_way": (
            "Validates against extracted data only — no re-reading of original proposal. "
            "Explicit required-fields list drives deterministic checking. "
            "Numeric scoring makes quality objective and comparable across vendors."
        ),
        "hallucination_controls": [
            "Validates extraction data, not original proposal (prevents new hallucination)",
            "Required field list is explicit and bounded",
            "passed threshold prevents weak validation from masking real issues",
        ],
    },
    "Recommendation Agent": {
        "system_prompt": RECOMMENDATION_SYSTEM_PROMPT,
        "user_prompt": RECOMMENDATION_USER_PROMPT,
        "purpose": "Generate per-vendor evidence-backed shortlisting recommendations with confidence scores",
        "why_structured_this_way": (
            "Evidence-backing requirement for every pro/con prevents opinion-based recommendations. "
            "Three-option taxonomy (shortlist/conditional/reject) forces clear categorization. "
            "Confidence score + conditions for 'conditional' gives buyer actionable next steps. "
            "Disclaimer preserves buyer decision authority."
        ),
        "hallucination_controls": [
            "All pros/cons must cite specific evidence from extraction",
            "Confidence score must be justified — not just a number",
            "No single winner selected — buyer decides",
            "Disclaimer mandated in output schema",
        ],
    },
}
