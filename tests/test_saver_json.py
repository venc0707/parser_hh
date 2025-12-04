import pytest
import json
import os
import tempfile
import shutil
import sys
from unittest.mock import patch, mock_open

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Теперь импортируем модули
from src.saver_json import JSONSaver, JobJSON
from src.vacancies import Vacancy


class TestJSONSaver:
    """Тесты для класса JSONSaver"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        # Создаем временную директорию для тестов
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'vacancies.json')

    def teardown_method(self):
        """Очистка после каждого теста"""
        # Удаляем временную директорию
        shutil.rmtree(self.test_dir)

    def test_init_default_filename(self):
        """Тест инициализации с именем файла по умолчанию"""
        with patch('os.makedirs') as mock_makedirs, \
                patch('os.path.exists', return_value=False), \
                patch('builtins.open', mock_open()) as mock_file:
            saver = JSONSaver()
            assert saver._JSONSaver__filename == 'vacancies.json'
            mock_makedirs.assert_called_once_with('../data', exist_ok=True)

    def test_init_custom_filename(self):
        """Тест инициализации с пользовательским именем файла"""
        with patch('os.makedirs') as mock_makedirs, \
                patch('os.path.exists', return_value=False), \
                patch('builtins.open', mock_open()):
            saver = JSONSaver('custom_vacancies.json')
            assert saver._JSONSaver__filename == 'custom_vacancies.json'

    def test_ensure_file_exists_creates_file(self):
        """Тест создания файла, если он не существует"""
        # Создаем объект с подмененным путем к файлу
        saver = JSONSaver()
        saver.file_path = self.test_file

        saver._ensure_file_exists()

        assert os.path.exists(self.test_file)

        # Проверяем, что файл содержит пустой список
        with open(self.test_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            assert content == []

    def test_ensure_file_exists_existing_file(self):
        """Тест, когда файл уже существует"""
        # Создаем файл с некоторым содержимым
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump([{"test": "data"}], f)

        saver = JSONSaver()
        saver.file_path = self.test_file

        saver._ensure_file_exists()

        # Проверяем, что содержимое не изменилось
        with open(self.test_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            assert content == [{"test": "data"}]

    def test_read_vacancies_empty_file(self):
        """Тест чтения из пустого файла"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        # Создаем пустой файл
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('[]')

        result = saver._read_vacancies()
        assert result == []

    def test_read_vacancies_with_data(self):
        """Тест чтения из файла с данными"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        test_data = [
            {"title": "Python Dev", "company": "Test Co"},
            {"title": "Java Dev", "company": "Another Co"}
        ]

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

        result = saver._read_vacancies()
        assert result == test_data

    def test_read_vacancies_invalid_json(self):
        """Тест чтения файла с невалидным JSON"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        # Создаем файл с невалидным JSON
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('{invalid json}')

        result = saver._read_vacancies()
        assert result == []

    def test_write_vacancies(self):
        """Тест записи вакансий в файл"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        test_vacancies = [
            {"title": "Test Vacancy", "company": "Test Corp"},
            {"title": "Another Vacancy", "company": "Another Corp"}
        ]

        saver._write_vacancies(test_vacancies)

        # Читаем и проверяем
        with open(self.test_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
            assert result == test_vacancies

    def test_vacancy_to_dict(self):
        """Тест преобразования Vacancy в словарь"""
        saver = JSONSaver()

        # Создаем реальный объект Vacancy
        vacancy = Vacancy(
            title="Python Developer",
            company="Google",
            url="https://hh.ru/vacancy/123",
            salary_range="100000-150000 руб.",
            description="Требования: Python"
        )

        result = saver._vacancy_to_dict(vacancy)

        expected = {
            "title": "Python Developer",
            "company": "Google",
            "url": "https://hh.ru/vacancy/123",
            "salary_range": "100000-150000 руб.",
            "description": "Требования: Python",
            "average_salary": vacancy.average_salary  # Используем вычисленное значение
        }

        assert result == expected

    def test_add_vacancy_new(self):
        """Тест добавления новой вакансии"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        # Инициализируем пустой файл
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump([], f)

        vacancy = Vacancy(
            title="New Vacancy",
            company="Test Company",
            url="https://test.com/vacancy/1",
            salary_range="100000-150000",
            description="Test description"
        )

        with patch('builtins.print') as mock_print:
            saver.add_vacancy(vacancy)

            # Проверяем, что вакансия добавлена
            with open(self.test_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                assert len(result) == 1
                assert result[0]["title"] == "New Vacancy"

            # Проверяем вывод
            mock_print.assert_called_with("Вакансия 'New Vacancy' успешно добавлена")

    def test_add_vacancy_duplicate(self):
        """Тест добавления дублирующей вакансии"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        # Создаем файл с уже существующей вакансией
        existing_vacancy = {
            "title": "Existing Vacancy",
            "url": "https://test.com/vacancy/1",
            "company": "Test Company"
        }

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump([existing_vacancy], f)

        vacancy = Vacancy(
            title="New Title",
            company="Test Company",
            url="https://test.com/vacancy/1",  # Тот же URL
            salary_range="100000-150000",
            description="Test description"
        )

        with patch('builtins.print') as mock_print:
            saver.add_vacancy(vacancy)

            # Проверяем, что вакансия не добавлена
            with open(self.test_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                assert len(result) == 1
                assert result[0]["title"] == "Existing Vacancy"

            # Проверяем вывод
            mock_print.assert_called_with("Вакансия 'New Title' уже существует в файле")

    def test_delete_vacancy_existing(self):
        """Тест удаления существующей вакансии"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        # Создаем файл с вакансиями (URL должны быть корректными)
        vacancies = [
            {"title": "Vacancy 1", "url": "https://test.com/1"},
            {"title": "Vacancy 2", "url": "https://test.com/2"},
            {"title": "Vacancy 3", "url": "https://test.com/3"}
        ]

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f)

        vacancy = Vacancy(
            title="Vacancy 2",
            company="Test Company",
            url="https://test.com/2",  # Корректный URL
            salary_range="100000-150000",
            description="Test description"
        )

        with patch('builtins.print') as mock_print:
            saver.delete_vacancy(vacancy)

            # Проверяем, что вакансия удалена
            with open(self.test_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                assert len(result) == 2
                urls = [v["url"] for v in result]
                assert "https://test.com/2" not in urls

            # Проверяем вывод
            mock_print.assert_called_with("Вакансия 'Vacancy 2' успешно удалена")

    def test_delete_vacancy_nonexistent(self):
        """Тест удаления несуществующей вакансии"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        # Создаем файл с вакансиями
        vacancies = [
            {"title": "Vacancy 1", "url": "https://test.com/1"},
            {"title": "Vacancy 2", "url": "https://test.com/2"}
        ]

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f)

        vacancy = Vacancy(
            title="Nonexistent",
            company="Test Company",
            url="https://test.com/999",  # Корректный URL
            salary_range="100000-150000",
            description="Test description"
        )

        with patch('builtins.print') as mock_print:
            saver.delete_vacancy(vacancy)

            # Проверяем, что ничего не изменилось
            with open(self.test_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                assert len(result) == 2

            # Проверяем вывод
            mock_print.assert_called_with("Вакансия 'Nonexistent' не найдена в файле")

    def test_get_vacancies_by_salary(self):
        """Тест фильтрации по зарплате"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        vacancies = [
            {"title": "Low Salary", "average_salary": 50000},
            {"title": "Medium Salary", "average_salary": 100000},
            {"title": "High Salary", "average_salary": 200000},
            {"title": "No Salary", "average_salary": 0}
        ]

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f)

        result = saver.get_vacancies_by_salary(100000)

        assert len(result) == 2
        titles = [v["title"] for v in result]
        assert "Medium Salary" in titles
        assert "High Salary" in titles
        assert "Low Salary" not in titles

    def test_get_vacancies_by_keyword(self):
        """Тест поиска по ключевому слову"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        vacancies = [
            {"title": "Python Developer", "company": "Google", "description": "Python Django Flask"},
            {"title": "Java Developer", "company": "Oracle", "description": "Java Spring"},
            {"title": "Python Data Scientist", "company": "Facebook", "description": "Python ML"},
            {"title": "Frontend Developer", "company": "Amazon", "description": "JavaScript React"}
        ]

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f)

        result = saver.get_vacancies_by_keyword("python")

        assert len(result) == 2
        titles = [v["title"] for v in result]
        assert "Python Developer" in titles
        assert "Python Data Scientist" in titles
        assert "Java Developer" not in titles

        # Тест поиска в компании
        result2 = saver.get_vacancies_by_keyword("google")
        assert len(result2) == 1
        assert result2[0]["company"] == "Google"

    def test_get_all_vacancies(self):
        """Тест получения всех вакансий"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        test_data = [
            {"title": "Vacancy 1"},
            {"title": "Vacancy 2"}
        ]

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

        result = saver.get_all_vacancies()
        assert result == test_data

    def test_clear_file(self):
        """Тест очистки файла"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        # Создаем файл с данными
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump([{"test": "data"}], f)

        with patch('builtins.print') as mock_print:
            saver.clear_file()

            # Проверяем, что файл пустой
            with open(self.test_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                assert result == []

            # Проверяем вывод
            mock_print.assert_called_with("Файл с вакансиями очищен")

    def test_print_all_vacancies_empty(self):
        """Тест вывода пустого списка вакансий"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump([], f)

        with patch('builtins.print') as mock_print:
            saver.print_all_vacancies()
            mock_print.assert_called_with("В файле нет вакансий")

    def test_print_all_vacancies_with_data(self):
        """Тест вывода списка вакансий с данными"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        vacancies = [
            {
                "title": "Python Developer",
                "company": "Google",
                "salary_range": "100000-150000 руб.",
                "average_salary": 125000,
                "url": "https://test.com",
                "description": "Требования: Python, опыт от 3 лет"
            }
        ]

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f)

        with patch('builtins.print') as mock_print:
            saver.print_all_vacancies()

            # Проверяем, что были вызовы print
            assert mock_print.call_count > 0

            # Собираем все вызовы в строку
            calls = [str(call[0][0]) for call in mock_print.call_args_list]
            output = "\n".join(calls)

            # Проверяем ключевую информацию
            assert "Python Developer" in output
            assert "Google" in output
            assert "100000-150000" in output

    def test_ensure_file_exists_exception(self):
        """Тест исключения при создании файла"""
        saver = JSONSaver()

        with patch('os.makedirs'), \
                patch('os.path.exists', return_value=False), \
                patch('builtins.open', side_effect=PermissionError("Permission denied")):
            with pytest.raises(Exception) as exc_info:
                saver._ensure_file_exists()

            assert "Ошибка при создании файла" in str(exc_info.value)


class TestJobJSONAbstract:
    """Тесты абстрактного класса JobJSON"""

    def test_abstract_methods(self):
        """Тест, что класс является абстрактным"""
        assert hasattr(JobJSON, '__abstractmethods__')
        abstract_methods = JobJSON.__abstractmethods__

        assert 'add_vacancy' in abstract_methods
        assert 'delete_vacancy' in abstract_methods
        assert 'print_all_vacancies' in abstract_methods

        # Проверяем, что нельзя создать экземпляр абстрактного класса
        with pytest.raises(TypeError):
            JobJSON()


# Тесты на граничные случаи
class TestJSONSaverEdgeCases:
    """Тесты граничных случаев"""

    def setup_method(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'vacancies.json')

    def teardown_method(self):
        shutil.rmtree(self.test_dir)

    def test_large_file(self):
        """Тест работы с большим файлом"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        # Создаем много вакансий
        large_list = [{"title": f"Vacancy {i}", "url": f"url{i}"} for i in range(1000)]

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(large_list, f)

        # Читаем и проверяем
        result = saver._read_vacancies()
        assert len(result) == 1000
        assert result[0]["title"] == "Vacancy 0"
        assert result[999]["title"] == "Vacancy 999"

    def test_unicode_characters(self):
        """Тест с Unicode символами"""
        saver = JSONSaver()
        saver.file_path = self.test_file

        test_data = [
            {"title": "Разработчик Python", "company": "Компания", "description": "Опыт от 3 лет"},
            {"title": "Emoji Test 😊", "company": "Test & Co", "description": "C++/C# разработка"}
        ]

        saver._write_vacancies(test_data)

        # Читаем обратно
        result = saver._read_vacancies()
        assert result == test_data

        # Проверяем, что JSON валидный
        with open(self.test_file, 'r', encoding='utf-8') as f:
            content = f.read()
            json.loads(content)  # Не должно вызывать исключение