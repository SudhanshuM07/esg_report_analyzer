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
    """Fallback data if API fails."""
    return {
        "company_name": "Demo Corp",
        "report_year": "2024",
        "overall_score": 70,
        "environmental_score": 72,
        "social_score": 68,
        "governance_score": 75,
        "environmental_findings": [
            "Reduced carbon emissions",
            "Increased renewable energy usage",
            "Improved waste management"
        ],
        "social_findings": [
            "Improved employee safety",
            "Better diversity inclusion",
            "Community engagement increased"
        ],
        "governance_findings": [
            "Strong board structure",
            "Anti-corruption policies",
            "Transparent reporting"
        ],
        "environmental_metrics": {
            "Carbon Emissions": "Reduced"
        },
        "key_risks": [
            "Climate risk",
            "Regulatory pressure"
        ],
        "recommendations": [
            "Adopt net-zero targets",
            "Improve ESG disclosure"
        ],
        "esg_rating": "B",
        "summary": "Company shows moderate ESG performance with improvement scope."
    }
