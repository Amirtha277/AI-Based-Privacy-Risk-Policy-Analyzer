import requests
import re

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

# reuse connection (faster)
session = requests.Session()

# Expanded privacy risk keywords
risk_keywords = [
    "third party",
    "third-party",
    "share",
    "sell",
    "advertising",
    "tracking",
    "cookies",
    "personal data",
    "personal information",
    "collect",
    "store",
    "retain",
    "location",
    "analytics",
    "partners",
    "service providers",
    "behavioral advertising",
    "data retention"
]


# ----------------------------------------------------
# Generic LLM Call
# ----------------------------------------------------
def call_llm(prompt):

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.2
    }

    try:
        response = session.post(OLLAMA_URL, json=data, timeout=60)

        if response.status_code != 200:
            return "LLM server error"

        result = response.json()
        text = result.get("response", "")

        return text.strip()

    except Exception as e:
        return f"LLM analysis failed: {str(e)}"


# ----------------------------------------------------
# Extract Risky Sentences Using Keywords
# ----------------------------------------------------
def extract_risky_sentences(text):

    sentences = re.split(r'[.!?]\s+', text)

    risky = []
    seen = set()

    for s in sentences:

        lower = s.lower()

        for k in risk_keywords:
            if k in lower and s not in seen:
                risky.append(s.strip())
                seen.add(s)
                break

    return risky[:8]   # limit for speed


# ----------------------------------------------------
# Clause-Level LLM Risk Analysis
# ----------------------------------------------------
def analyze_clause_with_llm(clause):

    clause = clause[:400]   # prevent long inputs

    prompt = f"""
You are a privacy policy analysis assistant.

Analyze the following privacy policy clause and identify potential risks to users.

Tasks:
1. Identify if the clause involves data collection, tracking, advertising, or third-party sharing.
2. Determine the privacy risk level.
3. Explain the risk in simple language.

Clause:
{clause}

Return ONLY in this format:

Risk Level: Low / Medium / High
Category: Data Sharing / Tracking / Personal Data / Advertising / Storage
Explanation: One short sentence explaining the risk.
"""

    return call_llm(prompt)


# ----------------------------------------------------
# Overall Privacy Risk Score
# ----------------------------------------------------
def llm_risk_score(summary):

    summary = summary[:800]   # speed optimization

    risky_sentences = extract_risky_sentences(summary)

    if risky_sentences:
        text_to_analyze = " ".join(risky_sentences)
    else:
        text_to_analyze = summary[:400]

    prompt = f"""
You are a privacy policy risk assessor.

Evaluate the privacy risk based on:
- Personal data collection
- Third-party data sharing
- Tracking technologies
- Advertising usage
- Data retention

Text:
{text_to_analyze}

Return ONLY in this format:

Score: (0-100)
Reason: One sentence explaining the score.
"""

    return call_llm(prompt)