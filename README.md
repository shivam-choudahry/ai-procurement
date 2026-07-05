# RFQ AI Procurement Copilot

> **Portfolio-quality multi-agent AI system for vendor evaluation.** Showcase-ready for AI Engineering interviews.

---

## Architecture

```
                  RFQ AI Procurement Copilot
┌────────────────────────────────────────────────────────────┐
│                   Frontend (Streamlit — 7 screens)         │
│  🏠 RFQ │ 📄 Vendors │ 📤 Upload │ 🔍 Extraction │ 📊 Comp │
│  ⚠️ Risks │ 📝 Prompt Trace                               │
└──────────────────────┬─────────────────────────────────────┘
                       │
                FastAPI Backend (port 8000)
                       │
                LangGraph Workflow (7-node pipeline)
                       │
      ┌─────────────────────────────────────────┐
      │              AI Agents (8)              │
      ├─────────────────────────────────────────┤
      │ RFQ Generator                           │
      │ Vendor Response Generator (5 personas)  │
      │ Document Parser (PDF/DOCX/XLSX/TXT)     │
      │ Extraction Agent (evidence anchoring)   │
      │ Validation Agent (contradiction detect) │
      │ Comparison Agent (6 dimensions)         │
      │ Recommendation Agent (confidence score) │
      │ UI Generation Agent                     │
      └─────────────────────────────────────────┘
                       │
               OpenAI GPT-4o  ·  Pydantic V2 Structured Outputs
                       │
               Langfuse (LLM Observability — prompts, tokens, latency)
```

---

## Quick Start

### 1. Install dependencies

```bash
# Recommended — project uses uv
uv sync

# Or with pip
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — add keys as needed:
#   OPENAI_API_KEY         — required for live AI (optional, demo works without it)
#   LANGFUSE_PUBLIC_KEY    — optional, enables LLM observability tracing
#   LANGFUSE_SECRET_KEY    — optional
#   LANGFUSE_HOST          — optional (default: https://cloud.langfuse.com)
```

### 3. Run Streamlit app (Demo Mode — no API key needed)

```bash
streamlit run app.py
```

### 4. Run FastAPI backend (optional)

```bash
uvicorn src.routers.api:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Run full LangGraph workflow

```bash
python -c "import asyncio; from src.agents.graph import rfq_workflow; r = asyncio.run(rfq_workflow()); print(r['workflow_status'])"
```

---

## 7-Screen Streamlit UI

| Screen | Icon | Purpose |
|--------|------|---------|
| RFQ Overview | 🏠 | Full RFQ — scope, timeline, compliance, questionnaire |
| Vendor Responses | 📄 | All vendor proposals with quality indicators + AI generation |
| Upload | 📤 | PDF / DOCX / XLSX / TXT / MD / JSON upload + instant parsing and extraction |
| Extraction Review | 🔍 | Per-vendor structured extraction with flags + evidence boxes |
| Vendor Comparison | 📊 | Scorecard, comparison matrix, key differentiators |
| Risks | ⚠️ | Buyer Risk Dashboard + confidence scores + shortlisting |
| Prompt Trace | 📝 | Full AI audit trail — 8 prompts + Langfuse trace link |

---

## Project Structure

```
rfq-ai-copilot/
├── app.py                          # 7-page Streamlit frontend
├── requirements.txt
├── pyproject.toml                  # uv project config
├── .env.example
│
├── src/
│   ├── __init__.py
│   ├── config.py                   # Settings, env vars (pydantic-settings)
│   │
│   ├── routers/
│   │   └── api.py                  # FastAPI — 8 endpoints
│   │
│   ├── agents/
│   │   ├── state.py                # RFQWorkflowState TypedDict (LangGraph)
│   │   ├── graph.py                # LangGraph workflow (7-node pipeline)
│   │   └── nodes/                  # Individual LangGraph node implementations
│   │       ├── rfq_generator.py    # RFQ generation agent
│   │       ├── vendor_generator.py # Vendor generation (5 distinct personas)
│   │       ├── parser.py           # Document parser node
│   │       ├── extractor.py        # Extraction agent (evidence anchoring)
│   │       ├── validator.py        # Validation agent
│   │       ├── comparator.py       # Comparison agent (6 dimensions)
│   │       ├── recommendation.py   # Recommendation agent
│   │       └── ui_agent.py         # UI generation agent
│   │
│   ├── schemas/                    # Pydantic V2 structured output models
│   │   ├── rfq.py                  # RFQ model
│   │   ├── vendor.py               # VendorResponse model
│   │   ├── extraction.py           # VendorExtraction + ValidationResult
│   │   └── comparison.py           # ComparisonMatrix + BuyerRecommendation
│   │
│   ├── prompts/                    # 8 individual prompt files
│   │   ├── prompt_library.py       # All prompts + PROMPT_PACK metadata
│   │   ├── rfq.md                  # RFQ generation
│   │   ├── vendor_generation.md    # Vendor generation (5 personas)
│   │   ├── messy_vendor.md         # Edge-case test data
│   │   ├── extraction.md           # Extraction agent
│   │   ├── validation.md           # Validation agent
│   │   ├── comparison.md           # Comparison agent
│   │   ├── recommendation.md       # Recommendation agent
│   │   └── ui_generation.md        # UI generation agent
│   │
│   ├── prompt_trace/               # Saved prompt trace JSON files
│   │   └── workflow_trace.json
│   │
│   └── utils/
│       ├── helpers.py              # UI helpers (badges, stars, truncate)
│       ├── llm.py                  # LLM wrapper (retry, Langfuse trace, fallback)
│       └── parsers/                # Document parsing
│           ├── pdf.py              # pdfplumber (primary) + PyPDF2 (fallback)
│           ├── docx.py             # python-docx with table support
│           ├── xlsx.py             # openpyxl — all sheets → Markdown tables
│           └── txt.py              # Plain text / Markdown passthrough
│
├── data/                           # Pre-generated demo data
│   ├── rfq_data.py                 # NourishKids RFQ (8 line items)
│   ├── vendor_data.py              # 3 vendor responses with deliberate complexity
│   ├── extracted_data.py           # Pre-extracted structured data with conflicts
│   └── comparison_data.py          # Pre-computed 6-dimension comparison matrix
│
├── generated/                      # LLM-generated outputs (rfq.json, vendors.json, etc.)
├── sample_data/                    # 5 sample vendor documents for upload testing
└── docs/
    ├── WRITE_UP.md
    └── RFQ_AI_Procurement_Copilot_Implementation_Plan.md
```

---

## FastAPI Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check + API key status |
| `/generate-rfq` | POST | Run RFQ Generator agent |
| `/generate-vendors` | POST | Run Vendor Generator (5 personas) |
| `/upload-vendor` | POST | Upload file → parse → extract |
| `/extract` | POST | Run Extraction + Validation |
| `/compare` | POST | Run Comparison + Recommendation |
| `/prompt-trace` | GET | Full prompt trace log |
| `/run-workflow` | POST | Full LangGraph pipeline end-to-end |

---

## LangGraph Workflow

```
START
↓ generate_rfq          — RFQ document (demo data or AI-generated); skipped if already seeded
↓ generate_vendors       — 5 vendor personas; skipped if already seeded
↓ parse_documents        — PDF / DOCX / XLSX / TXT parsing for uploaded docs
↓ extract_information    — Per-vendor structured extraction (concurrent asyncio.gather)
↓ validate_extraction    — Quality check + contradiction detection (concurrent)
↓ compare_vendors        — 6-dimension comparison matrix
↓ generate_recommendation — Confidence-scored shortlisting (no winner — buyer decides)
END
```

> All nodes are idempotent — if data already exists in state (seeded from session), the node returns early without calling the LLM.

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI + uvicorn |
| Orchestration | LangGraph (StateGraph) |
| LLM | OpenAI GPT-4o |
| LLM Observability | **Langfuse** (prompt traces, token usage, latency) |
| Data validation | Pydantic V2 + pydantic-settings |
| PDF parsing | pdfplumber (primary) + PyPDF2 (fallback) |
| DOCX parsing | python-docx |
| XLSX parsing | openpyxl (all sheets → Markdown tables) |
| Data analysis | pandas + plotly |
| Retry logic | tenacity (exponential backoff) |
| HTTP client | httpx |
| Package manager | uv |

---

## Prompt Design Principles

1. **Role assignment** — every prompt assigns a clear expert persona
2. **Evidence anchoring** — `present`/`partial` fields MUST cite source text
3. **5-value status taxonomy** — `present | partial | missing | unclear | conflicting`
4. **"NOT COMPARABLE"** is a valid and expected comparison output
5. **"Do not infer"** — CRITICAL RULE in extraction prevents hallucination
6. **No winner recommendation** — preserves buyer decision authority
7. **`missing` is rewarded** — model incentivized to flag gaps honestly

---

## Hallucination Controls

| Layer | Control |
|-------|---------|
| Extraction | "Do not infer, assume, or fill gaps" as CRITICAL RULE |
| Extraction | `missing` is valid, expected, rewarded output |
| Extraction | Evidence quotation required for all `present`/`partial` fields |
| Comparison | "Base ALL comparisons on extracted data only" |
| Comparison | No vendor recommendation — buyer decides |
| Validation | Contradiction detection across same vendor's fields |
| Validation | Unsupported claim flagging — evidence required |
| Recommendation | All pros/cons must cite specific evidence |

---

## Demo Mode

Works fully **without an API key** using pre-generated data:
- `data/rfq_data.py` — NourishKids RFQ (8 line items)
- `data/vendor_data.py` — 3 vendor responses with deliberate complexity
- `data/extracted_data.py` — Pre-extracted structured data with conflicts
- `data/comparison_data.py` — Pre-computed 6-dimension comparison matrix

Add `OPENAI_API_KEY` to `.env` to enable live AI generation for all agents.

---

## Sample Vendor Documents (Upload Testing)

5 ready-to-use vendor proposal files in `sample_data/` — designed to test different extraction edge cases:

| File | Vendor | Total Price | Complexity / Test Case |
|------|--------|-------------|------------------------|
| `vendor_apex_creative.txt` | Apex Creative Co. | INR 4,20,00,000 | Full scope; media commission (10%) outside total; English TVC is adaptation not independent |
| `vendor_spark_digital.txt` | Spark Digital Agency | INR 1,75,00,000 | Digital-only; broadcast TVC unconfirmed (INR 80–120L TBD); influencer fees quoted in USD |
| `vendor_brandsmith_group.txt` | Brandsmith Group | INR 3,90,00,000 | Itemized sum (3,64,00,000) ≠ stated total (3,90,00,000); "6–8 week" claim contradicts 15–16 week plan |
| `vendor_mediapro_solutions.txt` | MediaPro Solutions | INR 1,23,50,000 | **Incomplete scope** — LI2, LI3, LI7 explicitly "NOT IN SCOPE"; tests extraction when mandatory sections are absent |
| `vendor_nimble_brand_studio.txt` | Nimble Brand Studio | INR 1,80,00,000 | **Aggressive/risky** — 75% advance payment; 8-week "full campaign" promise with impossible TVC timeline; scope creep indicators; 4-year-old studio |

Upload any of these on the **📤 Upload** screen to test the extraction pipeline.

---

## Observability (Langfuse)

All LLM calls are automatically traced via Langfuse `CallbackHandler` attached in `LLMFactory.get_model()`. Each trace captures:
- Full system + user prompt
- Raw LLM response
- Token usage (prompt / completion / total)
- Latency per call
- Step name (e.g. `extraction`, `comparison`, `recommendation`)

To enable, add to `.env`:
```
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com   # optional, default shown
```

Traces are visible in the **📝 Prompt Trace → Live Traces** tab with a direct link to your Langfuse dashboard.

---

## Documentation

- `docs/WRITE_UP.md` — Short write-up: problem, assumptions, prompt architecture, product thinking, extraction approach, comparison approach, limitations
- `docs/RFQ_AI_Procurement_Copilot_Implementation_Plan.md` — Full implementation plan
- `src/prompt_trace/` — Saved AI prompt trace JSON files
