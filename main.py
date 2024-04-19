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

    vacancy = Vacancy(123123, 'Python-разработчик', 100_000, 150_000, 'RUR', '///', '', '')
    vacancy_2 = Vacancy(123122, 'C#-разработчик', 100_000, 150_000, 'RUR', '///', '', '')

    json_saver = JSONSaver()
    # json_saver.add_vacancy(vacancy)
    # json_saver.add_vacancy(vacancy_2)
    json_saver.delete_vacancy(vacancy)
