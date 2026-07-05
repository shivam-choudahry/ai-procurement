# Vendor Response Generation Prompt

## Role
You are simulating realistic vendor responses to a marketing services RFQ for the NourishKids brand launch.

## Task
Generate responses from **5 distinct vendor personas**. Each must feel like a real agency proposal with marketing language, inconsistencies, and varying professionalism.

**CRITICAL**: Every vendor response must be distinctly different. Do NOT make them uniformly good or bad.

## Vendor Personas

### Vendor A: Apex Creative Co. — Premium
- Profile: Full-service, 18-year established FMCG agency
- Style: Comprehensive, mostly clear, higher cost
- Include: Detailed itemized pricing (INR), minor media buying exclusion (10% commission), clear 28-week timeline, all 8 line items covered with good compliance section

### Vendor B: Spark Digital Agency — Budget
- Profile: Digital-first boutique, 6 years, performance-led
- Style: Strong on digital, weak on TVC
- Include: TVC production "TBD — INR 80–120L subject to production house RFQ", kids compliance vague/external, influencer fees in USD (currency inconsistency), timeline "10-12 weeks digital, TVC TBD", social content 50/month (RFQ asks 60, gap not acknowledged), media buying commission 12% net

### Vendor C: Brandsmith Group — Messy/Conflicting
- Profile: Claims full-service, 12 years, mid-market
- Style: Disorganized, internal contradictions
- Include:
  - **CRITICAL CONFLICT**: Executive summary states "INR 3,90,00,000 all-inclusive" but itemized total is INR 3,64,00,000 (unexplained INR 26L gap)
  - **TIMELINE CONFLICT**: Intro says "campaign live in 6-8 weeks" but timeline plan shows 15-16 weeks
  - Paid media buying: first says "included in all-inclusive", then adds separate INR 35L line item
  - TVC: 2x30s Hindi only, English is "extra INR 8L" (RFQ asked for Hindi + English)
  - Compliance: "ASCI compliant" with no process, no named reviewer
  - Team: claims "15 specialists" in intro, only 8 listed in team section
  - Social: 45 posts/month (RFQ asks 60)

### Vendor D: MediaPro Solutions — Incomplete
- Profile: Specialist media buying shop, 9 years
- Style: Strong on paid media, incomplete on creative and compliance
- Include: Excellent media buying section (INR, all included), completely missing TVC development/production sections, one-line compliance statement, no timeline for creative work, strong case studies, questionnaire mostly complete but skips compliance questions

### Vendor E: Nimble Brand Studio — Aggressive/Risky
- Profile: Young boutique (3 years), wants to punch above weight
- Style: Lowest cost, many assumptions/risks buried
- Include: Very low pricing (INR 1.8Cr, suspiciously low), key assumptions buried in fine print (all creative to be approved in one round, travel outside Bengaluru at actuals), payment terms 75% advance (vs. standard 30-40-30), "guaranteed ASCI compliance" with no evidence, delivery in 8 weeks for full campaign (unrealistic), scope creep indicators (mentions "phase 2 services" not in RFQ), no financial stability documentation

## Output Format

```json
[
  {
    "vendor_id": "V001",
    "vendor_name": "string",
    "tagline": "string",
    "submission_date": "2025-02-05",
    "response_text": "full markdown proposal text (800-1200 words)",
    "pricing_summary": { "total_stated": "string", "currency": "INR", "includes_gst": false },
    "persona": "premium"
  }
]
```

## Writing Style Requirements
Each response must include:
- Professional header and introduction with marketing language
- Line-by-line scope coverage
- Pricing table in INR
- Timeline with phase breakdown
- Team bios (named individuals)
- Questionnaire answers
- Assumptions and exclusions section
- Closing statement with contact information

