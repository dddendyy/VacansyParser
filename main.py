from src.classes.HH_API import HeadHunterAPI
from src.classes.vacancy import Vacancy
from src.classes.employer import Employer
from src.classes.JSONSaver import JSONSaver
from src.classes.DBManager import DBManager
from src.utils import (print_object_list,
                       print_sorted_by_salary,
                       add_vacancy_to_favorite,
                       delete_vacancy_from_favorite,
                       print_favorite_vacancies,
                       print_n_vacancies,
                       filter_by_keyword)

# создаем ЭК класса DBManager
db_manager = DBManager()

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
                  '7 - посмотреть избранных работодателей\n'
                  '8 - вывести все вакансии по избранным работодателям\n'
                  '0 - завершить работу\n'
                  'Введи одно из чисел выше: ')


if __name__ == '__main__':

    db_manager.create_employers_table()
    db_manager.create_vacancies_table()

    print('Приветствую! Перед тобой программа для парсинга вакансий на HH.ru!')
    print('Хочешь искать вакансии или посмотреть имеющихся работодателей?')
    user_keyword = input('Введи запрос, по которому мы будем искать вакансии: ').strip()

    # бесконечне циклы нужны для постоянного диалога с пользователем
    # + если запросить слишком много, на запрос вернётся 400 ошибка
    while True:
        user_length = int(input('Введи количество вакансий, которое нужно вывести (от 1 до 50): '))
        # проверка на количество, поставил 50, чтобы не выводил слишком много
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
    print_object_list(vacancies_list)

    # снова запускаем цикл для диалога
    while True:

        # запрашиваем у пользователя число, соответствующее одной из функций
        user_input = int(input(user_interface))

        # 1 - вывод вакансий по убыванию зп
        if user_input == 1:
            print_sorted_by_salary(vacancies_list)

        # 2 - добавление вакансии в избранное по ID
        elif user_input == 2:
            add_vacancy_to_favorite(vacancies_list, json_saver)

        # 3 - удаление вакансии из избранного по ID
        elif user_input == 3:
            delete_vacancy_from_favorite(json_saver)

        # 4 - вывод избранных вакансий на экран
        elif user_input == 4:
            print_favorite_vacancies()

        # 5 - вывод топ-N вакансий по зп
        elif user_input == 5:
            print_n_vacancies(vacancies_list)

        # 6 - поиск вакансий по ключевому слову
        elif user_input == 6:
            filter_by_keyword(vacancies_list)

        # 7 - вывод избранныx работодателей
        elif user_input == 7:
            employers = db_manager.get_employers()
            employers_list = Employer.convert_to_object_list(employers)
            print_object_list(employers_list)

        # 8 - вывод всех вакансий по избранным работодателям
        elif user_input == 8:
            db_manager.get_all_vacancies()

        # 9 - получить среднюю зарплату по вакансиям избранных работодателей
        elif user_input == 9:
            print('Среднюю зарплату можно получить только по одной валюте\n')
            user_currency = input('Введи валюту: ').upper() # проверяю на валюту
            average_salary = db_manager.get_average_salary(user_currency) # правда, в моем случае, не сильно актуально
            # т.к. все вакансии с RUR и если указать что-то, кроме RUR , будет None
            print(f'Средняя зарплату по вакансиям избранных работодателей составляет: {average_salary} {user_currency}')

        elif user_input == 10:
            pass

        # 0 - чтобы завершить работу
        elif user_input == 0:
            print('Работа завершена')
            break

        # если введено что-то не то, говорим, что пользователь ошибся
        else:
            print('Неизвестное значение! Введи число от 1 до 5!')
