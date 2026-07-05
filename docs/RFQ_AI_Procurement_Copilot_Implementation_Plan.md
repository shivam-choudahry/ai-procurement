# RFQ AI Procurement Copilot — Implementation Plan

> **Vision:** Portfolio-quality project, not just an assignment submission.
> Showcase-ready for AI Engineering interviews.

---

## What We Are Building

```
                  RFQ AI Procurement Copilot
┌────────────────────────────────────────────────────────────┐
│                   Frontend (Streamlit)                     │
│                                                            │
│  RFQ │ Vendors │ Upload │ Extraction │ Comparison │        │
│  Risks │ Prompt Trace                                      │
└──────────────────────┬─────────────────────────────────────┘
                       │
                FastAPI Backend
                       │
                LangGraph Workflow
                       │
      ┌─────────────────────────────────────────┐
      │              AI Agents                  │
      ├─────────────────────────────────────────┤
      │ RFQ Generator                           │
      │ Vendor Response Generator               │
      │ Document Parser                         │
      │ Extraction Agent                        │
      │ Validation Agent                        │
      │ Comparison Agent                        │
      │ Buyer Recommendation Agent              │
      │ UI Generation Agent                     │
      └─────────────────────────────────────────┘
                       │
               OpenAI Structured Outputs
                       │
              Pydantic Models + JSON
```

---

## Technology Stack

### Backend
- **FastAPI** — REST API layer
- **LangGraph** — multi-agent orchestration workflow
- **LangChain** — LLM tooling and chaining
- **OpenAI Responses API** — GPT-4o with structured outputs
- **Pydantic V2** — all structured outputs, never parse markdown/tables
- **python-docx** — DOCX file parsing
- **pdfplumber** — PDF text extraction
- **pandas** — comparison matrix, tabular data

### Frontend
- **Streamlit** — primary UI (fastest path to demo-ready)
- React + Tailwind — future upgrade path

### Storage (no DB required)
```
generated/
    rfq.json
    vendors/
    extractions/
src/prompt_trace/
    workflow_trace.json
```

---

## Repository Structure

```
rfq-ai-assignment/
│
├── app.py                          # Streamlit frontend entry point
├── README.md
├── requirements.txt
├── pyproject.toml
│
├── src/                            # All source code lives here
│   ├── __init__.py
│   ├── config.py                   # Settings, env vars (pydantic-settings)
│   │
│   ├── routers/
│   │   └── api.py                  # FastAPI endpoints
│   │
│   ├── agents/
│   │   ├── state.py                # RFQWorkflowState TypedDict (LangGraph)
│   │   ├── graph.py                # LangGraph workflow definition
│   │   └── nodes/                  # Individual LangGraph node implementations
│   │       ├── rfq_generator.py
│   │       ├── vendor_generator.py
│   │       ├── parser.py
│   │       ├── extractor.py
│   │       ├── validator.py
│   │       ├── comparator.py
│   │       ├── recommendation.py
│   │       └── ui_agent.py
│   │
│   ├── schemas/                    # Pydantic V2 structured output models
│   │   ├── rfq.py
│   │   ├── vendor.py
│   │   ├── extraction.py
│   │   └── comparison.py
│   │
│   ├── prompts/                    # Prompt templates
│   │   ├── prompt_library.py       # All prompts + PROMPT_PACK metadata
│   │   ├── rfq.md
│   │   ├── vendor_generation.md
│   │   ├── messy_vendor.md
│   │   ├── extraction.md
│   │   ├── validation.md
│   │   ├── comparison.md
│   │   ├── recommendation.md
│   │   └── ui_generation.md
│   │
│   ├── prompt_trace/               # Saved prompt trace JSON files
│   │   └── workflow_trace.json
│   │
│   └── utils/
│       ├── helpers.py              # UI helpers
│       ├── llm.py                  # LLM wrapper (retry, Langfuse, fallback)
│       └── parsers/                # Document parsing
│           ├── pdf.py
│           ├── docx.py
│           ├── xlsx.py
│           └── txt.py
│
├── data/                           # Pre-generated demo data
├── sample_data/                    # Sample vendor documents for upload testing
├── generated/                      # LLM-generated outputs at runtime
└── docs/
```

---

## Development Phases

### Phase 1 — Foundation
- FastAPI app skeleton with health endpoint
- LangGraph installed and wired
- OpenAI client configured with structured output support
- Streamlit shell with page routing
- `.env.example`, logging, `config.py`

---

### Phase 2 — Pydantic Models (`src/schemas/`)

All LLM outputs must be Pydantic. Never parse markdown. Never parse tables.

```python
class VendorExtraction(BaseModel):
    vendor_name: str
    pricing: Pricing
    timeline: Timeline
    compliance: Compliance
    risks: list[Risk]
    assumptions: list[str]
    exclusions: list[str]
    evidence: list[Evidence]
```

Models to build:
- `RFQ` — general_information, timeline, scope, pricing_expectation, questionnaire, compliance
- `VendorResponse` — vendor profile and raw proposal text
- `Pricing` — line items, totals, tax handling, currency
- `Timeline` — milestones, delivery dates, assumptions
- `Scope` — line items with included/excluded flags
- `Compliance` — certifications, regulatory, in-house vs outsourced
- `Risk` — severity (🔴/🟠/🟢), description, source evidence
- `Evidence` — quoted text, page/section reference, field it supports
- `VendorExtraction` — full structured extraction per vendor
- `ValidationResult` — missing values, contradictions, unsupported claims
- `ComparisonMatrix` — per-vendor scores across all dimensions
- `BuyerRecommendation` — pros, cons, risk, confidence, evidence
- `RFQWorkflowState` — TypedDict for LangGraph state

```python
class RFQWorkflowState(TypedDict):
    rfq: RFQ
    uploaded_documents: list[UploadedDoc]
    parsed_documents: list[ParsedDoc]
    vendor_extractions: list[VendorExtraction]
    validation: list[ValidationResult]
    comparison: ComparisonMatrix
    recommendation: BuyerRecommendation
    prompt_trace: list[PromptTraceEntry]
```

---

### Phase 3 — Prompt Management (`src/prompts/`)

Each prompt lives as an independent `.md` file — inspectable by recruiters.

| File | Purpose |
|------|---------|
| `rfq.md` | Generate structured RFQ JSON from procurement brief |
| `vendor_generation.md` | Generate varied, realistic vendor proposals |
| `messy_vendor.md` | 10 specific edge-case mess types for testing |
| `extraction.md` | 5-status taxonomy, evidence anchoring, no-inference rule |
| `validation.md` | Missing values, contradictions, hallucination prevention |
| `comparison.md` | Grounded comparison, NOT COMPARABLE as valid output |
| `recommendation.md` | Pros, cons, risk, confidence, evidence per vendor |
| `ui_generation.md` | Buyer-journey framing, uncertainty display, hierarchy |

**Prompt design rules:**
- Role assignment in every prompt
- Evidence anchoring — every present/partial field must cite source text
- Status taxonomy: `present / partial / missing / unclear / conflicting`
- "NOT COMPARABLE" is a valid and expected comparison output
- "Do not infer, assume, or fill gaps" as a CRITICAL RULE in extraction
- No winner recommendation — preserves buyer decision authority

---

### Phase 4 — LLM Wrapper

Common interface for all agents:
- Structured outputs via Pydantic (OpenAI `response_format`)
- Retry logic with exponential backoff
- Prompt trace capture (input → prompt → raw output → parsed JSON)
- Token usage and latency logging
- Error handling with graceful fallback to demo data

---

### Phase 5 — AI Agents (`src/agents/nodes/`)

#### RFQ Generator
- Input: procurement brief (category, budget, brand, timeline)
- Output:
```json
{
  "general_information": {},
  "timeline": {},
  "scope": [],
  "pricing_expectation": {},
  "questionnaire": [],
  "compliance": []
}
```

#### Vendor Response Generator
Generate 5 distinct vendor personas — every response must differ:

| Vendor | Profile |
|--------|---------|
| Vendor A | Premium — comprehensive, higher cost |
| Vendor B | Cheap — low cost, cuts corners |
| Vendor C | Messy — disorganized, contradictory |
| Vendor D | Conflicting — internal contradictions |
| Vendor E | Incomplete — missing critical sections |

#### Document Parser (`src/utils/parsers/`)
- `pdf.py` — pdfplumber text extraction
- `docx.py` — python-docx extraction
- `txt.py` — plain text passthrough
- `xlsx.py` — openpyxl all sheets → Markdown tables
- Accept: PDF, DOCX, TXT, Markdown
- Output: normalized plain text per vendor

#### Extraction Agent
Produces per-vendor structured extraction:
- Vendor name and profile
- Pricing (line items, totals, taxes, currency)
- Timeline (milestones, assumptions)
- Scope (included/excluded)
- Compliance (certifications, regulatory)
- Assumptions and exclusions (explicit lists)
- Risks (severity + evidence)
- Missing information (flagged explicitly)
- Evidence (quoted text + source reference)

#### Validation Agent
Checks extraction quality:
- Missing required values
- Internal contradictions (e.g., timeline conflict)
- Unsupported claims (no evidence)
- Hallucination prevention flags
- Outputs `ValidationResult` per vendor

#### Comparison Agent
Produces:
- Vendor scorecard across 6 dimensions
- Comparison matrix (pandas DataFrame → Streamlit table)
- Risk matrix (🔴/🟠/🟢 per vendor per dimension)
- Clarification questions (auto-generated, context-cited)
- Buyer summary

#### Recommendation Agent
Produces per vendor:
- Pros (evidence-backed)
- Cons (evidence-backed)
- Risk level
- Recommendation (shortlist / conditional / reject)
- Confidence score (0–100%)
- Evidence citations

---

### Phase 6 — LangGraph Workflow (`src/agents/graph.py`)

```
START
↓
Generate RFQ
↓
Generate Vendors
↓
Upload Vendor Documents        ← also accepts external uploads
↓
Parse Documents
↓
Extract Information
↓
Validate Extraction
↓
Compare Vendors
↓
Generate Recommendation
↓
Generate Prompt Trace
↓
END
```

State flows through `RFQWorkflowState` TypedDict at every node.

---

### Phase 7 — FastAPI Backend (`src/routers/api.py`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/generate-rfq` | POST | Run RFQ Generator agent |
| `/generate-vendors` | POST | Run Vendor Generator agent |
| `/upload-vendor` | POST | Accept file upload, parse, extract |
| `/extract` | POST | Run Extraction + Validation agents |
| `/compare` | POST | Run Comparison + Recommendation agents |
| `/prompt-trace` | GET | Return full prompt trace log |
| `/health` | GET | Health check |

---

### Phase 8 — Streamlit Frontend (`app.py`)

| Page | Icon | What It Shows |
|------|------|--------------|
| RFQ Overview | 🏠 | Full RFQ — scope, timeline, compliance, questionnaire |
| Vendor Responses | 📄 | All vendor proposals; upload new ones |
| Upload | 📤 | PDF / DOCX / TXT / Markdown upload + instant extraction |
| Extraction Review | 🔍 | Per-vendor structured extraction with flags and evidence |
| Vendor Comparison | 📊 | Scorecard, comparison matrix, differentiators |
| Risks | ⚠ | Buyer Risk Dashboard (🔴 High / 🟠 Medium / 🟢 Low) |
| Prompt Trace | 📝 | Full prompt pack + live traces |

**Confidence Score display:**
```
Pricing     ████████████████████░░  95%
Timeline    ████████████████████░░░  88%
Compliance  ████████████████░░░░░░░  73%
```

**Evidence Highlighting:**
```
Vendor claim: "We can deliver in six weeks."
Evidence:     Page 2, Paragraph 4
```

**Clarification Questions (auto-generated):**
- Please clarify whether GST is included in the total pricing.
- Please confirm the production timeline for the Hindi TVC.
- Please explain paid media planning assumptions.

**Buyer Risk Dashboard:**
```
🔴 High    Pricing unclear — no breakdown provided
🟠 Medium  Timeline assumption — 6 weeks not explained
🟢 Low     Compliance — certifications confirmed
```

---

### Phase 9 — Prompt Trace & Logging (`prompt_trace/`)

Capture for every LLM call:
1. Raw input (user data / state)
2. Rendered prompt (sent to OpenAI)
3. LLM raw response
4. Parsed JSON (Pydantic model)
5. Final UI output
6. Token usage (prompt + completion)
7. Latency (ms)
8. Errors (if any)

Saved as JSON files in `prompt_trace/`. Viewable in Prompt Trace screen.

---

### Phase 10 — Documentation & Demo

- **README.md** — full architecture, setup, prompt design rationale
- **Architecture Diagram** — system overview (this document's diagram)
- **Prompt Pack** — all 8 prompts with rationale, viewable in UI
- **Sample Data** — pre-generated RFQ + 5 vendor responses (demo mode, no API key needed)
- **Demo Video** — walkthrough of all 7 screens
- **Assignment Write-up** — covers each rubric point with implementation evidence

---

## Hallucination Controls

| Layer | Control |
|-------|---------|
| Extraction | "Do not infer, assume, or fill gaps" as CRITICAL RULE |
| Extraction | `missing` is an expected, rewarded output — not a failure |
| Comparison | "Base ALL comparisons on extracted data only" |
| Comparison | No vendor recommendation — buyer decides |
| Validation | Contradiction detection across same vendor's fields |
| Validation | Unsupported claim flagging — evidence required |

---

## Stretch Goals

- [ ] Human review workflow — "review and correct extraction" UI
- [ ] OCR support — Tesseract / AWS Textract for scanned PDFs
- [ ] Prompt versioning — track prompt changes over time
- [ ] Cost dashboard — per-run token cost breakdown
- [ ] Multi-model support — GPT-4o vs Claude comparison
- [ ] Benchmark evaluation — extraction accuracy vs ground truth
- [ ] Structured pricing schema — enforce template for comparability
- [ ] React + Tailwind frontend upgrade

---

## Final Deliverables

- [x] Complete LangGraph multi-agent application
- [x] FastAPI backend with full endpoint coverage
- [x] Streamlit frontend — 7 screens
- [x] Prompt pack — 8 independent `.md` prompt files
- [x] Pydantic V2 structured outputs throughout
- [x] RFQ Generator Agent
- [x] Vendor Generator Agent (5 distinct personas)
- [x] Document Parser (PDF, DOCX, TXT, MD)
- [x] Extraction Agent with evidence anchoring
- [x] Validation Agent with contradiction detection
- [x] Comparison Agent with matrix + risk matrix
- [x] Recommendation Engine with confidence scores
- [x] Prompt Trace — full audit trail
- [x] Sample data — demo mode, no API key required
- [x] Architecture diagram
- [x] README with design rationale
- [x] Demo-ready — suitable for AI Engineering interviews
