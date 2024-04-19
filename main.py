from src.classes.HH_API import HeadHunterAPI
from src.classes.vacancy import Vacancy
from src.classes.JSONSaver import JSONSaver


def salary_comp(salary_1: Vacancy, salary_2: Vacancy):
    """Функция для сравнения вакансий и отображения результата пользователю в консоль"""
    if salary_1 > salary_2:
        print(f'Зарплата у вакансии {salary_1.name} с ID: {salary_1.vacancie_id} больше')
    elif salary_1 == salary_2:
        print(f'У обеих вакансий зарплаты равны')
    else:
        print(f'Зарплата у вакансии {salary_2.name} с ID: {salary_2.vacancie_id} больше')


if __name__ == '__main__':

    # создаем ЭК класса HeadHunterAPI
    hh_api = HeadHunterAPI()

    # загружаем и сохраняем в файл список сырых вакансий
    json_vacancies = hh_api.load_vacancies('Python')

    # конвертируем данные из .json файла в список ЭК
    vacancies_list = Vacancy.convert_to_object_list(json_vacancies)

    vacancy = Vacancy(123123, 'Python-разработчик', 0, 140_000, 'RUR', '///', '', '')
    vacancy_2 = Vacancy(123122, 'C#-разработчик', 0, 140_000, 'RUR', '///', '', '')
    json_saver = JSONSaver()
