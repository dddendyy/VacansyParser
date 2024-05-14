class Employer:
    """Класс для описания работодателя"""

    employers_list = []
    favorite_employers_list = []

    def __init__(self, employer_id, name, open_vacancies, url):
        self.employer_id = employer_id
        self.name = name
        self.open_vacancies = open_vacancies
        self.url = url

    def __str__(self):
        return (f"ID работодателя: {self.employer_id}\n"
                f"Название: {self.name}\n"
                f"Открытых вакансий: {self.open_vacancies}\n"
                f"URL: {self.url}")

    @classmethod
    def convert_to_object_list(cls, employers: dict):
        for employer in employers:
            cls.employers_list.append(Employer(employer['id'],
                                               employer['name'],
                                               employer['open_vacancies'],
                                               employer['url']))
        return cls.employers_list
