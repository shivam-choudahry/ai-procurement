"""Pre-generated comparison data for demo mode."""

COMPARISON_DATA = {
    "comparison_id": "CMP-2026-NKL-001",
    "comparison_timestamp": "2026-07-25T11:00:00+05:30",
    "vendors_compared": ["Apex Creative Co.", "Spark Digital Agency", "Brandsmith Group"],
    "rfq_reference": "RFQ-MKT-2026-NKL-001",

    "dimension_scores": {
        "scope_coverage": {
            "description": "How completely each vendor covers all 8 RFQ line items",
            "scores": {
                "V001": {"score": 4, "rationale": "7.5/8 line items covered. Minor gap: English TVC is adaptation not independent.", "key_gaps": ["English TVC independently developed"]},
                "V002": {"score": 2, "rationale": "4/8 line items fully covered. Broadcast TVC (LI2, LI3) outside scope. Compliance absent (LI7).", "key_gaps": ["Broadcast TVC development", "Broadcast TVC production", "Kids compliance in-house", "Full PM scope"]},
                "V003": {"score": 3, "rationale": "6/8 covered but with significant caveats. English TVC extra cost. Social volume gap (45 vs 60).", "key_gaps": ["English TVC (additional cost)", "Social organic volume", "Detailed compliance"]}
            },
            "winner": "Apex Creative Co.",
            "comparability_note": "All 3 vendors can be compared on scope, but scope gap between Apex and others is significant."
        },
        "pricing_clarity": {
            "description": "How clear, complete, and comparable the pricing is",
            "scores": {
                "V001": {"score": 4, "rationale": "Fully itemized, internally consistent. Hidden cost: media buying commission (10%). Well disclosed.", "key_gaps": ["Media buying commission excluded from total"]},
                "V002": {"score": 1, "rationale": "Total is incomplete — broadcast TVC production is TBD (INR 80–120L range). Not a comparable quote.", "key_gaps": ["Broadcast TVC production unpriced", "Influencer fees in USD", "Compliance cost unknown"]},
                "V003": {"score": 2, "rationale": "PRICING CONFLICT: Summary INR 3.90 Cr vs itemized INR 3.64 Cr. INR 26L gap unexplained. Unreliable.", "key_gaps": ["INR 26L pricing conflict", "English TVC production unpriced"]}
            },
            "total_costs": {
                "V001": {"comparable_total": "INR 4,20,00,000 (+ GST + media commission)", "note": "Complete for RFQ scope minus English TVC independence"},
                "V002": {"comparable_total": "INCOMPLETE — INR 1,75,00,000 but excludes broadcast TVC (up to INR 1.20 Cr)", "note": "Cannot determine full cost"},
                "V003": {"comparable_total": "CONFLICTED — either INR 3,64,00,000 or INR 3,90,00,000; English TVC production also missing", "note": "Resolve conflict before comparison"}
            },
            "winner": "NOT COMPARABLE — pricing cannot be compared until V002 provides TVC cost and V003 resolves pricing conflict",
            "comparability_note": "Only V001 provides a complete, consistent price for full RFQ scope."
        },
        "commercial_completeness": {
            "description": "Payment terms, validity, assumptions, exclusions clarity",
            "scores": {
                "V001": {"score": 5, "rationale": "Most complete: payment terms, validity, escalation clause, full assumptions list, full exclusions list.", "key_gaps": []},
                "V002": {"score": 3, "rationale": "Payment terms and validity present. No escalation clause. Key exclusions identified.", "key_gaps": ["No escalation clause"]},
                "V003": {"score": 2, "rationale": "Payment terms present. No escalation. Pricing conflict undermines commercial reliability.", "key_gaps": ["No escalation clause", "Pricing conflict"]}
            },
            "winner": "Apex Creative Co.",
            "comparability_note": "Apex is significantly ahead on commercial completeness."
        },
        "timeline_quality": {
            "description": "Realism, clarity, and consistency of proposed timelines",
            "scores": {
                "V001": {"score": 4, "rationale": "Detailed 52-week plan with per-phase breakdown. Consistent. Minor: explicit Feb 2027 date not confirmed.", "key_gaps": ["Feb 2 go-live date not explicitly confirmed"]},
                "V002": {"score": 2, "rationale": "Digital timeline (10–12 weeks) provided. TVC timeline entirely undefined — critical gap.", "key_gaps": ["Broadcast TVC timeline missing"]},
                "V003": {"score": 1, "rationale": "CRITICAL CONFLICT: 6–8 week claim vs 15–16 week plan. Timeline is unreliable.", "key_gaps": ["6-8 week claim contradicts 15-16 week plan"]}
            },
            "winner": "Apex Creative Co.",
            "comparability_note": "Apex has the only complete and consistent timeline for full RFQ scope."
        },
        "compliance_quality": {
            "description": "Depth and credibility of ASCI, FSSAI, and platform compliance coverage",
            "scores": {
                "V001": {"score": 5, "rationale": "Named ex-ASCI reviewer, FSSAI checklist, platform policies, 3 verified case studies.", "key_gaps": []},
                "V002": {"score": 1, "rationale": "No in-house capability. External specialist recommended. Cannot deliver this requirement.", "key_gaps": ["No in-house ASCI/FSSAI capability"]},
                "V003": {"score": 2, "rationale": "Vague 'ASCI compliant' claim. No reviewer named. FSSAI absent. Not credible.", "key_gaps": ["No named reviewer", "No FSSAI mention", "No compliance process detail"]}
            },
            "winner": "Apex Creative Co.",
            "comparability_note": "Apex has a clear, verifiable compliance capability. Others do not meet RFQ requirement."
        },
        "risk_level": {
            "description": "Overall risk profile (higher score = LOWER risk = better)",
            "scores": {
                "V001": {"score": 4, "rationale": "Low risk overall. Main risks: media commission gap and English TVC ambiguity — both manageable.", "key_gaps": []},
                "V002": {"score": 1, "rationale": "High risk: scope gaps, incomplete pricing, no compliance capability, no relevant experience.", "key_gaps": []},
                "V003": {"score": 2, "rationale": "High risk: 4 internal conflicts, pricing unreliable, compliance vague, team claims unverified.", "key_gaps": []}
            },
            "note": "Higher score = LOWER risk. V001 is lowest risk; V002 and V003 are HIGH risk."
        }
    },

    "key_differentiators": [
        {"dimension": "Compliance", "finding": "Only Apex Creative Co. has a named, credentialed ASCI compliance reviewer (ex-ASCI panelist). Spark cannot deliver compliance in-house. Brandsmith makes a vague claim with no evidence.", "vendors_affected": ["V001", "V002", "V003"], "buyer_implication": "Compliance is a mandatory RFQ requirement. V002 and V003 cannot be shortlisted without resolving this gap."},
        {"dimension": "TVC Scope", "finding": "Apex delivers full broadcast TVC (Hindi + English adaptation). Spark delivers online video only, explicitly not broadcast TVC. Brandsmith delivers Hindi only (English is extra).", "vendors_affected": ["V001", "V002", "V003"], "buyer_implication": "If broadcast TV is a key channel, only Apex can deliver the full scope."},
        {"dimension": "Pricing Reliability", "finding": "Apex has consistent, complete pricing. Brandsmith has a INR 26L pricing conflict. Spark has an incomplete quote (TVC is TBD).", "vendors_affected": ["V002", "V003"], "buyer_implication": "Cannot compare total cost until V002 and V003 resolve pricing issues."},
        {"dimension": "Digital & Paid Media", "finding": "Spark is strongest on paid media performance (certified team, 3.2x ROAS claimed). Apex has in-house trading desk. Brandsmith has in-house capability but no performance metrics cited.", "vendors_affected": ["V001", "V002", "V003"], "buyer_implication": "If digital performance is the primary KPI, Spark has the strongest track record — but only for digital scope."},
        {"dimension": "Category Experience", "finding": "Apex has deep kids/FMCG experience (Nestlé, Britannia, Kinder Joy, Bournvita). Brandsmith has family FMCG (Haldirams). Spark has no kids or traditional FMCG experience.", "vendors_affected": ["V001", "V002", "V003"], "buyer_implication": "Kids advertising requires category knowledge. Apex has the strongest relevant experience."}
    ],

    "cannot_compare_because": [
        {"area": "Total campaign cost", "reason": "V002 has unpriced broadcast TVC; V003 has a pricing conflict of INR 26L", "vendors_affected": ["V002", "V003"], "resolution": "Ask V002 for firm TVC production price. Ask V003 to reconcile INR 26L gap and provide English TVC production cost."},
        {"area": "English TVC delivery", "reason": "V001 proposes adaptation (not independent development). V002 does not cover broadcast TVC. V003 prices it as extra.", "vendors_affected": ["V001", "V002", "V003"], "resolution": "Clarify RFQ requirement: is independently developed English TVC mandatory, or is adaptation acceptable?"},
        {"area": "Media buying cost equivalence", "reason": "V001 quotes 10% on gross spend; V002 quotes 12% on net spend. Different bases.", "vendors_affected": ["V001", "V002"], "resolution": "Normalise: ask both vendors to provide total commission assuming same media budget (e.g., INR 1 Cr/month × 4 months)."}
    ],

    "critical_conflicts_detected": [
        {"vendor": "Brandsmith Group (V003)", "conflict": "Summary price INR 3.90 Cr vs itemized total INR 3.64 Cr — INR 26L unexplained discrepancy", "impact": "Cannot trust either figure. True proposal cost is unknown.", "recommended_action": "Require written reconciliation before comparison."},
        {"vendor": "Brandsmith Group (V003)", "conflict": "'Campaign live in 6–8 weeks' in executive summary vs 15–16 weeks in detailed plan", "impact": "Vendor may be misleading buyer on delivery speed.", "recommended_action": "Require firm committed timeline with sign-off."},
        {"vendor": "Brandsmith Group (V003)", "conflict": "Paid media buying described as 'part of all-inclusive offering' then separately priced at INR 35L", "impact": "Scope and cost of this line item are unclear.", "recommended_action": "Require written clarification on whether INR 35L is included in or additional to total."}
    ],

    "buyer_attention_points": [
        {"priority": "HIGH", "point": "Kids advertising compliance is a mandatory requirement. Only Apex Creative Co. has credible in-house capability.", "vendor": "ALL", "action_required": "Confirm compliance approach before shortlisting V002 or V003."},
        {"priority": "HIGH", "point": "Pricing comparison is not yet possible — V002 quote is incomplete, V003 has a conflict.", "vendor": "V002, V003", "action_required": "Request revised pricing from V002 (include firm TVC cost) and V003 (reconcile discrepancy)."},
        {"priority": "HIGH", "point": "V001 total of INR 4.20 Cr excludes media buying commission (~INR 40L at assumed spend).", "vendor": "V001", "action_required": "Calculate true all-in cost including commission for fair comparison."},
        {"priority": "MEDIUM", "point": "English TVC scope differs across all 3 vendors. Clarify RFQ intent before evaluation.", "vendor": "ALL", "action_required": "Confirm whether independently developed English TVC is mandatory."},
        {"priority": "MEDIUM", "point": "Spark Digital has no kids or FMCG experience in cited portfolio.", "vendor": "V002", "action_required": "Ask for relevant experience examples before further evaluation."},
        {"priority": "LOW", "point": "Apex has 90-day validity; Brandsmith only 60 days. Award timeline is Feb 20 — within all validities.", "vendor": "ALL", "action_required": "Note for record. No immediate action required."}
    ],

    "clarification_questions_per_vendor": {
        "V001": [
            "What is the all-in cost of paid media management including the 10% commission, based on INR 1 Cr/month × 4 months?",
            "Can you confirm the English TVC will be independently developed (unique narrative), not just a dubbed adaptation?",
            "Please name the backup TVC director and confirm availability for August–November 2026."
        ],
        "V002": [
            "Provide a firm price for broadcast TVC production (2×30s + 4×10s). The range of INR 80–120L is insufficient for comparison.",
            "Name the specialist compliance consultant you would engage. Provide credentials and confirm ASCI/FSSAI capability.",
            "Do you have experience with kids advertising (ASCI Chapter III) or FMCG brands? Please provide references.",
            "Convert your media buying fee to a gross-spend equivalent for INR 1 Cr/month × 4 months."
        ],
        "V003": [
            "Reconcile in writing: your executive summary states INR 3,90,00,000 but your itemized table totals INR 3,64,00,000. What is the correct total, and what is included in the INR 26L difference?",
            "Confirm your committed campaign go-live timeline. Is it 6–8 weeks or 15–16 weeks?",
            "Is paid media buying and optimization (INR 35,00,000) included in or additional to your stated total?",
            "Provide the cost for English TVC production (not just development).",
            "Name your ASCI compliance reviewer and describe your review process.",
            "Reconcile: you state '15 specialists' but list 8 people. Who are the remaining 7?"
        ]
    },

    "overall_risk_summary": {
        "V001": {
            "risk_level": "LOW",
            "top_risks": [
                "Media buying commission adds ~INR 40L not visible in headline price",
                "English TVC is adaptation — may not meet RFQ independence requirement"
            ],
            "missing_before_decision": ["Confirm English TVC approach", "Clarify all-in paid media cost"]
        },
        "V002": {
            "risk_level": "HIGH",
            "top_risks": [
                "Cannot deliver broadcast TVC (core RFQ scope)",
                "Cannot deliver kids advertising compliance in-house",
                "No relevant kids or FMCG experience",
                "Total cost is incomplete"
            ],
            "missing_before_decision": ["Firm TVC cost", "Compliance plan", "Relevant experience evidence", "Complete pricing"]
        },
        "V003": {
            "risk_level": "HIGH",
            "top_risks": [
                "4 internal conflicts in proposal — low reliability",
                "Pricing total is untrustworthy (INR 26L gap)",
                "Timeline claim is misleading",
                "Compliance is vague and unverifiable"
            ],
            "missing_before_decision": ["Pricing reconciliation", "Timeline commitment", "Compliance reviewer details", "Team composition"]
        }
    },

    "comparison_limitations": [
        "Pricing comparison is not meaningful at this stage — V002 and V003 have incomplete/conflicting pricing",
        "V002 and V003 cannot be fairly scored against V001 on TVC scope — different scopes make direct comparison misleading",
        "Digital performance claims (V002's 3.2x ROAS) cannot be independently verified from proposal alone",
        "Compliance claims for all vendors should be independently verified before award decision"
    ]
}
