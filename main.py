import json
import os

from config import config
from utils import get_hh_data, create_database, save_data_to_database



def main():
    params = config()
    employers = json.load(open(os.path.abspath("employers.json"), 'r', encoding='utf=8'))

    data = get_hh_data(employers)
    create_database('hh_vacancies', params)
    save_data_to_database(employers, data, 'hh_vacancies', params)


if __name__ == '__main__':
    main()
