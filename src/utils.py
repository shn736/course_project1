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

user_settings = load_user_settings('../user_settings.json')


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

transactions = reading_operations_excel(transactions_excel='../data/operations.xlsx')


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
    # Фильтрация транзакций по дате
    filtered_transactions = [
        txn for txn in transactions
        if start_date <= search_parse_date(txn['Дата операции']) <= target_date
    ]
    # Сортировка по дате
    sorted_transactions = sorted(filtered_transactions, key=lambda x: search_parse_date(x['Дата операции']))
    return sorted_transactions
target_date = "2020-05-30 15:30:00"
result = filter_and_sort_transactions(transactions, target_date)


def calculate_card_data(transactions):
    card_data = {}
    for transaction in transactions:
        card_last_digits = str(transaction['Номер карты'])[-4:]
        amount = transaction['Сумма операции']
        if card_last_digits not in card_data:
            card_data[card_last_digits] = {'Общая сумма расходов': 0, 'Кешбэк': 0}
        card_data[card_last_digits]['Общая сумма расходов'] += round(amount)
        card_data[card_last_digits]['Кешбэк'] +=  round(amount / 100)  # 1 рубль на каждые 100 рублей
    return card_data

print(calculate_card_data(transactions=result))


def get_top_transactions(transactions, top_n=5):
    """Возвращает топ-N транзакций по сумме платежа."""
    return sorted(transactions, key=lambda x: x["Сумма операции"], reverse=True)[:top_n]

print(get_top_transactions(transactions=result, top_n=5))

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


print(get_currency_rates(user_currencies=user_settings['user_currencies']))

def get_stock_prices(user_stocks):
    stock_prices = {}
    for stock in user_stocks:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={API_KEY_STOCK2}'
        response = requests.get(url)  # Пример API
        print(response.text)
        if response.ok:
            stock_prices[stock] = response.json().get("Global Quote").get('05. price', None)
    return stock_prices

print(get_stock_prices(user_stocks=user_settings['user_stocks']))
# def main(date_str):
#     # Настройки
#     user_settings = load_user_settings('../user_settings.json')
#     user_currencies = user_settings['user_currencies']
#     user_stocks = user_settings['user_stocks']
#
#     # Определение диапазона дат
#     request_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
#     start_date = request_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#     end_date = request_date
#
#     # Загрузка транзакций
#     transactions = load_transactions('../data/operations.xlsx')
#
#     # Фильтрация транзакций по дате
#     #filtered_transactions = filter_transactions(transactions, start_date, end_date)
#
#     # Получение данных по картам
#     cards_data = calculate_card_data(transactions)
#
#     # Получение Топ-5 транзакций
#     top_transactions = get_top_transactions(transactions)
#
#     # Получение курсов валют
#     currency_rates = get_currency_rates(user_currencies)
#
#     # Получение стоимости акций
#     stock_prices = get_stock_prices(user_stocks)
#
#     # Формирование JSON-ответа
#     response = {
#         "greeting": get_greeting(),
#         "cards": cards_data,
#         "top_transactions": top_transactions,
#         "currency_rates": currency_rates,
#         "stock_prices": stock_prices,
#     }
#
#     return json.dumps(response, ensure_ascii=False, indent=4)


# Пример вызова
# if __name__ == "__main__":
#     result = main("2020-05-20 15:30:00")
#     print(result)


















# def get_greeting(current_time):
#     """Возвращает приветствие в зависимости от времени суток."""
#     if current_time.hour < 6:
#         return "Доброй ночи"
#     elif 6 <= current_time.hour < 12:
#         return "Доброе утро"
#     elif 12 <= current_time.hour < 18:
#         return "Добрый день"
#     else:
#         return "Добрый вечер"
#
# print(get_greeting(current_time=datetime.datetime.now().time()))
#
# def reading_operations_excel(transactions_excel: str) -> Any:
#     """считывает финансовые операции из Excel выдает список словарей с транзакциями"""
#     try:
#         df = pd.read_excel(transactions_excel)
#         list_transaction_excel = df.to_dict(orient='records')
#         return list_transaction_excel
#     except FileNotFoundError:
#         return f"Ошибка: Файл не найден по указанному пути: {transactions_excel}"
#     except ValueError:
#         return "Ошибка: Не удалось прочитать файл. Убедитесь, что это файл Excel."
#     except Exception as e:
#         return f"Произошла ошибка: {e}"
#
# #print(reading_operations_excel(transactions_excel='../data/operations.xlsx'))
# transactions = reading_operations_excel(transactions_excel='../data/operations.xlsx')
#
# def get_card_details(transactions):
#     """Возвращает последние 4 цифры карты, сумму расходов и кешбэк."""
#     card_info = {}
#     total_spent = 0
#
#     for transaction in transactions:
#         if type(transaction['Номер карты']) == str:
#             card_last4 = transaction['Номер карты'][-4:]
#             amount = transaction['Сумма операции']
#             total_spent += amount
#
#             if card_last4 not in card_info:
#                 card_info[card_last4] = {
#                     "total_spent": 0,
#                     "transactions": []
#                 }
#
#             card_info[card_last4]["total_spent"] += amount
#             card_info[card_last4]["transactions"].append(transaction)
#
#         # Добавляем кешбэк
#         for card in card_info.values():
#             card['Кэшбэк'] = card["total_spent"] // 100  # 1 рубль за 100 рублей
#
#         return card_info
#
# print(get_card_details(transactions))
#
# def get_top_transactions(transactions, top_n=5):
#     """Возвращает топ-N транзакций по сумме платежа."""
#     return sorted(transactions, key=lambda x: x["Сумма операции"], reverse=True)[:top_n]
#
# print(get_top_transactions(transactions))
# def get_currency_rates():
#     """Возвращает пример курсов валют (можно получить данные из API для реальных данных)."""
#     return {
#         "USD": round(random.uniform(60, 100), 2),
#         "EUR": round(random.uniform(70, 120), 2),
#         "JPY": round(random.uniform(0.5, 1.5), 2)
#     }
#
#
# def get_sp500_stock_prices():
#     """Возвращает пример цен акций из S&P500 (можно получить данные из API для реальных данных)."""
#     return {
#         "AAPL": round(random.uniform(100, 200), 2),
#         "GOOGL": round(random.uniform(1000, 3000), 2),
#         "AMZN": round(random.uniform(1500, 3500), 2),
#         "MSFT": round(random.uniform(200, 300), 2),
#         "TSLA": round(random.uniform(600, 900), 2),
#     }
#
#
# def main(date_time_str):
#     # Парсинг входной строки с датой и временем
#     current_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
