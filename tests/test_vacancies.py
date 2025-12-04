import pytest
import sys
import os

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.vacancies import Vacancy


class TestVacancyInit:
    """Тесты инициализации класса Vacancy"""

    def test_init_basic(self):
        """Тест базовой инициализации"""
        vacancy = Vacancy(
            title="Python Developer",
            company="Google",
            url="https://hh.ru/vacancy/123",
            salary_range="100000-150000 руб.",
            description="Требования: Python 3+"
        )

        assert vacancy.title == "Python Developer"
        assert vacancy.company == "Google"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary_range == "100000-150000 руб."
        assert vacancy.description == "Требования: Python 3+"

    def test_init_without_salary(self):
        """Тест инициализации без зарплаты"""
        vacancy = Vacancy(
            title="Python Developer",
            company="Google",
            url="https://hh.ru/vacancy/123",
            description="Требования: Python 3+"
        )

        assert vacancy.title == "Python Developer"
        assert vacancy.company == "Google"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary_range is None
        assert vacancy.description == "Требования: Python 3+"
        assert vacancy.average_salary == 0.0

    def test_init_with_empty_description(self):
        """Тест инициализации с пустым описанием"""
        vacancy = Vacancy(
            title="Python Developer",
            company="Google",
            url="https://hh.ru/vacancy/123",
            salary_range="100000-150000 руб.",
            description=""
        )

        assert vacancy.description == ""

    def test_init_with_none_description(self):
        """Тест инициализации с None описанием"""
        vacancy = Vacancy(
            title="Python Developer",
            company="Google",
            url="https://hh.ru/vacancy/123",
            salary_range="100000-150000 руб.",
            description=None
        )

        # Теперь сеттер вызывается, и None преобразуется в ""
        assert vacancy.description == ""

    def test_slots_attribute(self):
        """Тест, что используются __slots__"""
        vacancy = Vacancy(
            title="Test",
            company="Test",
            url="https://test.com",
            salary_range="100000-150000 руб."
        )

        # Проверяем наличие __slots__
        assert hasattr(Vacancy, '__slots__')

        # Пытаемся добавить новый атрибут (должно вызвать ошибку)
        with pytest.raises(AttributeError):
            vacancy.new_attribute = "test"


class TestVacancyProperties:
    """Тесты свойств (property) класса Vacancy"""

    def test_title_property(self):
        """Тест свойства title"""
        vacancy = Vacancy("Test", "Test", "https://test.com")

        # Чтение
        assert vacancy.title == "Test"

        # Запись с валидацией
        vacancy.title = "New Title"
        assert vacancy.title == "New Title"

        # Запись с пробелами
        vacancy.title = "  Title with spaces  "
        assert vacancy.title == "Title with spaces"

    def test_title_validation(self):
        """Тест валидации title"""
        vacancy = Vacancy("Test", "Test", "https://test.com")

        # Пустой title
        with pytest.raises(ValueError, match="Название вакансии не может быть пустым"):
            vacancy.title = ""

        # None title
        with pytest.raises(ValueError, match="Название вакансии не может быть пустым"):
            vacancy.title = None

        # Не строка
        with pytest.raises(ValueError, match="Название вакансии не может быть пустым"):
            vacancy.title = 123

    def test_company_property(self):
        """Тест свойства company"""
        vacancy = Vacancy("Test", "Test", "https://test.com")

        # Чтение
        assert vacancy.company == "Test"

        # Запись с валидацией
        vacancy.company = "New Company"
        assert vacancy.company == "New Company"

        # Запись с пробелами
        vacancy.company = "  Company with spaces  "
        assert vacancy.company == "Company with spaces"

    def test_company_validation(self):
        """Тест валидации company"""
        vacancy = Vacancy("Test", "Test", "https://test.com")

        # Пустая company
        with pytest.raises(ValueError, match="Название компании не может быть пустым"):
            vacancy.company = ""

        # None company
        with pytest.raises(ValueError, match="Название компании не может быть пустым"):
            vacancy.company = None

        # Не строка
        with pytest.raises(ValueError, match="Название компании не может быть пустым"):
            vacancy.company = 123

    def test_url_property(self):
        """Тест свойства url"""
        vacancy = Vacancy("Test", "Test", "https://test.com")

        # Чтение
        assert vacancy.url == "https://test.com"

        # Запись с валидацией
        vacancy.url = "https://new-url.com"
        assert vacancy.url == "https://new-url.com"

        # Запись с пробелами
        vacancy.url = "  https://test.com  "
        assert vacancy.url == "https://test.com"

    def test_url_validation(self):
        """Тест валидации url"""
        vacancy = Vacancy("Test", "Test", "https://test.com")

        # Пустой url
        with pytest.raises(ValueError, match="URL не может быть пустым"):
            vacancy.url = ""

        # None url
        with pytest.raises(ValueError, match="URL не может быть пустым"):
            vacancy.url = None

        # Не строка
        with pytest.raises(ValueError, match="URL не может быть пустым"):
            vacancy.url = 123

        # Неправильный протокол
        with pytest.raises(ValueError, match="URL должен начинаться с http:// или https://"):
            vacancy.url = "ftp://test.com"

        with pytest.raises(ValueError, match="URL должен начинаться с http:// или https://"):
            vacancy.url = "test.com"

        # HTTP протокол (должно работать)
        vacancy.url = "http://test.com"
        assert vacancy.url == "http://test.com"

    def test_salary_range_property(self):
        """Тест свойства salary_range"""
        vacancy = Vacancy("Test", "Test", "https://test.com", "100000-150000 руб.")

        # Чтение
        assert vacancy.salary_range == "100000-150000 руб."

        # Запись None
        vacancy.salary_range = None
        assert vacancy.salary_range is None
        assert vacancy.average_salary == 0.0

        # Запись новой зарплаты
        vacancy.salary_range = "200000-300000 руб."
        assert vacancy.salary_range == "200000-300000 руб."
        assert vacancy.average_salary == 250000.0

    def test_salary_range_validation(self):
        """Тест валидации salary_range"""
        vacancy = Vacancy("Test", "Test", "https://test.com")

        # Не строка (кроме None)
        with pytest.raises(ValueError, match="Диапазон зарплаты должен быть строкой"):
            vacancy.salary_range = 123456

        # Строка без дефиса
        with pytest.raises(ValueError, match="Диапазон зарплаты должен содержать '-'"):
            vacancy.salary_range = "100000 руб."

        # С дефисом (должно работать)
        vacancy.salary_range = "100000-150000 руб."
        assert vacancy.salary_range == "100000-150000 руб."

    def test_description_property(self):
        """Тест свойства description"""
        vacancy = Vacancy("Test", "Test", "https://test.com", description="Initial")

        # Чтение
        assert vacancy.description == "Initial"

        # Запись
        vacancy.description = "New description"
        assert vacancy.description == "New description"

        # Запись с пробелами
        vacancy.description = "  Description with spaces  "
        assert vacancy.description == "Description with spaces"

        # Запись None (преобразуется в "")
        vacancy.description = None
        assert vacancy.description == ""

        # Запись не строки (преобразуется в строку)
        vacancy.description = 123
        assert vacancy.description == "123"

    def test_average_salary_property_readonly(self):
        """Тест, что average_salary только для чтения"""
        vacancy = Vacancy("Test", "Test", "https://test.com", "100000-150000")

        # Можно читать
        assert vacancy.average_salary == 125000.0

        # Нельзя записывать
        with pytest.raises(AttributeError):
            vacancy.average_salary = 200000.0


class TestCalculateAverageSalary:
    """Тесты вычисления средней зарплаты"""

    def test_calculate_with_range(self):
        """Тест вычисления с диапазоном"""
        test_cases = [
            ("100000-150000", 125000.0),  # Простые числа
            ("100000-150000 руб.", 125000.0),  # С текстом
            ("100000 - 150000", 125000.0),  # С пробелами
        ]

        for salary_range, expected in test_cases:
            vacancy = Vacancy("Test", "Test", "https://test.com", salary_range)
            assert vacancy.average_salary == expected

    def test_calculate_single_value(self):
        """Тест вычисления с одним значением - в текущей реализации требует дефис"""
        # В текущей реализации всегда нужен дефис
        with pytest.raises(ValueError, match="Диапазон зарплаты должен содержать '-'"):
            vacancy = Vacancy("Test", "Test", "https://test.com", "100000руб.")

    def test_calculate_no_salary(self):
        """Тест вычисления без зарплаты"""
        vacancy = Vacancy("Test", "Test", "https://test.com")
        assert vacancy.average_salary == 0.0

        # Пустая строка не допускается (требует дефис)
        with pytest.raises(ValueError, match="Диапазон зарплаты должен содержать '-'"):
            vacancy = Vacancy("Test", "Test", "https://test.com", salary_range="")

    def test_calculate_invalid_formats(self):
        """Тест вычисления с невалидными форматами"""
        # Эти форматы не содержат дефис, поэтому вызовут ошибку
        test_cases = [
            "з/п не указана",
            "по договоренности",
            "открытая зарплата",
            "100-тысяч",  # Есть дефис, но нет чисел
            "100 - 150 тысяч",  # Есть дефис и числа, должно работать
        ]

        for salary_range in test_cases:
            if '-' in salary_range:
                # Строки с дефисом должны создаваться
                vacancy = Vacancy("Test", "Test", "https://test.com", salary_range)
                # Проверяем, что объект создан
                assert vacancy is not None
            else:
                # Строки без дефиса должны вызывать ошибку
                with pytest.raises(ValueError, match="Диапазон зарплаты должен содержать '-'"):
                    Vacancy("Test", "Test", "https://test.com", salary_range)
    def test_calculate_with_decimal_numbers(self):
        """Тест вычисления с десятичными числами"""
        vacancy = Vacancy("Test", "Test", "https://test.com", "100000.50-150000.75")
        assert vacancy.average_salary == 125000.625


class TestComparisonMethods:
    """Тесты методов сравнения"""

    def test_lt_method(self):
        """Тест оператора < (меньше)"""
        vacancy1 = Vacancy("Test1", "Company1", "https://test.com/1", "100000-150000")
        vacancy2 = Vacancy("Test2", "Company2", "https://test.com/2", "200000-250000")
        vacancy3 = Vacancy("Test3", "Company3", "https://test.com/3")  # Без зарплаты

        # vacancy1 < vacancy2 (125k < 225k)
        assert vacancy1 < vacancy2
        assert not vacancy2 < vacancy1

        # vacancy3 < vacancy1 (0 < 125k)
        assert vacancy3 < vacancy1
        assert not vacancy1 < vacancy3

        # vacancy3 < vacancy2 (0 < 225k)
        assert vacancy3 < vacancy2
        assert not vacancy2 < vacancy3

    def test_eq_method(self):
        """Тест оператора == (равно) - сравнивает по title, company и url"""
        vacancy1 = Vacancy(
            title="Python Developer",
            company="Google",
            url="https://hh.ru/vacancy/123",
            salary_range="100000-150000 руб.",
            description="Description 1"
        )

        vacancy2 = Vacancy(
            title="Python Developer",
            company="Google",
            url="https://hh.ru/vacancy/123",  # Тот же URL
            salary_range="200000-250000 руб.",  # Другая зарплата
            description="Description 2"  # Другое описание
        )

        vacancy3 = Vacancy(
            title="Java Developer",  # Другое название
            company="Google",
            url="https://hh.ru/vacancy/124",  # Другой URL
            salary_range="100000-150000 руб."
        )

        # Вакансии с одинаковым title, company и url считаются равными
        assert vacancy1 == vacancy2

        # Разные данные - разные вакансии
        assert vacancy1 != vacancy3


class TestVacancyEdgeCases:
    """Тесты граничных случаев"""

    def test_unicode_characters(self):
        """Тест с Unicode символами"""
        vacancy = Vacancy(
            title="Python Разработчик 🐍",
            company="Компания «Рога и копыта»",
            url="https://hh.ru/vacancy/123",
            salary_range="100000-150000",
            description="Ищем разработчика для работы над интересным проектом! 😊"
        )

        assert "🐍" in vacancy.title
        assert "«Рога и копыта»" in vacancy.company
        assert "😊" in vacancy.description
