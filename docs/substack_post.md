# Engineering an AI Procurement Copilot: Multi-Agent LLM Orchestration, Hallucination Control, and Full Observability

*Prompt architecture, LangGraph state graphs, Langfuse tracing, and a 5-value status taxonomy — applied to one of enterprise procurement's most persistent unsolved problems.*

---

Here's a real scenario that plays out in every mid-to-large company, every quarter:

A marketing team issues an RFQ to five agencies. The proposals come back in completely different formats. One vendor gives you a 40-page PDF with everything bundled. Another sends a two-page email and calls it a full response. A third quotes in USD even though the contract is INR-denominated, buries a 10% media commission outside the stated total, and confidently claims "all-inclusive pricing" in the executive summary while listing six exclusions in the appendix.

A procurement buyer now has to manually read all of this, cross-reference it against the original RFQ, and present a coherent vendor comparison to a room full of stakeholders — without getting the numbers wrong.

That's the problem I set out to solve.

---

## What I Built (Demo First)

**RFQ AI Procurement Copilot** is a prompt-driven multi-agent AI system that:

- Generates a realistic, structured RFQ for a marketing services procurement event
- Generates messy, real-world-quality vendor responses — with deliberate gaps, contradictions, and complexity baked in
- Extracts structured procurement data from each vendor response, grounded in source evidence
- Flags every missing, unclear, conflicting, and risky piece of information — without hallucinating
- Compares vendors across six evaluation dimensions in a buyer-readable format
- Presents everything in a 7-screen buyer-facing Streamlit UI with risk dashboards, evidence boxes, and confidence scores

---

### The 7 Screens

**Screen 1 — RFQ Overview 🏠**

Before showing the buyer any vendor data, the system shows them the RFQ. Scope, timelines, compliance requirements, the vendor questionnaire — all of it. A buyer who hasn't deeply read their own RFQ cannot evaluate responses meaningfully. This screen anchors the buyer in the procurement context first.

**Screen 2 — Vendor Responses 📄**

All vendor proposals are shown with quality badges (HIGH / MEDIUM / LOW) and their most critical flags visible at a glance. The buyer can see which vendors responded comprehensively and which are already missing important sections — before doing any deep review.

**Screen 3 — Upload 📤**

Supports file upload (PDF, DOCX, TXT, Markdown) or plain text paste. When a document comes in, the extraction pipeline runs on it immediately. No hardcoded outputs — the AI reads whatever you give it.

**Screen 4 — Extraction Review 🔍**

This is where the real work shows. Per-vendor, with six sub-tabs covering scope, pricing, timeline, compliance, commercial terms, and risks. Every extracted value shows the evidence snippet from the original proposal. Missing fields are shown as 🔴 badges — not greyed out, not hidden. A vendor who hasn't answered the compliance question is telling the buyer something.

**Screen 5 — Vendor Comparison 📊**

Scorecard + comparison matrix + differentiator callouts. Six evaluation dimensions side by side. Scores are accompanied by evidence snippets and buyer flags — not just a number. The system never picks a winner.

**Screen 6 — Risks ⚠️**

Consolidated risk dashboard across all vendors. Confidence scores. Shortlisting recommendations: Shortlist / Conditional / Reject — with specific reasons and traceable evidence for every call.

**Screen 7 — Prompt Trace 📝**

Full AI audit trail. Every prompt with its design explanation. A live log of every LLM call in the workflow. Buyers and reviewers can see exactly what the AI was asked and what it produced.

---

### The Three Demo Vendors

The system ships with three pre-generated vendor responses that are deliberately complex:

| Vendor | Total Price | What Makes It Messy |
|--------|-------------|----------------------|
| **Apex Creative Co.** | INR 4,20,00,000 | Full scope covered; 10% media commission sits outside the stated total; English TVC quoted as adaptation, not independent production |
| **Spark Digital Agency** | INR 1,75,00,000 | Digital-only house; broadcast TVC production listed as "TBD (INR 80–120L)"; influencer fees quoted in USD in an INR contract |
| **Brandsmith Group** | INR 3,90,00,000 | Itemized sum (INR 3,64,00,000) doesn't match stated total (INR 3,90,00,000); "6–8 week" delivery claim directly contradicts their own 15–16 week timeline table |

These aren't clean sample files. They're designed to break naive extraction — and to test whether the AI system can surface contradictions rather than smooth them over.

---

## How It Works (The Theory)

### Architecture

```
Streamlit Frontend (7 screens)
         ↓
   FastAPI Backend
         ↓
  LangGraph Workflow (9-node pipeline)
         ↓
      8 AI Agents
         ↓
  OpenAI GPT-4o · Pydantic V2 Structured Outputs
         ↓
  Langfuse (automatic trace per LLM call)
```

The backend is a LangGraph `StateGraph` that chains 8 agents in sequence. Each agent receives only the output of the prior step — this prevents early-stage hallucinations from compounding downstream. The state is a typed `TypedDict` (Pydantic V2), so every LLM output is structured. The system never parses raw markdown tables.

---

### The 8 Agents

**1. RFQ Generation Agent**
Generates a realistic, structured RFQ. The prompt assigns a "Senior Procurement Director" persona, specifies the procurement domain (marketing services for NourishKids — a fortified kids snack brand), and enforces a structured output schema covering: general information, timeline, scope per line item, commercial expectations, vendor questionnaire, and compliance requirements. The output feels like a real procurement document because the prompt was written to produce one.

**2. Vendor Response Generation Agent**
Generates five vendor personas with explicitly varied response quality. The prompt instructs the model to vary completeness, pricing structure, use of assumptions, scope interpretation, and compliance depth across each vendor. The point is not to generate clean data — it's to generate data that will meaningfully test the extraction and comparison agents downstream.

**3. Messy Vendor Generation (Edge-Case Stress Test)**
A separate prompt specifically generates edge-case complexity: missing pricing, vague timelines, partial scope, bundled pricing, currency mismatches. This is the "data quality stress test" layer. If your extraction agent can handle the messy vendor, it can handle real procurement data.

**4. Document Parser Agent**
Handles PDF (pdfplumber primary, PyPDF2 fallback), DOCX (python-docx with table support), and plain text / Markdown passthrough. The parser strips formatting and passes clean text to the extraction agent.

**5. Extraction Agent**
This is the core of the system. It reads raw vendor text and produces structured JSON covering: scope coverage per line item, pricing (total, itemized, and a consistency check), timeline, compliance, commercial terms, assumptions, exclusions, risks, buyer flags, conflicts, and clarification questions.

The critical design decision here is the **5-value status taxonomy**: `present | partial | missing | unclear | conflicting`. More on this below.

**6. Validation Agent**
Validates the extraction quality. Detects contradictions across a single vendor's own fields (e.g., "all-inclusive" in the executive summary vs. six exclusions in the appendix). Flags unsupported claims where the vendor made an assertion without evidence.

**7. Comparison Agent**
Compares vendors across six dimensions: scope coverage, pricing clarity, commercial completeness, timeline clarity, compliance quality, and risk level. The comparison output is grounded exclusively in the extraction output — no inference from raw vendor text at this stage.

**8. Recommendation Agent**
Generates shortlisting recommendations with confidence scores. Three possible outcomes per vendor: Shortlist / Conditional / Reject. Every pro and con must cite specific, traceable evidence. The system never declares a winner — it identifies readiness for shortlisting and surfaces the conditions the buyer needs to resolve first.

---

### The Prompt Architecture

Eight purpose-built prompts. Each one is in a separate `.md` file, loaded at runtime, and versioned alongside the code.

**The most important design principle across all prompts:** role assignment before any instruction. Every prompt starts by telling the model who it is — Senior Procurement Director, Expert Procurement Data Extraction Analyst, Senior Vendor Comparison Analyst. This isn't a stylistic choice; role-assigned prompts produce more consistently structured, domain-appropriate outputs.

**Prompt chaining:** The workflow passes only the immediately prior step's output to the next agent. The extraction agent receives raw vendor text. The comparison agent receives extraction output — not the raw text. The recommendation agent receives the comparison output. This isolation prevents hallucinations from compounding.

**The `extraction.md` prompt is worth looking at in detail.** It opens with:

> *You are an Expert Procurement Data Extraction Analyst with 15 years of experience evaluating vendor proposals for large enterprises.*

It then defines the 5-value status taxonomy, establishes evidence anchoring as a requirement, and — critically — includes this rule in a `CRITICAL_RULES` section:

> *"Do not infer, assume, or fill gaps. If a value is not explicitly stated, use `missing` or `unclear`. Accurately flagging missing information is more valuable than filling gaps."*

This instruction does two things. It explicitly rewards the `missing` outcome, which counteracts the model's natural tendency to fill gaps with plausible values. And it makes hallucination a failure condition rather than a neutral outcome.

---

### The Hallucination Control Stack

Hallucination in procurement AI has real consequences. An AI that fills in a missing price estimate, or invents a compliance certification that wasn't in the proposal, creates exactly the kind of buyer confusion that procurement workflows are designed to avoid.

The system uses four layers of hallucination control:

| Layer | Control |
|-------|---------|
| **Extraction** | "Do not infer, assume, or fill gaps" — `CRITICAL_RULES` section |
| **Extraction** | `missing` is a valid, expected, and rewarded output |
| **Extraction** | Evidence quotation required for every `present` and `partial` field |
| **Comparison** | "Base ALL comparisons on extracted data only — no inference" |
| **Comparison** | "NOT COMPARABLE" is a valid and expected comparison output |
| **Comparison** | No winner recommendation — buyer decides |
| **Validation** | Contradiction detection across a single vendor's own fields |
| **Validation** | Unsupported claim flagging — evidence required for every assertion |
| **Recommendation** | All pros/cons must cite specific, traceable evidence |

The `NOT COMPARABLE` output deserves special mention. When two vendors have responded to different interpretations of the same scope item — say, one vendor quoted broadcast TVC production and another quoted digital video only — the comparison agent outputs `NOT COMPARABLE` for that dimension rather than forcing a false equivalence. This is a deliberate product decision. Misleading the buyer with an apples-to-oranges score is worse than flagging incomparability explicitly.

---

### The 5-Value Status Taxonomy

This is the design choice I'm most confident in.

Naive extraction systems produce binary outputs: either the information is there or it isn't. Real procurement data doesn't work that way. Consider these cases:

- A vendor gives a pricing total but no breakdown — **`partial`**
- A vendor says "timelines are flexible and subject to discussion" — **`unclear`**
- A vendor's executive summary says "all-inclusive" and their appendix lists six exclusions — **`conflicting`**
- A compliance section is completely absent — **`missing`**
- A price breakdown is itemized, totalled, and signed off — **`present`**

Forcing a binary present/absent label would either hallucinate the `partial` into `present` or lose the distinction between `missing` (never addressed) and `unclear` (addressed vaguely). The 5-value taxonomy maps to buyer decision states: `present` values are usable, `partial` values need verification, `missing` and `unclear` values need clarification, and `conflicting` values need resolution before comparison can even begin.

---

### Product Thinking

The screens are ordered around the buyer's decision journey, not the system's data model.

**The buyer reads the RFQ first.** Before seeing any vendor data, the system shows them what was asked. This sounds obvious, but most procurement tools jump straight to vendor summaries. A buyer who hasn't anchored in their own requirements will evaluate vendor responses without a reference frame.

**Missing information is surfaced, not hidden.** Every missing field gets a visible 🔴 badge. The temptation in UI design is to grey out absent data or collapse empty sections. We resist that. A vendor who didn't answer the compliance question is telling the buyer something — that silence should be visible.

**Conflicts are shown as conflicts, not resolved.** When the validation agent detects a contradiction within a vendor's response, it surfaces that as a conflict box in the UI — not a resolved score. The buyer needs to know the conflict exists, not be given an averaged value that obscures it.

**The system never picks a winner.** The recommendation agent shortlists, flags conditions, and quantifies confidence — but the final decision belongs to the buyer. An AI procurement copilot that declares a winner is making a commercial decision it has no authority to make. The buyer has context the AI doesn't: relationship history, strategic priorities, risk appetite. The system's job is to give the buyer a clear, evidence-backed starting point for their decision, not to make it for them.

---

### Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI + uvicorn |
| Orchestration | LangGraph (StateGraph) |
| LLM | OpenAI GPT-4o |
| Observability | Langfuse (automatic LLM call tracing) |
| Data validation | Pydantic V2 + pydantic-settings |
| PDF parsing | pdfplumber (primary) + PyPDF2 (fallback) |
| DOCX parsing | python-docx |
| Data viz | pandas + plotly |
| Retry logic | tenacity (exponential backoff) |

The LangGraph `StateGraph` is the right tool for this workflow because the pipeline is stateful — each agent's output feeds the next — but the logic at each node is simple and predictable. There's no dynamic routing needed in this prototype. The graph is linear by design: generate → parse → extract → validate → compare → recommend → trace.

---

### Observability with Langfuse

Every LLM call in the pipeline is automatically traced using **Langfuse** — an open-source observability platform purpose-built for LLM applications.

The implementation is deliberately low-friction. A `LangfuseHelper` class initializes a Langfuse client from environment variables (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`). A `CallbackHandler` is then attached to the LLM at the `LLMFactory.get_model()` level — not at the individual agent level. This means the entire 8-agent pipeline is instrumented from a single point of configuration, with zero per-agent tracing code.

When Langfuse is configured, every invocation across all agents — RFQ generation, vendor response generation, extraction, validation, comparison, recommendation — automatically produces a trace entry containing: the full prompt sent, the raw model response, token usage, latency, and model metadata.

What this gives you in practice:

- **Prompt debugging at scale.** When extraction behaves unexpectedly on a specific vendor document, you can pull the exact prompt and response from the Langfuse trace rather than re-running the workflow with logging.
- **Latency profiling per agent.** The extraction agent is the most token-intensive step. Langfuse makes it easy to see where the pipeline's time actually goes.
- **Token cost tracking.** Each extraction run across three vendors triggers multiple GPT-4o calls. Langfuse aggregates these into a per-run cost view.
- **Regression detection.** If a prompt edit changes extraction behavior, a side-by-side trace comparison shows exactly what changed — not just that the output changed.

Observability is optional: if `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` are not set, the system falls back gracefully with no tracing. For local development or demo mode, it's a no-op. For production use or active prompt iteration, it's the difference between debugging with visibility and debugging blind.

---

### The Procurement Domain: Why Marketing Services?

The RFQ is for marketing services procurement — specifically, a campaign launch for NourishKids (a fortified snack product by NourishPlus Foods India Ltd., an Indian FMCG brand). The eight line items are: strategy and creative development, TVC development, TVC production, social organic content, social paid media planning, social paid media buying and optimization, kids advertising and claims compliance review, and launch program management.

This is a deliberately non-trivial procurement scenario. Why?

1. **Compliance complexity:** Kids advertising in India involves ASCI (Advertising Standards Council of India) and FSSAI (health claims) compliance. Vendors who wave this off with a one-liner are signaling something.
2. **Scope interpretation variance:** "TVC development" and "TVC production" are separate line items. Vendors routinely conflate these. The system has to detect when a vendor priced them as a bundle vs. separately.
3. **Pricing structure diversity:** Marketing agencies price differently — some bundle everything, some itemize by deliverable, some charge retainers plus project fees, some add media commission on top of stated totals. The system has to compare these without forcing normalization.
4. **Kids nutrition compliance:** FSSAI nutritional claims compliance for products targeting children is a real, specific regulatory domain. It's not interchangeable with general advertising compliance. The extraction agent has to recognize the difference.

---

### Limitations (Being Honest)

- **No real OCR.** Scanned PDFs or image-based documents can't be processed. This is a text-extraction-only prototype.
- **Single LLM dependency.** GPT-4o exclusively, no fallback. A production system would have alternative model routing.
- **Demo data is synthetic.** The pre-generated vendor data is AI-generated. It's realistic — but it's not sourced from real procurement events.
- **No persistent storage.** File-based state in `generated/` and `prompt_trace/`. No database. Not multi-user.
- **Linear LangGraph pipeline.** If validation flags a critical extraction failure, the system doesn't loop back to re-run extraction. Conditional branching would require more state logic.
- **No PPT or Excel parsing.** Python-pptx and openpyxl aren't implemented. Vendors who submit proposals as PowerPoint decks can't be processed.

---

### What I'd Build Next

1. **Conditional LangGraph branching.** If the validation agent flags extraction failures above a threshold, trigger a repair prompt and re-run extraction before comparison.
2. **OCR support.** pytesseract for local OCR or Azure Form Recognizer for production-grade scanned document handling.
3. **Human-in-the-loop review.** Let the buyer annotate the extraction review screen — correct a misextracted value, mark a field as manually verified. Feed corrections back as few-shot examples for the next extraction run.
4. **Prompt evaluation framework.** Instrument extraction quality with an LLM-as-judge step that scores each extraction on completeness, hallucination, and evidence quality. Without evaluation, prompt improvement is guesswork.
5. **Structured export.** Generate a procurement-ready Excel or PDF comparison report that a buyer can share with stakeholders without showing the AI interface.
6. **Feedback loop.** Capture buyer shortlisting decisions and use them to improve future recommendation prompts. A model that learns from buyer behavior gets better at surface-level risk calibration over time.

---

### The Core Insight

The hardest part of this project wasn't the LangGraph orchestration or the Streamlit UI. It was the prompt design — specifically, the extraction prompt.

Getting a language model to say "I don't know" when it doesn't know, consistently, across varied vendor documents, without it hallucinating plausible values to fill the gap — that requires explicit reward shaping in the prompt. The `CRITICAL_RULES` section, the 5-value status taxonomy, the evidence anchoring requirement — these aren't nice-to-haves. They're the difference between an extraction agent that's useful and one that's confidently wrong.

The second hardest part was the comparison design. It's tempting to score everything and declare a winner. Resisting that — building "NOT COMPARABLE" as a first-class output, removing the winner declaration entirely — required actively pushing back against what the model wants to do by default.

Procurement AI is useful when it makes the buyer's job easier *and* more accurate. It fails when it replaces the buyer's judgment with a confident-sounding AI guess. Getting that line right is what prompt design is actually for.

---

*The full source is available at the link below. Demo mode requires no API key. Add an OpenAI key to run all agents live.*

*Stack: Python · Streamlit · FastAPI · LangGraph · OpenAI GPT-4o · Pydantic V2 · Langfuse*

---

