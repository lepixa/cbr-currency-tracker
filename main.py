from datetime import datetime
from src.api import CBRAPIClient
from src.db import (
    create_table,
    save_rates,
    get_last_selected_rates,
    get_rates_by_date,
    get_average_rates_last_3_full_months
)


def print_header():
    print("\n" + "=" * 60)
    print("💱  CBR CURRENCY TRACKER")
    print("Курсы валют ЦБ РФ: USD / EUR / CNY")
    print("=" * 60)


def print_rates(rows):
    if not rows:
        print("\nНет данных.")
        return

    print("\n" + "-" * 60)
    print(f"{'Дата':<12} {'Код':<5} {'Номинал':<10} {'Курс':<12} {'Валюта'}")
    print("-" * 60)

    for row in rows:
        rate_date, char_code, nominal, value, currency_name = row
        print(f"{str(rate_date):<12} {char_code:<5} {nominal:<10} {value:<12} {currency_name}")

    print("-" * 60)


def print_api_rates(rates):
    if not rates:
        print("\nНет данных.")
        return

    print("\n" + "-" * 60)
    print(f"{'Дата':<12} {'Код':<5} {'Номинал':<10} {'Курс':<12} {'Валюта'}")
    print("-" * 60)

    for rate in rates:
        print(
            f"{rate['rate_date']:<12} "
            f"{rate['char_code']:<5} "
            f"{rate['nominal']:<10} "
            f"{rate['value']:<12} "
            f"{rate['currency_name']}"
        )

    print("-" * 60)


def print_average_rows(rows):
    if not rows:
        print("\nНет данных для расчёта среднего за последние 3 полных месяца.")
        return

    print("\n" + "-" * 60)
    print(f"{'Код':<5} {'Средний курс за 3 полных месяца'}")
    print("-" * 60)

    for row in rows:
        char_code, avg_value = row
        print(f"{char_code:<5} {avg_value}")

    print("-" * 60)


def load_today_rates():
    client = CBRAPIClient()
    rates = client.get_selected_rates()
    inserted = save_rates(rates)

    print("\n✅ Курсы за сегодня загружены")
    print(f"Получено валют: {len(rates)}")
    print(f"Сохранено новых записей: {inserted}")

    print_api_rates(rates)


def load_rates_by_date():
    date_input = input("\nВведите дату в формате ДД/ММ/ГГГГ: ").strip()

    try:
        datetime.strptime(date_input, "%d/%m/%Y")
    except ValueError:
        print("❌ Неверный формат даты. Пример: 08/04/2026")
        return

    client = CBRAPIClient()
    rates = client.get_selected_rates(date_req=date_input)
    inserted = save_rates(rates)

    print("\n✅ Курсы на выбранную дату загружены")
    print(f"Получено валют: {len(rates)}")
    print(f"Сохранено новых записей: {inserted}")

    print_api_rates(rates)


def show_last_rates():
    rows = get_last_selected_rates()
    print("\n📋 Последние сохранённые курсы")
    print_rates(rows)


def show_rates_for_date():
    date_input = input("\nВведите дату из базы в формате ДД.ММ.ГГГГ: ").strip()

    try:
        db_date = datetime.strptime(date_input, "%d.%m.%Y").date()
    except ValueError:
        print("❌ Неверный формат даты. Пример: 08.04.2026")
        return

    rows = get_rates_by_date(db_date)
    print(f"\n📅 Курсы из базы за {db_date}")
    print_rates(rows)


def show_average_last_3_full_months():
    rows = get_average_rates_last_3_full_months()
    print("\n📊 Средний курс за последние 3 полных месяца")
    print_average_rows(rows)


def main():
    create_table()

    while True:
        print_header()
        print("1. Загрузить курсы за сегодня")
        print("2. Загрузить курсы на конкретную дату")
        print("3. Показать последние сохранённые курсы")
        print("4. Показать курсы из базы на дату")
        print("5. Показать средний курс за последние 3 полных месяца")
        print("6. Выход")

        choice = input("\nВыбери пункт меню: ").strip()

        if choice == "1":
            load_today_rates()
        elif choice == "2":
            load_rates_by_date()
        elif choice == "3":
            show_last_rates()
        elif choice == "4":
            show_rates_for_date()
        elif choice == "5":
            show_average_last_3_full_months()
        elif choice == "6":
            print("\nПока!")
            break
        else:
            print("\n❌ Неверный пункт меню. Попробуй ещё раз.")


if __name__ == "__main__":
    main()