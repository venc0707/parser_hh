

class Vacancy:

    __slots__ = ("_title", "_company", "_url", "_salary_range", "_description", "_average_salary")

    def __init__(self, title: str, company: str, url: str, salary_range: str = None, description: str = ""):
        self._title = title
        self._company = company
        self._url = url
        self._salary_range = salary_range
        self._description = description

        self._average_salary = self._calculate_average_salary()



    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Название вакансии не может быть пустым")
        self._title = value.strip()

    @property
    def company(self) -> str:
        return self._company

    @company.setter
    def company(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Название компании не может быть пустым")
        self._company = value.strip()

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("URL не может быть пустым")
        if not value.startswith(('http://', 'https://')):
            raise ValueError("URL должен начинаться с http:// или https://")
        self._url = value.strip()

    @property
    def salary_range(self) -> str:
        """Диапазон зарплаты"""
        return self._salary_range

    @salary_range.setter
    def salary_range(self, value: str):
        """Установка диапазона зарплаты"""
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("Диапазон зарплаты должен быть строкой")

            # Базовая валидация формата
            if '-' not in value:
                raise ValueError("Диапазон зарплаты должен содержать '-' (например: '100000-150000')")

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value.strip() if isinstance(value, str) else ""

    @property
    def average_salary(self) -> float:
        """Средняя зарплата (только чтение)"""
        return self._average_salary

    def _calculate_average_salary(self) -> float:
        """Вычисление средней зарплаты из диапазона"""
        if not self._salary_range:
            return 0.0

        try:
            import re

            # Очищаем строку от всех нецифровых символов (ВКЛЮЧАЯ пробелы)
            clean = re.sub(r'[^\d-]', '', self._salary_range)  # Убрали \s!

            # Ищем числа в строке
            numbers = re.findall(r'\d+', clean)

            if len(numbers) >= 2:
                # Берем первые два числа как from и to
                salary_from = float(numbers[0])
                salary_to = float(numbers[1])
                return (salary_from + salary_to) / 2
            elif len(numbers) == 1:
                # Если только одно число
                return float(numbers[0])
            else:
                return 0.0

        except (ValueError, IndexError, AttributeError):
            return 0.0

    def __lt__(self, other: 'Vacancy') -> bool:
            """Сравнение вакансий по средней зарплате (меньше)"""
            if not isinstance(other, Vacancy):
                return NotImplemented
            return self._average_salary < other._average_salary

    def __eq__(self, other: object) -> bool:
            """Сравнение вакансий"""
            if not isinstance(other, Vacancy):
                return NotImplemented
            return (self._title == other._title and
                    self._company == other._company and
                    self._url == other._url)

if __name__ == '__main__':
    vacancy1 = Vacancy("Python Developer","Google", "https://hh.ru/vacancy/123456", "100 000-150 000 руб.",
                      "Требования: опыт работы от 3 лет...")
    vacancy2 = Vacancy("Pyth Developer","Googl", "https://hh.ru/vacancy/3456", "100 000-180 000 руб.",
                      "Требования: опыт работы от 3 лет...")

    print(vacancy1 < vacancy2)
    print(vacancy2 == vacancy1)