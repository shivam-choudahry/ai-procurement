"""
RFQ AI Procurement Copilot — Streamlit Application (v2)
NourishKids Brand Launch Vendor Evaluation System

7 Screens:
1. 🏠 RFQ Overview      — Full RFQ: scope, timeline, compliance, questionnaire
2. 📄 Vendor Responses  — All vendor proposals; run AI generation
3. 📤 Upload            — PDF / DOCX / TXT / Markdown upload + instant extraction
4. 🔍 Extraction Review — Per-vendor structured extraction with flags and evidence
5. 📊 Vendor Comparison — Scorecard, comparison matrix, differentiators
6. ⚠️  Risks            — Buyer Risk Dashboard (🔴 High / 🟠 Medium / 🟢 Low)
7. 📝 Prompt Trace      — Full prompt pack + live traces
"""

import asyncio
import concurrent.futures
import os
import json
import logging
import streamlit as st
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)

# ─── Async helper ────────────────────────────────────────────────
def run_async(coro):
    """
    Safely run an async coroutine from Streamlit.

    Streamlit uses a Tornado event loop internally, so plain
    asyncio.run() raises "This event loop is already running."
    This helper runs the coroutine in a dedicated thread with its
    own fresh event loop, bypassing that restriction.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(asyncio.run, coro)
        return future.result()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
    force=True,   # override any handlers Streamlit already installed
)

# ─── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="NourishKids RFQ AI Copilot",
    page_icon="🥦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
.badge-present  { background:#d4edda; color:#155724; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:600; }
.badge-partial  { background:#fff3cd; color:#856404; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:600; }
.badge-missing  { background:#f8d7da; color:#721c24; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:600; }
.badge-unclear  { background:#fff3cd; color:#856404; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:600; }
.badge-conflict { background:#f8d7da; color:#721c24; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:600; }
.risk-high   { color:#dc3545; font-weight:700; }
.risk-medium { color:#fd7e14; font-weight:700; }
.risk-low    { color:#28a745; font-weight:700; }
.evidence-box  { background:#f8f9fa; border-left:3px solid #6c757d; padding:8px 12px; font-size:13px; color:#495057; margin:4px 0; border-radius:0 4px 4px 0; }
.conflict-box  { background:#fff5f5; border-left:3px solid #dc3545; padding:8px 12px; font-size:13px; color:#721c24; margin:4px 0; border-radius:0 4px 4px 0; }
.flag-box      { background:#fff3cd; border-left:3px solid #ffc107; padding:8px 12px; font-size:13px; color:#856404; margin:4px 0; border-radius:0 4px 4px 0; }
.rec-shortlist { background:#d4edda; border-left:4px solid #28a745; padding:12px; border-radius:4px; margin:4px 0; }
.rec-conditional { background:#fff3cd; border-left:4px solid #ffc107; padding:12px; border-radius:4px; margin:4px 0; }
.rec-reject    { background:#f8d7da; border-left:4px solid #dc3545; padding:12px; border-radius:4px; margin:4px 0; }
.section-header { font-size:18px; font-weight:700; margin-top:16px; margin-bottom:8px; }
.metric-card { background:#f8f9fa; padding:12px; border-radius:8px; text-align:center; }
.confidence-label { font-size:12px; color:#6c757d; margin-bottom:2px; }
</style>
""", unsafe_allow_html=True)

# ─── Data imports ────────────────────────────────────────────────
from data.rfq_data import RFQ_DATA
from data.vendor_data import VENDOR_RESPONSES
from data.extracted_data import EXTRACTED_DATA
from data.comparison_data import COMPARISON_DATA
from src.prompts.prompt_library import PROMPT_PACK, EXTRACTION_SYSTEM_PROMPT, EXTRACTION_USER_PROMPT
from src.utils.helpers import parse_uploaded_file, status_badge, score_to_stars, truncate
from src.utils.llm import has_api_key

# ─── Session state init ──────────────────────────────────────────
def _init():
    defaults = {
        "vendors": list(VENDOR_RESPONSES),
        "extracted": dict(EXTRACTED_DATA),
        "comparison": dict(COMPARISON_DATA),
        "recommendation": {},
        "page": "🏠 RFQ Overview",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()

# ─── Sidebar ──────────────────────────────────────────────────────
def render_sidebar():
    """Render the sidebar: navigation, status indicators, and workflow button."""
    with st.sidebar:
        st.markdown("## 🥦 NourishKids RFQ AI")
        st.caption("AI Procurement Copilot")
        st.divider()

        page = st.radio(
            "Navigate",
            ["🏠 RFQ Overview", "📄 Vendor Responses", "📤 Upload",
             "🔍 Extraction Review", "📊 Vendor Comparison", "⚠️ Risks", "📝 Prompt Trace"],
            key="nav"
        )
        st.session_state.page = page

        st.divider()
        if has_api_key():
            st.success("✅ API Key Active\nLive AI enabled")
        else:
            st.info("ℹ️ **Demo Mode**\nPre-generated data shown.\nAdd `OPENAI_API_KEY` to `.env`.")

        st.divider()
        st.caption(f"RFQ: {RFQ_DATA['rfq_id']}")
        st.caption(f"Vendors: {len(st.session_state.vendors)}")
        extracted_cnt = len([v for v in st.session_state.vendors
                             if v['vendor_id'] in st.session_state.extracted])
        st.caption(f"Extracted: {extracted_cnt}/{len(st.session_state.vendors)}")

        if has_api_key():
            st.divider()
            if st.button("🚀 Run Full Workflow", width="stretch", type="primary"):
                with st.spinner("Running LangGraph workflow..."):
                    try:
                        from src.agents.graph import rfq_workflow
                        # Seed the workflow with existing session-state data so
                        # nodes that are already populated are skipped.
                        initial = {
                            "rfq": RFQ_DATA,
                            "vendor_responses": list(st.session_state.vendors),
                            "vendor_extractions": list(st.session_state.extracted.values()),
                        }
                        result = run_async(rfq_workflow(initial))
                        for ex in result.get("vendor_extractions", []):
                            st.session_state.extracted[ex.get("vendor_id", "")] = ex
                        if result.get("comparison"):
                            st.session_state.comparison = result["comparison"]
                        if result.get("recommendation"):
                            st.session_state.recommendation = result["recommendation"]
                        st.success("✅ Workflow complete!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Workflow error: {e}")
        st.divider()
        st.markdown("🗺️ RFQ Workflow diagram")
        st.image("graph_output.png", caption="Workflow Graph")

render_sidebar()


# ═══════════════════════════════════════════════════════════════
# PAGE 1: RFQ OVERVIEW
# ═══════════════════════════════════════════════════════════════
def page_rfq_overview():
    rfq = RFQ_DATA
    st.title("🏠 RFQ Overview")
    st.subheader(rfq["title"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("RFQ ID", rfq["rfq_id"].split("-")[-1])
    c2.metric("Submission Deadline", rfq["timelines"].get("submission_deadline","—")[:12])
    c3.metric("Line Items", len(rfq.get("scope_of_work",[])))
    c4.metric("Budget Range", rfq.get("commercial_expectations",{}).get("budget_range","INR 4–6 Cr"))

    st.divider()
    t1, t2, t3, t4, t5 = st.tabs(["📌 Overview","🎯 Scope","💰 Commercial","❓ Questionnaire","⚖️ Compliance"])

    with t1:
        c1, c2 = st.columns([2,1])
        with c1:
            st.markdown("#### Brand Background"); st.write(rfq.get("brand_description",""))
            st.markdown("#### Overview"); st.write(rfq.get("overview",""))
        with c2:
            st.markdown("#### Key Dates")
            for k, v in rfq.get("timelines",{}).items():
                st.markdown(f"**{k.replace('_',' ').title()}**  \n{v}"); st.write("")
            i = rfq.get("issuer",{}); st.markdown("#### Issuer")
            st.markdown(f"**{i.get('company','')}**  \n{i.get('department','')}  \n{i.get('contact_name','')}  \n{i.get('contact_email','')}")

    with t2:
        for li in rfq.get("scope_of_work",[]):
            with st.expander(f"**LI{li['line_item_id']}: {li['name']}**"):
                st.markdown(f"**Desc:** {li['description']}")
                st.markdown("**Deliverables:**")
                for d in li.get("deliverables",[]): st.markdown(f"  - {d}")
                ca, cb = st.columns(2)
                ca.markdown(f"**Volume:** {li.get('volume','—')}")
                cb.markdown(f"**Deps:** {li.get('dependencies','—')}")

    with t3:
        ce = rfq.get("commercial_expectations",{})
        st.info(ce.get("pricing_format",""))
        c1, c2 = st.columns(2)
        c1.markdown(f"**Payment Terms**\n\n{ce.get('payment_terms','—')}")
        c2.markdown(f"**Budget Range**\n\n{ce.get('budget_range','—')}")
        import pandas as pd
        ec_df = pd.DataFrame(rfq.get("evaluation_criteria",[]))
        if not ec_df.empty: st.dataframe(ec_df, hide_index=True, width="stretch")

    with t4:
        q_list = rfq.get("vendor_questionnaire",[])
        st.markdown(f"#### {len(q_list)} Questions")
        for q in q_list:
            with st.expander(f"**{q.get('q_id','')}**: {q.get('question','')}"):
                st.caption(f"Guidance: {q.get('guidance','')}")

    with t5:
        for cr in rfq.get("compliance_requirements",[]):
            with st.expander(f"**{cr.get('area','')}**"):
                st.write(cr.get("requirement",""))
                st.markdown(f"**Docs required:** {cr.get('documentation_required','—')}")

    if has_api_key():
        st.divider()
        if st.button("🤖 Regenerate RFQ via AI"):
            from src.agents.nodes.rfq_generator import generate_rfq_from_brief
            brief_text = st.session_state.get("rfq_brief_input", "")
            with st.spinner("Generating..."):
                r = run_async(generate_rfq_from_brief(brief=brief_text))
                if "error" not in r: st.success("✅ Done!"); st.json(r)
                else: st.error(r["error"])
        st.text_area(
            "Optional brief / extra context for AI",
            key="rfq_brief_input",
            placeholder=(
                "e.g. Focus on Tier-2 city rollout, add OOH media as a line item, "
                "increase budget to INR 8 Cr, submission deadline March 2026…"
            ),
            height=100,
        )


# ═══════════════════════════════════════════════════════════════
# PAGE 2: VENDOR RESPONSES
# ═══════════════════════════════════════════════════════════════
def page_vendor_responses():
    st.title("📄 Vendor Responses")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Vendors", len(st.session_state.vendors))
    c2.metric("Extracted", len([v for v in st.session_state.vendors if v["vendor_id"] in st.session_state.extracted]))
    c3.metric("Total Buyer Flags", sum(len(st.session_state.extracted.get(v["vendor_id"],{}).get("buyer_flags",[])) for v in st.session_state.vendors))
    st.divider()

    if has_api_key():
        with st.expander("🤖 Generate Vendor Responses via AI"):
            if st.button("Generate 3 Vendors", type="primary"):
                from src.agents.nodes.vendor_generator import generate_vendor_responses
                with st.spinner("Generating..."):
                    vendors = run_async(generate_vendor_responses(rfq_context=RFQ_DATA))
                    if vendors: st.session_state.vendors = vendors; st.success(f"✅ {len(vendors)} vendors!"); st.rerun()
                    else: st.error("Failed.")

    cols = st.columns(min(len(st.session_state.vendors), 3))
    for i, vendor in enumerate(st.session_state.vendors):
        with cols[i % 3]:
            try:
                vid  = str(vendor.get("vendor_id", f"V{i+1}"))
                name = str(vendor.get("vendor_name", "Unknown Vendor"))
                tag  = str(vendor.get("tagline", ""))

                # Pricing — guard against None / non-dict pricing_summary
                ps       = vendor.get("pricing_summary") or {}
                if not isinstance(ps, dict):
                    ps = {}
                total    = str(ps.get("total_stated") or "—")

                # Extraction data
                ex       = st.session_state.extracted.get(vid, {})
                if not isinstance(ex, dict):
                    ex = {}
                dq       = str(ex.get("overall_data_quality") or "—")
                sc_data  = ex.get("scope_coverage") or {}
                if not isinstance(sc_data, dict):
                    sc_data = {}
                sc       = str(sc_data.get("overall_coverage_score") or "—")
                qc       = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}.get(dq, "⚪")

                # Persona badge — pre-computed so no inline conditional in f-string
                persona  = str(vendor.get("persona") or "")
                persona_labels = {
                    "premium": "⭐ Premium", "cheap": "💸 Budget",
                    "messy": "🔀 Messy", "conflicting": "⚡ Conflicting",
                    "incomplete": "📭 Incomplete",
                }
                pb_label = persona_labels.get(persona, "")
                badge_html = (
                    f'<span style="background:#e9ecef;padding:2px 8px;'
                    f'border-radius:10px;font-size:12px;display:inline-block;'
                    f'margin-bottom:6px">{pb_label}</span>'
                    if pb_label else ""
                )

                card_html = (
                    '<div style="border:1px solid #dee2e6;border-radius:8px;'
                    'padding:16px;margin-bottom:8px;">'
                    f'<h4 style="margin:0 0 4px 0">{name}</h4>'
                    f'<p style="color:#6c757d;font-size:13px;margin:0 0 8px 0">{tag}</p>'
                    f'{badge_html}'
                    f'<p style="margin:4px 0"><b>ID:</b> {vid} &nbsp; '
                    f'<b>Scope:</b> {sc}/100 &nbsp; <b>Quality:</b> {qc} {dq}</p>'
                    f'<p style="margin:4px 0"><b>Total (stated):</b> {total}</p>'
                    '</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

                # Buyer flags (max 2)
                for flag in ex.get("buyer_flags", [])[:2]:
                    st.markdown(
                        f"<div class='flag-box'>{flag}</div>",
                        unsafe_allow_html=True,
                    )

            except Exception as card_err:
                # Fallback: show vendor name + error without crashing the whole page
                st.warning(f"⚠️ Could not render card for vendor #{i+1}: {card_err}")
                st.write(vendor)

    st.divider()
    vendor_names = [v["vendor_name"] for v in st.session_state.vendors]
    sel = st.selectbox("View full proposal", vendor_names)
    v_obj = next(v for v in st.session_state.vendors if v["vendor_name"] == sel)
    with st.expander(f"Full proposal: {sel}", expanded=True):
        st.markdown(v_obj.get("response_text","No text."))

    st.divider()
    st.markdown("### 🤖 Run AI Extraction")
    if not has_api_key():
        st.info("ℹ️ Demo mode: pre-extracted results loaded.")
    else:
        run_for = st.multiselect("Select vendors", [v["vendor_name"] for v in st.session_state.vendors],
                                 default=[v["vendor_name"] for v in st.session_state.vendors if v["vendor_id"] not in st.session_state.extracted])
        if st.button("🚀 Run Extraction Agent", type="primary"):
            from src.agents.nodes.extractor import extract_vendor_response
            prog = st.progress(0); sp = st.empty()
            sel_v = [v for v in st.session_state.vendors if v["vendor_name"] in run_for]
            for idx, vendor in enumerate(sel_v):
                sp.info(f"Extracting {vendor['vendor_name']}...")
                st.session_state.extracted[vendor["vendor_id"]] = run_async(extract_vendor_response(
                    vendor["vendor_id"], vendor["vendor_name"], vendor.get("response_text","")))
                prog.progress((idx+1)/len(sel_v))
            sp.success("✅ Extraction complete!"); prog.empty()


# ═══════════════════════════════════════════════════════════════
# PAGE 3: UPLOAD
# ═══════════════════════════════════════════════════════════════
def page_upload():
    st.title("📤 Upload Vendor Document")
    st.caption("Upload a PDF, DOCX, XLSX, TXT, or Markdown vendor proposal for instant parsing and extraction.")

    c1, c2 = st.columns([1,2])
    with c1:
        new_name = st.text_input("Vendor Name *", placeholder="Creative Spark Agency")
        new_id = st.text_input("Vendor ID *", placeholder="V006")
        uploaded_file = st.file_uploader("Upload proposal", type=["txt","md","pdf","docx","xlsx","xls","json"])
        run_extraction = st.checkbox("Run extraction after upload", value=has_api_key(), disabled=not has_api_key())
    with c2:
        pasted_text = st.text_area("Or paste proposal text", height=250)

    st.divider()
    if st.button("📤 Upload & Process", type="primary", width="stretch"):
        if not new_name.strip(): st.error("Enter vendor name."); return
        if not new_id.strip(): st.error("Enter vendor ID."); return
        if new_id in [v["vendor_id"] for v in st.session_state.vendors]:
            st.error(f"Vendor ID '{new_id}' exists."); return

        text, parse_method = "", "plaintext"
        if uploaded_file:
            from src.utils.parsers import parse_document
            content = uploaded_file.read()
            text = parse_document(uploaded_file.name, content)
            ext = uploaded_file.name.rsplit(".",1)[-1].lower()
            parse_method = {"pdf":"pdfplumber","docx":"python-docx","xlsx":"openpyxl","xls":"openpyxl"}.get(ext,"plaintext")
        elif pasted_text.strip():
            text = pasted_text.strip()

        if not text: st.error("Upload a file or paste text."); return

        st.session_state.vendors.append({
            "vendor_id": new_id, "vendor_name": new_name.strip(),
            "tagline": f"Uploaded — {uploaded_file.name if uploaded_file else 'pasted text'}",
            "submission_date": "2025-02-05",
            "pricing_summary": {"total_stated":"—","currency":"INR","includes_gst":None},
            "response_text": text, "persona": "uploaded"
        })
        st.success(f"✅ Added **{new_name}** — {len(text):,} chars via {parse_method}")
        with st.expander("Preview"): st.text(text[:1500])

        if run_extraction and has_api_key():
            from src.agents.nodes.extractor import extract_vendor_response
            with st.spinner(f"Extracting {new_name}..."):
                result = run_async(extract_vendor_response(new_id, new_name, text))
                st.session_state.extracted[new_id] = result
                if "error" not in result:
                    st.success(f"✅ Extracted — Quality: **{result.get('overall_data_quality','—')}**, Flags: **{len(result.get('buyer_flags',[]))}**")
                    st.info("Go to **Extraction Review** for full results.")
                else:
                    st.warning(f"Extraction issue: {result['error']}")
        else:
            st.info("Go to **Vendor Responses** → Run Extraction to process.")

    st.divider()
    st.markdown("### 📋 Supported Formats")
    fc1, fc2, fc3, fc4, fc5 = st.columns(5)
    fc1.markdown("**PDF** 📕\npdfplumber\nMulti-page")
    fc2.markdown("**DOCX** 📘\npython-docx\nIncludes tables")
    fc3.markdown("**XLSX** 📗\nopenpyxl\nAll sheets")
    fc4.markdown("**TXT/MD** 📄\nPlain text\nMarkdown")
    fc5.markdown("**JSON** 📋\n`response_text` field")


# ═══════════════════════════════════════════════════════════════
# PAGE 4: EXTRACTION REVIEW
# ═══════════════════════════════════════════════════════════════
def page_extraction_review():
    import pandas as pd
    st.title("🔍 Extraction Review")
    st.caption("AI-extracted procurement information. Flags highlight missing, unclear, or conflicting data.")

    if not st.session_state.extracted:
        st.warning("No extraction data. Go to Vendor Responses and run extraction."); return

    extracted_vendors = [v for v in st.session_state.vendors if v["vendor_id"] in st.session_state.extracted]
    if not extracted_vendors: st.warning("No extracted vendors."); return

    vendor_tabs = st.tabs([v["vendor_name"] for v in extracted_vendors])
    for tab, vendor in zip(vendor_tabs, extracted_vendors):
        vid = vendor["vendor_id"]
        ex = st.session_state.extracted.get(vid, {})
        with tab:
            if "error" in ex: st.error(f"Error: {ex['error']}"); continue

            dq = ex.get("overall_data_quality","UNKNOWN")
            flags = ex.get("buyer_flags",[])
            conflicts = ex.get("conflicting_info",[])
            dq_f = getattr(st, {"HIGH":"success","MEDIUM":"warning","LOW":"error"}.get(dq,"info"))
            dq_f(f"**Quality: {dq}** — {len(flags)} buyer flags | {len(conflicts)} conflicts | "
                 f"Scope: {ex.get('scope_coverage',{}).get('overall_coverage_score','N/A')}/100")

            if flags:
                with st.expander(f"🚩 {len(flags)} Buyer Flags", expanded=True):
                    for f in flags:
                        c = "conflict-box" if "🚨" in f else "flag-box" if "⚠️" in f else "evidence-box"
                        st.markdown(f"<div class='{c}'>{f}</div>", unsafe_allow_html=True)

            if conflicts:
                with st.expander(f"🚨 {len(conflicts)} Conflicts", expanded=True):
                    for c in conflicts:
                        st.markdown(f"**Area:** {c.get('area','')}")
                        cc1, cc2 = st.columns(2)
                        cc1.markdown(f"<div class='conflict-box'>📌 Statement 1<br>{c.get('statement_1','')}</div>", unsafe_allow_html=True)
                        cc2.markdown(f"<div class='conflict-box'>📌 Statement 2<br>{c.get('statement_2','')}</div>", unsafe_allow_html=True)
                        st.caption(f"⚡ Buyer impact: {c.get('buyer_impact','')}")
                        st.divider()

            s1, s2, s3, s4, s5, s6 = st.tabs(["📦 Scope","💰 Pricing","📅 Timeline","⚖️ Compliance","⚠️ Risks","❓ Clarifications"])

            with s1:
                sc = ex.get("scope_coverage",{})
                items = sc.get("line_items",[])
                if items:
                    rows = []
                    for li in items:
                        cv = li.get("covered"); sv = li.get("status","unknown")
                        badge = {"present":"✅","partial":"🟡",True:"✅",False:"🔴","missing":"🔴","unclear":"⚠️","conflicting":"🚨"}.get(cv if cv is not None else sv,"❓")
                        rows.append({"LI":li.get("id"),"Line Item":li.get("name"),"Status":badge,"Detail":truncate(li.get("detail",""),100),"Flags":len(li.get("flags",[]))})
                    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
                    for li in items:
                        if li.get("flags"):
                            with st.expander(f"LI{li.get('id')} flags"):
                                for f in li["flags"]: st.markdown(f"<div class='flag-box'>⚠️ {f}</div>", unsafe_allow_html=True)
                                if li.get("evidence"): st.markdown(f"<div class='evidence-box'>📄 \"{li['evidence']}\"</div>", unsafe_allow_html=True)
                for u in sc.get("uncovered_items",[]): st.markdown(f"🔴 {u}")

            with s2:
                pricing = ex.get("pricing",{})
                cc1, cc2, cc3 = st.columns(3)
                cc1.metric("Total Stated", pricing.get("total_stated") or "N/A")
                cc2.metric("Currency", pricing.get("currency") or "N/A")
                check = pricing.get("consistency_check","UNKNOWN")
                cc3.metric("Consistency", {"PASS":"✅ PASS","FAIL":"❌ FAIL","PARTIAL":"🟡 PARTIAL","UNKNOWN":"❓ UNKNOWN"}.get(check,check))
                note = pricing.get("consistency_note","")
                if note:
                    c = "conflict-box" if "FAIL" in check else "evidence-box"
                    st.markdown(f"<div class='{c}'>{note}</div>", unsafe_allow_html=True)
                items_p = pricing.get("itemized",[])
                if items_p:
                    st.dataframe(pd.DataFrame([{"Line Item":r.get("item",""),"Cost":r.get("cost",""),"Status":status_badge(r.get("status",""))} for r in items_p]), hide_index=True, width="stretch")
                for f in pricing.get("flags",[]): st.markdown(f"<div class='flag-box'>{f}</div>", unsafe_allow_html=True)
                ct = ex.get("commercial_terms",{})
                if ct:
                    ct_rows = [{"Field":fld.replace("_"," ").title(),"Value":ct.get(fld,{}).get("value") or "MISSING","Status":status_badge(ct.get(fld,{}).get("status",""))}
                               for fld in ["payment_terms","proposal_validity","gst_treatment","escalation_clause"] if isinstance(ct.get(fld),dict)]
                    if ct_rows: st.markdown("#### Commercial Terms"); st.dataframe(pd.DataFrame(ct_rows), hide_index=True, width="stretch")

            with s3:
                tl = ex.get("timeline",{})
                check = tl.get("consistency_check","UNKNOWN")
                cc1, cc2 = st.columns(2)
                cc1.metric("Consistency", {"PASS":"✅ PASS","FAIL":"❌ FAIL","UNKNOWN":"❓ UNKNOWN"}.get(check,check))
                dur = tl.get("total_duration",{})
                cc2.metric("Duration", (dur.get("value") if isinstance(dur,dict) else str(dur)) or "N/A")
                note = tl.get("consistency_note","")
                if note:
                    st.markdown(f"<div class='{'conflict-box' if 'FAIL' in check else 'evidence-box'}'>{note}</div>", unsafe_allow_html=True)
                for fld in ["proposed_kickoff","campaign_go_live","total_duration"]:
                    val = tl.get(fld,{})
                    if isinstance(val,dict):
                        st.markdown(f"**{fld.replace('_',' ').title()}:** {val.get('value') or 'MISSING'} [{status_badge(val.get('status',''))}]")
                        if val.get("evidence"): st.markdown(f"<div class='evidence-box'>📄 \"{val['evidence']}\"</div>", unsafe_allow_html=True)
                for f in tl.get("flags",[]): st.markdown(f"<div class='flag-box'>{f}</div>", unsafe_allow_html=True)

            with s4:
                comp_ex = ex.get("compliance",{})
                def comp_row(label, field):
                    val = comp_ex.get(field,{})
                    if not isinstance(val,dict): return
                    st.markdown(f"**{label}**")
                    s = val.get("status","missing"); dl = val.get("detail_level","")
                    dl_b = {"high":"🟢 High","medium":"🟡 Medium","low":"🔴 Low","none":"⛔ None"}.get(dl,"")
                    ca, cb = st.columns([3,1])
                    ca.write(val.get("value") or "Not mentioned"); cb.markdown(f"{status_badge(s)}")
                    if dl_b: cb.caption(dl_b)
                    if val.get("evidence"): st.markdown(f"<div class='evidence-box'>📄 \"{val['evidence']}\"</div>", unsafe_allow_html=True)
                    st.write("")
                comp_row("ASCI Kids Code","asci_kids_code")
                comp_row("FSSAI Health Claims","fssai_health_claims")
                comp_row("Platform Policies","platform_policies")
                rv = comp_ex.get("compliance_reviewer_named",False)
                st.markdown(f"**Named Reviewer:** {'✅ Yes' if rv else '🔴 No'}")
                for f in comp_ex.get("flags",[]): st.markdown(f"<div class='flag-box'>{f}</div>", unsafe_allow_html=True)

            with s5:
                risks = ex.get("risks",[])
                if risks:
                    rdf = pd.DataFrame([{"Severity":{"high":"🔴 HIGH","medium":"🟡 MEDIUM","low":"🟢 LOW"}.get(r.get("severity","").lower(),r.get("severity","")),"Category":r.get("category","").title(),"Risk":r.get("risk",""),"Evidence":truncate(r.get("evidence",""),80)} for r in risks])
                    st.dataframe(rdf, hide_index=True, width="stretch")
                else: st.success("No significant risks.")
                mis = ex.get("missing_info",[]); unc = ex.get("unclear_info",[])
                mc1, mc2 = st.columns(2)
                if mis:
                    mc1.markdown(f"**🔴 Missing ({len(mis)})**")
                    for m in mis: mc1.markdown(f"- {m}")
                if unc:
                    mc2.markdown(f"**⚠️ Unclear ({len(unc)})**")
                    for u in unc: mc2.markdown(f"- {u}")

            with s6:
                cq = ex.get("clarification_questions",[])
                if cq:
                    st.markdown("#### Clarification Questions")
                    for i_q, q in enumerate(cq, 1): st.markdown(f"**Q{i_q}.** {q}")
                else: st.info("No clarification questions generated.")


# ═══════════════════════════════════════════════════════════════
# PAGE 5: VENDOR COMPARISON
# ═══════════════════════════════════════════════════════════════
def page_vendor_comparison():
    import pandas as pd
    st.title("📊 Vendor Comparison")
    st.caption("Side-by-side evaluation across 6 dimensions. Grounded in extracted data only.")

    comp = st.session_state.comparison
    if not comp or "error" in comp:
        st.warning("No comparison data.")
        if has_api_key():
            if st.button("Run Comparison Agent", type="primary"):
                from src.agents.nodes.comparator import compare_vendors
                with st.spinner("Running..."):
                    r = run_async(compare_vendors(list(st.session_state.extracted.values())))
                    st.session_state.comparison = r; st.rerun()
        return

    vendors_compared = comp.get("vendors_compared",[])
    attention = comp.get("buyer_attention_points",[])
    high_att = [a for a in attention if a.get("priority")=="HIGH"]
    if high_att:
        st.error(f"🚨 {len(high_att)} HIGH-priority attention points")
        for a in high_att:
            st.markdown(f"<div class='conflict-box'><b>{a.get('vendor','')}</b>: {a.get('point','')}<br><i>Action: {a.get('action_required','')}</i></div>", unsafe_allow_html=True)

    st.divider(); st.markdown("### 📊 Scorecard")
    dim_scores = comp.get("dimension_scores",{})
    score_rows = []
    for dk, dd in dim_scores.items():
        scores = dd.get("scores",{}); row = {"Dimension":dk.replace("_"," ").title()}
        for vn in vendors_compared:
            vo = next((v for v in st.session_state.vendors if v["vendor_name"]==vn), None)
            if vo:
                sc = scores.get(vo["vendor_id"],{}).get("score","N/A")
                row[vn] = score_to_stars(sc) if sc != "N/A" else "N/A"
        row["Winner"] = dd.get("winner","N/A"); score_rows.append(row)
    if score_rows: st.dataframe(pd.DataFrame(score_rows), hide_index=True, width="stretch")

    st.markdown("### 🔎 Dimension Detail")
    dimensions = list(dim_scores.keys())
    sel_dim = st.selectbox("Dimension", [d.replace("_"," ").title() for d in dimensions])
    if not sel_dim:
        return
    sdk = sel_dim.lower().replace(" ","_"); dd = dim_scores.get(sdk,{})
    st.caption(dd.get("description",""))
    cn = dd.get("comparability_note","")
    if cn: st.info(f"📊 {cn}")
    scores = dd.get("scores",{})
    if vendors_compared:
        cols = st.columns(len(vendors_compared))
        for col, vn in zip(cols, vendors_compared):
            vo = next((v for v in st.session_state.vendors if v["vendor_name"]==vn), None)
            if vo:
                sd = scores.get(vo["vendor_id"],{}); sc = sd.get("score","N/A")
                with col:
                    st.markdown(f"#### {vn}")
                    st.markdown(f"**Score:** {score_to_stars(sc)}" if sc!="N/A" else "**Score:** N/A")
                    st.write(sd.get("rationale","—"))
                    for g in sd.get("key_gaps",[]): st.markdown(f"<div class='flag-box'>⚠️ {g}</div>", unsafe_allow_html=True)
    if sdk == "pricing_clarity":
        st.markdown("#### Comparable Costs")
        for vn in vendors_compared:
            vo = next((v for v in st.session_state.vendors if v["vendor_name"]==vn), None)
            if vo:
                tc = dd.get("total_costs",{}).get(vo["vendor_id"],{})
                if isinstance(tc, dict):
                    ct = tc.get("comparable_total","N/A"); note = tc.get("note","")
                else:
                    ct = str(tc) if tc else "N/A"; note = ""
                c = "conflict-box" if "INCOMPLETE" in str(ct) else "evidence-box"
                st.markdown(f"<div class='{c}'><b>{vn}</b>: {ct}<br>{note}</div>", unsafe_allow_html=True)

    cant = comp.get("cannot_compare_because",[])
    if cant:
        st.divider(); st.markdown("### 🚫 Cannot Yet Compare")
        for cc in cant:
            with st.expander(f"**{cc.get('area','')}** — {', '.join(cc.get('vendors_affected',[]))}"):
                st.write(cc.get("reason","")); st.markdown(f"**Resolution:** {cc.get('resolution','')}")

    diffs = comp.get("key_differentiators",[])
    if diffs:
        st.divider(); st.markdown("### 💡 Key Differentiators")
        for d in diffs:
            with st.expander(f"**{d.get('dimension','')}**: {truncate(d.get('finding',''),80)}"):
                st.write(d.get("finding","")); st.markdown(f"**Buyer implication:** {d.get('buyer_implication','')}")

    risk_sum = comp.get("overall_risk_summary",{})
    if risk_sum and vendors_compared:
        st.divider(); st.markdown("### 🛡️ Risk Summary")
        cols = st.columns(len(vendors_compared))
        for col, vn in zip(cols, vendors_compared):
            vo = next((v for v in st.session_state.vendors if v["vendor_name"]==vn), None)
            if vo:
                rs = risk_sum.get(vo["vendor_id"],{}); rl = rs.get("risk_level","N/A")
                rl_icon = {"HIGH":"🔴","MEDIUM":"🟡","LOW":"🟢"}.get(rl,"")
                with col:
                    st.markdown(f"#### {vn}")
                    st.markdown(f"**{rl_icon} {rl} Risk**")
                    for r in rs.get("top_risks",[]): st.markdown(f"<div class='flag-box'>⚠️ {r}</div>", unsafe_allow_html=True)
                    for m in rs.get("missing_before_decision",[]): st.markdown(f"🔴 {m}")

    cl_qs = comp.get("clarification_questions_per_vendor",{})
    if cl_qs and vendors_compared:
        st.divider(); st.markdown("### ❓ Clarification Questions")
        for vn in vendors_compared:
            vo = next((v for v in st.session_state.vendors if v["vendor_name"]==vn), None)
            if vo:
                qs = cl_qs.get(vo["vendor_id"],[])
                if qs:
                    with st.expander(f"**{vn}** — {len(qs)} questions"):
                        for i_q, q in enumerate(qs,1): st.markdown(f"**Q{i_q}.** {q}")

    st.divider()
    if has_api_key():
        if st.button("🔄 Re-run Comparison", type="secondary"):
            from src.agents.nodes.comparator import compare_vendors
            with st.spinner("Running..."):
                r = run_async(compare_vendors(list(st.session_state.extracted.values())))
                if "error" not in r: st.session_state.comparison = r; st.success("✅ Updated."); st.rerun()
                else: st.error(r["error"])


# ═══════════════════════════════════════════════════════════════
# PAGE 6: RISKS
# ═══════════════════════════════════════════════════════════════
def page_risks():
    import pandas as pd
    st.title("⚠️ Buyer Risk Dashboard")
    st.caption("Consolidated risk view. Evidence-backed risk signals from extraction and validation.")

    if not st.session_state.extracted:
        st.warning("No extraction data. Run extraction first."); return

    extracted_vendors = [v for v in st.session_state.vendors if v["vendor_id"] in st.session_state.extracted]

    # Risk matrix
    st.markdown("### 🗂️ Risk Matrix")
    risk_rows = []
    for vendor in extracted_vendors:
        vid = vendor["vendor_id"]; ex = st.session_state.extracted.get(vid,{})
        risks = ex.get("risks",[]); conf = ex.get("conflicting_info",[]); mis = ex.get("missing_info",[])
        h = len([r for r in risks if r.get("severity")=="high"])
        m = len([r for r in risks if r.get("severity")=="medium"])
        l = len([r for r in risks if r.get("severity")=="low"])
        dq = ex.get("overall_data_quality","UNKNOWN")
        overall = "🔴 HIGH" if h>0 or len(conf)>1 else ("🟠 MEDIUM" if m>2 or conf or len(mis)>5 else "🟢 LOW")
        risk_rows.append({"Vendor":vendor["vendor_name"],"Overall Risk":overall,"🔴 High":h,"🟠 Medium":m,"🟢 Low":l,"⚡ Conflicts":len(conf),"❓ Missing":len(mis),"Quality":f"{'🟢' if dq=='HIGH' else '🟡' if dq=='MEDIUM' else '🔴'} {dq}"})
    if risk_rows: st.dataframe(pd.DataFrame(risk_rows), hide_index=True, width="stretch")

    # Recommendation
    rec = st.session_state.get("recommendation",{})
    if rec and rec.get("vendors"):
        st.divider(); st.markdown("### 🎯 Shortlisting Recommendation")
        st.caption("Evidence-backed shortlisting per vendor. No winner — buyer decides.")
        cols = st.columns(min(len(rec["vendors"]),3))
        for i, vr in enumerate(rec["vendors"]):
            rt = vr.get("recommendation","conditional")
            css = f"rec-{rt}"; icon = {"shortlist":"✅","conditional":"🟡","reject":"❌"}.get(rt,"")
            conf = vr.get("confidence_score",0); rl = vr.get("risk_level","UNKNOWN")
            with cols[i%3]:
                st.markdown(f"<div class='{css}'><h4 style='margin:0'>{icon} {vr.get('vendor_name','')}</h4><p><b>Status:</b> {rt.upper()} &nbsp; <b>Risk:</b> {rl}</p></div>", unsafe_allow_html=True)
                st.markdown("<div class='confidence-label'>Confidence</div>", unsafe_allow_html=True)
                st.progress(conf/100, text=f"{conf}%")
                with st.expander("Pros & Cons"):
                    for p in vr.get("pros",[]): st.markdown(f"✅ {p}")
                    for c in vr.get("cons",[]): st.markdown(f"❌ {c}")
                    for cond in vr.get("conditions",[]): st.markdown(f"⚠️ {cond}")
        if rec.get("disclaimer"): st.info(f"ℹ️ {rec['disclaimer']}")
    elif has_api_key():
        st.divider()
        if st.button("🤖 Generate AI Recommendations", type="primary"):
            from src.agents.nodes.recommendation import generate_recommendation
            with st.spinner("Generating..."):
                r = run_async(generate_recommendation(list(st.session_state.extracted.values())))
                st.session_state.recommendation = r; st.rerun()
    else:
        st.divider()
        if st.button("📊 Generate Rule-Based Recommendations", type="secondary"):
            from src.agents.nodes.recommendation import _demo_recommendation
            r = _demo_recommendation(list(st.session_state.extracted.values()))
            st.session_state.recommendation = r; st.rerun()

    # Confidence scores
    st.divider(); st.markdown("### 📊 Confidence Scores by Dimension")
    def _conf(section):
        if not section: return 0
        ss = [v.get("status","missing") for v in section.values() if isinstance(v,dict)]
        if not ss: return 50
        sm = {"present":100,"partial":65,"unclear":40,"conflicting":20,"missing":0}
        return int(sum(sm.get(s,0) for s in ss)/len(ss))

    for vendor in extracted_vendors:
        vid = vendor["vendor_id"]; ex = st.session_state.extracted.get(vid,{})
        with st.expander(f"**{vendor['vendor_name']}**"):
            dims = [
                ("📦 Scope Coverage", int(float(ex.get("scope_coverage",{}).get("overall_coverage_score","0") or 0))),
                ("💰 Pricing", {"PASS":95,"PARTIAL":65,"UNKNOWN":40,"FAIL":15}.get(ex.get("pricing",{}).get("consistency_check","UNKNOWN"),40)),
                ("📅 Timeline", {"PASS":88,"UNKNOWN":50,"FAIL":20}.get(ex.get("timeline",{}).get("consistency_check","UNKNOWN"),50)),
                ("⚖️ Compliance", _conf(ex.get("compliance",{}))),
                ("📋 Commercial", _conf(ex.get("commercial_terms",{}))),
            ]
            for label, conf in dims:
                st.markdown(f"<div class='confidence-label'>{label}</div>", unsafe_allow_html=True)
                st.progress(min(conf,100)/100, text=f"{min(conf,100)}%")

    # Detailed risks per vendor
    st.divider(); st.markdown("### 🔍 Detailed Risk Breakdown")
    sel_v = st.selectbox("Select vendor", [v["vendor_name"] for v in extracted_vendors], key="risk_v")
    v_obj = next(v for v in extracted_vendors if v["vendor_name"]==sel_v)
    for r in sorted(st.session_state.extracted.get(v_obj["vendor_id"],{}).get("risks",[]), key=lambda x: {"high":0,"medium":1,"low":2}.get(x.get("severity",""),3)):
        sev = r.get("severity","medium"); icon = {"high":"🔴","medium":"🟠","low":"🟢"}.get(sev,"⚪")
        with st.expander(f"{icon} {r.get('risk','')[:80]}"):
            st.markdown(f"**Category:** {r.get('category','').title()} | **Severity:** {sev.upper()}")
            if r.get("evidence"): st.markdown(f"<div class='evidence-box'>📄 \"{r['evidence']}\"</div>", unsafe_allow_html=True)

    # All-vendor risk dashboard
    st.divider(); st.markdown("### 🚦 All-Vendor Risks")
    all_risks = []
    for vendor in extracted_vendors:
        for r in st.session_state.extracted.get(vendor["vendor_id"],{}).get("risks",[]):
            all_risks.append({**r, "vendor_name": vendor["vendor_name"]})
    for sev, icon, css in [("high","🔴","conflict-box"),("medium","🟠","flag-box"),("low","🟢","evidence-box")]:
        sv_risks = [r for r in all_risks if r.get("severity")==sev]
        if sv_risks:
            st.markdown(f"#### {icon} {sev.upper()} Severity")
            for r in sv_risks[:8]:
                st.markdown(f"<div class='{css}'><b>{r.get('vendor_name','')}</b> — {r.get('risk','')}</div>", unsafe_allow_html=True)
            if len(sv_risks)>8: st.caption(f"...and {len(sv_risks)-8} more")


# ═══════════════════════════════════════════════════════════════
# PAGE 7: PROMPT TRACE
# ═══════════════════════════════════════════════════════════════
def page_prompt_trace():
    st.title("📝 Prompt Trace & Prompt Pack")
    st.caption("Full AI transparency — 8 prompts, design rationale, live traces, and audit trail.")

    t1, t2, t3 = st.tabs(["📚 Prompt Pack (8)", "🔍 Live Traces", "🔬 Example Trace"])

    with t1:
        st.info("8 purpose-built prompts with explicit hallucination controls and structured output requirements. Individual `.md` files in `prompts/`.")
        for pname, pdata in PROMPT_PACK.items():
            with st.expander(f"**{pname}**"):
                st.markdown(f"**Purpose:** {pdata['purpose']}")
                st.write(pdata["why_structured_this_way"])
                for hc in pdata.get("hallucination_controls",[]): st.markdown(f"- ✅ {hc}")
                sp = pdata.get("prompt") or pdata.get("system_prompt","")
                if sp:
                    with st.expander("📄 View prompt"):
                        sp_text = sp.template if hasattr(sp, "template") else str(sp)
                        st.code(sp_text, language="text")
                up = pdata.get("user_prompt","")
                if up:
                    with st.expander("📄 User prompt template"):
                        up_text = up.template if hasattr(up, "template") else str(up)
                        st.code(up_text, language="text")
        st.divider(); st.markdown("### 📁 Prompt Files (`prompts/*.md`)")
        for fname, label in [("rfq.md","RFQ Generation"),("vendor_generation.md","Vendor Generation"),("messy_vendor.md","Messy Data"),
                              ("extraction.md","Extraction"),("validation.md","Validation"),("comparison.md","Comparison"),
                              ("recommendation.md","Recommendation"),("ui_generation.md","UI Generation")]:
            fpath = os.path.join(os.path.dirname(__file__), "prompts", fname)
            if os.path.exists(fpath):
                with st.expander(f"📄 {label} (`{fname}`)"):
                    with open(fpath) as f: st.markdown(f.read())

    with t2:
        st.markdown("### 🔍 Observability via Langfuse")
        st.info(
            "All LLM calls are automatically traced by **Langfuse** — including prompts, "
            "outputs, token usage, and latency. Open your Langfuse dashboard to inspect traces.\n\n"
            "Configure `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and optionally `LANGFUSE_HOST` "
            "in your `.env` file to enable tracing."
        )

    with t3:
        st.markdown("### Example: Extraction Trace — Brandsmith Group (V003)")
        st.markdown("#### Step 1: Input")
        with st.expander("Vendor response text"):
            v003 = next((v for v in st.session_state.vendors if v.get("vendor_id")=="V003"), None)
            if v003: st.text(v003.get("response_text","")[:2000]+"\n\n[...truncated...]")
        st.markdown("#### Step 2: System Prompt")
        with st.expander("Extraction System Prompt"): st.code(EXTRACTION_SYSTEM_PROMPT.template, language="text")
        st.markdown("#### Step 3: User Prompt Template")
        with st.expander("User Prompt"): st.code(EXTRACTION_USER_PROMPT.template.replace("{vendor_id}","V003").replace("{vendor_name}","Brandsmith Group").replace("{vendor_response_text}","[full text]")[:3000], language="text")
        st.markdown("#### Step 4: Structured Output")
        ex = st.session_state.extracted.get("V003",{})
        if ex and "error" not in ex:
            for c in ex.get("conflicting_info",[]): st.markdown(f"<div class='conflict-box'><b>Area:</b> {c.get('area','')}<br><b>S1:</b> {c.get('statement_1','')}<br><b>S2:</b> {c.get('statement_2','')}</div>", unsafe_allow_html=True)
            pricing = ex.get("pricing",{}); st.json({k: pricing.get(k) for k in ["total_stated","itemized_total","consistency_check","consistency_note"]})
        st.markdown("#### Step 5: Buyer-Facing Display")
        st.info("JSON rendered as structured UI in Extraction Review — color-coded badges, evidence boxes, conflict highlights.")


# ═══════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════
page = st.session_state.page

if "RFQ Overview" in page:
    page_rfq_overview()
elif "Vendor Responses" in page:
    page_vendor_responses()
elif "Upload" in page:
    page_upload()
elif "Extraction" in page:
    page_extraction_review()
elif "Comparison" in page:
    page_vendor_comparison()
elif "Risks" in page:
    page_risks()
elif "Prompt" in page:
    page_prompt_trace()
