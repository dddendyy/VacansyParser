import json

from src.classes.vacancy import Vacancy
from src.classes.JSONSaver import JSONSaver


def get_favorite_vacancies():
    """Метод для получения списка избранных вакансий"""
    with open('data/favorite_vacancies.json') as file:
        # считываем файл
        json_favorite_vacancies = json.load(file)
    # конвертируем в список
    favorite_vacancies = Vacancy.favorite_to_object_list(json_favorite_vacancies)
    return favorite_vacancies


favorite_vacancies_list = get_favorite_vacancies()


def print_object_list(object_list):
    """Функция для вывода классовой структуры на экран
    P.S. Работает только при реализованно __str__"""
    for element in object_list:
        print(element)
        print('--------------------------------------------------------\n')


def print_sorted_by_salary(vacancies):
    """Функция для вывода вакансий по убыванию зарплат"""
    print('Логика сравнения следующая:\n'
          '1. зарплата, у которой не указана верхняя вилка считается большей;\n'
          '2. если у обеих вакансий указаны только нижние вилки, то сравниваются они;\n'
          '3. если у обеих вакансий указаны верхние вилки, сравниваются они;\n'
          '4. если у одной указана нижняя вилка и не указана верхняя вилка,'
          ' а у второй указана верхняя вилка и не указана нижняя вилка,'
          ' то больше считается та, у которой не указана верхняя вилка\n'
          '5. вакансии с неуказанной зарплатой выводиться не будут')
    currency = input('Введи валюту, по которой будет сортировать зарплату: ')
    # через генератор делаем список, в котором лежат вакансии с указанной валютой
    currency_vacancies = [vacancy for vacancy in vacancies if vacancy.currency == currency]
    print('--------------------------------------------------------\n')
    currency_vacancies = sorted(currency_vacancies)
    # выводим всё в обратном порядке
    for vacancy in currency_vacancies[::-1]:
        print(vacancy)
        print('--------------------------------------------------------\n')


def add_vacancy_to_favorite(vacancies, saver: JSONSaver):
    """Функция для добавления вакансии в избранное по ID"""
    vacancie_id = input('Введи ID вакансии, которую хочешь добавить в избранное: ')
    for vacancy in vacancies:
        # проходимся по списку и ищем вакансию с нужным ID
        if vacancy.vacancie_id == vacancie_id:
            # после чего добавляем её в файл
            saver.add_vacancy(vacancy)
            # но в файл добавить мало, надо ещё добавить в список
            favorite_vacancies_list.append(vacancy)
            print('Вакансия добавлена в избранное')
            break


def delete_vacancy_from_favorite(saver: JSONSaver):
    """Функция для удаления вакансии из избранного по ID"""
    vacancie_id = input('Введи ID вакансии, которую хочешь удалить из избранного: ')
    for i in range(len(favorite_vacancies_list)):
        # схема аналогична методу добавления, но тут итерируемся не по
        # содержимому списка, а по индексам, чтобы потом спокойно по нему удалить
        if favorite_vacancies_list[i].vacancie_id == vacancie_id:
            saver.delete_vacancy(favorite_vacancies_list[i])
            # удаляем и из файла и из списка
            del favorite_vacancies_list[i]
            print('Вакансия удалена из избранного')
            break


def print_favorite_vacancies():
    """Функция для вывода избранных вакансий на экран"""
    print('--------------------------------------------------------\n')
    for vacancy in favorite_vacancies_list:
        print(vacancy)
        print('--------------------------------------------------------\n')


def print_n_vacancies(vacancies):
    """Метод, который выводит топ-N вакансий по убыванию зарплаты.
    Тоже самое. что и с сортировкой по зарплате, только со срезом"""
    currency = input('Введи валюту, по которой будет сортировать зарплату: ')
    currency_vacancies = [vacancy for vacancy in vacancies if vacancy.currency == currency]
    n = int(input(f'Введи количество выводимых вакансий (1 - {len(currency_vacancies)}): '))
    print('Логика сравнения следующая:\n'
          '1. зарплата, у которой не указана верхняя вилка считается большей;\n'
          '2. если у обеих вакансий указаны только нижние вилки, то сравниваются они;\n'
          '3. если у обеих вакансий указаны верхние вилки, сравниваются они;\n'
          '4. если у одной указана нижняя вилка и не указана верхняя вилка,'
          ' а у второй указана верхняя вилка и не указана нижняя вилка,'
          ' то больше считается та, у которой не указана верхняя вилка\n'
          '5. вакансии с неуказанной зарплатой выводиться не будут')
    # бесконечный цикл нужен для диалога с пользователем
    while True:
        if n > len(currency_vacancies):
            print('Введено число большее, чем количество вакансий!')
            continue
        break
    print('--------------------------------------------------------\n')
    for vacancy in sorted(currency_vacancies[-n::], reverse=True):
        print(vacancy)
        print('--------------------------------------------------------\n')


def filter_by_keyword(vacancies):
    """Функция фильтрации по ключевому слову,
    которое будет искаться в имени, требованиях и обязанностях"""
    keyword = input('Введи ключевое слово (фразу) по которому(-ой) будем искать вакансии\n'
                    'Искать будем в названии вакансии, требованиях и обязанностях: ')
    print('--------------------------------------------------------\n')
    for vacancy in vacancies:
        try:
            # просто ищем совпадения через in
            if (keyword in vacancy.name or
                    keyword in vacancy.requirements or
                    keyword in vacancy.responsibility):
                print(vacancy)
        except TypeError:
            print('К сожалению, ничего не найдено :(')
