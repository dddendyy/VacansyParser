import psycopg2


class DBManager:
    """Класс для работы с БД"""

    # def __init__(self):
    #     self.dbname = 'head_hunter',
    #     self.user = 'postgres',
    #     self.password = '123',
    #     self.host = 'localhost',
    #     self.port = 5432

    @staticmethod
    def create_employers_table():
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
                                "employer_id serial PRIMARY KEY, "
                                "name varchar(50), "
                                "open_vacancies int, "
                                "url text)")
        finally:
            conn.close()

    @staticmethod
    def create_vacancies_table():
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
                                "vacancy_id serial PRIMARY KEY, "
                                "name varchar(50), "
                                "salary_from int, "
                                "salary_to int, "
                                "currency varchar(3),"
                                "employer_id int REFERENCES employers(employer_id), "
                                "url text, "
                                "responsibility text, "
                                "requirement text)")
        finally:
            conn.close()

