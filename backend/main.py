from backend.services import find_customer, read_excel_data, initialize_database

if __name__ == '__main__':
    df = read_excel_data()
    initialize_database(df)
    find_customer('Cieślak Krzysztof')
