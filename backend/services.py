from fastapi import FastAPI
from sqlalchemy import create_engine, text
import pandas as pd

app = FastAPI()

engine = create_engine("sqlite:///poc_database.db")


@app.get("/")
def home():
    df = pd.read_sql("SELECT * FROM dane", "sqlite:///poc_database.db")
    return df.to_dict(orient="records")


def read_data():
    df = pd.read_excel("dane.xlsx", engine="openpyxl", header=8)
    df = df.drop(df.columns[0], axis=1)

    with engine.connect() as connection:
        connection.execute(text("DROP TABLE IF EXISTS dane"))
        connection.commit()

    df.to_sql(
        "dane",
        engine,
        if_exists="replace",
        index=False,
    )


@app.get("/dane")
def get_data(kontrahent: str = None):
    query = "SELECT * FROM dane"
    params = {}

    if kontrahent:
        query += " WHERE kontrahent = :kontrahent"
        params["kontrahent"] = kontrahent

    with engine.connect() as connection:
        result = connection.execute(text(query), params)

        return [dict(row._mapping) for row in result]
