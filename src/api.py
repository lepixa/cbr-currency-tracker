import requests
import xml.etree.ElementTree as ET
from datetime import datetime


class CBRAPIClient:
    def __init__(self):
        self.url = "https://www.cbr.ru/scripts/XML_daily.asp"

    def get_daily_rates(self, date_req=None):
        params = {}

        if date_req:
            datetime.strptime(date_req, "%d/%m/%Y")
            params["date_req"] = date_req

        print("Идёт запрос к ЦБ РФ...")
        response = requests.get(self.url, params=params, timeout=15)
        print("Ответ получен, статус:", response.status_code)

        response.raise_for_status()

        root = ET.fromstring(response.content)
        rate_date = root.attrib.get("Date")
        rates = []

        for valute in root.findall("Valute"):
            char_code = valute.find("CharCode").text
            nominal = int(valute.find("Nominal").text)
            name = valute.find("Name").text
            value_text = valute.find("Value").text
            value = float(value_text.replace(",", "."))

            rates.append({
                "rate_date": rate_date,
                "char_code": char_code,
                "nominal": nominal,
                "value": value,
                "currency_name": name
            })

        return rates

    def get_selected_rates(self, date_req=None, codes=None):
        if codes is None:
            codes = ["USD", "EUR", "CNY"]

        rates = self.get_daily_rates(date_req=date_req)
        return [rate for rate in rates if rate["char_code"] in codes]