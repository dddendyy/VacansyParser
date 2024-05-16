import psycopg2
import requests
from src.classes.vacancy import Vacancy


class DBManager:
    """Класс для работы с БД"""

    @staticmethod
    def create_employers_table():
        """Метод для создания таблицы работодайтелей"""
        conn = psycopg2.connect(
            host='localhost',
            database='head_hunter',
            user='postgres',
            password='123'
        )
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("CREATE TABLE IF NOT EXISTS employers("
                                "employer_id varchar(10) PRIMARY KEY, "
                                "name varchar(50), "
                                "open_vacancies int, "
                                "url text)")
        finally:
            conn.close()

    @staticmethod
    def create_vacancies_table():
        """Метод для создания таблицы вакансий"""
        conn = psycopg2.connect(
            host='localhost',
            database='head_hunter',
            user='postgres',
            password='123'
        )
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("CREATE TABLE IF NOT EXISTS vacancies("
                                "vacancy_id varchar(10) PRIMARY KEY, "
                                "name text, "
                                "salary_from int, "
                                "salary_to int, "
                                "currency varchar(3),"
                                "employer_id varchar(10) REFERENCES employers(employer_id), "
                                "url text, "
                                "responsibility text, "
                                "requirement text)")
        finally:
            conn.close()

    @staticmethod
    def get_employers():
        """Метод для получения записей по работодателям из БД"""
        conn = psycopg2.connect(
            host='localhost',
            database='head_hunter',
            user='postgres',
            password='123'
        )
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM employers;")
                    result = cur.fetchall()
        finally:
            conn.close()

        return result

    @staticmethod
    def get_all_vacancies():
        """Метод, который получает все вакансии по избранным работодателям
        и добавляет их в БД"""
        conn = psycopg2.connect(
            host='localhost',
            database='head_hunter',
            user='postgres',
            password='123'
        )
        try:
            with conn:
                with conn.cursor() as cur:
                    # получил все ID работодателей, чтобы итерироваться по ним
                    cur.execute("SELECT employer_id FROM employers;")
                    result = cur.fetchall()
                    # запускаем цикл
                    for employer_id in result:
                        # формируем ссылку для запроса через конкатенацию строк
                        request = 'https://api.hh.ru/vacancies/?employer_id=' + str(employer_id[0])
                        response = requests.get(request)
                        # преобразуем ответ в json по ключу items для дальнейшей итерации по нему
                        response_json = response.json()['items']
                        Vacancy.vacancies_list = []  # в списке уже хранятся данные, надо занулить его
                        # полученные вакансии конвертим в список ЭК и запускаем итерацию по нему
                        vacancies_list = Vacancy.convert_to_object_list(response_json)
                        for vacancy in vacancies_list:
                            if vacancy.salary_to == 0 and vacancy.salary_from == 0:  # проверяем указана ли зп
                                cur.execute("INSERT INTO vacancies VALUES(%s, %s, NULL, NULL, NULL, %s, %s, %s, %s) "
                                            "ON CONFLICT DO NOTHING",  # при возникновении ошибки в запросе ничего не делаем
                                            (vacancy.vacancie_id,
                                             vacancy.name,
                                             vacancy.employer_id,
                                             vacancy.url,
                                             vacancy.responsibility,
                                             vacancy.requirements))

                            elif vacancy.salary_from is None and vacancy.salary_to is not None:
                                cur.execute("INSERT INTO vacancies VALUES(%s, %s, NULL, %s, %s, %s, %s, %s, %s) "
                                            "ON CONFLICT DO NOTHING",
                                            (vacancy.vacancie_id,
                                             vacancy.name,
                                             vacancy.salary_to,
                                             vacancy.currency,
                                             vacancy.employer_id,
                                             vacancy.url,
                                             vacancy.responsibility,
                                             vacancy.requirements))

                            elif vacancy.salary_from is not None and vacancy.salary_to is None:
                                cur.execute("INSERT INTO vacancies VALUES(%s, %s, %s, NULL, %s, %s, %s, %s, %s) "
                                            "ON CONFLICT DO NOTHING",
                                            (vacancy.vacancie_id,
                                             vacancy.name,
                                             vacancy.salary_from,
                                             vacancy.currency,
                                             vacancy.employer_id,
                                             vacancy.url,
                                             vacancy.responsibility,
                                             vacancy.requirements))

                            else:
                                cur.execute("INSERT INTO vacancies VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) "
                                            "ON CONFLICT DO NOTHING",
                                            (vacancy.vacancie_id,
                                             vacancy.name,
                                             vacancy.salary_from,
                                             vacancy.salary_to,
                                             vacancy.currency,
                                             vacancy.employer_id,
                                             vacancy.url,
                                             vacancy.responsibility,
                                             vacancy.requirements))

                        # в классе вакансий добавлен только id работодателя, поэтому для вывода
                        # с названием использовал JOIN, знаю, что это лишнее действие, хочу
                        # продемонстрировать, что могу работать с JOIN'ами  :)
                        cur.execute("SELECT * FROM vacancies JOIN employers USING (employer_id)")
                        result = cur.fetchall()
                        for i in result:
                            if i[3] == 0 and i[4] == 0:
                                print(f"ID вакансии: {i[1]}\n"
                                      f"Название вакаснии: {i[2]}\n"
                                      f"Название работодателя: {i[9]}\n"
                                      f"Зарплата не указана\n"
                                      f"URL: {i[6]}"
                                      f"Требования: {i[8]}"
                                      f"Обязанности: {i[7]}")
                                print('--------------------------------------------------------\n')
                            elif i[3] != 0 and i[4] == 0:
                                print(f"ID вакансии: {i[1]}\n"
                                      f"Название вакансии: {i[2]}\n"
                                      f"Название работодателя: {i[9]}\n"
                                      f"Зарплата от {i[3]}\n"
                                      f"URL: {i[6]}\n"
                                      f"Требования: {i[8]}\n"
                                      f"Обязанности: {i[7]}\n")
                                print('--------------------------------------------------------\n')
                            elif i[3] == 0 and i[4] != 0:
                                print(f"ID вакансии: {i[1]}\n"
                                      f"Название вакансии: {i[2]}\n"
                                      f"Название работодателя: {i[9]}\n"
                                      f"Зарплата до {i[4]}\n"
                                      f"URL: {i[6]}\n"
                                      f"Требования: {i[8]}\n"
                                      f"Обязанности: {i[7]}\n")
                                print('--------------------------------------------------------\n')
                            else:
                                print(f"ID вакансии: {i[1]}\n"
                                      f"Название вакансии: {i[2]}\n"
                                      f"Название работодателя: {i[9]}\n"
                                      f"Зарплата: {i[3]} - {i[4]}\n"
                                      f"URL: {i[6]}\n"
                                      f"Требования: {i[8]}\n"
                                      f"Обязанности: {i[7]}\n")
                                print('--------------------------------------------------------\n')
        finally:
            conn.close()

    @staticmethod
    def get_average_salary(currency):
        """Метод для получения средней зарплаты"""
        conn = psycopg2.connect(
            host='localhost',
            database='head_hunter',
            user='postgres',
            password='123'
        )
        try:
            with conn:
                with conn.cursor() as cur:
                    # здесь просто получаем среднюю зарпалту из таблица
                    cur.execute("SELECT AVG(salary_to) FROM vacancies WHERE currency = %s;", (currency, ))
                    average_salary = cur.fetchone()[0]
        finally:
            conn.close()

        return int(average_salary)  # запрос возвращает decimal, нас это не устраивает и мы конвертир в int

    @staticmethod
    def get_overprice_vacancies(average_price, currency):
        """Получаем все вакансии, где зарплата выше средней"""
        conn = psycopg2.connect(
            host='localhost',
            database='head_hunter',
            user='postgres',
            password='123'
        )
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM vacancies JOIN employers USING (employer_id) WHERE salary_to > %s OR salary_to = 0 AND currency = %s;",
                                (average_price, currency))
                    result = cur.fetchall()
                    for i in result:
                        if i[3] == 0 and i[4] == 0:
                            print(f"ID вакансии: {i[1]}\n"
                                  f"Название вакаснии: {i[2]}\n"
                                  f"Название работодателя: {i[9]}\n"
                                  f"Зарплата не указана\n"
                                  f"URL: {i[6]}"
                                  f"Требования: {i[8]}"
                                  f"Обязанности: {i[7]}")
                            print('--------------------------------------------------------\n')
                        elif i[3] != 0 and i[4] == 0:
                            print(f"ID вакансии: {i[1]}\n"
                                  f"Название вакансии: {i[2]}\n"
                                  f"Название работодателя: {i[9]}\n"
                                  f"Зарплата от {i[3]}\n"
                                  f"URL: {i[6]}\n"
                                  f"Требования: {i[8]}\n"
                                  f"Обязанности: {i[7]}\n")
                            print('--------------------------------------------------------\n')
                        elif i[3] == 0 and i[4] != 0:
                            print(f"ID вакансии: {i[1]}\n"
                                  f"Название вакансии: {i[2]}\n"
                                  f"Название работодателя: {i[9]}\n"
                                  f"Зарплата до {i[4]}\n"
                                  f"URL: {i[6]}\n"
                                  f"Требования: {i[8]}\n"
                                  f"Обязанности: {i[7]}\n")
                            print('--------------------------------------------------------\n')
                        else:
                            print(f"ID вакансии: {i[1]}\n"
                                  f"Название вакансии: {i[2]}\n"
                                  f"Название работодателя: {i[9]}\n"
                                  f"Зарплата: {i[3]} - {i[4]}\n"
                                  f"URL: {i[6]}\n"
                                  f"Требования: {i[8]}\n"
                                  f"Обязанности: {i[7]}\n")
                            print('--------------------------------------------------------\n')
        finally:
            conn.close()

    @staticmethod
    def get_vacancies_by_keyword(keyword):
        """Получаем все вакансии, где зарплата выше средней"""
        conn = psycopg2.connect(
            host='localhost',
            database='head_hunter',
            user='postgres',
            password='123'
        )
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM vacancies JOIN employers USING(employer_id)"
                        " WHERE vacancies.name LIKE %s OR responsibility LIKE %s OR requirement LIKE %s",
                        (keyword, keyword, keyword))
                    result = cur.fetchall()
                    for i in result:
                        if i[3] == 0 and i[4] == 0:
                            print(f"ID вакансии: {i[1]}\n"
                                  f"Название вакаснии: {i[2]}\n"
                                  f"Название работодателя: {i[9]}\n"
                                  f"Зарплата не указана\n"
                                  f"URL: {i[6]}"
                                  f"Требования: {i[8]}"
                                  f"Обязанности: {i[7]}")
                            print('--------------------------------------------------------\n')
                        elif i[3] != 0 and i[4] == 0:
                            print(f"ID вакансии: {i[1]}\n"
                                  f"Название вакансии: {i[2]}\n"
                                  f"Название работодателя: {i[9]}\n"
                                  f"Зарплата от {i[3]}\n"
                                  f"URL: {i[6]}\n"
                                  f"Требования: {i[8]}\n"
                                  f"Обязанности: {i[7]}\n")
                            print('--------------------------------------------------------\n')
                        elif i[3] == 0 and i[4] != 0:
                            print(f"ID вакансии: {i[1]}\n"
                                  f"Название вакансии: {i[2]}\n"
                                  f"Название работодателя: {i[9]}\n"
                                  f"Зарплата до {i[4]}\n"
                                  f"URL: {i[6]}\n"
                                  f"Требования: {i[8]}\n"
                                  f"Обязанности: {i[7]}\n")
                            print('--------------------------------------------------------\n')
                        else:
                            print(f"ID вакансии: {i[1]}\n"
                                  f"Название вакансии: {i[2]}\n"
                                  f"Название работодателя: {i[9]}\n"
                                  f"Зарплата: {i[3]} - {i[4]}\n"
                                  f"URL: {i[6]}\n"
                                  f"Требования: {i[8]}\n"
                                  f"Обязанности: {i[7]}\n")
                            print('--------------------------------------------------------\n')
        finally:
            conn.close()
