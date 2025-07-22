from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Sample dataset for dialect translation
DIALECT_DATA = {
    "Oyo": {
        "Good morning": "E kaaro",
        "Thank you": "Ese",
        "How are you?": "Bawo ni?",
        "Goodbye": "O dabo",
    },
    "Egba": {
        "Good morning": "E kaaro",
        "Thank you": "Ese",
        "How are you?": "Bawo",
        "Goodbye": "O dabo",
    },
    "Ijebu": {
        "Good morning": "E karo",
        "Thank you": "O se",
        "How are you?": "Shé wa dada ni?",
        "Goodbye": "O digbose",
    },
    "Ekiti": {
        "Good morning": "E kaaro",
        "Thank you": "Ese pupo",
        "How are you?": "Bawo l'awa?",
        "Goodbye": "O dabo",
    },
    "Ondo": {
        "Good morning": "E kaaro",
        "Thank you": "O se gan",
        "How are you?": "Bawo ni o se wa?",
        "Goodbye": "O dabo",
    },
    "Egun": {
        "Good morning": "E kaaro",
        "Thank you": "O se",
        "How are you?": "Bawo ni?",
        "Goodbye": "O dabo",
    },
    "Ibadan": {
        "Good morning": "E kaaro",
        "Thank you": "O se",
        "How are you?": "Bawo ni?",
        "Goodbye": "O dabo",
    },
    "Ife": {
        "Good morning": "E kaaro",
        "Thank you": "Ese",
        "How are you?": "Bawo ni?",
        "Goodbye": "O dabo",
    },
}

# Reverse lookup for phrase to English
ENGLISH_LOOKUP = {}
for dialect, phrases in DIALECT_DATA.items():
    for eng, phrase in phrases.items():
        ENGLISH_LOOKUP.setdefault(phrase.lower(), eng)

def translate_dialect(text, source, target):
    # Normalize input
    text = text.strip().lower()
    # Find English meaning from source dialect
    eng = ENGLISH_LOOKUP.get(text)
    if not eng:
        return f"[No translation found for '{text}' in {source} dialect]"
    # Get target dialect translation
    return DIALECT_DATA.get(target, {}).get(eng, f"[No translation for '{eng}' in {target}]")

@app.post("/translate", response_class=HTMLResponse)
def translate(request: Request, source: str = Form(...), target: str = Form(...), text: str = Form(...)):
    translated = translate_dialect(text, source, target)
    return templates.TemplateResponse("index.html", {"request": request, "result": translated, "source": source, "target": target, "text": text})