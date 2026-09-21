# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
from sqlalchemy import create_engine
from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

engine = create_engine("sqlite:///poc_database.db")


def read_data():
    df = pd.read_excel("dane.xlsx", engine="openpyxl")

    df.to_sql(
        "dane",
        engine,
        if_exists="append",
        index=False
    )


@app.get("/dane")
def get_data(kontrahent: str = None):
    query = "SELECT * FROM dane"
    params = {}

    if kontrahent:
        query += " WHERE kontrahent LIKE :kontrahent"
        params["kontrahent"] = f"%{kontrahent}%"

    with engine.connect() as connection:
        result = connection.execute(text(query), params)

        return [dict(row._mapping) for row in result]


@app.get("/")
def home():
    df = pd.read_sql("SELECT * FROM dane", "sqlite:///poc_database.db")
    return df.to_dict(orient="records")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_data()
    home()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
