import json
import os

import pandas as pd
import requests
from datetime import datetime
from typing import Any, List, Dict
from dotenv import load_dotenv


def get_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_user_settings(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def reading_operations_excel(transactions_excel: str) -> Any:
    """считывает финансовые операции из Excel выдает список словарей с транзакциями"""
    try:
        df = pd.read_excel(transactions_excel)
        list_transaction_excel = df.to_dict(orient='records')
        return list_transaction_excel
    except FileNotFoundError:
        return f"Ошибка: Файл не найден по указанному пути: {transactions_excel}"
    except ValueError:
        return "Ошибка: Не удалось прочитать файл. Убедитесь, что это файл Excel."
    except Exception as e:
        return f"Произошла ошибка: {e}"


def parse_date(date_str: str) -> datetime:
    """Парсит дату из строки в формате 'dd.mm.yyyy'."""
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


def search_parse_date(search_date_str: str) -> datetime:
    """Парсит дату из строки в формате 'dd.mm.yyyy'."""
    return datetime.strptime(search_date_str, "%d.%m.%Y %H:%M:%S")


def get_first_day_of_month(date: datetime) -> datetime:
    """Возвращает первое число месяца заданной даты."""
    return date.replace(day=1)


def filter_and_sort_transactions(transactions: List[Dict[str, str]], target_date_str: str) -> List[Dict[str, str]]:
    """Фильтрует и сортирует транзакции по дате в заданном диапазоне."""
    target_date = parse_date(target_date_str)
    start_date = get_first_day_of_month(target_date)
    filtered_transactions = [
        txn for txn in transactions
        if start_date <= search_parse_date(txn['Дата операции']) <= target_date
    ]
    sorted_transactions = sorted(filtered_transactions, key=lambda x: search_parse_date(x['Дата операции']))
    return sorted_transactions


def calculate_card_data(transactions):
    card_data = {}
    for transaction in transactions:
        card_last_digits = str(transaction['Номер карты'])[-4:]
        amount = transaction['Сумма операции']
        if card_last_digits not in card_data:
            card_data[card_last_digits] = {'Общая сумма расходов': 0, 'Кешбэк': 0}
        card_data[card_last_digits]['Общая сумма расходов'] += round(amount)
        card_data[card_last_digits]['Кешбэк'] += round(amount / 100)  # 1 рубль на каждые 100 рублей
    return card_data


def get_top_transactions(transactions, top_n=5):
    """Возвращает топ-N транзакций по сумме платежа."""
    return sorted(transactions, key=lambda x: x["Сумма операции"], reverse=True)[:top_n]


load_dotenv('../.env')
API_KEY = os.getenv('API_KEY')
API_KEY_STOCK2 = os.getenv('API_KEY_STOCK2')


def get_currency_rates(user_currencies):
    rates = {}
    for currency in user_currencies:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
        headers = {"apikey": API_KEY}
        payload = {}
        response = requests.get(url, headers=headers, data=payload)
        rates[currency] = response.json().get('rates', {}).get('RUB')
    return rates


def get_stock_prices(user_stocks):
    stock_prices = {}
    for stock in user_stocks:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={API_KEY_STOCK2}'
        response = requests.get(url)
        if response.ok:
            stock_prices[stock] = response.json().get("Global Quote").get('05. price', None)
    return stock_prices


def main(target_date):
    # Настройки
    user_settings = load_user_settings('../user_settings.json')
    print(user_settings)
    user_currencies = user_settings['user_currencies']
    print(user_currencies)
    user_stocks = user_settings['user_stocks']
    print(user_stocks)

    # Загрузка транзакций
    transactions = reading_operations_excel(transactions_excel='../data/operations.xlsx')
    print(transactions)
    # Фильтрация транзакций по дате
    filtered_transactions = filter_and_sort_transactions(transactions, target_date)
    print(filtered_transactions)
    # Получение данных по картам
    cards_data = calculate_card_data(filtered_transactions)
    print(cards_data)
    # Получение Топ-5 транзакций
    top_transactions = get_top_transactions(filtered_transactions)
    print(top_transactions)
    # Получение курсов валют
    currency_rates = get_currency_rates(user_currencies)
    print(currency_rates)
    # Получение стоимости акций
    stock_prices = get_stock_prices(user_stocks)
    print(stock_prices)
    # Формирование JSON-ответа
    response = {
        "greeting": get_greeting(),
        "cards": cards_data,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(response, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    result = main("2020-05-30 15:30:00")
    print(result)
