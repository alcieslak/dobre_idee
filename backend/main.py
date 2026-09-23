import pandas as pd
from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

engine = create_engine("sqlite:///poc_database.db")


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
        query += " WHERE kontrahent LIKE :kontrahent"
        params["kontrahent"] = f"%{kontrahent}%"

    with engine.connect() as connection:
        result = connection.execute(text(query), params)

        return [dict(row._mapping) for row in result]


@app.get("/")
def home():
    df = pd.read_sql("SELECT * FROM dane", "sqlite:///poc_database.db")
    return df.to_dict(orient="records")


if __name__ == '__main__':
    read_data()
    print(get_data('Cieślak Krzysztof'))
    get_data('Cieślak Krzysztof')
