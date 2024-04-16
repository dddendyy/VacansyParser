from src.classes.HH_API import HeadHunterAPI
from src.classes.vacancy import Vacancy
from src.classes.JSONSaver import JSONSaver

if __name__ == '__main__':

    # создаем ЭК класса HeadHunterAPI
    hh_api = HeadHunterAPI()

    # загружаем и сохраняем в файл список сырых вакансий
    json_vacancies = hh_api.load_vacancies('Python')

    # конвертируем данные из .json файла в список ЭК
    vacancies_list = Vacancy.convert_to_object_list(json_vacancies)

    vacancy = Vacancy('Python-разработчик', 100_000, 150_000, 'RUR', '///', '', '')

    json_saver = JSONSaver()
