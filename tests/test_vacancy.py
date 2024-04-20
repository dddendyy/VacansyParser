import pytest
from src.classes.vacancy import Vacancy


@pytest.fixture()
def python_vacancy():
    return Vacancy('123123',
                   'Python-разработчик',
                   100_000,
                   150_000,
                   'RUR',
                   'https://hh.ru/vacancy/123123',
                   'Системное мышление',
                   'Просто кайфуй')


@pytest.fixture()
def golang_vacancy():
    return Vacancy('1234566',
                   'GO-разработчик',
                   0,
                   280_000,
                   'RUR',
                   'https://hh.ru/vacancy/1234566',
                   'Гоу? Куда?',
                   'Быть умницей!')


@pytest.fixture()
def c_sharp_vacancy():
    return Vacancy('567483',
                   'C#-разработчик',
                   100_000,
                   0,
                   'RUR',
                   'https://hh.ru/vacancy/567483',
                   'Очень системное мышление',
                   'Работать!')


@pytest.fixture()
def devops_vacancy():
    return Vacancy('11111',
                   'DevOps-инженер',
                   0,
                   0,
                   'RUR',
                   'https://hh.ru/vacancy/11111',
                   'Пока что я не знаю, что такое девопс :(',
                   'Узнавать новое!')


@pytest.fixture()
def vacancies():
    return dict()


def test_vacancy_init(python_vacancy):
    assert python_vacancy.vacancie_id == '123123'
    assert python_vacancy.name == 'Python-разработчик'
    assert python_vacancy.salary_from == 100_000
    assert python_vacancy.salary_to == 150_000
    assert python_vacancy.currency == 'RUR'
    assert python_vacancy.url == 'https://hh.ru/vacancy/123123'
    assert python_vacancy.requirements == 'Системное мышление'
    assert python_vacancy.responsibility == 'Просто кайфуй'


def test_vacancies_comparsion(python_vacancy, c_sharp_vacancy, golang_vacancy, devops_vacancy):
    assert not python_vacancy > golang_vacancy
    assert golang_vacancy > python_vacancy
    assert not golang_vacancy > c_sharp_vacancy
    assert c_sharp_vacancy > golang_vacancy
    with pytest.raises(TypeError, match='У одной из вакансий не указана зарплата'):
        assert devops_vacancy > golang_vacancy
    with pytest.raises(TypeError, match='Можно сравнивать только ЭК класса вакансии'):
        assert golang_vacancy > 150


def test_golang_str(golang_vacancy):
    assert golang_vacancy.__str__() == ("ID вакансии: 1234566, название: GO-разработчик\n"
                                        "Зарплата: до 280000 RUR\n"
                                        "Требования: Гоу? Куда?\n"
                                        "Обязанности: Быть умницей!\n"
                                        "Ссылка: https://hh.ru/vacancy/1234566\n")


def test_pythonc_str(python_vacancy):
    assert python_vacancy.__str__() == ("ID вакансии: 123123, название: Python-разработчик\n"
                                        "Зарплата: 100000 - 150000 RUR\n"
                                        "Требования: Системное мышление\n"
                                        "Обязанности: Просто кайфуй\n"
                                        "Ссылка: https://hh.ru/vacancy/123123\n")


def test_devops_str(devops_vacancy):
    assert devops_vacancy.__str__() == ("ID вакансии: 11111, название: DevOps-инженер\n"
                                        "Зарплата: не указана\n"
                                        "Требования: Пока что я не знаю, что такое девопс :(\n"
                                        "Обязанности: Узнавать новое!\n"
                                        "Ссылка: https://hh.ru/vacancy/11111\n")


def test_c_sharp_str(c_sharp_vacancy):
    assert c_sharp_vacancy.__str__() == ("ID вакансии: 567483, название: C#-разработчик\n"
                                         "Зарплата: от 100000 RUR\n"
                                         "Требования: Очень системное мышление\n"
                                         "Обязанности: Работать!\n"
                                         "Ссылка: https://hh.ru/vacancy/567483\n")


def test_convert_to_object_list(vacancies):
    vacancy_object_list = Vacancy.convert_to_object_list(vacancies)
    assert isinstance(vacancy_object_list, list)


def test_favorite_to_object_list(vacancies):
    favorite_vacancies_list = Vacancy.favorite_to_object_list(vacancies)
    assert isinstance(favorite_vacancies_list, list)
