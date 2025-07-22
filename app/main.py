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

@app.post("/translate", response_class=HTMLResponse)
def translate(request: Request, source: str = Form(...), target: str = Form(...), text: str = Form(...)):
    # Placeholder translation logic
    translated = f"[Translated {text} from {source} to {target}]"
    return templates.TemplateResponse("index.html", {"request": request, "result": translated, "source": source, "target": target, "text": text})