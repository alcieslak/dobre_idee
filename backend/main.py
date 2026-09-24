import pandas as pd
from fastapi import FastAPI

from services import find_customer

app = FastAPI()


@app.get("/")
def home():
    df = pd.read_sql("SELECT * FROM dane", "sqlite:///poc_database.db")
    return df.to_dict(orient="records")


@app.get("/dane")
def dane(kontrahent: str = None):
    return find_customer(kontrahent)

# Uvicorn to program, który uruchamia Twoją aplikację FastAPI jako serwer WWW.
# uvicorn main:app --reload
# http://127.0.0.1:8000/dane?kontrahent=Cie%C5%9Blak%20Krzysztof
