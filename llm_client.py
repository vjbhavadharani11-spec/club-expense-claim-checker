"""
llm_client.py - Groq LLM API integration with 5-role prompt and deterministic offline fallback.
CIT AI-Native Engineering Capstone Project: Club Expense Claim Checker
"""

import os
import json
import re
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SYSTEM_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "system_prompt.txt")

def load_system_prompt() -> str:
    """Reads the 5-role system prompt from system_prompt.txt."""
    if os.path.exists(SYSTEM_PROMPT_PATH):
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def _deterministic_extractor(note: str) -> dict:
    """
    Offline fallback extractor.
    Implements the exact same rules as the 5-role system prompt:
    - Never calculates
    - Never extracts words as amounts
    - Extracts amount only if written in digits
    - Detects bill presence and checks for negative qualifiers
    - Categorizes into allowed categories
    """
    note_lower = note.lower()
    amount = None
    
    # Check if calculation is required
    requires_calc = any(term in note_lower for term in ["per person", "per head", "per member", "each for", "each"])
    
    if not requires_calc:
        matches = re.findall(r'(?<!\d-)(?<!\d/)\b(\d{1,3}(?:,\d{3})+|\d+)\b', note)
        if matches:
            for m in matches:
                val = int(m.replace(',', ''))
                # Filter out calendar year like 2026
                if val != 2026:
                    amount = val
                    break

    # 2. Extract category
    if any(w in note_lower for w in ["print", "banner", "pamphlet", "sticker", "badge"]):
        category = "printing"
    elif any(w in note_lower for w in ["food", "snack", "refreshment", "tea", "lunch", "dinner"]):
        category = "food"
    elif any(w in note_lower for w in ["travel", "auto", "bus", "train", "fare", "cab", "taxi"]):
        category = "travel"
    elif any(w in note_lower for w in ["prize", "trophy", "trophies", "medal", "award", "book"]):
        category = "prizes"
    elif any(w in note_lower for w in ["kit", "sensor", "arduino", "tripod", "camera", "sound", "mixer", "keyboard", "mouse", "equipment", "cricket", "shuttlecock", "balls"]):
        category = "equipment"
    elif any(w in note_lower for w in ["costume", "props", "makeup", "stage decoration"]):
        category = "costumes"
    else:
        category = "other"

    # 3. Extract bill boolean
    # True only if bill/receipt/invoice/ticket is mentioned and NOT marked as missing/lost/no bill/later
    has_bill_mention = any(w in note_lower for w in ["bill", "receipt", "invoice", "ticket"])
    has_negative = any(neg in note_lower for neg in ["no bill", "bill lost", "lost", "without bill", "later", "coming later"])
    bill = bool(has_bill_mention and not has_negative)

    # 4. Extract summary (10 words or fewer)
    words = note.split()
    summary = " ".join(words[:6]) if words else "Expense claim"

    return {
        "amount": amount,
        "category": category,
        "bill": bill,
        "summary": summary
    }

def call_llm(note: str) -> dict:
    """
    Calls Groq Cloud API with the 5-role system prompt to extract claim facts.
    Uses OpenAI-compatible endpoint: https://api.groq.com/openai/v1/chat/completions
    If the API key is not configured, invalid, or offline, falls back safely to
    the deterministic rule-based extractor so the system never crashes.
    """
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
    system_instruction = load_system_prompt()

    # If key is mock or unset, use deterministic extractor safely
    if not api_key or api_key.startswith("mock-") or api_key == "YOUR_GROQ_API_KEY":
        return _deterministic_extractor(note)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_instruction
            },
            {
                "role": "user",
                "content": f"Extract the claim facts from this note:\n\"{note}\""
            }
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.0
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            raw_text = data["choices"][0]["message"]["content"].strip()
            # Clean possible markdown wrapping if returned
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            return json.loads(raw_text.strip())
        else:
            # On API error, fallback safely without crashing
            return _deterministic_extractor(note)
    except Exception:
        # Robustness rule: never crash on network/JSON errors
        return _deterministic_extractor(note)
