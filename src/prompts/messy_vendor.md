# Messy Vendor Data Generation Prompt

## Role
You are generating edge-case complexity for vendor proposal test data in a procurement AI system.

## Task
Generate 10 specific real-world mess types that appear in vendor proposals. These are used to test extraction robustness and hallucination prevention.

## Mess Types to Generate

1. **BUNDLED PRICING** — "TVC development and production are bundled at INR 2.5Cr, not broken out separately" — makes line-by-line comparison impossible

2. **CURRENCY INCONSISTENCY** — Mix INR and USD across line items without explanation (e.g., "$1,200/month platform fee" in an INR proposal)

3. **VAGUE COMPLIANCE CLAIM** — "We are fully compliant with all applicable regulations" — no specifics, no documentation, no named compliance owner

4. **CONDITIONAL PRICING** — "Prices valid subject to: (a) brief approved within 5 days, (b) no scope changes after Week 2, (c) media budget minimum INR 80L/month"

5. **ASSUMPTION BURIED IN LEGAL** — Key scope exclusion (e.g., "post-production colour grading excluded from TVC cost") only in legal footer disclaimer

6. **CONFLICTING TIMELINE** — Project summary says "8 weeks" but dependency table shows Phase 3 alone takes 6 weeks

7. **MISSING SECTION WITH DEFLECTION** — For Line Item 7 (Kids compliance): "Our team is well-versed in all content guidelines and will ensure full compliance" — zero specifics about ASCI or FSSAI

8. **UNVERIFIABLE CLAIM** — "We have cleared 50+ ASCI compliance reviews" — no case study, no client reference, no verifiable detail

9. **SCOPE CREEP INDICATOR** — Proposal includes "phase 2 digital amplification" and "influencer seeding program" without pricing — implying additional out-of-scope work

10. **PAYMENT RISK** — Payment terms "75% advance, 25% on final delivery" vs. typical 30-40-30 structure, creating significant cash flow and delivery risk for buyer

## Output Format

```json
[
  {
    "scenario_id": "MESS-001",
    "type": "string",
    "description": "string",
    "example_text": "how it appears verbatim in a vendor proposal",
    "extraction_challenge": "why this is hard to extract correctly",
    "buyer_risk": "what the buyer should watch out for",
    "handling_instruction": "how the extraction agent should flag this"
  }
]
```

