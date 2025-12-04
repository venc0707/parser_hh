import re

class Vacancy:

    __slots__ = ("_title", "_company", "_url", "_salary_range", "_description", "_average_salary")

    def __init__(self, title: str, company: str, url: str, salary_range: str = None, description: str = ""):
        self.title = title
        self.company = company
        self.url = url
        self.salary_range = salary_range
        self.description = description
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
        value = value.strip()  # Обрезать пробелы
        if not value.startswith(('http://', 'https://')):
            raise ValueError("URL должен начинаться с http:// или https://")
        self._url = value

    @property
    def salary_range(self) -> str:
        """Диапазон зарплаты"""
        return self._salary_range

    @salary_range.setter
    def salary_range(self, value: str):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("Диапазон зарплаты должен быть строкой")
            # Базовая валидация
            if '-' not in value:
                raise ValueError("Диапазон зарплаты должен содержать '-'")
        self._salary_range = value
        # Пересчитать среднюю зарплату
        self._average_salary = self._calculate_average_salary()

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if value is None:
            self._description = ""
        elif isinstance(value, str):
            self._description = value.strip()
        else:
            self._description = str(value).strip()

    @property
    def average_salary(self) -> float:
        """Средняя зарплата (только чтение)"""
        return self._average_salary

    def _calculate_average_salary(self) -> float:
        """ вычисление средней зарплаты """
        if not self._salary_range:
            return 0.0

        try:
            # Удаляем все символы, кроме цифр, дефиса, точки и запятых
            clean = re.sub(r'[^\d\-.,]', '', self._salary_range)
            # Заменяем запятые на точки для десятичных чисел
            clean = clean.replace(',', '.')

            # Ищем все числа (целые и десятичные)
            numbers = re.findall(r'[\d\.]+', clean)

            if len(numbers) >= 2:
                salary_from = float(numbers[0])
                salary_to = float(numbers[1])
                return (salary_from + salary_to) / 2
            elif len(numbers) == 1:
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

