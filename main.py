from src.classes.HH_API import HeadHunterAPI

if __name__ == '__main__':

    # создаем ЭК класса HeadHunterAPI
    hh_api = HeadHunterAPI()

    # загружаем список сырых вакансий
    hh_api.load_vacancies()
