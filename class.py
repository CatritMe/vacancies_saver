import psycopg2


class DBManager:

    def __init__(self, database_name: str, params: dict):
        self.conn = psycopg2.connect(dbname=database_name, **params)

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT e.title, COUNT(*) FROM vacancies JOIN employers as e USING (employer_id)
            GROUP BY e.title""")
            result = cur.fetchall()
            print(result)

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT v.title, e.title, v.salary_from, v.salary_to, v.url
            FROM vacancies as v
            JOIN employers as e USING (employer_id)""")
            result = cur.fetchall()
            print(result)

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT avg((salary_from + salary_to)/2)
            FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL""")
            result = cur.fetchall()
            print(result)

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT * FROM vacancies WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL 
            AND ((salary_from + salary_to)/2) > (SELECT avg((salary_from + salary_to)/2)
            FROM vacancies
            WHERE salary_from IS NOT null AND salary_to IS NOT NULL)""")
            result = cur.fetchall()
            print(result)

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        with self.conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM vacancies
            WHERE title LIKE '%{keyword}%'""")
            result = cur.fetchall()
            print(result)

    def finish_work(self):
        self.conn.close()
