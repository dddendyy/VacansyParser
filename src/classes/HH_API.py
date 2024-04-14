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
        with open('data/vacancies.json', 'w', encoding='UTF-8') as file:
            file.write(response.text)
