from backend.services import read_data, get_data

if __name__ == '__main__':
    read_data()
    print(get_data('Cieślak Krzysztof'))
    get_data('Cieślak Krzysztof')
