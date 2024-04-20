from abc import ABC, abstractmethod


class AbsctractAPI(ABC):
    """Здесь описываем абстрактный класс для HeadHunterAPI"""

    @abstractmethod
    def load_vacancies(self, keyword, page, per_page):
        pass
