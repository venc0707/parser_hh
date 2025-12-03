from abc import ABC, abstractmethod
import requests
from typing import Dict, Any, List, Optional


class JobApi(ABC):
    """Абстрактный класс API для работы с вакансиями"""

    def __connect(self) -> bool:
        """Подключение к API"""
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str, per_page: int) -> List[Dict[str, Any]]:
        """Получение вакансий по поисковому запросу"""
        pass


class HeadHunterAPI(JobApi):
    """Класс для работы с API hh.ru"""

    __BASE_URL = "https://api.hh.ru"

    def __init__(self):
        self.__session = requests.Session()
        self.__connected = False
        # self.headers = {
        #     "User-Agent": "HH-Parser/1.0 (your-email@example.com)",
        #     "Accept": "application/json"
        # }

    def __connect(self) -> bool:
        """Подключение к API hh.ru"""
        try:
            response = self.__session.get(f"{self.__BASE_URL}/vacancies", params={"per_page": 1})
            response.raise_for_status()
            self.__connected = True
            return True
        except requests.RequestException as e:
            print(f"Ошибка подключения к API hh.ru: {e}")
            self.__connected = False
            return False


    def get_vacancies(self, search_query: str, per_page: int = 100):
        """ Получение вакансий с hh.ru по заданным параметрам
             Args:
                search_query: Поисковый запрос """

        params = {'text': search_query,
                  'per_page': per_page
                  }

        try:
            self.__connected = True
            response = self.__session.get(f"{self.__BASE_URL}/vacancies", params=params, timeout=30)

            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])
            return items

        except requests.exceptions.Timeout:
            raise ConnectionError("Превышено время ожидания ответа от API")

        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError(f"Ошибка HTTPError: {e}")

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Не удалось подключиться к API hh.ru: {e}")

        except Exception as e:
            raise f"Неожиданная ошибка: {e}"

if __name__ == '__main__':
   # Создание экземпляра класса для работы с API сайтов с вакансиями
   hh_api = HeadHunterAPI()

   # Получение вакансий с hh.ru в формате JSON
   hh_vacancies = hh_api.get_vacancies("Python")
   print(hh_vacancies)
