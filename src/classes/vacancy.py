class Vacancy:
    """Класс вакансии, с его помощью будет формировать ЭК
    вакансий и список из ЭК вакансий полученных от API"""

    vacancies_list = []

    def __init__(self, name, salary_from, salary_to, currency, url, requirements, responsibility):
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.url = url
        self.requirements = requirements
        self.responsibility = responsibility

    def __gt__(self, other):
        pass

    def __str__(self):
        if self.salary_from == 0 and self.salary_to != 0:
            return (f"Вакансия: {self.name}\n"
                    f"Зарплата: до {self.salary_to} {self.currency}\n"
                    f"Требования: {self.requirements}\n"
                    f"Обязанности: {self.responsibility}\n"
                    f"Ссылка: {self.url}\n")
        elif self.salary_from != 0 and self.salary_to == 0:
            return (f"Вакансия: {self.name}\n"
                    f"Зарплата: от {self.salary_from} {self.currency}\n"
                    f"Требования: {self.requirements}\n"
                    f"Обязанности: {self.responsibility}\n"
                    f"Ссылка: {self.url}\n")
        elif self.salary_from == 0 and self.salary_to == 0:
            return (f"Вакансия: {self.name}\n"
                    f"Зарплата: не указана\n"
                    f"Требования: {self.requirements}\n"
                    f"Обязанности: {self.responsibility}\n"
                    f"Ссылка: {self.url}\n")
        else:
            return (f"Вакансия: {self.name}\n"
                    f"Зарплата: {self.salary_from} - {self.salary_to} {self.currency}\n"
                    f"Требования: {self.requirements}\n"
                    f"Обязанности: {self.responsibility}\n"
                    f"Ссылка: {self.url}\n")

    @classmethod
    def convert_to_object_list(cls, vacancies: dict):
        """Передаем в качестве аргумента """
        for i in vacancies['items']:
            if i['salary'] is None:
                cls.vacancies_list.append(Vacancy(i['name'],
                                                  0,
                                                  0,
                                                  '',
                                                  i['url'],
                                                  i['snippet']['requirement'],
                                                  i['snippet']['responsibility']))
            elif i['salary']['from'] is None and i['salary']['to'] is not None:
                cls.vacancies_list.append(Vacancy(i['name'],
                                                  0,
                                                  i['salary']['to'],
                                                  i['salary']['currency'],
                                                  i['url'],
                                                  i['snippet']['requirement'],
                                                  i['snippet']['responsibility']))
            elif i['salary']['from'] is not None and i['salary']['to'] is None:
                cls.vacancies_list.append(Vacancy(i['name'],
                                                  i['salary']['from'],
                                                  0,
                                                  i['salary']['currency'],
                                                  i['url'],
                                                  i['snippet']['requirement'],
                                                  i['snippet']['responsibility']))
            else:
                cls.vacancies_list.append(Vacancy(i['name'],
                                                  i['salary']['from'],
                                                  i['salary']['to'],
                                                  i['salary']['currency'],
                                                  i['url'],
                                                  i['snippet']['requirement'],
                                                  i['snippet']['responsibility']))

        return cls.vacancies_list