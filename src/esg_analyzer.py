"""
ESG Analyzer — uses Gemini API to analyze ESG reports and answer questions.
This is the core LLM / RAG layer of the project.
"""
import streamlit as st
import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# 🔑 Configure Gemini API
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

# ── System Prompts ────────────────────────────────────────────

ANALYSIS_SYSTEM = """You are an expert ESG (Environmental, Social, and Governance) analyst.
Always respond with valid JSON only. No extra text."""

QA_SYSTEM = """You are an ESG finance assistant.
Answer clearly using the given context."""


# ── Main Analysis Function ─────────────────────────────────────

def analyze_esg_report(text: str) -> dict:
    """
    Analyze ESG report using Gemini and return structured JSON.
    """
    truncated = text[:12000] if len(text) > 12000 else text

    prompt = f"""
    You are an ESG analyst.

    Analyze the ESG report and return STRICT JSON:

    {{
      "company_name": "string",
      "report_year": "string",
      "overall_score": number,
      "environmental_score": number,
      "social_score": number,
      "governance_score": number,
      "environmental_findings": ["finding1", "finding2", "finding3"],
      "social_findings": ["finding1", "finding2", "finding3"],
      "governance_findings": ["finding1", "finding2", "finding3"],
      "environmental_metrics": {{"Carbon Emissions": "value"}},
      "key_risks": ["risk1", "risk2"],
      "recommendations": ["rec1", "rec2"],
      "esg_rating": "A/B/C/D",
      "summary": "short summary"
    }}

    ESG Report:
    {truncated}

    Return ONLY JSON. No explanation.
    """

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Clean markdown if Gemini wraps JSON
        raw = re.sub(r'^```json\s*', '', raw)
        raw = re.sub(r'^```', '', raw)
        raw = re.sub(r'\s*```$', '', raw)

        return json.loads(raw)

    except Exception as e:
        return {"error": str(e), **_fallback_result(text)}


# ── RAG Question Answering ────────────────────────────────────

def answer_question(question: str, context: str) -> str:
    """
    Answer question using retrieved context.
    """
    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer clearly based only on context.
    If not found, say: "I couldn't find this in the report."
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating answer: {e}"


# ── Fallback (unchanged logic) ─────────────────────────────────

def _fallback_result(text: str) -> dict:
    text_lower = text.lower()

    # --- Environmental scoring ---
    env_score = 50
    if "carbon" in text_lower: env_score += 10
    if "renewable" in text_lower: env_score += 10
    if "emission" in text_lower: env_score += 10
    if "waste" in text_lower: env_score += 5

    # --- Social scoring ---
    soc_score = 50
    if "employee" in text_lower: soc_score += 10
    if "diversity" in text_lower: soc_score += 10
    if "safety" in text_lower: soc_score += 10
    if "community" in text_lower: soc_score += 5

    # --- Governance scoring ---
    gov_score = 50
    if "board" in text_lower: gov_score += 10
    if "compliance" in text_lower: gov_score += 10
    if "audit" in text_lower: gov_score += 10
    if "transparency" in text_lower: gov_score += 5

    # Clamp scores
    env_score = min(env_score, 95)
    soc_score = min(soc_score, 95)
    gov_score = min(gov_score, 95)

    overall = int((env_score + soc_score + gov_score) / 3)

    # Rating logic
    if overall >= 80:
        rating = "A"
    elif overall >= 65:
        rating = "B"
    elif overall >= 50:
        rating = "C"
    else:
        rating = "D"

    return {
        "company_name": "Analyzed Company",
        "report_year": "2024",
        "overall_score": overall,
        "environmental_score": env_score,
        "social_score": soc_score,
        "governance_score": gov_score,
        "environmental_findings": [
            "Carbon and emission related initiatives detected",
            "Renewable energy usage identified",
            "Environmental policies present"
        ],
        "social_findings": [
            "Employee and diversity initiatives found",
            "Workplace safety mentioned",
            "Community engagement detected"
        ],
        "governance_findings": [
            "Board and governance structure present",
            "Compliance and audit systems identified",
            "Transparency practices found"
        ],
        "environmental_metrics": {
            "Keyword Density": str(text_lower.count("carbon") + text_lower.count("emission"))
        },
        "key_risks": [
            "Climate risk",
            "Regulatory compliance risk"
        ],
        "recommendations": [
            "Improve ESG disclosures",
            "Increase sustainability investments",
            "Enhance governance transparency"
        ],
        "esg_rating": rating,
        "summary": "This ESG analysis is generated based on keyword-driven evaluation of the uploaded report."
    }