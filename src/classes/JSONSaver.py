from src.classes.abstract.JSONSaver_abstract import AbstractJSONSaver


class JSONSaver(AbstractJSONSaver):
    """Класс для работы с JSON файлом вакансий
    Если конкретнее, то для добавления и удаления вакансий"""

    def add_vacancy(self, vacancy=''):
        with open('data/vacancies.json', 'w', encoding='utf-8') as file:
            pass

    def delete_vacancy(self, vacancy):
        with open('data/vacancies.json', 'w', encoding='utf-8') as file:
            pass
