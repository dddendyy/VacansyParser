import requests
import json
from src.classes.abstract.API_absctract import AbsctractAPI


class HeadHunterAPI(AbsctractAPI):
    """Создаём класс для работы с hh.ru
    С помощью него мы будем подгружать сырой список вакасний
    с api.hh.ru/vacancies, для дальнейшей обработки через класс Vacancy"""

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'

    def load_vacancies(self):
        """Получаем список вакансий с помощью библиотеки requests"""
        response = requests.get(self.url)
        with open('data/vacancies.json', 'w', encoding='utf-8') as file:
            # запишем JSON-ответ в файл
            file.write(response.text)

        with open('data/vacancies.json', 'r', encoding='utf-8') as file:
            # возвращаем словарь для работы с вакансиями
            response_json = json.load(file)

        return response_json
