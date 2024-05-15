import requests
import json
from src.classes.abstract.API_absctract import AbsctractAPI


class HeadHunterAPI(AbsctractAPI):
    """Создаём класс для работы с hh.ru
    С помощью него мы будем подгружать сырой список вакасний
    с api.hh.ru/vacancies, для дальнейшей обработки через класс Vacancy"""

    def __init__(self):
        self.vacancies_url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}

    def load_vacancies(self, keyword, page=0, per_page=20):
        """Получаем список вакансий с помощью библиотеки requests
        в объявлении стоят именованные аргументы page  per_page,
        чтобы задать значение по умолчанию и сделать возможность вывода
        разного количества вакансий"""
        response = requests.get(self.vacancies_url,
                                params={'text': keyword, 'page': page, 'per_page': per_page},
                                headers=self.headers)
        response_json = response.json()['items']
        with open('data/vacancies.json', 'w', encoding='utf-8') as file:
            # запишем JSON-ответ в файл
            file.write(json.dumps(response_json, indent=4))

        return response_json
