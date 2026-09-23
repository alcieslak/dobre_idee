from sqlalchemy import create_engine, text

from backend.services import engine, get_data


def test_get_data_with_filter():
    with engine.connect() as connection:
        connection.execute(text("DROP TABLE IF EXISTS dane"))
        connection.execute(text("""
            CREATE TABLE dane (
                Kontrahent TEXT,
                telefon TEXT
            )
        """))
        connection.execute(text("""
            INSERT INTO dane (Kontrahent, telefon)
            VALUES
                ('ABC Sp. z o.o.', '123'),
                ('XYZ Jan Kowalski', '456'),
                ('XZ', '456')
        """))
        connection.commit()

    result = get_data('XYZ')

    assert len(result) == 1