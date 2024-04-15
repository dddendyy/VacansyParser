from src.classes.HH_API import HeadHunterAPI
from src.classes.vacancy import Vacancy


if __name__ == '__main__':

    # создаем ЭК класса HeadHunterAPI
    hh_api = HeadHunterAPI()

    # загружаем и сохраняем в файл список сырых вакансий
    json_vacancies = hh_api.load_vacancies()

    # конвертируем данные из .json файла в список ЭК
    vacancies_list = Vacancy.convert_to_object_list(json_vacancies)
