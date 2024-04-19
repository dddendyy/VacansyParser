import json
from src.classes.abstract.JSONSaver_abstract import AbstractJSONSaver


class JSONSaver(AbstractJSONSaver):
    """Класс для работы с JSON файлом вакансий
    Если конкретнее, то для добавления и удаления вакансий"""
    def add_vacancy(self, vacancy):
        with open('data/favorite_vacancies.json', 'r', encoding='utf-8') as file:
            try:
                # если что-то есть, то просто считываем JSON-файл
                result = json.load(file)
            except json.decoder.JSONDecodeError:
                # если ничего нет, то упадёт исключение
                # результату присваиваем пустой список
                result = []

        with open('data/favorite_vacancies.json', 'w', encoding='utf-8') as file:
            # тут уже просто добавляем к результату нашу вакансию и записываем в файл
            result.append(vacancy.__dict__)
            file.write(json.dumps(result))

    def delete_vacancy(self, vacancy):
        with open('data/favorite_vacancies.json', 'r', encoding='utf-8') as file:
            try:
                # если в файле что-то есть, считываем его
                result = json.load(file)
            except json.decoder.JSONDecodeError:
                # если он пуст, выкидываем исключение
                raise TypeError('Список избранных вакансий пуст!')

        with open('data/favorite_vacancies.json', 'w', encoding='utf-8') as file:
            for i in range(len(result)):
                # ищем вакансию с нужным нам id и удаляем её
                if result[i]['vacancie_id'] == vacancy.vacancie_id:
                    del result[i]
                    break

            file.write(json.dumps(result))
