Парсер для поиска вакансий на сайте hh.ru у заданных компаний и сохранения их в базу данных.

Список работодателей хранится в файле employers.json в формате словаря, где каждому названию компании соответствует id компании с сайта hh.ru.
Для изменения/добавления списка компаний найдите нужную компанию на сайте hh.ru и скопируйте ее id из url (https://ekaterinburg.hh.ru/employer/{id}), например, у компании "Газпром" url https://ekaterinburg.hh.ru/employer/104628, 
следовательно их id на hh.ru - 104628, а затем скорректируйте словарь в файле employers.json.

Перед началом работы необходимо в репозитории создать файл database.ini и заполнить его по шаблону:

[postgresql]

host=localhost

user=postgres

password=12345

port=5432

Для создания и заполнения базы данных запустите скрипт main.py. 
После запуска скрипта будет создана база данных hh_vacancies на базе PostgreSQL с двумя таблицами - employers и vacancies.
В таблице employers хранится список работодателей - компаний, которые были выбраны в файл employers.json.
В таблице vacancies хранится список найденных вакансий (по умолчанию по 20 у каждого работодателя).
Таблицы связаны полем employer_id.

Для работы с БД создан класс DBManager в файле class.
Класс имеет методы для поиска в БД вакансий, соответствующим заданным условиям:

get_companies_and_vacancies_count()
 — получает список всех компаний и количество вакансий у каждой компании.
 
get_all_vacancies()
 — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
 
get_avg_salary()
 — получает среднюю зарплату по вакансиям.

get_vacancies_with_higher_salary()
 — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
 
get_vacancies_with_keyword()
 — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.

По окончании работы для закрытия коннекта нужно вызвать метод finish_work().