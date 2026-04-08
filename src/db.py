import psycopg2
from datetime import datetime
from src.config import DB_CONFIG


def get_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"]
    )


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS currency_rates (
            id SERIAL PRIMARY KEY,
            rate_date DATE NOT NULL,
            char_code VARCHAR(10) NOT NULL,
            nominal INTEGER NOT NULL,
            value NUMERIC(12, 4) NOT NULL,
            currency_name VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'unique_rate_per_day'
            ) THEN
                ALTER TABLE currency_rates
                ADD CONSTRAINT unique_rate_per_day UNIQUE (rate_date, char_code);
            END IF;
        END
        $$;
    """)

    conn.commit()
    cur.close()
    conn.close()


def save_rates(rates):
    conn = get_connection()
    cur = conn.cursor()

    inserted = 0

    for rate in rates:
        rate_date = datetime.strptime(rate["rate_date"], "%d.%m.%Y").date()

        cur.execute("""
            INSERT INTO currency_rates (rate_date, char_code, nominal, value, currency_name)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (rate_date, char_code) DO NOTHING
        """, (
            rate_date,
            rate["char_code"],
            rate["nominal"],
            rate["value"],
            rate["currency_name"]
        ))

        if cur.rowcount > 0:
            inserted += 1

    conn.commit()
    cur.close()
    conn.close()
    return inserted


def get_last_selected_rates(limit=20):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT rate_date, char_code, nominal, value, currency_name
        FROM currency_rates
        WHERE char_code IN ('USD', 'EUR', 'CNY')
        ORDER BY rate_date DESC, char_code
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_rates_by_date(rate_date):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT rate_date, char_code, nominal, value, currency_name
        FROM currency_rates
        WHERE rate_date = %s
          AND char_code IN ('USD', 'EUR', 'CNY')
        ORDER BY char_code
    """, (rate_date,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_average_rates_last_3_full_months():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            char_code,
            ROUND(AVG(value), 4) AS avg_value
        FROM currency_rates
        WHERE char_code IN ('USD', 'EUR', 'CNY')
          AND rate_date >= date_trunc('month', current_date) - interval '3 months'
          AND rate_date < date_trunc('month', current_date)
        GROUP BY char_code
        ORDER BY char_code
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows