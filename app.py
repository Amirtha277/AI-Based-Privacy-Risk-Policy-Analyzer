from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from summarizer import summarize_text
from risk_rules import detect_risks
from optimizer import optimize_text
from audio_generator import generate_audio
from infographic import generate_infographic
from web_reader import fetch_tc_from_url
from quantum_risk import quantum_risk_score
from translation import translate_text
import re
import base64
from llm_risk_analyzer import analyze_clause_with_llm
from llm_risk_analyzer import llm_risk_score

app = Flask(__name__)
CORS(app)  # ✅ Allow Chrome extension to call API


# ---------------- CLEANING FUNCTIONS ----------------

def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\s+', ' ', text)

    sentences = text.split(". ")
    cleaned = []

    for s in sentences:
        s = s.strip()

        if len(s) < 40:
            continue

        words = s.split()
        capitalized = sum(1 for w in words if w.istitle())

        if capitalized > len(words) * 0.6:
            continue

        cleaned.append(s)

    return ". ".join(cleaned)


def remove_repetition(text):
    words = text.split()
    clean_words = []
    prev = ""

    for w in words:
        if w != prev:
            clean_words.append(w)
        prev = w

    return " ".join(clean_words)


# ---------------- WEB UI ROUTES ----------------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    url = request.form["url"]
    lang = request.form["lang"]

    text = fetch_tc_from_url(url)
    text = clean_text(text)
    # 2 Optimize text
    optimized_text = optimize_text(text)

    summary = summarize_text(optimized_text)

    if not summary.strip():
        summary = "This policy explains how the company collects, uses, and protects user data."

    summary = remove_repetition(summary)
    summary = translate_text(summary, lang)
    ai_result = llm_risk_score(summary)

    match = re.search(r'\d+', ai_result)
    ai_score = int(match.group()) if match else 50
    risks = detect_risks(summary)

    translated_risks = []
    for clause, level in risks:
        translated_clause = translate_text(clause, lang)
        translated_risks.append((translated_clause, level))

    score = quantum_risk_score(risks,ai_score)

    if score <= 30:
        overall_level = "Low Risk"
    elif score <= 60:
        overall_level = "Medium Risk"
    else:
        overall_level = "High Risk"

    display_overall_level = translate_text(overall_level, lang)

    generate_infographic(score, translated_risks, lang)

    risk_text = ""
    for clause, level in translated_risks:
        risk_text += f"{clause}. Risk level is {level}. "

    generate_audio(risk_text, lang)

    return render_template(
        "result.html",
        summary=summary,
        score=score,
        overall_level=display_overall_level,
        risks=translated_risks, 
        ai_score=ai_score
    )

    
# ---------------- API ROUTE (FOR CHROME EXTENSION) ----------------

# ---------------- API ROUTE (FOR CHROME EXTENSION) ----------------

# ---------------- API ROUTE (FOR CHROME EXTENSION) ----------------
from concurrent.futures import ThreadPoolExecutor

cache = {}

@app.route("/analyze_api", methods=["POST"])
def analyze_api():

    data = request.get_json(force=True)

    url = data.get("url")
    lang = data.get("lang", "en")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # cache should depend on url + language
    cache_key = f"{url}_{lang}"

    if cache_key in cache:
        print("Returning cached result")
        return jsonify(cache[cache_key])

    # ---------- FETCH POLICY ----------
    text = fetch_tc_from_url(url)

    if not text:
        return jsonify({"error": "Unable to fetch policy"}), 500

    text = clean_text(text)

    # reduce size early (big speed improvement)
    text = text[:3500]
    # 2 Optimize text
    optimized_text = optimize_text(text)
    # ---------- SUMMARIZE ----------
    summary = summarize_text(optimized_text)

    if not summary.strip():
        summary = "This policy explains how the company collects, uses, and protects user data."

    summary = remove_repetition(summary)

    # ---------- AI RISK SCORE ----------
    ai_result = llm_risk_score(summary)

    match = re.search(r'\d+', ai_result)
    ai_score = int(match.group()) if match else 50

    # ---------- RULE BASED RISKS ----------
    risks = detect_risks(text)

    translated_risks = []
    risk_text_for_audio = ""

    # translate risk sentences
    for clause, level in risks:
        translated_clause = translate_text(clause, lang)

        translated_risks.append((translated_clause, level))

        risk_text_for_audio += f"{translated_clause}. Risk level is {level}. "

    # ---------- FINAL SCORE ----------
    score = quantum_risk_score(risks, ai_score)

    # ---------- PARALLEL TASKS ----------
    with ThreadPoolExecutor(max_workers=3) as executor:

        img_future = executor.submit(
            generate_infographic,
            score,
            translated_risks,
            lang
        )

        audio_future = executor.submit(
            generate_audio,
            risk_text_for_audio,
            lang
        )

        img_future.result()
        audio_future.result()

    # ---------- PREPARE RISK LIST ----------
    risk_list = [
        {"clause": clause, "level": level}
        for clause, level in translated_risks
    ]

    # ---------- LOAD FILES ----------
    with open("static/infographic.png", "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    with open("static/output.mp3", "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")

    result = {
        "score": score,
        "ai_score": ai_score,
        "risks": risk_list,
        "image_base64": image_base64,
        "audio_base64": audio_base64
    }

    # save in cache
    cache[cache_key] = result

    return jsonify(result)
# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    app.run(debug=True)