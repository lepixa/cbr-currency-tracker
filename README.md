# CBR Currency Tracker 💱

**Python pet-проект**: загрузка курсов валют ЦБ РФ (USD/EUR/CNY), PostgreSQL, аналитика.

## 🚀 Демо
Загрузить курсы за сегодня

Загрузить курсы на дату

Последние курсы из базы

Курсы из базы на дату

Средний курс за 3 месяца

Выход


## 🛠 Стек

```python
requests + psycopg2-binary
PostgreSQL + XML parsing
date_trunc('month') + AVG()
ON CONFLICT DO NOTHING
```

## 📊 Функционал

| Функция | API ЦБ РФ | PostgreSQL |
|---------|-----------|------------|
| Сегодняшние курсы | `XML_daily.asp` | `INSERT ... ON CONFLICT` |
| Курсы на дату | `date_req=dd/mm/yyyy` | `rate_date + char_code UNIQUE` |
| История | `get_last_selected_rates()` | `ORDER BY rate_date DESC` |
| Аналитика | - | `AVG(value)` за 3 месяца |

## 🏃‍♂️ Запуск

```bash
git clone https://github.com/lepixa/cbr-currency-tracker
cd cbr-currency-tracker
pip install -r requirements.txt
py main.py
```

## 🔄 Автоматизация

```python
# load_last_3_months.py — за 90+ дней истории
for date in daterange(start_date, end_date):
    rates = client.get_selected_rates(date_req=date_str)
```

## 📈 Что дальше

- `.env` + `python-dotenv`
- Task Scheduler daily job
- Streamlit dashboard
- MLflow для MLOps

---
**lepixa/cbr-currency-tracker** — [github.com/lepixa/cbr-currency-tracker](https://github.com/lepixa/cbr-currency-tracker)