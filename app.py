import streamlit as st
import os
import json
import time
from src.pdf_processor import extract_text_from_pdf
from src.esg_analyzer import analyze_esg_report
from src.report_generator import generate_html_report
from src.vector_store import VectorStore

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ESG Finance Report Analyzer",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #0f4c35 0%, #1a7a52 50%, #2eb87a 100%);
        padding: 2rem; border-radius: 12px; color: white; margin-bottom: 2rem;
        text-align: center;
    }
    .metric-card {
        background: white; border: 1px solid #e2e8f0; border-radius: 10px;
        padding: 1.2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .score-badge {
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        font-weight: 600; font-size: 0.85rem;
    }
    .badge-high   { background:#d1fae5; color:#065f46; }
    .badge-medium { background:#fef3c7; color:#92400e; }
    .badge-low    { background:#fee2e2; color:#991b1b; }
    .stButton>button {
        background: linear-gradient(135deg, #0f4c35, #2eb87a);
        color: white; border: none; border-radius: 8px;
        padding: 0.6rem 2rem; font-weight: 600;
        transition: transform 0.2s;
    }
    .stButton>button:hover { transform: translateY(-2px); }
    .section-header {
        border-left: 4px solid #2eb87a; padding-left: 1rem;
        font-size: 1.1rem; font-weight: 600; color: #0f4c35;
        margin: 1.5rem 0 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 ESG Report Analyzer")
    
    st.divider()
    st.markdown("### Navigation")
    page = st.radio("Navigation", ["📄 Analyze Report", "💬 Ask Questions", "📊 Dashboard", "ℹ️ About"])
    st.divider()
    st.markdown("### Settings")
    analysis_depth = st.selectbox("Analysis Depth", ["Standard", "Deep", "Quick"])
    show_raw_text = st.checkbox("Show Extracted Text", False)
    st.markdown("---")
    st.caption("Built with Streamlit")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🌿 ESG Finance Report Analyzer</h1>
    <p>AI-powered Environmental, Social & Governance analysis using RAG</p>
</div>
""", unsafe_allow_html=True)

# ── Initialize session state ──────────────────────────────────────────────────
for key in ["analysis_result", "extracted_text", "vector_store", "chat_history"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "chat_history" else []

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — ANALYZE REPORT
# ═══════════════════════════════════════════════════════════════════════════════
if "Analyze" in page:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-header">Upload ESG Report (PDF)</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        if uploaded_file:
            with st.spinner("📄 Extracting text from PDF..."):
                text = extract_text_from_pdf(uploaded_file)
                st.session_state.extracted_text = text
            st.success(f"✅ Extracted {len(text.split())} words from report")

            if show_raw_text:
                with st.expander("Raw Extracted Text"):
                    st.text_area("", text[:3000] + "...", height=200)

            if st.button("🔍 Run ESG Analysis"):
                with st.spinner("🤖 Analyzing with AI..."):
                    progress = st.progress(0)
                    for i in range(5):
                        time.sleep(0.3)
                        progress.progress((i+1)*20)
                    result = analyze_esg_report(text)
                    st.session_state.analysis_result = result

                    vs = VectorStore()
                    vs.add_document(text)
                    st.session_state.vector_store = vs

                st.success("✅ Analysis Complete!")

    with col2:
        st.markdown('<div class="section-header">Demo Mode (No PDF needed)</div>', unsafe_allow_html=True)
        st.info("💡 Click below to analyze a sample ESG report and see the full demo")

        if st.button("▶ Run Demo Analysis"):
            sample_text = open("data/sample_reports/sample_esg.txt").read()
            st.session_state.extracted_text = sample_text
            with st.spinner("🤖 Analyzing sample report..."):
                result = analyze_esg_report(sample_text)
                st.session_state.analysis_result = result
                vs = VectorStore()
                vs.add_document(sample_text)
                st.session_state.vector_store = vs
            st.success("✅ Demo analysis complete!")

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.analysis_result:
        r = st.session_state.analysis_result
        st.divider()
        st.markdown("## 📊 Analysis Results")

        # Score cards
        c1, c2, c3, c4 = st.columns(4)
        scores = {
            "🌍 Environmental": r.get("environmental_score", 72),
            "👥 Social": r.get("social_score", 68),
            "🏛 Governance": r.get("governance_score", 75),
            "⭐ Overall ESG": r.get("overall_score", 71),
        }
        for col, (label, score) in zip([c1,c2,c3,c4], scores.items()):
            badge = "high" if score>=70 else "medium" if score>=50 else "low"
            col.metric(label, f"{score}/100")

        st.divider()

        # Detailed breakdown
        tab1, tab2, tab3 = st.tabs(["🌍 Environmental", "👥 Social", "🏛 Governance"])

        with tab1:
            st.markdown("### Environmental Findings")
            for finding in r.get("environmental_findings", []):
                st.markdown(f"- {finding}")
            st.markdown("### Key Metrics")
            for k, v in r.get("environmental_metrics", {}).items():
                st.metric(k, v)

        with tab2:
            st.markdown("### Social Findings")
            for finding in r.get("social_findings", []):
                st.markdown(f"- {finding}")

        with tab3:
            st.markdown("### Governance Findings")
            for finding in r.get("governance_findings", []):
                st.markdown(f"- {finding}")

        # Download report
        st.divider()
        if st.button("📥 Generate Report"):
            html = generate_html_report(r)
            st.download_button("⬇ Download Report", html, "esg_report.html", "text/html")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — ASK QUESTIONS (RAG)
# ═══════════════════════════════════════════════════════════════════════════════
elif "Ask" in page:
    st.markdown("## 💬 Ask Questions About the Report")
    st.info("Upload and analyze a report first, then ask any questions about it.")

    if not st.session_state.vector_store:
        st.warning("⚠️ No report loaded. Please analyze a report first.")
    else:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        question = st.chat_input("Ask anything about the ESG report...")
        if question:
            st.session_state.chat_history.append({"role":"user","content":question})
            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    vs = st.session_state.vector_store
                    context = vs.search(question)
                    from src.esg_analyzer import answer_question
                    answer = answer_question(question, context)
                st.write(answer)
                st.session_state.chat_history.append({"role":"assistant","content":answer})

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
elif "Dashboard" in page:
    st.markdown("## 📊 ESG Score Dashboard")
    if not st.session_state.analysis_result:
        st.warning("⚠️ Run an analysis first to see the dashboard.")
    else:
        r = st.session_state.analysis_result
        import plotly.graph_objects as go
        import plotly.express as px

        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=r.get("overall_score", 71),
                title={"text": "Overall ESG Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#2eb87a"},
                    "steps": [
                        {"range": [0,50], "color":"#fee2e2"},
                        {"range": [50,75], "color":"#fef3c7"},
                        {"range": [75,100], "color":"#d1fae5"},
                    ],
                }
            ))
            st.plotly_chart(fig, width="stretch")

        with col2:
            categories = ["Environmental","Social","Governance"]
            values = [r.get("environmental_score",72), r.get("social_score",68), r.get("governance_score",75)]
            fig2 = go.Figure(go.Scatterpolar(
                r=values+[values[0]], theta=categories+[categories[0]],
                fill="toself", fillcolor="rgba(46,184,122,0.3)",
                line_color="#2eb87a"
            ))
            fig2.update_layout(polar=dict(radialaxis=dict(range=[0,100])), title="ESG Radar Chart")
            st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — ABOUT
# ═══════════════════════════════════════════════════════════════════════════════
elif "About" in page:
    st.markdown("""
    ## ℹ️ About This Project

    ### ESG Finance Report Analyzer
    A final-year AI project that uses **RAG (Retrieval-Augmented Generation)** to analyze
    Environmental, Social, and Governance (ESG) reports automatically.

    ### Tech Stack
    | Layer | Technology |
    |---|---|
    | Frontend | Streamlit |
    | AI Model | Claude API (claude-sonnet-4) |
    | Vector DB | FAISS (in-memory) |
    | PDF Parsing | PyMuPDF |
    | Embeddings | sentence-transformers |
    | Charts | Plotly |

    ### Architecture (RAG Pipeline)
    1. **PDF Upload** → PyMuPDF extracts text
    2. **Chunking** → Text split into 500-token chunks
    3. **Embedding** → sentence-transformers encodes chunks
    4. **Vector Store** → FAISS stores embeddings
    5. **Query** → User question → top-k retrieval
    6. **Generation** → Claude API generates answer with context

    ### Project Steps Followed
    Following all 10 steps: Problem Understanding → Requirements → Data Collection →
    Preprocessing → Embedding → RAG Design → App Dev → Evaluation → Optimization → Demo
    """)
