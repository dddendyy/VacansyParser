class Vacancy:
    """Класс вакансии, с его помощью будет формировать ЭК
    вакансий и список из ЭК вакансий полученных от API"""

    vacancies_list = []
    favorite_vacancies_list = []

    def __init__(self,
                 vacancie_id: str,
                 employer_id: str,
                 name: str,
                 salary_from: int,
                 salary_to: int,
                 currency: str,
                 url: str,
                 requirements: str,
                 responsibility: str):

        self.vacancie_id = vacancie_id
        self.employer_id = employer_id
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

        if not isinstance(other, Vacancy):
            raise TypeError('Можно сравнивать только ЭК класса вакансии')

        if self.salary_from == 0 and self.salary_to == 0:
            # если одна из зарплат не указана - исключение
            raise TypeError(f'У одной из вакансий не указана зарплата')

        elif other.salary_from == 0 and other.salary_to == 0:
            # если одна из зарплат не указана - исключение
            raise TypeError(f'У одной из вакансий не указана зарплата')

        if self.salary_to == 0 and other.salary_to != 0:
            return True

        elif self.salary_to != 0 and other.salary_to == 0:
            return False

        elif self.salary_to != 0 and other.salary_to != 0:
            return self.salary_to > other.salary_to

        else:
            return self.salary_from > other.salary_from

    def __str__(self):
        if self.salary_from == 0 and self.salary_to != 0:
            return (f"ID вакансии: {self.vacancie_id}, название: {self.name}\n"
                    f"ID работодателя {self.employer_id}\n"
                    f"Зарплата: до {self.salary_to} {self.currency}\n"
                    f"Требования: {self.requirements}\n"
                    f"Обязанности: {self.responsibility}\n"
                    f"Ссылка: {self.url}\n")
        elif self.salary_from != 0 and self.salary_to == 0:
            return (f"ID вакансии: {self.vacancie_id}, название: {self.name}\n"
                    f"ID работодателя {self.employer_id}\n"
                    f"Зарплата: от {self.salary_from} {self.currency}\n"
                    f"Требования: {self.requirements}\n"
                    f"Обязанности: {self.responsibility}\n"
                    f"Ссылка: {self.url}\n")
        elif self.salary_from == 0 and self.salary_to == 0:
            return (f"ID вакансии: {self.vacancie_id}, название: {self.name}\n"
                    f"ID работодателя {self.employer_id}\n"
                    f"Зарплата: не указана\n"
                    f"Требования: {self.requirements}\n"
                    f"Обязанности: {self.responsibility}\n"
                    f"Ссылка: {self.url}\n")
        else:
            return (f"ID вакансии: {self.vacancie_id}, название: {self.name}\n"
                    f"ID работодателя {self.employer_id}\n"
                    f"Зарплата: {self.salary_from} - {self.salary_to} {self.currency}\n"
                    f"Требования: {self.requirements}\n"
                    f"Обязанности: {self.responsibility}\n"
                    f"Ссылка: {self.url}\n")

    @classmethod
    def convert_to_object_list(cls, vacancies: dict):
        """Метод, который конвертирует полученный список вакансий в список ЭК"""
        for i in vacancies:
            # если зарплата не указана
            if i['salary'] is None:
                cls.vacancies_list.append(Vacancy(i['id'],
                                                  i['employer']['id'],
                                                  i['name'],
                                                  0,
                                                  0,
                                                  '',
                                                  i['url'],
                                                  i['snippet']['requirement'],
                                                  i['snippet']['responsibility']))
            # если указана только верхняя вилка
            elif i['salary']['from'] is None and i['salary']['to'] is not None:
                cls.vacancies_list.append(Vacancy(i['id'],
                                                  i['employer']['id'],
                                                  i['name'],
                                                  0,
                                                  i['salary']['to'],
                                                  i['salary']['currency'],
                                                  i['url'],
                                                  i['snippet']['requirement'],
                                                  i['snippet']['responsibility']))
            # если указана только нижняявилка
            elif i['salary']['from'] is not None and i['salary']['to'] is None:
                cls.vacancies_list.append(Vacancy(i['id'],
                                                  i['employer']['id'],
                                                  i['name'],
                                                  i['salary']['from'],
                                                  0,
                                                  i['salary']['currency'],
                                                  i['url'],
                                                  i['snippet']['requirement'],
                                                  i['snippet']['responsibility']))
            # если указано всё
            else:
                cls.vacancies_list.append(Vacancy(i['id'],
                                                  i['employer']['id'],
                                                  i['name'],
                                                  i['salary']['from'],
                                                  i['salary']['to'],
                                                  i['salary']['currency'],
                                                  i['url'],
                                                  i['snippet']['requirement'],
                                                  i['snippet']['responsibility']))

        return cls.vacancies_list

    @classmethod
    def favorite_to_object_list(cls, vacancies: dict):
        """Так как набор полей у сырого файла и нашего класса разный,
        то я создал отдельный метод, который возвращает список избранных вакансий
        принцип работы такой же, как у метода выше"""
        for i in vacancies:
            cls.favorite_vacancies_list.append(Vacancy(i['vacancie_id'],
                                                       i['employer_id'],
                                                       i['name'],
                                                       i['salary_from'],
                                                       i['salary_to'],
                                                       i['currency'],
                                                       i['url'],
                                                       i['requirements'],
                                                       i['responsibility']))
        return cls.favorite_vacancies_list
