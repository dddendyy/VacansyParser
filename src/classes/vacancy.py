class Vacancy:
    """Класс вакансии, с его помощью будет формировать ЭК
    вакансий и список из ЭК вакансий полученных от API"""

    vacancies_list = []

    def __init__(self, vacancie_id, name, salary_from, salary_to, currency, url, requirements, responsibility):
        self.vacancie_id = vacancie_id
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.url = url
        self.requirements = requirements
        self.responsibility = responsibility

    def __gt__(self, other):
        """Метод сравнения зарплат у вакансий, обработка оператора '>'
        Ниже реализован дандер-метод __eq__, в нём НЕ указаны рэйзы, так как
        механизм сравнения будет всегда один, пользователь не сможет его менять,
        соотвтетсвенно все исключения отлавливаются при первом сравнении:
        1. self > other;
        2. self == other
        3. self < other"""

        if self.currency != other.currency:
            # если не совпадают валюты - исключение
            raise TypeError('Можно сравнивать вакансии только с одинаковыми валютами зарплат!')

        if self.salary_from == 0 and self.salary_to == 0:
            # если одна из зарплат не указана - исключение
            raise TypeError(f'У вакансии {self.name} с ID: {self.vacancie_id} не указана зарплата')

        elif other.salary_from == 0 and other.salary_to == 0:
            # если одна из зарплат не указана - исключение
            raise TypeError(f'У вакансии {other.name} с ID: {other.vacancie_id} не указана зарплата')

        elif self.salary_to != 0 and other.salary_to != 0:
            print('У обеих вакансий указаны верхние вилки зарплаты, сравнение пойдет по ним')
            return self.salary_to > other.salary_to

        elif self.salary_from != 0 and other.salary_from != 0:
            print('У обеих вакансий указаный нижние вилки зарплаты, cравнение пойдет по ним')
            return self.salary_from > other.salary_from

        else:
            raise TypeError('У одной из вакансий указана вилка, которая не указана у второй')

    def __eq__(self, other):
        """Метод сравнения зарплат у вакансий, обработка оператора '==' """
        if self.salary_to != 0 and other.salary_to != 0:
            return self.salary_to == other.salary_to

        elif self.salary_from != 0 and other.salary_from != 0:
            return self.salary_from == other.salary_from

    def __str__(self):
        if self.salary_from == 0 and self.salary_to != 0:
            return (f"ID вакансии: {self.vacancie_id}, название: {self.name}\n"
                    f"Зарплата: до {self.salary_to} {self.currency}\n"
                    f"Требования: {self.requirements}\n"
                    f"Обязанности: {self.responsibility}\n"
                    f"Ссылка: {self.url}\n")
        elif self.salary_from != 0 and self.salary_to == 0:
            return (f"ID вакансии: {self.vacancie_id}, название: {self.name}\n"
                    f"Зарплата: от {self.salary_from} {self.currency}\n"
                    f"Требования: {self.requirements}\n"
                    f"Обязанности: {self.responsibility}\n"
                    f"Ссылка: {self.url}\n")
        elif self.salary_from == 0 and self.salary_to == 0:
            return (f"ID вакансии: {self.vacancie_id}, название: {self.name}\n"
                    f"Зарплата: не указана\n"
                    f"Требования: {self.requirements}\n"
                    f"Обязанности: {self.responsibility}\n"
                    f"Ссылка: {self.url}\n")
        else:
            return (f"ID вакансии: {self.vacancie_id}, название: {self.name}\n"
                    f"Зарплата: {self.salary_from} - {self.salary_to} {self.currency}\n"
                    f"Требования: {self.requirements}\n"
                    f"Обязанности: {self.responsibility}\n"
                    f"Ссылка: {self.url}\n")

    @classmethod
    def convert_to_object_list(cls, vacancies: dict):
        """Передаем в качестве аргумента """
        for i in vacancies:
            if i['salary'] is None:
                cls.vacancies_list.append(Vacancy(i['id'],
                                                  i['name'],
                                                  0,
                                                  0,
                                                  '',
                                                  i['url'],
                                                  i['snippet']['requirement'],
                                                  i['snippet']['responsibility']))
            elif i['salary']['from'] is None and i['salary']['to'] is not None:
                cls.vacancies_list.append(Vacancy(i['id'],
                                                  i['name'],
                                                  0,
                                                  i['salary']['to'],
                                                  i['salary']['currency'],
                                                  i['url'],
                                                  i['snippet']['requirement'],
                                                  i['snippet']['responsibility']))
            elif i['salary']['from'] is not None and i['salary']['to'] is None:
                cls.vacancies_list.append(Vacancy(i['id'],
                                                  i['name'],
                                                  i['salary']['from'],
                                                  0,
                                                  i['salary']['currency'],
                                                  i['url'],
                                                  i['snippet']['requirement'],
                                                  i['snippet']['responsibility']))
            else:
                cls.vacancies_list.append(Vacancy(i['id'],
                                                  i['name'],
                                                  i['salary']['from'],
                                                  i['salary']['to'],
                                                  i['salary']['currency'],
                                                  i['url'],
                                                  i['snippet']['requirement'],
                                                  i['snippet']['responsibility']))

        return cls.vacancies_list
