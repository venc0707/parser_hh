from vacancies import Vacancy
from job_api import HeadHunterAPI
from saver_json import JSONSaver


def user_interaction():
    """ Функция для взаимодействия с пользователем через консоль """

    print("=" * 60)
    print("ПОИСК И АНАЛИЗ ВАКАНСИЙ С HH.RU")
    print("=" * 60)

    # Инициализация объектов
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver("vacancies.json")

    loaded_vacancies = []

    while True:
        print("\n" + "=" * 60)
        print("ГЛАВНОЕ МЕНЮ")
        print("=" * 60)
        print("1. 🔍 Поиск вакансий на HH.ru")
        print("2. 📊 Топ N вакансий по зарплате")
        print("3. 🔑 Поиск вакансий по ключевому слову в описании")
        print("4. 💾 Сохранить текущие вакансии в файл")
        print("5. 📁 Загрузить вакансии из файла")
        print("6. 👀 Показать все загруженные вакансии")
        print("7. 🗑️ Очистить список вакансий")
        print("8. 💰 Фильтр по зарплате (от)")
        print("9. 📋 Показать статистику")
        print("10. 🗂️ Очистить файл от всех вакансий")
        print("0. 🔚 Выход")
        print("-" * 60)

        try:
            choice = input("Выберите действие (0-10): ").strip()

            if choice == "0":
                print("\nДо свидания!")
                break

            elif choice == "1":
                # Поиск вакансий на HH.ru
                search_query = input("Введите поисковый запрос (например: 'Python разработчик'): ").strip()
                if not search_query:
                    print("❌ Поисковый запрос не может быть пустым!")
                    continue

                try:
                    per_page = int(input("Сколько вакансий загрузить (макс. 100)?: ").strip() or "50")
                    per_page = min(per_page, 100)  # Ограничение API
                except ValueError:
                    per_page = 50

                print(f"\n⏳ Ищу вакансии '{search_query}'...")

                try:
                    vacancies_data = hh_api.get_vacancies(search_query, per_page)
                    loaded_vacancies = []

                    for item in vacancies_data:
                        try:
                            vacancy = Vacancy(
                                title=item.get('name', ''),
                                company=item.get('employer', {}).get('name', ''),
                                url=item.get('alternate_url', ''),
                                salary_range=parse_salary(item.get('salary')),
                                description=parse_description(item),
                                # Дополнительные поля если нужно
                            )
                            loaded_vacancies.append(vacancy)
                        except Exception as e:
                            print(f"Ошибка при создании вакансии: {e}")
                            continue

                    print(f"✅ Найдено и загружено {len(loaded_vacancies)} вакансий")

                except Exception as e:
                    print(f"❌ Ошибка при поиске вакансий: {e}")

            elif choice == "2":
                # Топ N вакансий по зарплате
                if not loaded_vacancies:
                    print("❌ Нет загруженных вакансий. Сначала выполните поиск (пункт 1).")
                    continue

                try:
                    n = int(input(f"Сколько вакансий показать (всего {len(loaded_vacancies)})?: ").strip())
                    n = min(n, len(loaded_vacancies))
                except ValueError:
                    n = 10

                # Сортируем по убыванию зарплаты
                sorted_vacancies = sorted(loaded_vacancies, key=lambda x: x.average_salary, reverse=True)

                print(f"\n🏆 ТОП-{n} ВАКАНСИЙ ПО ЗАРПЛАТЕ:")
                print("=" * 80)

                for i, vacancy in enumerate(sorted_vacancies[:n], 1):
                    print(f"{i}. {vacancy.title}")
                    print(f"   Компания: {vacancy.company}")
                    print(f"   Зарплата: {vacancy.salary_range or 'Не указана'}")
                    print(f"   Средняя: {vacancy.average_salary:,.0f} руб.")
                    print(f"   Город: {getattr(vacancy, 'city', 'Не указан')}")
                    print(f"   URL: {vacancy.url}")
                    print("-" * 80)

            elif choice == "3":
                # Поиск по ключевому слову в описании
                if not loaded_vacancies:
                    print("❌ Нет загруженных вакансий. Сначала выполните поиск (пункт 1).")
                    continue

                keyword = input("Введите ключевое слово для поиска в описании: ").strip().lower()
                if not keyword:
                    print("❌ Ключевое слово не может быть пустым!")
                    continue

                found_vacancies = []
                for vacancy in loaded_vacancies:
                    if (keyword in vacancy.title.lower() or
                            keyword in vacancy.description.lower() or
                            keyword in vacancy.company.lower()):
                        found_vacancies.append(vacancy)

                print(f"\n🔎 Найдено {len(found_vacancies)} вакансий с ключевым словом '{keyword}':")
                print("=" * 80)

                for i, vacancy in enumerate(found_vacancies, 1):
                    print(f"{i}. {vacancy.title}")
                    print(f"   Компания: {vacancy.company}")
                    print(f"   Зарплата: {vacancy.salary_range or 'Не указана'}")
                    # Показываем фрагмент описания с ключевым словом
                    desc = vacancy.description
                    if keyword in desc.lower():
                        idx = desc.lower().find(keyword)
                        start = max(0, idx - 50)
                        end = min(len(desc), idx + len(keyword) + 50)
                        snippet = desc[start:end]
                        if start > 0:
                            snippet = "..." + snippet
                        if end < len(desc):
                            snippet = snippet + "..."
                        print(f"   Описание: {snippet}")
                    print("-" * 80)

            elif choice == "4":
                # Сохранение в файл
                if not loaded_vacancies:
                    print("❌ Нет вакансий для сохранения.")
                    continue

                save_all = input("Сохранить все вакансии? (y/n): ").strip().lower() == 'y'

                if save_all:
                    for vacancy in loaded_vacancies:
                        json_saver.add_vacancy(vacancy)
                    print(f"✅ Все {len(loaded_vacancies)} вакансий сохранены в файл.")
                else:
                    print("\nВыберите вакансии для сохранения (через запятую):")
                    for i, vacancy in enumerate(loaded_vacancies, 1):
                        print(f"{i}. {vacancy.title} - {vacancy.company}")

                    try:
                        indices = input("Номера вакансий: ").strip()
                        if indices:
                            indices = [int(idx.strip()) - 1 for idx in indices.split(',')]
                            for idx in indices:
                                if 0 <= idx < len(loaded_vacancies):
                                    json_saver.add_vacancy(loaded_vacancies[idx])
                            print(f"✅ Сохранено {len(indices)} вакансий.")
                        else:
                            print("❌ Не выбрано ни одной вакансии.")
                    except ValueError:
                        print("❌ Ошибка ввода. Используйте номера через запятую.")

            elif choice == "5":
                # Загрузка из файла
                try:
                    file_vacancies = json_saver.get_all_vacancies()
                    if file_vacancies:
                        loaded_vacancies = []
                        for v_dict in file_vacancies:
                            vacancy = Vacancy(
                                title=v_dict.get('title', ''),
                                company=v_dict.get('company', ''),
                                url=v_dict.get('url', ''),
                                salary_range=v_dict.get('salary_range'),
                                description=v_dict.get('description', '')
                            )
                            loaded_vacancies.append(vacancy)
                        print(f"✅ Загружено {len(loaded_vacancies)} вакансий из файла.")
                    else:
                        print("📭 Файл с вакансиями пуст.")
                except Exception as e:
                    print(f"❌ Ошибка при загрузке из файла: {e}")

            elif choice == "6":
                # Показать все вакансии
                if not loaded_vacancies:
                    print("📭 Нет загруженных вакансий.")
                    continue

                print(f"\n📋 ВСЕ ЗАГРУЖЕННЫЕ ВАКАНСИИ ({len(loaded_vacancies)} шт.):")
                print("=" * 80)

                for i, vacancy in enumerate(loaded_vacancies, 1):
                    print(f"{i}. {vacancy.title}")
                    print(f"   Компания: {vacancy.company}")
                    print(f"   Зарплата: {vacancy.salary_range or 'Не указана'}")
                    print(
                        f"   Средняя: {vacancy.average_salary:,.0f} руб." if vacancy.average_salary > 0 else "   Средняя: Не указана")
                    print(f"   URL: {vacancy.url}")
                    if vacancy.description:
                        desc_preview = vacancy.description[:100] + "..." if len(
                            vacancy.description) > 100 else vacancy.description
                        print(f"   Описание: {desc_preview}")
                    print("-" * 80)

            elif choice == "7":
                # Очистить список
                if loaded_vacancies:
                    confirm = input("Вы уверены, что хотите очистить список вакансий? (y/n): ").strip().lower()
                    if confirm == 'y':
                        loaded_vacancies = []
                        print("✅ Список вакансий очищен.")
                else:
                    print("📭 Список вакансий уже пуст.")

            elif choice == "8":
                # Фильтр по минимальной зарплате
                if not loaded_vacancies:
                    print("❌ Нет загруженных вакансий.")
                    continue

                try:
                    min_salary = float(input("Минимальная зарплата (руб.): ").strip())
                    filtered = [v for v in loaded_vacancies if v.average_salary >= min_salary]

                    print(f"\n💰 ВАКАНСИИ С ЗАРПЛАТОЙ ОТ {min_salary:,.0f} РУБ.:")
                    print(f"Найдено: {len(filtered)} из {len(loaded_vacancies)}")
                    print("=" * 80)

                    for i, vacancy in enumerate(filtered, 1):
                        print(f"{i}. {vacancy.title}")
                        print(f"   Компания: {vacancy.company}")
                        print(f"   Зарплата: {vacancy.salary_range}")
                        print(f"   Средняя: {vacancy.average_salary:,.0f} руб.")
                        print("-" * 80)

                except ValueError:
                    print("❌ Введите корректное число.")

            elif choice == "9":
                # Статистика
                if not loaded_vacancies:
                    print("📭 Нет данных для статистики.")
                    continue

                print("\n📊 СТАТИСТИКА ПО ВАКАНСИЯМ")
                print("=" * 50)
                print(f"Всего вакансий: {len(loaded_vacancies)}")

                # Статистика по зарплатам
                salaries = [v.average_salary for v in loaded_vacancies if v.average_salary > 0]
                if salaries:
                    print(f"Вакансий с указанной зарплатой: {len(salaries)}")
                    print(f"Средняя зарплата: {sum(salaries) / len(salaries):,.0f} руб.")
                    print(f"Максимальная зарплата: {max(salaries):,.0f} руб.")
                    print(f"Минимальная зарплата: {min(salaries):,.0f} руб.")
                else:
                    print("Нет данных о зарплатах")

                # Статистика по компаниям
                companies = {}
                for v in loaded_vacancies:
                    companies[v.company] = companies.get(v.company, 0) + 1

                if companies:
                    print(f"\nУникальных компаний: {len(companies)}")
                    print("Топ-5 компаний по количеству вакансий:")
                    sorted_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5]
                    for company, count in sorted_companies:
                        print(f"  {company}: {count} вакансий")

                # Распределение по городам (если есть атрибут city)
                cities = {}
                for v in loaded_vacancies:
                    city = getattr(v, 'city', 'Не указан')
                    cities[city] = cities.get(city, 0) + 1

                if cities:
                    print(f"\nРаспределение по городам:")
                    for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True):
                        print(f"  {city}: {count} вакансий")

                elif choice == "10":
                    # Очистить файл от всех вакансий
                    try:
                        # Проверяем, есть ли вакансии в файле
                        current_vacancies = json_saver.get_all_vacancies()
                        if not current_vacancies:
                            print("📭 Файл с вакансиями уже пуст.")
                            continue

                        print(f"\n⚠️  ВНИМАНИЕ! В файле сейчас {len(current_vacancies)} вакансий.")
                        print("Это действие удалит ВСЕ вакансии из файла и их нельзя будет восстановить!")

                        confirm = input(
                            "\nВы уверены, что хотите удалить ВСЕ вакансии из файла? (yes/NO): ").strip().lower()

                        if confirm == 'yes':
                            # Очищаем файл
                            json_saver.clear_file()
                            print("✅ Файл успешно очищен. Все вакансии удалены.")

                            # Если в памяти есть вакансии, спрашиваем удалять ли их тоже
                            if loaded_vacancies:
                                clear_memory = input("Очистить также вакансии в памяти? (y/n): ").strip().lower()
                                if clear_memory == 'y':
                                    loaded_vacancies = []
                                    print("✅ Вакансии в памяти также очищены.")
                        else:
                            print("❌ Операция отменена. Файл не изменен.")

                    except Exception as e:
                        print(f"❌ Ошибка при очистке файла: {e}")

            else:
                print("❌ Неверный выбор. Попробуйте снова.")



        except KeyboardInterrupt:
            print("\n\n⏹️  Программа прервана пользователем.")
            break
        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")


# Вспомогательные функции для парсинга данных из API

def parse_salary(salary_data: dict) -> str:
    """Парсинг данных о зарплате из API HH.ru"""
    if not salary_data:
        return None

    try:
        salary_from = salary_data.get('from')
        salary_to = salary_data.get('to')
        currency = salary_data.get('currency', 'RUR')

        if salary_from and salary_to:
            return f"{salary_from:,} - {salary_to:,} {currency}"
        elif salary_from:
            return f"от {salary_from:,} {currency}"
        elif salary_to:
            return f"до {salary_to:,} {currency}"
        else:
            return None
    except:
        return None


def parse_description(item: dict) -> str:
    """Парсинг описания вакансии из API HH.ru"""
    description = item.get('snippet', {}).get('requirement', '')
    responsibility = item.get('snippet', {}).get('responsibility', '')

    result = ""
    if description:
        result += description
    if responsibility:
        if result:
            result += "\n\n"
        result += responsibility

    return result


# Запуск программы
if __name__ == "__main__":
    user_interaction()