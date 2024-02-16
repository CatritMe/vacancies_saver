from typing import Any

import requests
import psycopg2


def get_hh_data(employers: dict):
    """Получает данные с сайта hh.ru"""
    data = []
    for key, item in employers.items():
        vacancies_hh = requests.get('https://api.hh.ru/vacancies', params={'employer_id': item}).json()
        vacancies_list = vacancies_hh['items']
        for i in range(0, len(vacancies_list)):
            data.append(vacancies_list[i])
    return data


def create_database(database_name: str, params: dict):
    """Создание базы данных"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id int PRIMARY KEY,
                title varchar(30) NOT NULL
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id serial PRIMARY KEY,
                employer_id int REFERENCES employers(employer_id),
                title varchar NOT NULL,
                city varchar,
                salary_from int DEFAULT NULL,
                salary_to int DEFAULT NULL,
                url text,
                requirement text
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(employers, data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохраняет данные с сайта в созданную БД"""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for key, item in employers.items():
            cur.execute("""
                INSERT INTO employers (employer_id, title) 
                VALUES (%s, %s)""", (item, key)
                        )
        for vac in data:
            try:
                salary_from = int(vac['salary']['from'])
            except TypeError:
                salary_from = None

            try:
                salary_to = int(vac['salary']['to'])
            except TypeError:
                salary_to = None
            cur.execute("""
            INSERT INTO vacancies (employer_id, title, city, salary_from, salary_to, url, requirement)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                        (vac['employer']['id'], vac['name'], vac['area']['name'], salary_from,
                            salary_to, vac['url'], vac['snippet']['requirement'])
                        )

    conn.commit()
    conn.close()
