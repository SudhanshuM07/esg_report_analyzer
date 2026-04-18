<<<<<<< HEAD
# 🌿 ESG Finance Report Analyzer
### Final Year Project — AI-Powered ESG Analysis using RAG

---

## 📌 What This Project Does

This application allows users to upload any corporate ESG (Environmental, Social & Governance) 
PDF report and get an AI-powered analysis including:

- **Automated ESG Scoring** (0-100 for E, S, G + Overall)
- **Key Findings Extraction** per ESG pillar
- **Risk Identification** and recommendations
- **Downloadable HTML Report**
- **Chat Interface** — ask any question about the report (RAG pipeline)
- **Visual Dashboard** with gauge charts and radar chart

---

## 🧱 Tech Stack

| Component         | Technology                      |
|-------------------|---------------------------------|
| Frontend / UI     | Streamlit                       |
| LLM               | Claude Sonnet 4 (Anthropic API) |
| PDF Parsing       | PyMuPDF (fitz)                  |
| Embeddings        | sentence-transformers           |
| Vector Database   | FAISS (in-memory)               |
| Charts            | Plotly                          |
| Language          | Python 3.10+                    |

---

## 🗂️ Project Structure

```
esg_analyzer/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── README.md                       # This file
│
├── src/
│   ├── __init__.py
│   ├── pdf_processor.py            # Step 3-4: PDF extraction & chunking
│   ├── esg_analyzer.py             # Step 5-6: LLM analysis & RAG Q&A
│   ├── vector_store.py             # Step 5: FAISS embeddings & retrieval
│   └── report_generator.py        # Step 10: HTML report generation
│
└── data/
    └── sample_reports/
        └── sample_esg.txt          # Demo sample report
```

---

## ⚙️ Setup Instructions (Step by Step)

### Step 1 — Install Python
Make sure you have Python 3.10 or higher installed.
```bash
python --version
```

### Step 2 — Create Virtual Environment
```bash
cd esg_analyzer
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```
> ⚠️ sentence-transformers downloads a ~90MB model on first run. Requires internet.

### Step 4 — Get Your Anthropic API Key
1. Go to https://console.anthropic.com
2. Sign up / log in
3. Click "API Keys" → "Create Key"
4. Copy the key

### Step 5 — Set Your API Key
```bash
# Option A: Create a .env file (recommended)
cp .env.example .env
# Open .env and replace "your_api_key_here" with your actual key

# Option B: Set environment variable directly
# Windows:
set ANTHROPIC_API_KEY=sk-ant-xxxxx

# Mac/Linux:
export ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### Step 6 — Run the App
```bash
streamlit run app.py
```

The app will open automatically at: **http://localhost:8501**

---

## 🚀 How to Use

### Method 1 — Demo Mode (No PDF needed)
1. Open the app
2. Click **"▶ Run Demo Analysis"** on the right side
3. Explore the results in the tabs
4. Go to **Dashboard** page to see visual charts
5. Go to **Ask Questions** to chat about the report

### Method 2 — Real PDF Upload
1. Go to **Analyze Report** page
2. Upload any corporate ESG/sustainability PDF report
3. Click **"🔍 Run ESG Analysis"**
4. Wait ~10-20 seconds for AI analysis
5. Download the HTML report

---

## 📊 Following the 10-Step Framework

| Step | Phase                | How This Project Does It |
|------|---------------------|--------------------------|
| 1    | Problem Understanding | ESG report analysis for investors & researchers |
| 2    | Requirement Analysis  | Score extraction, Q&A, report generation |
| 3    | Data Collection       | PDF upload + sample ESG report included |
| 4    | Data Preprocessing    | `pdf_processor.py` — clean, chunk text |
| 5    | Embedding & Vector DB | `vector_store.py` — FAISS + sentence-transformers |
| 6    | LLM / RAG Design      | `esg_analyzer.py` — Claude API + context retrieval |
| 7    | Application Development| `app.py` — full Streamlit UI |
| 8    | Evaluation            | Score accuracy, hallucination check via Q&A |
| 9    | Optimization          | Chunking overlap, top-k tuning, prompt tuning |
| 10   | Documentation & Demo  | This README + HTML report download |

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `AuthenticationError` | Check ANTHROPIC_API_KEY in `.env` |
| PDF text empty | Try another PDF; some are image-only (scanned) |
| FAISS not installing | Run `pip install faiss-cpu` separately |
| Slow first run | sentence-transformers downloads model (~90MB) |

---

## 🏆 Project Evaluation Points

- ✅ Working RAG pipeline (retrieval + generation)
- ✅ Real Claude API integration
- ✅ Clean UI with Streamlit
- ✅ Structured JSON output with scores
- ✅ Downloadable HTML report
- ✅ Chat / Q&A over documents
- ✅ Visual charts (Plotly)
- ✅ Follows all 10 project phases

---

*Built as Final Year Project — AI/ML stream*
=======
# esg_report_analyzer
>>>>>>> f0bdbdeaf0f9d9d979da3ed087ce8d1448e5406f
