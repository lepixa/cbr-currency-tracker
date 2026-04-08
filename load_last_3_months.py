from datetime import date, timedelta
from src.api import CBRAPIClient
from src.db import create_table, save_rates


def get_last_3_full_months_range():
    today = date.today()
    first_day_current_month = today.replace(day=1)

    end_date = first_day_current_month - timedelta(days=1)
    start_month = (first_day_current_month.month - 3) % 12
    start_year = first_day_current_month.year

    if start_month <= 0:
        start_month += 12
        start_year -= 1

    start_date = date(start_year, start_month, 1)
    return start_date, end_date


def daterange(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)


def main():
    create_table()
    client = CBRAPIClient()

    start_date, end_date = get_last_3_full_months_range()
    print(f"Загружаем данные с {start_date} по {end_date}")

    total_inserted = 0
    total_days = 0

    for current_date in daterange(start_date, end_date):
        date_str = current_date.strftime("%d/%m/%Y")
        print(f"\nДата: {date_str}")

        try:
            rates = client.get_selected_rates(date_req=date_str)
            inserted = save_rates(rates)
            total_inserted += inserted
            total_days += 1
            print(f"Получено валют: {len(rates)} | Сохранено новых: {inserted}")
        except Exception as e:
            print(f"Ошибка на дате {date_str}: {e}")

    print("\nГотово!")
    print(f"Обработано дней: {total_days}")
    print(f"Всего новых записей сохранено: {total_inserted}")


if __name__ == "__main__":
    main()