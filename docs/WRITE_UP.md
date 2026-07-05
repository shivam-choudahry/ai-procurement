# RFQ AI Procurement Copilot — Short Write-Up

**Author:** Shivam Choudhary  
**Date:** July 2026  
**Assignment:** Generative AI Expert / Applied AI Engineer — Prototyping Assignment

---

## 1. Problem Solved

Procurement buyers evaluating marketing agencies face a recurring challenge: vendors respond in wildly different formats, use different pricing structures, make vague claims, omit critical information, and contradict themselves within their own proposals. A buyer evaluating three to five proposals must manually cross-reference dozens of dimensions — scope coverage, pricing clarity, compliance capability, timeline realism — often under time pressure.

This prototype solves that. It uses a prompt-driven multi-agent AI workflow to:
- Generate a realistic, structured RFQ for a marketing services procurement event
- Generate messy, real-world-quality vendor responses with deliberate complexity
- Extract structured procurement information from each vendor response with evidence anchoring
- Flag missing, unclear, conflicting, and risky information — without hallucinating
- Compare vendors across six evaluation dimensions in a buyer-readable format
- Present everything in a 7-screen buyer-facing UI with risk dashboards, evidence boxes, and confidence scores

---

## 2. Key Assumptions

- **Domain:** Marketing services procurement for NourishKids (a fortified kids snack brand by NourishPlus Foods India Ltd.). This is a realistic, representative scenario for FMCG marketing agency selection.
- **Vendor count:** Three vendor responses in demo mode (Apex Creative Co., Spark Digital Agency, Brandsmith Group). The AI generation pipeline produces five distinct vendor personas.
- **Currency / Market:** Indian market, INR pricing, ASCI and FSSAI compliance context — a deliberately non-trivial compliance landscape.
- **No OCR required:** The prototype accepts text-based document formats (PDF, DOCX, TXT, Markdown, JSON, or pasted text). Production-grade OCR is out of scope for this prototype.
- **Demo mode:** The system runs fully without an OpenAI API key using pre-generated data, enabling reviewers to explore all screens without incurring API cost.
- **LLM:** OpenAI GPT-4o via structured outputs (Pydantic V2 models). All LLM outputs are typed — the system never parses raw markdown or tables.

---

## 3. Prompt Architecture

Eight purpose-built prompts drive the system, chained through a LangGraph workflow:

| Prompt | Purpose | Key Design Choice |
|--------|---------|-------------------|
| `rfq.md` | Generate a structured RFQ with all 8 line items | Role-assigned persona (Senior Procurement Director); output schema enforced via Pydantic |
| `vendor_generation.md` | Generate 5 distinct vendor personas with varied response quality | Explicit instruction to vary completeness, pricing structure, assumptions, and compliance depth across vendors |
| `messy_vendor.md` | Generate edge-case complexity: missing prices, vague timelines, partial scope | Used as a "data quality stress test" — ensures extraction agents encounter real-world messiness |
| `extraction.md` | Extract structured procurement data from vendor responses | "Do not infer" as CRITICAL RULE; 5-value status taxonomy; evidence anchoring for all `present`/`partial` fields |
| `validation.md` | Validate extraction quality; detect contradictions and unsupported claims | Contradiction detection across same vendor's fields; flags inconsistencies between stated scope and pricing |
| `comparison.md` | Compare vendors across 6 dimensions | "NOT COMPARABLE" is a valid output; no winner recommendation — buyer decides; all comparisons grounded in extracted data only |
| `recommendation.md` | Generate shortlisting recommendation with confidence scores | Every pro/con must cite specific evidence; three outcomes: Shortlist / Conditional / Reject |
| `ui_generation.md` | Generate buyer-facing UI structure and UX copy | Frames the AI as a procurement analyst, not a dashboard generator |

**Prompt chaining logic:** Each prompt receives only the output of the prior step — extraction receives raw vendor text; comparison receives extraction output; recommendation receives comparison output. This prevents early-stage hallucinations from compounding downstream.

**Hallucination controls** are layered across four agents:
- Extraction: "Do not infer, assume, or fill gaps" — `missing` is a valid and rewarded output
- Extraction: Evidence quotation required for all `present` and `partial` fields
- Comparison: "Base ALL comparisons on extracted data only — no inference"
- Recommendation: All pros and cons must cite specific, traceable evidence

---

## 4. Product Thinking

**What the buyer should see first:** The RFQ Overview (what was asked) before any vendor data. A buyer who hasn't read their own RFQ carefully cannot evaluate responses meaningfully.

**How missing data is surfaced:** Missing fields are shown as 🔴 badges — not hidden or greyed out. The absence of information is information. A vendor who hasn't answered the compliance question is telling the buyer something.

**How conflicts are handled:** Contradictions within a vendor's response (e.g., "all-inclusive" in the executive summary vs. items excluded in the commercial section) are surfaced explicitly as conflict boxes, not silently resolved.

**How comparisons are presented:** Vendors are scored on six dimensions, but scores are accompanied by evidence snippets and buyer flags — not just a number. A vendor scoring 6/10 on compliance means something different from one scoring 6/10 on pricing; the UI preserves that context.

**What the buyer decides:** The system never picks a winner. It shortlists, flags conditions, and identifies risks. The Recommendation screen shows which vendors are ready to shortlist, which are conditional on clarification, and which should be rejected — with confidence scores that signal how much certainty the AI has.

---

## 5. UI/UX Decisions

The 7-screen Streamlit UI was designed around the buyer's decision journey, not the system's data model:

1. **RFQ Overview** — Anchors the buyer in the procurement context before showing any vendor data
2. **Vendor Responses** — Shows all proposals with quality badges (HIGH / MEDIUM / LOW) and top flags visible at a glance
3. **Upload** — Supports both file upload and text paste; processes dynamically via the extraction pipeline
4. **Extraction Review** — Per-vendor view with 6 sub-tabs; evidence boxes for every claimed value; conflict and risk highlights inline
5. **Vendor Comparison** — Scorecard + matrix + differentiator callouts; designed for side-by-side decision support
6. **Risks** — Consolidated risk dashboard across all vendors; confidence scores; shortlisting recommendations
7. **Prompt Trace** — Full AI audit trail; 8 prompts with explanations; live trace log of every LLM call

Design principles: information density without cognitive overload; evidence always visible alongside conclusions; no hidden AI decisions.

---

## 6. Extraction Approach

The extraction agent reads raw vendor text and produces a structured JSON output covering: scope coverage per line item, pricing (total, itemized, consistency check), timeline, compliance, commercial terms, assumptions, exclusions, risks, buyer flags, conflicts, and clarification questions.

The critical design choice is the **5-value status taxonomy**: `present | partial | missing | unclear | conflicting`. This forces the model to be honest about data quality rather than hallucinating plausible values. The `missing` outcome is explicitly rewarded in the prompt — the model is told that accurately flagging missing information is more valuable than filling gaps.

Every `present` or `partial` field must include an `evidence` field quoting the relevant source text. This makes the extraction auditable: a buyer can trace every extracted value back to the original proposal.

---

## 7. Comparison Approach

The comparison agent receives extraction outputs from all vendors and compares them across: scope coverage, pricing clarity, commercial completeness, timeline clarity, compliance quality, and risk level.

Key design choices:
- **"NOT COMPARABLE"** is a valid output when vendors have responded to different scope interpretations (e.g., one vendor quoted broadcast TVC production, another quoted digital video only)
- **No winner declaration** — the agent identifies differences, not the best vendor
- **Buyer attention points** call out the highest-stakes differences requiring human judgment
- **Clarification questions** are generated per vendor, enabling the buyer to run a structured clarification round before final shortlisting

---

## 8. Limitations

- **No real OCR:** Scanned PDFs or image-based documents cannot be processed; text extraction requires machine-readable files
- **Single LLM dependency:** The system uses GPT-4o exclusively; no fallback to alternative models if the API is unavailable
- **Demo data is synthetic:** The pre-generated vendor data, while realistic, was AI-generated — not sourced from real procurement events
- **No persistent storage:** The system uses file-based storage (`generated/`, `prompt_trace/`); there is no database for multi-user or multi-session workflows
- **LangGraph workflow is linear:** The pipeline does not support conditional branching (e.g., re-running extraction if validation fails) in the current implementation
- **PPT and Excel parsing not supported:** Vendor proposals submitted as PowerPoint or Excel files cannot be processed

---

## 9. What I Would Improve with More Time

1. **Conditional LangGraph branching:** If validation flags critical extraction failures, re-run extraction with a repair prompt before proceeding to comparison
2. **Multi-format support:** Add PPT (python-pptx) and Excel (openpyxl) parsers; add OCR support via pytesseract or Azure Form Recognizer for scanned documents
3. **Human-in-the-loop review:** Add a buyer annotation layer where the extraction review can be manually corrected before comparison runs, with corrections fed back as few-shot examples
4. **Prompt evaluation framework:** Instrument extraction quality with an LLM-as-judge step that scores each extraction on completeness, hallucination, and evidence quality — enabling systematic prompt improvement
5. **Structured vendor comparison export:** Generate a procurement-ready Excel/PDF comparison report that a buyer can share with stakeholders without showing the AI interface
6. **Multi-session support:** Replace file-based state with a lightweight database (SQLite or Postgres) to support multiple concurrent procurement events
7. **Feedback loop:** Capture buyer decisions (shortlist / reject) and use them to improve future recommendation prompts via fine-tuning or few-shot examples

---

*Total system: 8 AI agents · 8 purpose-built prompts · 7 buyer-facing screens · LangGraph orchestration · Pydantic V2 structured outputs · OpenAI GPT-4o*

