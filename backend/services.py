from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine("sqlite:///poc_database.db")


def read_excel_data():
    return pd.read_excel(
        "dane.xlsx",
        engine="openpyxl",
        header=8
    )


def initialize_database(df):
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


def find_customer(kontrahent: str = None):
    query = "SELECT * FROM dane"
    params = {}

    if kontrahent:
        query += " WHERE kontrahent LIKE :kontrahent"
        params["kontrahent"] = f"%{kontrahent}%"

    with engine.connect() as connection:
        result = connection.execute(text(query), params)

        return [dict(row._mapping) for row in result]
