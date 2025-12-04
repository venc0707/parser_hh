from abc import ABC, abstractmethod
import json
import os
from typing import List, Dict, Any
from vacancies import Vacancy 


class JobJSON(ABC):

    @abstractmethod
    def add_vacancy(self):
        pass

    @abstractmethod
    def delete_vacancy(self):
        pass

    @abstractmethod
    def print_all_vacancies(self):
        pass


class JSONSaver(JobJSON):
    """ Класс для сохранения информации о вакансиях в файл """

    def __init__(self, filename: str = 'vacancies.json'):
        self.__filename = filename
        self.file_path = f'../data/{self.__filename}'
        
        self._ensure_file_exists()


    def _ensure_file_exists(self):
        """Создает пустой файл, если он не существует"""

        os.makedirs('../data', exist_ok=True)

        if not os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f)
            except Exception as e:
                raise Exception(f"Ошибка при создании файла: {e}")


    def _read_vacancies(self) -> List[Dict[str, Any]]:
        """Чтение вакансий из файла"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []


    def _write_vacancies(self, vacancies: List[Dict[str, Any]]):
        """Запись вакансий в файл"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)


    def _vacancy_to_dict(self, vacancy: Vacancy) -> Dict[str, Any]:
        """Преобразование объекта Vacancy в словарь"""
        return {
            "title": vacancy.title,
            "company": vacancy.company,
            "url": vacancy.url,
            "salary_range": vacancy.salary_range,
            "description": vacancy.description,
            "average_salary": vacancy.average_salary
        }


    def add_vacancy(self, vacancy: Vacancy):
        """ Добавление вакансии в файл """
        vacancies = self._read_vacancies()
        vacancy_dict = self._vacancy_to_dict(vacancy)

        for v in vacancies:
            if v.get("url") == vacancy.url:
                print(f"Вакансия '{vacancy.title}' уже существует в файле")
                return

        vacancies.append(vacancy_dict)
        self._write_vacancies(vacancies)
        print(f"Вакансия '{vacancy.title}' успешно добавлена")


    def delete_vacancy(self, vacancy: Vacancy):
        """ Удаление вакансии из файла """
        vacancies = self._read_vacancies()

        initial_length = len(vacancies)
        vacancies = [v for v in vacancies if v.get("url") != vacancy.url]

        if len(vacancies) < initial_length:
            self._write_vacancies(vacancies)
            print(f"Вакансия '{vacancy.title}' успешно удалена")
        else:
            print(f"Вакансия '{vacancy.title}' не найдена в файле")


    def get_vacancies_by_salary(self, min_salary: float) -> List[Dict[str, Any]]:
        """ Получение вакансий с зарплатой выше указанной """
        vacancies = self._read_vacancies()
        return [v for v in vacancies if v.get("average_salary", 0) >= min_salary]


    def get_vacancies_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """ Поиск вакансий по ключевому слову """
        vacancies = self._read_vacancies()
        keyword_lower = keyword.lower()

        return [
            v for v in vacancies
            if (keyword_lower in v.get("title", "").lower() or
                keyword_lower in v.get("description", "").lower() or
                keyword_lower in v.get("company", "").lower())
        ]


    def clear_file(self):
        """Очистка файла с вакансиями"""
        self._write_vacancies([])
        print("Файл с вакансиями очищен")

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """Получение всех вакансий из файла"""
        return self._read_vacancies()

    def print_all_vacancies(self):
        """Вывод всех вакансий на экран"""
        vacancies = self._read_vacancies()

        if not vacancies:
            print("В файле нет вакансий")
            return

        print(f"Всего вакансий в файле: {len(vacancies)}")
        print("=" * 50)

        for i, vacancy in enumerate(vacancies, 1):
            print(f"{i}. {vacancy.get('title')}")
            print(f"   Компания: {vacancy.get('company')}")
            print(f"   Зарплата: {vacancy.get('salary_range', 'Не указана')}")
            print(f"   Средняя зарплата: {vacancy.get('average_salary')}")
            print(f"   URL: {vacancy.get('url')}")
            print(f"   Описание: {vacancy.get('description', '')[:100]}..." if vacancy.get('description') else "")
            print("-" * 50)


# Пример использования
if __name__ == "__main__":
    vacancy1 = Vacancy(
        "Python Developer",
        "Google",
        "https://hh.ru/vacancy/123456",
        "100 000-150 000 руб.",
        "Требования: опыт работы от 3 лет, знание Django"
    )

    vacancy2 = Vacancy(
        "Java Developer",
        "Yandex",
        "https://hh.ru/vacancy/789012",
        "120000-180000 руб.",
        "Требования: Spring Framework, опыт от 2 лет"
    )

    # Сохранение информации о вакансиях в файл
    json_saver = JSONSaver()

    # Добавляем вакансии
    json_saver.add_vacancy(vacancy1)
    json_saver.add_vacancy(vacancy2)

    # Выводим все вакансии
    json_saver.print_all_vacancies()

    # Поиск по ключевому слову
    print("\nПоиск вакансий по слову 'Python':")
    python_vacancies = json_saver.get_vacancies_by_keyword("Python")
    for v in python_vacancies:
        print(f"  - {v['title']} в {v['company']}")

    # Поиск по зарплате
    print("\nВакансии с зарплатой от 130000:")
    high_salary_vacancies = json_saver.get_vacancies_by_salary(130000)
    for v in high_salary_vacancies:
        print(f"  - {v['title']}: {v['average_salary']}")

    # Удаляем одну вакансию
    json_saver.delete_vacancy(vacancy1)

    # Показываем оставшиеся
    print("\nОставшиеся вакансии после удаления:")
    json_saver.print_all_vacancies()

    # Очистка файла (опционально)
    json_saver.clear_file()