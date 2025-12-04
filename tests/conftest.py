import pytest
import json
import tempfile
import os
from unittest.mock import Mock
from src.vacancies import Vacancy


@pytest.fixture
def mock_hh_api_response():
    """Фикстура с мок-ответом от HH API"""
    def _create_response(items=None, found=0, pages=0):
        return {
            "items": items or [],
            "found": found,
            "pages": pages,
            "per_page": 100,
            "page": 0,
            "clusters": None,
            "arguments": None,
            "alternate_url": "https://hh.ru/search/vacancy"
        }
    return _create_response


@pytest.fixture
def sample_vacancy_data():
    """Фикстура с примером данных вакансии"""
    return {
        "id": "123456",
        "name": "Python Developer",
        "salary": {
            "from": 100000,
            "to": 200000,
            "currency": "RUR"
        },
        "employer": {
            "name": "Test Company"
        },
        "snippet": {
            "requirement": "Python, Django, Flask"
        }
    }


@pytest.fixture
def temp_json_file():
    """Фикстура для временного JSON файла"""
    # Создаем временный файл
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
    temp_file.write('[]')
    temp_file.close()

    yield temp_file.name

    # Удаляем временный файл
    os.unlink(temp_file.name)


@pytest.fixture
def sample_vacancy_dict():
    """Фикстура с примером словаря вакансии"""
    return {
        "title": "Python Developer",
        "company": "Google",
        "url": "https://hh.ru/vacancy/123",
        "salary_range": "100000-150000 руб.",
        "description": "Требования: Python, Django",
        "average_salary": 125000.0
    }


@pytest.fixture
def mock_vacancy():
    """Фикстура с мок-объектом Vacancy"""
    vacancy = Mock(spec=Vacancy)
    vacancy.title = "Test Vacancy"
    vacancy.company = "Test Company"
    vacancy.url = "https://test.com/vacancy/1"
    vacancy.salary_range = "100000-150000"
    vacancy.description = "Test description"
    vacancy.average_salary = 125000.0
    return vacancy


@pytest.fixture
def json_saver_with_data(temp_json_file, sample_vacancy_dict):
    """Фикстура с JSONSaver и данными"""
    # Записываем тестовые данные в файл
    with open(temp_json_file, 'w', encoding='utf-8') as f:
        json.dump([sample_vacancy_dict], f)

    # Создаем saver с подмененным путем
    from src.saver_json import JSONSaver  # Замените на имя вашего модуля
    saver = JSONSaver()
    saver.file_path = temp_json_file
    return saver


@pytest.fixture
def mock_vacancy_data():
    """Фикстура с тестовыми данными вакансии от API"""
    return {
        'name': 'Python Developer',
        'employer': {'name': 'Google'},
        'alternate_url': 'https://hh.ru/vacancy/123',
        'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'},
        'snippet': {
            'requirement': 'Python experience',
            'responsibility': 'Backend development'
        }
    }


@pytest.fixture
def mock_user_inputs():
    """Фикстура с последовательностью пользовательских вводов"""

    def _create_inputs(*inputs):
        return list(inputs)

    return _create_inputs


@pytest.fixture
def capture_print():
    """Фикстура для захвата вывода print"""
    import io
    from contextlib import redirect_stdout

    def _capture(func, *args, **kwargs):
        f = io.StringIO()
        with redirect_stdout(f):
            func(*args, **kwargs)
        return f.getvalue()

    return _capture


@pytest.fixture
def sample_vacancy():
    """Фикстура с образцом вакансии"""
    return Vacancy(
        title="Python Developer",
        company="Google",
        url="https://hh.ru/vacancy/123",
        salary_range="100000-150000 руб.",
        description="Требования: Python 3+"
    )


@pytest.fixture
def vacancy_without_salary():
    """Фикстура с вакансией без зарплаты"""
    return Vacancy(
        title="Python Developer",
        company="Google",
        url="https://hh.ru/vacancy/456",
        description="Требования: Python 3+"
    )


@pytest.fixture
def vacancies_for_comparison():
    """Фикстура с несколькими вакансиями для сравнения"""
    return [
        Vacancy("Low", "C1", "https://test.com/1", "50000-70000"),
        Vacancy("Medium", "C2", "https://test.com/2", "100000-150000"),
        Vacancy("High", "C3", "https://test.com/3", "200000-250000"),
    ]
