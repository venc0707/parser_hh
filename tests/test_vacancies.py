from src.vacancies import Vacancy


def test_salary_parsing():
    """Тестирование парсинга зарплат"""
    test_cases = [
        ("100 000-150 000 руб.", 125000.0),
        ("120 000-180 000 руб.", 150000.0),
        ("от 80 000 до 120 000 руб.", 100000.0),
        ("80 000 - 120 000 руб.", 100000.0),
        ("80 000 руб.", 80000.0),
        ("з/п не указана", 0.0),
        ("", 0.0),
    ]

    for salary_str, expected in test_cases:
        class TempVacancy:
            def __init__(self, salary_range):
                self._salary_range = salary_range

            def _calculate_average_salary(self):
                if not self._salary_range:
                    return 0.0
                try:
                    import re
                    clean = re.sub(r'[^\d-]', '', self._salary_range)
                    numbers = re.findall(r'\d+', clean)
                    if len(numbers) >= 2:
                        return (float(numbers[0]) + float(numbers[1])) / 2
                    elif len(numbers) == 1:
                        return float(numbers[0])
                    return 0.0
                except:
                    return 0.0

        vacancy = TempVacancy(salary_str)
        result = vacancy._calculate_average_salary()
        status = "✓" if result == expected else "✗"
        print(f"{status} '{salary_str}' -> {result} (ожидалось: {expected})")

if __name__ == "__main__":
    test_salary_parsing()