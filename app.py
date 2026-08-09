"""
NyayaAI - AI-powered Indian Legal Information Assistant
Backend: Flask + Gemini API
"""

import os
import re
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

MAX_QUESTION_LENGTH = 1500

client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"[NyayaAI] Failed to initialize Gemini client: {e}")
        client = None
else:
    print("[NyayaAI] WARNING: GEMINI_API_KEY not found. Set it in your .env file.")


# ---------------------------------------------------------------------------
# System prompt for the AI
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are NyayaAI, an Indian legal information assistant. Your job is to help
users understand legal concepts and possible next steps in simple language.
You are NOT a lawyer and must not present yourself as one.

STRICT RULES:
- Focus on Indian legal context only.
- Use simple, plain language. Avoid unnecessary legal jargon.
- Do NOT fabricate laws, sections, court cases, penalties, or deadlines. If you
  are not confident about a specific law or section, say so explicitly and
  advise the user to verify it with an official source or a qualified lawyer.
- Clearly separate general legal information from case-specific legal advice.
- Never encourage illegal activity. Never tell users to lie, destroy evidence,
  threaten someone, or evade law enforcement.
- If the situation sounds like an emergency or involves immediate danger,
  clearly advise the user to contact emergency services (police: 100 / 112)
  or appropriate authorities immediately, at the top of your response.
- For serious legal matters, recommend consulting a qualified lawyer.
- Give practical, actionable next steps.
- Mention relevant official authorities, government bodies, or portals where
  appropriate (e.g. consumer forums, labour commissioner, rent authority).
- If the question lacks important facts, either ask a small number of
  clarifying questions, or give a general answer while clearly stating the
  assumptions you made.

RESPONSE FORMAT (always follow this exact structure, using these exact
headings, in this order, each on its own line):

UNDERSTANDING:
<2-4 sentences restating and clarifying the user's situation in simple language>

LEGAL_INFO:
<Relevant Indian laws/rights that reasonably apply. Use bullet points starting with "- ". If unsure of an exact section/act, say so explicitly rather than inventing one.>

NEXT_STEPS:
<Practical possible next steps as bullet points starting with "- ">

DOCUMENTS:
<Documents or evidence that may help, as bullet points starting with "- ". If none are obviously relevant, say "No specific documents are typically required at this stage.">

SEEK_HELP:
<When and why the user should contact a lawyer, police, consumer forum, or other authority. Be specific about which authority when possible.>

SOURCES:
<Any official sources, acts, or authorities to check, as bullet points starting with "- ". If you are not confident of specific citations, say "Please verify current legal provisions with an official source or a qualified lawyer" instead of inventing a source.>

Do not add any text before "UNDERSTANDING:" or after the "SOURCES:" section."""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SECTION_KEYS = [
    ("UNDERSTANDING", "understanding"),
    ("LEGAL_INFO", "legalInfo"),
    ("NEXT_STEPS", "nextSteps"),
    ("DOCUMENTS", "documents"),
    ("SEEK_HELP", "seekHelp"),
    ("SOURCES", "sources"),
]


def parse_ai_response(raw_text: str) -> dict:
    """Parse the structured Gemini response into a dict of sections.
    Falls back gracefully if the model doesn't follow the format exactly.
    """
    sections = {key: "" for _, key in SECTION_KEYS}

    # Build a regex that captures content between known headings
    pattern = r"(" + "|".join(k for k, _ in SECTION_KEYS) + r"):\s*(.*?)(?=(?:" + \
        "|".join(k for k, _ in SECTION_KEYS) + r"):|\Z)"
    matches = re.findall(pattern, raw_text, flags=re.DOTALL)

    if matches:
        heading_to_key = {k: v for k, v in SECTION_KEYS}
        for heading, content in matches:
            key = heading_to_key.get(heading)
            if key:
                sections[key] = content.strip()

    # Fallback: if parsing failed entirely, put everything into "understanding"
    if not any(sections.values()):
        sections["understanding"] = raw_text.strip()

    return sections


def build_error_response(message: str, status_code: int = 400):
    return jsonify({"success": False, "error": message}), status_code


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    if client is None:
        return build_error_response(
            "The AI service is not configured. Please set GEMINI_API_KEY in the .env file.",
            503,
        )

    data = request.get_json(silent=True)
    if not data or "question" not in data:
        return build_error_response("Invalid request. A 'question' field is required.", 400)

    question = str(data.get("question", "")).strip()

    if not question:
        return build_error_response("Please enter a question describing your situation.", 400)

    if len(question) > MAX_QUESTION_LENGTH:
        return build_error_response(
            f"Your question is too long. Please limit it to {MAX_QUESTION_LENGTH} characters.",
            400,
        )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.4,
                max_output_tokens=1200,
            ),
        )

        raw_text = (response.text or "").strip()

        if not raw_text:
            return build_error_response(
                "NyayaAI could not generate a response. Please try rephrasing your question.",
                502,
            )

        sections = parse_ai_response(raw_text)

        return jsonify({"success": True, "answer": sections})

    except Exception as e:
        # Never expose raw internal/API errors to the user
        print(f"[NyayaAI] Gemini API error: {e}")
        return build_error_response(
            "NyayaAI is having trouble reaching the AI service right now. Please try again in a moment.",
            502,
        )


@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Not found."}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"success": False, "error": "Something went wrong on our end."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
