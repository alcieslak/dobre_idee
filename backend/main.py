from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles

from services import find_customer

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    html_file = Path(__file__).parent / "templates" / "index.html"

    return html_file.read_text(encoding="utf-8")


@app.get("/dane")
def dane(kontrahent: str = None):
    return find_customer(kontrahent)

# Uvicorn to program, który uruchamia Twoją aplikację FastAPI jako serwer WWW.
# uvicorn main:app --reload
# http://127.0.0.1:8000/dane?kontrahent=Cie%C5%9Blak%20Krzysztof
