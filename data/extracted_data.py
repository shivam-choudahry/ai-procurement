"""
Pre-extracted vendor data for demo mode.
Represents the output of the Extraction Agent applied to all 3 vendor responses.
"""

EXTRACTED_DATA = {
    "V001": {
        "vendor_id": "V001",
        "vendor_name": "Apex Creative Co.",
        "extraction_timestamp": "2026-07-25T10:30:00+05:30",
        "scope_coverage": {
            "line_items": [
                {"id": 1, "name": "Strategy and Creative Development", "covered": True, "detail": "Fully covered with strategy doc, creative platform, 3 concept routes, messaging architecture", "status": "present", "evidence": "Full brand strategy document... Campaign creative platform and big idea... 3 creative concept directions", "flags": []},
                {"id": 2, "name": "TVC Development", "covered": "partial", "detail": "Covered, but English TVC is a language adaptation of Hindi master — not independently developed as required by RFQ", "status": "partial", "evidence": "The English TVC will be a language adaptation of the Hindi master TVC... share the same core narrative and visual concept", "flags": ["RFQ requires independently developed Hindi and English TVCs. Vendor proposes adaptation only."]},
                {"id": 3, "name": "TVC Production", "covered": True, "detail": "Fully covered. Additional shoot days and out-of-city travel are extra.", "status": "present", "evidence": "Full production of 2 × 30-second TVCs + 4 × 10-second cutdowns... Each TVC includes 1 day of principal photography", "flags": ["Out-of-city shoots attract travel at cost", "Additional shoot days billed at INR 8L/day"]},
                {"id": 4, "name": "Social Organic Content", "covered": True, "detail": "60 posts/month as requested. Detailed breakdown provided across platforms.", "status": "present", "evidence": "60 posts/month across Instagram, Facebook, and YouTube for 6 months", "flags": ["Influencer fees excluded"]},
                {"id": 5, "name": "Social Paid Media Planning", "covered": True, "detail": "Covered, but assumes INR 1 Cr/month media budget — needs client confirmation", "status": "present", "evidence": "developed based on INR 1 Crore monthly media spend assumption; actual budget to be confirmed by client", "flags": ["Budget assumption may need revision if actual spend differs significantly"]},
                {"id": 6, "name": "Social Paid Media Buying and Optimization", "covered": True, "detail": "Covered, but 10% commission on gross media spend is SEPARATE from proposal total. INR 30L in proposal covers management/reporting only.", "status": "partial", "evidence": "Media buying is managed at a 10% commission on gross media spend... This commission is NOT included in the INR 4,20,00,000 proposal total", "flags": ["IMPORTANT: 10% commission adds significant cost. At INR 1Cr/month x 4 months = INR 40L in commission not in proposal total"]},
                {"id": 7, "name": "Kids Advertising and Claims Compliance", "covered": True, "detail": "Well covered. Named reviewer (Kavita Shah, ex-ASCI panelist) with track record.", "status": "present", "evidence": "dedicated compliance reviewer, Kavita Shah (ex-ASCI panelist, 15 years)... cleared campaigns for Nestlé Milo, Britannia Bournvita, and Cadbury Bournvita", "flags": []},
                {"id": 8, "name": "Launch Program Management", "covered": True, "detail": "Fully covered. PMP-certified PM (Shreya Bose) for 10 months.", "status": "present", "evidence": "Shreya Bose, PMP-certified, 9 years of campaign project management experience, assigned full-time", "flags": []}
            ],
            "overall_coverage_score": "88",
            "uncovered_items": ["English TVC independently developed (adaptation only)"]
        },
        "pricing": {
            "total_stated": "INR 4,20,00,000",
            "currency": "INR",
            "includes_gst": False,
            "itemized": [
                {"item": "Strategy & Creative Development", "cost": "INR 45,00,000", "status": "present"},
                {"item": "TVC Development", "cost": "INR 28,00,000", "status": "present"},
                {"item": "TVC Production", "cost": "INR 1,85,00,000", "status": "present"},
                {"item": "Social Organic Content (6 months)", "cost": "INR 72,00,000", "status": "present"},
                {"item": "Social Paid Media Planning", "cost": "INR 18,00,000", "status": "present"},
                {"item": "Social Paid Media Management (4 months)", "cost": "INR 30,00,000", "status": "present"},
                {"item": "Kids Compliance Review", "cost": "INR 22,00,000", "status": "present"},
                {"item": "Launch Program Management (10 months)", "cost": "INR 20,00,000", "status": "present"}
            ],
            "itemized_total": "INR 4,20,00,000",
            "consistency_check": "PASS",
            "consistency_note": "Itemized total matches stated total of INR 4.20 Cr",
            "status": "present",
            "evidence": "TOTAL: 4,20,00,000",
            "flags": [
                "Media buying commission (10% on gross spend) is NOT in proposal total — significant additional cost",
                "Influencer fees not included",
                "Revision rounds beyond 3 billed at INR 1.5L each"
            ]
        },
        "commercial_terms": {
            "payment_terms": {"value": "30% on PO, 40% on milestone, 30% on final delivery", "status": "present", "evidence": "30% on PO, 40% on milestone completion (defined in project charter), 30% on final delivery"},
            "proposal_validity": {"value": "90 days from 24 Jul 2026", "status": "present", "evidence": "Validity: 90 days from submission date (24 July 2026)"},
            "gst_treatment": {"value": "18% GST applicable, billed separately", "status": "present", "evidence": "GST: 18% applicable on all services (billed separately)"},
            "escalation_clause": {"value": "8% per annum after 12 months from PO date", "status": "present", "evidence": "Price Escalation: 8% per annum; applicable after 12 months from PO date"},
            "flags": []
        },
        "timeline": {
            "proposed_kickoff": {"value": "Week 1 from project kickoff (assumed 24 August 2026)", "status": "present", "evidence": "Weeks 1–6 from project kickoff"},
            "campaign_go_live": {"value": "Week 14 onwards (social), Week 18 (TVC)", "status": "present", "evidence": "Content creation begins Week 14 (6 weeks before go-live)"},
            "total_duration": {"value": "52 weeks (Weeks 1–52)", "status": "present", "evidence": "Weeks 1–52 (full campaign duration)"},
            "consistency_check": "PASS",
            "consistency_note": "Timeline phases are internally consistent; TVC at Week 18 aligns with Feb 2027 go-live if kickoff is March",
            "flags": ["Campaign go-live date of 15 February 2027 not explicitly confirmed — inferred from phase timing"]
        },
        "team_and_experience": {
            "key_personnel": [
                {"role": "Account Director", "name": "Rohit Malhotra", "experience": "14 years; ex-Ogilvy"},
                {"role": "Creative Director", "name": "Sunita Kapoor", "experience": "12 years"},
                {"role": "Strategy Lead", "name": "Aditya Menon", "experience": "10 years"},
                {"role": "Social Media Lead", "name": "Priya Nair", "experience": "8 years"},
                {"role": "Compliance Reviewer", "name": "Kavita Shah", "experience": "15 years; ex-ASCI panelist"},
                {"role": "Project Manager", "name": "Shreya Bose", "experience": "9 years; PMP"}
            ],
            "team_size_claimed": {"value": "6 named personnel (team size not stated overall)", "status": "partial", "evidence": "Named 6 roles above"},
            "kids_category_experience": {"value": "Yes — Kinder Joy, Bournvita, Milo campaigns; ASCI compliant", "status": "present", "evidence": "Yes — Kinder Joy (Ferrero), Bournvita (Mondelez), Milo (Nestlé). All three cleared ASCI compliance."},
            "relevant_clients": ["Nestlé India", "Britannia", "Marico", "Dabur", "Emami", "Ferrero", "Mondelez"],
            "flags": []
        },
        "compliance": {
            "asci_kids_code": {"value": "Covered — ASCI Chapter III review, named reviewer with ASCI background", "status": "present", "evidence": "ASCI Chapter III compliance review for all TV and digital creatives... Kavita Shah (ex-ASCI panelist)", "detail_level": "high"},
            "fssai_health_claims": {"value": "Covered — FSSAI nutrition claims validation checklist mentioned", "status": "present", "evidence": "FSSAI nutrition and health claims validation checklist", "detail_level": "medium"},
            "platform_policies": {"value": "Covered — YouTube Kids, Meta under-13, OTT platform policies", "status": "present", "evidence": "YouTube Kids and Meta under-13 policy review per platform"},
            "compliance_reviewer_named": True,
            "flags": []
        },
        "assumptions": {
            "listed": [
                "Up to 3 rounds of revisions per deliverable",
                "Client provides brand guidelines and market research by Week 1",
                "TVC shoot within Mumbai or Delhi",
                "Media buying commission (10%) is separate",
                "Influencer fees are separate",
                "English TVC is adaptation, not independently developed",
                "Media budget assumed at INR 1 Cr/month"
            ],
            "status": "present",
            "count": 7
        },
        "exclusions": {
            "listed": ["GST", "Media buying budget", "Media buying commission (10% on gross spend)", "Influencer fees", "Travel outside Mumbai/Delhi", "Out-of-pocket expenses", "Third-party licensing", "Primary consumer research"],
            "hidden_costs_detected": ["10% media buying commission adds ~INR 40-60L based on expected media spend", "Additional shoot days at INR 8L/day", "Revision rounds beyond 3 at INR 1.5L each"],
            "status": "present"
        },
        "risks": [
            {"risk": "Media buying commission not in proposal total — could add INR 40–60L based on assumed media budget", "severity": "high", "category": "commercial", "evidence": "10% commission on gross media spend... NOT included in the INR 4,20,00,000 proposal total"},
            {"risk": "English TVC is adaptation only — may not meet brand/market requirements for independent development", "severity": "medium", "category": "scope", "evidence": "The English TVC will be a language adaptation of the Hindi master TVC"},
            {"risk": "TVC director subject to availability — primary confirmed, backup not named", "severity": "low", "category": "team", "evidence": "primary and backup director options confirmed"}
        ],
        "missing_info": ["Overall team size not stated", "Explicit campaign go-live date of 15 Sep not confirmed"],
        "unclear_info": ["Line Item 6: INR 30L covers management but commission is separate — total paid media cost needs clarification"],
        "conflicting_info": [],
        "overall_data_quality": "HIGH",
        "buyer_flags": [
            "🚨 IMPORTANT: Total cost of INR 4.20 Cr excludes media buying commission (10% on gross spend). At INR 1Cr/month media budget × 4 months, this adds ~INR 40 lakhs to total.",
            "⚠️ English TVC is an adaptation of Hindi — not independently developed as the RFQ specifies. Clarify if this meets NourishKids' bilingual requirements.",
            "ℹ️ Strongest compliance capability of all 3 vendors — named ex-ASCI reviewer with proven track record."
        ],
        "clarification_questions": [
            "What is the firm total cost of paid media management including the 10% commission, assuming INR 1 Cr/month media spend for 4 months?",
            "Can you confirm the English TVC will have independently developed creative (unique script/storyline), not just a dubbed/adapted version of the Hindi TVC?",
            "Can you name the backup TVC director and confirm their availability for the March–June production window?"
        ]
    },

    "V002": {
        "vendor_id": "V002",
        "vendor_name": "Spark Digital Agency",
        "extraction_timestamp": "2026-07-25T10:32:00+05:30",
        "scope_coverage": {
            "line_items": [
                {"id": 1, "name": "Strategy and Creative Development", "covered": "partial", "detail": "Digital strategy only — explicitly excludes ATL/traditional advertising strategy", "status": "partial", "evidence": "Our strategy is optimised for digital channels. We are not an ATL/traditional advertising agency.", "flags": ["ATL/broadcast strategy not covered — significant gap for a TV-led launch"]},
                {"id": 2, "name": "TVC Development", "covered": "partial", "detail": "Online video development only — explicitly NOT broadcast TVC. Different format (90s online vs 30s broadcast).", "status": "partial", "evidence": "This covers online video development optimised for digital platforms. We do not develop scripts or storyboards for traditional broadcast television.", "flags": ["CRITICAL: RFQ requires broadcast TVC scripts/storyboards. Vendor explicitly excludes this."]},
                {"id": 3, "name": "TVC Production", "covered": "partial", "detail": "Digital production only. Broadcast TVC production cost is TBD (INR 80–120L estimate, unconfirmed).", "status": "unclear", "evidence": "Traditional broadcast TVC production for TV channels... Estimated cost: INR 80–120 lakhs — however, this cannot be confirmed at this stage", "flags": ["CRITICAL: No firm price for broadcast TVC production. Cannot compare on this item."]},
                {"id": 4, "name": "Social Organic Content", "covered": "partial", "detail": "50 posts/month proposed vs 60 required by RFQ. YouTube deprioritised. Gap acknowledged but framed as recommendation.", "status": "partial", "evidence": "50 posts/month across Instagram and Facebook... The RFQ mentions 60 posts/month. Based on our experience, 50 high-quality posts outperform 60", "flags": ["Volume gap: 50 vs 60 posts/month. Vendor's rationale is a recommendation, not a confirmed match to RFQ scope."]},
                {"id": 5, "name": "Social Paid Media Planning", "covered": True, "detail": "Fully covered", "status": "present", "evidence": "Full paid media strategy and channel plan... Platform selection: Meta (Instagram + Facebook), Google/YouTube, and 1 OTT platform", "flags": []},
                {"id": 6, "name": "Social Paid Media Buying and Optimization", "covered": True, "detail": "Covered, but fee is 12% on NET media spend (RFQ norm is typically 10% on gross). Difference in base and rate should be clarified.", "status": "present", "evidence": "12% on net media spend, billed monthly", "flags": ["Fee basis is NET spend at 12% — different from standard 10% on GROSS. Buyer should compare total cost, not just rate."]},
                {"id": 7, "name": "Kids Advertising and Claims Compliance", "covered": False, "detail": "Explicitly not in scope. Vendor recommends external specialist. Only facilitation offered.", "status": "missing", "evidence": "formal ASCI Kids Advertising Code compliance review and FSSAI health claims validation... recommend engaging a specialist compliance consultant. This is a specialised regulatory area", "flags": ["CRITICAL: Kids compliance is a mandatory RFQ requirement. Vendor cannot deliver this in-house."]},
                {"id": 8, "name": "Launch Program Management", "covered": "partial", "detail": "Lean PM model — account manager, Notion tracker. No dedicated senior PM, no formal project charter or risk register.", "status": "partial", "evidence": "Our PM approach is lean and digital-first. We use tools rather than heavy documentation.", "flags": ["PM scope is significantly lighter than RFQ requirement. No project charter, no steering committee facilitation."]}
            ],
            "overall_coverage_score": "52",
            "uncovered_items": ["Kids advertising compliance (in-house)", "Broadcast TVC development", "Broadcast TVC production (confirmed price)", "Social organic volume gap (50 vs 60)", "Full PM scope"]
        },
        "pricing": {
            "total_stated": "INR 1,75,00,000",
            "currency": "INR (with USD for influencer fees)",
            "includes_gst": False,
            "itemized": [
                {"item": "Strategy & Creative Development (digital)", "cost": "INR 28,00,000", "status": "present"},
                {"item": "Online Video Development (not broadcast TVC)", "cost": "INR 22,00,000", "status": "present"},
                {"item": "Digital Production (shoots, not broadcast TVC)", "cost": "INR 18,00,000", "status": "present"},
                {"item": "Social Organic Content (50 posts/mo, 6 months)", "cost": "INR 54,00,000", "status": "present"},
                {"item": "Paid Media Planning", "cost": "INR 12,00,000", "status": "present"},
                {"item": "Paid Media Management (6 months)", "cost": "INR 24,00,000", "status": "present"},
                {"item": "Compliance Facilitation Only", "cost": "INR 5,00,000", "status": "present"},
                {"item": "Account Management", "cost": "INR 12,00,000", "status": "present"},
                {"item": "Broadcast TVC Production", "cost": "TBD — INR 80–120L range only", "status": "missing"}
            ],
            "itemized_total": "INR 1,75,00,000 (EXCLUDES broadcast TVC production — unpriced)",
            "consistency_check": "PARTIAL",
            "consistency_note": "Digital items are internally consistent. However, broadcast TVC production is unpriced — total is incomplete for full RFQ scope.",
            "status": "partial",
            "evidence": "TOTAL: 1,75,00,000... Broadcast TVC production for TV channels... cannot be confirmed at this stage",
            "flags": [
                "CRITICAL: Total is incomplete — broadcast TVC production (potentially INR 80–120L) is TBD",
                "Influencer fees quoted in USD — currency mismatch with INR RFQ requirement",
                "12% commission on NET spend (not gross) — not directly comparable to standard 10% on gross",
                "Compliance specialist fees are additional (cost unknown)"
            ]
        },
        "commercial_terms": {
            "payment_terms": {"value": "50% advance, 50% on completion", "status": "present", "evidence": "50% advance on PO, 50% on project completion"},
            "proposal_validity": {"value": "45 days from 24 Jul 2026", "status": "present", "evidence": "Proposal validity: 45 days from submission date"},
            "gst_treatment": {"value": "18% GST applicable", "status": "present", "evidence": "GST at 18%"},
            "escalation_clause": {"value": None, "status": "missing", "evidence": None},
            "flags": ["50% advance is higher than RFQ's expected 30% — potential cash flow risk", "Shorter validity (45 days vs Apex's 90 days)"]
        },
        "timeline": {
            "proposed_kickoff": {"value": "Week 1", "status": "present", "evidence": "Phase 1: Strategy & brief development, Weeks 1–4"},
            "campaign_go_live": {"value": "10–12 weeks for digital; TVC timeline TBD", "status": "partial", "evidence": "Overall digital campaign live: approximately 10–12 weeks from project kickoff. Broadcast TVC timeline: Cannot be confirmed"},
            "total_duration": {"value": "Digital: 10–12 weeks. TVC: undefined.", "status": "unclear", "evidence": "approximately 10–12 weeks from project kickoff"},
            "consistency_check": "UNKNOWN",
            "consistency_note": "Timeline only covers digital scope. Broadcast TVC timeline is undefined.",
            "flags": ["TVC timeline completely undefined — cannot assess against Feb 2027 go-live", "Digital timeline of 10–12 weeks seems feasible but TVC would likely push go-live later"]
        },
        "team_and_experience": {
            "key_personnel": [
                {"role": "Founder & Strategy", "name": "Arjun Reddy", "experience": "8 years; ex-iProspect"},
                {"role": "Creative Director", "name": "Nisha Pillai", "experience": "7 years"},
                {"role": "Paid Media Head", "name": "Vikram Singh", "experience": "6 years; Google & Meta certified"},
                {"role": "Social Content Lead", "name": "Tanya Agarwal", "experience": "5 years"}
            ],
            "team_size_claimed": {"value": "45-person agency; team for this project not specified", "status": "partial", "evidence": "We're a 45-person team"},
            "kids_category_experience": {"value": "Not stated for kids specifically. Client list is D2C/consumer brands (Mamaearth, Wow, Sugar).", "status": "missing", "evidence": "Mamaearth, Wow Skin Science, Sugar Cosmetics, Lenskart, boAt Lifestyle", "flags": ["No kids advertising experience mentioned. All cited clients are adult consumer brands."]},
            "relevant_clients": ["Mamaearth", "Wow Skin Science", "Sugar Cosmetics", "Lenskart", "boAt Lifestyle"],
            "flags": ["No FMCG or kids category clients in cited experience — significant gap for this brief"]
        },
        "compliance": {
            "asci_kids_code": {"value": "Not available in-house. External specialist recommended.", "status": "missing", "evidence": "formal ASCI Kids Advertising Code compliance review... recommend engaging a specialist compliance consultant", "detail_level": "none"},
            "fssai_health_claims": {"value": "Not mentioned", "status": "missing", "evidence": None, "detail_level": "none"},
            "platform_policies": {"value": "Not mentioned specifically for kids", "status": "missing", "evidence": None},
            "compliance_reviewer_named": False,
            "flags": ["CRITICAL: No in-house compliance capability. Kids advertising compliance is a mandatory RFQ requirement."]
        },
        "assumptions": {
            "listed": ["Broadcast TVC treated as separate project", "50 posts/month preferred over 60", "Influencer fees in USD"],
            "status": "partial",
            "count": 3
        },
        "exclusions": {
            "listed": ["Broadcast TVC production (TBD)", "Media buying commission (12% on net)", "Influencer fees (USD billed)", "Compliance specialist fees", "GST"],
            "hidden_costs_detected": ["Compliance consultant at unknown cost", "TVC production range INR 80–120L unconfirmed"],
            "status": "present"
        },
        "risks": [
            {"risk": "Broadcast TVC scope entirely outside this agency's core capability — highest risk item", "severity": "high", "category": "scope", "evidence": "We do not develop scripts or storyboards for traditional broadcast television"},
            {"risk": "Kids advertising compliance is undeliverable in-house — mandatory RFQ requirement", "severity": "high", "category": "compliance", "evidence": "recommend engaging a specialist compliance consultant"},
            {"risk": "No kids or FMCG category experience in cited client portfolio", "severity": "high", "category": "team", "evidence": "Mamaearth, Wow Skin Science, Sugar Cosmetics, Lenskart, boAt Lifestyle"},
            {"risk": "Total cost is incomplete — broadcast TVC adds INR 80–120L unknown", "severity": "high", "category": "commercial", "evidence": "cannot be confirmed at this stage"},
            {"risk": "50% advance payment requirement is higher than industry norm", "severity": "medium", "category": "commercial", "evidence": "50% advance on PO"}
        ],
        "missing_info": ["Kids category experience", "Broadcast TVC firm pricing", "Compliance reviewer credentials", "Escalation clause", "Financial information", "ASCI track record"],
        "unclear_info": ["Total comparable cost (TVC is TBD)", "12% net vs 10% gross commission equivalence", "Team assigned to this account (only 4 named, rest TBD)"],
        "conflicting_info": [],
        "overall_data_quality": "LOW",
        "buyer_flags": [
            "🚨 CRITICAL: Broadcast TVC scope is not covered. This vendor is a digital-only agency that cannot deliver the full RFQ scope.",
            "🚨 CRITICAL: Kids advertising compliance (Line Item 7) is NOT available in-house. This is a mandatory RFQ requirement.",
            "🚨 CRITICAL: Total cost is incomplete — broadcast TVC production (INR 80–120L) is unpriced.",
            "⚠️ No kids or FMCG category experience in cited client portfolio.",
            "⚠️ 50% advance requirement is above RFQ norm (30%)."
        ],
        "clarification_questions": [
            "Can you provide a firm price for broadcast TVC production, or confirm that this is outside your scope?",
            "Can you name a specific compliance consultant you would engage for ASCI/FSSAI review, and provide their credentials?",
            "Do you have any experience with kids advertising campaigns or FMCG brands in the past 3 years?",
            "Can you convert your media buying fee to a gross-spend equivalent so it can be compared to other proposals?"
        ]
    },

    "V003": {
        "vendor_id": "V003",
        "vendor_name": "Brandsmith Group",
        "extraction_timestamp": "2026-07-25T10:35:00+05:30",
        "scope_coverage": {
            "line_items": [
                {"id": 1, "name": "Strategy and Creative Development", "covered": True, "detail": "Covered. Note: primary research is additional.", "status": "present", "evidence": "Full brand strategy, creative platform development, 3 campaign concept routes", "flags": []},
                {"id": 2, "name": "TVC Development", "covered": "partial", "detail": "Hindi TVCs only. English TVC development is extra (INR 8L). RFQ requires both languages.", "status": "partial", "evidence": "2 x 30-second TVC scripts (Hindi)... English language TVC versions are available at an additional cost of INR 8,00,000", "flags": ["English TVC not included in proposal price — additional INR 8L. RFQ requires Hindi AND English."]},
                {"id": 3, "name": "TVC Production", "covered": "partial", "detail": "Hindi TVC production only. English TVC production cost is not mentioned at all.", "status": "partial", "evidence": "2 x 30-second TVCs (Hindi)... Travel and accommodation for crew required outside Mumbai are charged at actuals", "flags": ["English TVC production cost not stated anywhere in proposal", "Out-of-city travel excluded"]},
                {"id": 4, "name": "Social Organic Content", "covered": "partial", "detail": "45 posts/month vs 60 required. Vendor frames lower volume as a recommendation.", "status": "partial", "evidence": "45 posts/month for 6 months... quality and consistency outperform volume", "flags": ["Volume gap: 45 vs 60 posts/month. Not acknowledged as a scope gap."]},
                {"id": 5, "name": "Social Paid Media Planning", "covered": True, "detail": "Covered", "status": "present", "evidence": "Comprehensive paid media strategy, platform selection, audience framework, budget model", "flags": []},
                {"id": 6, "name": "Social Paid Media Buying and Optimization", "covered": True, "detail": "Covered, but with internal conflict — initially included in 'all-inclusive' then separately priced at INR 35L", "status": "conflicting", "evidence": "Statement 1: 'paid media buying and optimization service is part of our integrated offering to NourishPlus' | Statement 2: 'Please note the paid media management fee below: Paid Media Management Fee: INR 35,00,000'", "flags": ["CONFLICT: First says included in all-inclusive, then separately priced. Buyer cannot determine actual scope inclusion."]},
                {"id": 7, "name": "Kids Advertising and Claims Compliance", "covered": "partial", "detail": "Vague claim of ASCI compliance with no process detail, no named reviewer, no regulatory specifics.", "status": "unclear", "evidence": "Brandsmith is ASCI compliant. All our advertising is created with full awareness of the ASCI code", "flags": ["ASCI claim is vague — no process described, no reviewer named, no ASCI case studies", "No FSSAI mention at all"]},
                {"id": 8, "name": "Launch Program Management", "covered": "partial", "detail": "Basic PM. Dedicated project coordinator (not senior PM). No steering committee facilitation.", "status": "partial", "evidence": "Dedicated project coordinator... Weekly status reports... Risk management and escalation", "flags": ["Project coordinator vs senior PM as RFQ requires", "No steering committee facilitation mentioned"]}
            ],
            "overall_coverage_score": "62",
            "uncovered_items": ["English TVC (priced as extra)", "Full social organic volume (45 vs 60)", "Detailed compliance process", "Senior PM as specified"]
        },
        "pricing": {
            "total_stated": "INR 3,90,00,000",
            "currency": "INR",
            "includes_gst": False,
            "itemized": [
                {"item": "Brand Strategy & Creative", "cost": "INR 40,00,000", "status": "present"},
                {"item": "TVC Development (Hindi only)", "cost": "INR 32,00,000", "status": "present"},
                {"item": "TVC Production (Hindi only)", "cost": "INR 1,60,00,000", "status": "present"},
                {"item": "Social Organic Content (45 posts)", "cost": "INR 60,00,000", "status": "present"},
                {"item": "Paid Media Planning", "cost": "INR 15,00,000", "status": "present"},
                {"item": "Paid Media Buying & Optimization (6 months)", "cost": "INR 35,00,000", "status": "present"},
                {"item": "Kids Compliance Review", "cost": "INR 12,00,000", "status": "present"},
                {"item": "Program Management", "cost": "INR 10,00,000", "status": "present"},
                {"item": "English TVC Development", "cost": "INR 8,00,000 (ADDITIONAL — not in total)", "status": "partial"},
                {"item": "English TVC Production", "cost": "NOT STATED", "status": "missing"}
            ],
            "itemized_total": "INR 3,64,00,000",
            "consistency_check": "FAIL",
            "consistency_note": "CONFLICT: Executive summary states INR 3,90,00,000 but itemized line items total INR 3,64,00,000. Discrepancy of INR 26,00,000. Vendor explains as 'contingency and project infrastructure' but this is not itemized.",
            "status": "conflicting",
            "evidence": "Statement 1: 'Our proposed investment for the complete NourishKids campaign: INR 3,90,00,000' | Statement 2: [itemized table totals to INR 3,64,00,000]",
            "flags": [
                "🚨 CRITICAL CONFLICT: Summary total (INR 3.90 Cr) vs itemized total (INR 3.64 Cr) — INR 26L unexplained",
                "English TVC production cost completely missing — INR unknown",
                "Micro-influencer fees additional (above INR 5,000/post)",
                "Out-of-city travel at actuals not priced"
            ]
        },
        "commercial_terms": {
            "payment_terms": {"value": "40% advance, 30% at mid-campaign, 30% at completion", "status": "present", "evidence": "40% advance, 30% at mid-campaign milestone, 30% at campaign completion"},
            "proposal_validity": {"value": "60 days from 23 Jul 2026", "status": "present", "evidence": "Validity: 60 days from submission date"},
            "gst_treatment": {"value": "18% GST applicable", "status": "present", "evidence": "GST: 18% applicable on all services"},
            "escalation_clause": {"value": None, "status": "missing", "evidence": None},
            "flags": ["40% advance is higher than RFQ's expected 30%"]
        },
        "timeline": {
            "proposed_kickoff": {"value": "Week 1", "status": "present", "evidence": "Phase 1: Strategy, brief, stakeholder alignment, Weeks 1–3"},
            "campaign_go_live": {"value": "Week 15 (digital/social) and Week 16 (TVC on-air)", "status": "present", "evidence": "Campaign launch (social + digital): Week 15... TVC on-air + full campaign live: Week 16"},
            "total_duration": {"value": "52 weeks (full year through Phase 11)", "status": "present", "evidence": "Ongoing optimisation, content, management: Weeks 16–52"},
            "consistency_check": "FAIL",
            "consistency_note": "CRITICAL CONFLICT: Executive summary states '6–8 weeks to go-live' but detailed plan shows 15–16 weeks minimum. These cannot both be true.",
            "flags": [
                "🚨 CRITICAL CONFLICT: Executive summary claims '6–8 weeks to campaign go-live' but detailed plan shows 15–16 weeks minimum",
                "Vendor acknowledges conflict and attributes 6–8 weeks to digital only, but executive summary is misleading"
            ]
        },
        "team_and_experience": {
            "key_personnel": [
                {"role": "Account Director", "name": "Manoj Kumar", "experience": "Not stated"},
                {"role": "Creative Director", "name": "Divya Sharma", "experience": "Not stated"},
                {"role": "Strategist", "name": "Kiran Mehta", "experience": "Not stated"},
                {"role": "Social Media Manager", "name": "Rahul Gupta", "experience": "Not stated"},
                {"role": "Performance Lead", "name": "Anita Singh", "experience": "Not stated"},
                {"role": "Project Coordinator", "name": "Sunita Rao", "experience": "Not stated"},
                {"role": "Post-Production", "name": "Suresh Iyer", "experience": "Not stated"},
                {"role": "TVC Director", "name": "TBD", "experience": "TBD"}
            ],
            "team_size_claimed": {"value": "15 specialists claimed, but only 8 people listed", "status": "conflicting", "evidence": "Statement 1: 'We will assign a dedicated team of 15 specialists' | Statement 2: [8 people listed in team table]"},
            "kids_category_experience": {"value": "Haldirams Snacks cited but targets families, not specifically kids advertising", "status": "partial", "evidence": "Haldirams snack campaigns target families including children", "flags": ["Haldirams family snacks ≠ ASCI Chapter III kids advertising. Not equivalent to dedicated kids advertising experience."]},
            "relevant_clients": ["ITC Foods (Bingo)", "Haldirams", "Paper Boat", "Marico (Livon)", "Voltas"],
            "flags": [
                "Team size conflict: 15 claimed vs 8 listed",
                "Team member experience years not provided for any person",
                "TVC Director listed as TBD — key role unconfirmed"
            ]
        },
        "compliance": {
            "asci_kids_code": {"value": "Vague claim: 'ASCI compliant' with no process, reviewer, or evidence", "status": "unclear", "evidence": "Brandsmith is ASCI compliant. Our internal review process ensures every piece of communication meets regulatory standards", "detail_level": "low"},
            "fssai_health_claims": {"value": "Not mentioned at all", "status": "missing", "evidence": None, "detail_level": "none"},
            "platform_policies": {"value": "Not mentioned", "status": "missing", "evidence": None},
            "compliance_reviewer_named": False,
            "flags": ["ASCI claim lacks any supporting evidence or process detail", "FSSAI completely absent from proposal", "No named compliance reviewer"]
        },
        "assumptions": {
            "listed": ["Primary research is additional", "Out-of-city travel at actuals", "English TVC is additional", "Micro-influencer fees additional above INR 5K"],
            "status": "partial",
            "count": 4
        },
        "exclusions": {
            "listed": ["Media buying budget", "English TVC development and production", "Micro-influencer fees above INR 5K", "Travel outside Mumbai at actuals", "Primary consumer research"],
            "hidden_costs_detected": ["English TVC production cost not priced anywhere", "INR 26L discrepancy between summary and itemized total unexplained"],
            "status": "partial"
        },
        "risks": [
            {"risk": "CRITICAL: Pricing conflict — INR 26L gap between summary and itemized total, unexplained", "severity": "high", "category": "commercial", "evidence": "contingency reserve and project infrastructure costs of INR 26,00,000 which are not broken out"},
            {"risk": "CRITICAL: Timeline conflict — claims 6-8 weeks but plan shows 15-16 weeks", "severity": "high", "category": "timeline", "evidence": "we guarantee campaign go-live within 6–8 weeks [vs] Campaign launch: Week 15, TVC on-air: Week 16"},
            {"risk": "CRITICAL: Line Item 6 conflict — first included in all-inclusive, then separately priced", "severity": "high", "category": "commercial", "evidence": "paid media buying and optimization service is part of our integrated offering [vs] Paid Media Management Fee: INR 35,00,000"},
            {"risk": "Team size conflict — 15 claimed, 8 listed, TVC director TBD", "severity": "medium", "category": "team", "evidence": "dedicated team of 15 specialists [vs] 8 listed"},
            {"risk": "Compliance vague — 'ASCI compliant' with no evidence, no FSSAI mention, no reviewer named", "severity": "high", "category": "compliance", "evidence": "Brandsmith is ASCI compliant"},
            {"risk": "English TVC cost completely unknown — missing from pricing", "severity": "high", "category": "commercial", "evidence": "English language TVC versions are available at an additional cost"}
        ],
        "missing_info": ["English TVC production cost", "Team member experience years", "Financial information", "FSSAI compliance process", "Named compliance reviewer", "Escalation clause", "TVC director name"],
        "unclear_info": ["INR 26L discrepancy between summary and itemized pricing", "Actual scope of Line Item 6 (included vs separate)", "What exactly 'ASCI compliant' means in practice"],
        "conflicting_info": [
            {"area": "Total pricing", "statement_1": "Our proposed investment for the complete NourishKids campaign: INR 3,90,00,000", "statement_2": "Itemized line items total INR 3,64,00,000", "buyer_impact": "True cost of proposal is unclear. INR 26L is unexplained."},
            {"area": "Project timeline", "statement_1": "We guarantee campaign go-live within 6–8 weeks of project kickoff", "statement_2": "Detailed plan shows Campaign launch at Week 15, TVC on-air Week 16", "buyer_impact": "Vendor may be misleading the buyer on delivery speed."},
            {"area": "Paid media buying inclusion", "statement_1": "paid media buying and optimization service is part of our integrated offering to NourishPlus", "statement_2": "Please note the paid media management fee below: Paid Media Management Fee: INR 35,00,000", "buyer_impact": "Is paid media management included or not? Cannot determine from proposal."},
            {"area": "Team size", "statement_1": "We will assign a dedicated team of 15 specialists to the NourishKids account", "statement_2": "Team table lists 8 people (including 1 TBD)", "buyer_impact": "Either 7 unnamed team members exist or claim is inflated."}
        ],
        "overall_data_quality": "LOW",
        "buyer_flags": [
            "🚨 CRITICAL: 4 internal conflicts detected in pricing, timeline, scope, and team — proposal reliability is low",
            "🚨 CRITICAL: Pricing total conflict (INR 26L gap) must be resolved before any comparison",
            "🚨 CRITICAL: 6–8 week go-live claim is contradicted by their own 15–16 week plan",
            "⚠️ English TVC (mandatory per RFQ) is priced separately and production cost unknown",
            "⚠️ Compliance is vague — FSSAI not mentioned, no reviewer named",
            "ℹ️ Payment terms (40% advance) are higher than RFQ norm"
        ],
        "clarification_questions": [
            "Please reconcile the executive summary price of INR 3,90,00,000 with the itemized total of INR 3,64,00,000. What is included in the INR 26,00,000 difference?",
            "Your executive summary states 'campaign live in 6–8 weeks' but your detailed plan shows 15–16 weeks. Which timeline is correct, and what is your commitment?",
            "Is paid media buying and optimization included in your all-inclusive proposal price, or is the INR 35,00,000 fee in addition to the total?",
            "What is the cost of English TVC production (not just development)?",
            "Who is your named ASCI compliance reviewer? What is their background and process?",
            "Your team section lists 8 people. Who are the remaining 7 of the 15 specialists you mention?"
        ]
    }
}
