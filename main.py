from src.classes.HH_API import HeadHunterAPI
from src.classes.vacancy import Vacancy
from src.classes.JSONSaver import JSONSaver
from src.utils import (print_vacancies,
                       print_sorted_by_salary,
                       add_vacancy_to_favorite,
                       delete_vacancy_from_favorite,
                       print_favorite_vacancies,
                       print_n_vacancies,
                       filter_by_keyword)
# создаем ЭК класса HeadHunterAPI
hh_api = HeadHunterAPI()

# создаем ЭК класса для работы с JSON файлом
json_saver = JSONSaver()

keyword_vacancies = []

user_interface = ('1 - сортировка по убыванию зарплат\n'
                  '2 - добавить вакансию в избранное (по ID)\n'
                  '3 - удалить вакансию из избранного (по ID)\n'
                  '4 - вывести избранные вакансии\n'
                  '5 - вывод топ-N вакансий по зарплате\n'
                  '6 - сортировка по ключевому слову\n'
                  '0 - завершить работу\n'
                  'Введи одно из чисел выше: ')


if __name__ == '__main__':

    print('Приветствую! Перед тобой программа для парсинга вакансий на HH.ru!')
    user_keyword = input('Введи запрос, по которому мы будем искать вакансии: ').strip()

    while True:
        user_length = int(input('Введи количество вакансий, которое нужно вывести (от 1 до 50): '))
        if user_length not in range(1, 51):
            print('Обрати внимание, что нужно ввести число от 1 до 50')
            continue
        break

    while True:
        user_page = int(input('Введи страницу, с которой начнем просматривать вакансии (от 0 до 20): '))
        if user_page not in range(0, 21):
            print('Обрати внимание, что нужно ввести число от 0 до 20')
            continue
        break

    # загружаем и сохраняем в файл список сырых вакансий
    json_vacancies = hh_api.load_vacancies(user_keyword, page=user_page, per_page=user_length)

    # конвертируем данные из .json файла в список ЭК
    vacancies_list = Vacancy.convert_to_object_list(json_vacancies)

    # выводим полученные вакансии
    print_vacancies(vacancies_list)

    while True:

        user_input = int(input(user_interface))

        if user_input == 1:
            print_sorted_by_salary(vacancies_list)

        elif user_input == 2:
            add_vacancy_to_favorite(vacancies_list, json_saver)

        elif user_input == 3:
            delete_vacancy_from_favorite(json_saver)

        elif user_input == 4:
            print_favorite_vacancies()

        elif user_input == 5:
            print_n_vacancies(vacancies_list)

        elif user_input == 6:
            filter_by_keyword(vacancies_list)

        elif user_input == 0:
            print('Работа завершена')
            break

        else:
            print('Неизвестное значение! Введи число от 1 до 5!')
