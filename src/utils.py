import json

from src.classes.vacancy import Vacancy
from src.classes.JSONSaver import JSONSaver


def get_favorite_vacancies():
    with open('data/favorite_vacancies.json') as file:
        json_favorite_vacancies = json.load(file)
    favorite_vacancies = Vacancy.favorite_to_object_list(json_favorite_vacancies)
    return favorite_vacancies


favorite_vacancies_list = get_favorite_vacancies()


def print_vacancies(vacancies):
    """Функция для вывода вакансий на экран"""
    for vacancy in vacancies:
        print(vacancy)
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
    currency_vacancies = [vacancy for vacancy in vacancies if vacancy.currency == currency]
    print('--------------------------------------------------------\n')
    currency_vacancies = sorted(currency_vacancies)
    for vacancy in currency_vacancies[::-1]:
        print(vacancy)
        print('--------------------------------------------------------\n')


def add_vacancy_to_favorite(vacancies, saver: JSONSaver):
    """Функция для добавления вакансии в избранное по ID"""
    vacancie_id = input('Введи ID вакансии, которую хочешь добавить в избранное: ')
    for vacancy in vacancies:
        if vacancy.vacancie_id == vacancie_id:
            saver.add_vacancy(vacancy)
            favorite_vacancies_list.append(vacancy)
            print('Вакансия добавлена в избранное')
            break


def delete_vacancy_from_favorite(saver: JSONSaver):
    """Функция для удаления вакансии из избранного по ID"""
    vacancie_id = input('Введи ID вакансии, которую хочешь удалить из избранного: ')
    for i in range(len(favorite_vacancies_list)):
        if favorite_vacancies_list[i].vacancie_id == vacancie_id:
            saver.delete_vacancy(favorite_vacancies_list[i])
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
    while True:
        if n > len(currency_vacancies):
            print('Введено число большее, чем количество вакансий!')
            continue
        break
    print('--------------------------------------------------------\n')
    for vacancy in sorted(currency_vacancies[-n::], reverse=True):
        print(vacancy)
        print('--------------------------------------------------------\n')
