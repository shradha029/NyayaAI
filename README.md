# ⚖️ NyayaAI

**Understand your rights. Know your next step.**

An AI-powered Indian legal information assistant.

---

## Problem Statement

Most Indians don't understand their basic legal rights because legal language
is complicated, legal help is expensive or hard to reach, and there is no
simple, trustworthy starting point that explains "what does this mean for me,
and what do I do next?" in plain language.

## Solution

NyayaAI lets anyone describe a legal situation in their own words and
receive an easy-to-understand, structured response covering:

1. A simple explanation of the issue
2. Relevant Indian laws/rights, where reasonably applicable
3. Possible next steps
4. Documents/evidence that may help
5. When to contact a lawyer, police, consumer forum, or other authority
6. Sources/references to verify further

**NyayaAI provides general legal information, not professional legal advice.**
This disclaimer is shown clearly throughout the website.

## Why NyayaAI?

**The problem:** Legal information in India is often locked behind complicated
terminology, scattered across acts and sources, and inaccessible to ordinary
citizens who don't know where to begin — whether it's a landlord withholding
a deposit, an employer skipping a salary, or a defective product a seller
won't refund.

**The solution:** NyayaAI provides a simple, conversational interface where
anyone can describe their situation in plain language and get back a
structured, easy-to-read explanation of potentially relevant Indian legal
information and possible next steps — clearly flagged as a starting point,
not a final answer, with guidance on when to involve a real lawyer or
authority.

## Features

- ✓ Simple legal language, no jargon
- ✓ AI-powered assistance (Google Gemini)
- ✓ Indian legal context
- ✓ Suggested, practical next steps
- ✓ Evidence/document checklist
- ✓ Mobile responsive, modern UI
- ✓ Privacy-conscious — no accounts, no storage of your questions
- ✓ Clear, repeated disclaimers that this is not legal advice

## Technology Stack

**Frontend:** HTML5, CSS3, Vanilla JavaScript (no frameworks)
**Backend:** Python, Flask
**AI:** Google Gemini API (`google-genai` SDK)

## Project Structure

```
NyayaAI/
│
├── app.py                # Flask app, /ask route, Gemini integration
├── requirements.txt      # Python dependencies
├── .env.example           # Template for your API key
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html         # Single-page site
│
└── static/
    ├── style.css           # Styling (navy/blue/gold theme)
    └── script.js           # Frontend logic (fetch, rendering, UI)
```

## Installation

### 1. Clone / open the project folder

```bash
cd NyayaAI
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## How to Create a Gemini API Key

1. Go to **https://aistudio.google.com/apikey**
2. Sign in with a Google account
3. Click **"Create API key"**
4. Copy the generated key

## How to Create Your `.env` File

1. In the project root, copy the example file:

   ```bash
   # Windows
   copy .env.example .env

   # macOS / Linux
   cp .env.example .env
   ```

2. Open `.env` and paste your key:

   ```
   GEMINI_API_KEY=your_actual_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```

3. **Never commit `.env` to GitHub** — it's already in `.gitignore`.

## How to Run the Project

```bash
python app.py
```

Then open your browser at:

```
http://127.0.0.1:5000
```

## Example Questions to Try

- "My landlord is refusing to return my security deposit. What can I do?"
- "My employer has not paid my salary for two months."
- "I bought a defective product and the seller refuses to refund me."
- "What are my rights if I am stopped by the police?"

## Future Improvements

- Multi-language support (Hindi and other regional languages)
- Save/export a response as a PDF summary
- Location-aware guidance (state-specific rules, nearby consumer forums)
- Optional chat history within a session
- Voice input for accessibility

## Disclaimer

NyayaAI provides general legal information for educational purposes and does
not replace advice from a qualified lawyer or legal professional. Laws can
change and individual cases may differ. Always verify important information
with official government/legal sources or a qualified professional.
