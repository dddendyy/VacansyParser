from abc import ABC, abstractmethod


class AbstractJSONSaver(ABC):
    """Создаем абстрактный класс-родитель для JSONSaver'a,
    который в свою очередь будет """

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass
