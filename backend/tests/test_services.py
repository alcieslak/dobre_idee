import pandas as pd
import pytest
from sqlalchemy import create_engine, text

from backend.services import engine, find_customer, initialize_database


@pytest.fixture
def init():
    with engine.connect() as connection:
        connection.execute(text("DROP TABLE IF EXISTS dane"))
        connection.execute(text("""
            CREATE TABLE dane (
                kontrahent TEXT,
                telefon TEXT
            )
        """))
        connection.execute(text("""
            INSERT INTO dane (kontrahent, telefon)
            VALUES
                ('ABC Sp. z o.o.', '123'),
                ('XYZ Jan Kowalski', '456'),
                ('Krzysztof Nowak', '111'),
                ('XZ', '456')
        """))
        connection.commit()


def test_initialize_database_creates_table():
    df = pd.DataFrame({
        "do_usuniecia": ["x", "y"],
        "kontrahent": ["Anna", "Jan"],
        "telefon": ["123", "456"]
    })

    initialize_database(df)

    with engine.connect() as connection:
        actual = connection.execute(text("PRAGMA table_info(dane)"))
        columns = [row[1] for row in actual]

    assert columns == ["kontrahent", "telefon"]


def test_get_all_data(init):
    actual = find_customer()

    assert len(actual) == 4


def test_get_data_by_contractor(init):
    actual = find_customer('Krzysztof Nowak')

    assert len(actual) == 1
    assert actual[0]["kontrahent"] == "Krzysztof Nowak"


def test_get_data_partial_name(init):
    actual = find_customer('ABC Sp. z o.o.')

    assert len(actual) == 1
    assert actual[0]["kontrahent"] == "ABC Sp. z o.o."


def test_get_data_not_found(init):
    actual = find_customer("Nieistniejący")

    assert actual == []


def test_get_data_with_filter(init):
    actual = find_customer('XYZ')
    assert actual[0]["kontrahent"] == "XYZ Jan Kowalski"
    assert len(actual) == 1
