import pytest
from sqlalchemy import create_engine, text

from backend.services import engine, get_data


@pytest.fixture
def test_database():
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


def test_get_all_data(test_database):
    actual = get_data()

    assert len(actual) == 4


def test_get_data_by_contractor(test_database):
    actual = get_data('Krzysztof Nowak')

    assert len(actual) == 1
    assert actual[0]["kontrahent"] == "Krzysztof Nowak"


def test_get_data_partial_name(test_database):
    actual = get_data('ABC Sp. z o.o.')

    assert len(actual) == 1
    assert actual[0]["kontrahent"] == "ABC Sp. z o.o."


def test_get_data_not_found(test_database):
    actual = get_data("Nieistniejący")

    assert actual == []


def test_get_data_with_filter(test_database):
    actual = get_data('XYZ')

    assert len(actual) == 0