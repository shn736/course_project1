import json
import os
import logging
import pandas as pd
import requests
from datetime import datetime
from typing import Any, Dict
from dotenv import load_dotenv


logger = logging.getLogger('utils')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('C:/Users/shn-7/PycharmProjects/course_project1/logs/utils.log')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_greeting() -> str:
    """Определяет время суток"""
    current_hour = datetime.now().hour
    logger.info('Определяем время суток')
    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_user_settings(filepath: Any) -> Any:
    """Считывает пользовательские настройки"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def reading_operations_excel(transactions_excel: str) -> Any:
    """считывает финансовые операции из Excel выдает список словарей с транзакциями"""
    try:
        logger.info('Распаковываем EXCEL файл')
        df = pd.read_excel(transactions_excel)
        list_transaction_excel = df.to_dict(orient='records')
        return list_transaction_excel
    except FileNotFoundError:
        logger.error('Файл не найден')
        return f"Ошибка: Файл не найден по указанному пути: {transactions_excel}"
    except ValueError:
        logger.error('Не удалось прочитать файл')
        return "Ошибка: Не удалось прочитать файл. Убедитесь, что это файл Excel."
    except Exception as e:
        logger.error(f'Произошла ошибка {e}')
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


def filter_and_sort_transactions(transactions: dict, target_date_str: str) -> list[Any]:
    """Фильтрует и сортирует транзакции по дате в заданном диапазоне."""
    logger.info('Фильтруем и сортируем транзакции по дате в заданном диапазоне')
    target_date = parse_date(target_date_str)
    start_date = get_first_day_of_month(target_date)
    filtered_transactions = [
        txn for txn in transactions
        if start_date <= search_parse_date(txn['Дата операции']) <= target_date
    ]
    sorted_transactions = sorted(filtered_transactions, key=lambda x: search_parse_date(x['Дата операции']))
    return sorted_transactions


def calculate_card_data(transactions: list[Any]) -> Dict:
    """Выводим информацию по каждой карте"""
    logger.info('Выводим информацию по каждой карте')
    card_data = {}
    for transaction in transactions:
        card_last_digits = str(transaction['Номер карты'])[-4:]
        amount = transaction['Сумма операции']
        if card_last_digits not in card_data:
            card_data[card_last_digits] = {'Общая сумма расходов': 0, 'Кешбэк': 0}
        card_data[card_last_digits]['Общая сумма расходов'] += round(amount)
        card_data[card_last_digits]['Кешбэк'] += round(amount / 100)  # 1 рубль на каждые 100 рублей
    return card_data


def get_top_transactions(transactions: list[Any], top_n: int = 5) -> list[Any]:
    """Возвращает топ-N транзакций по сумме платежа."""
    logger.info('Возвращает топ-5 транзакций по сумме платежа')
    return sorted(transactions, key=lambda x: x["Сумма операции"], reverse=True)[:top_n]


load_dotenv('../.env')
API_KEY = os.getenv('API_KEY')
API_KEY_STOCK2 = os.getenv('API_KEY_STOCK2')


def get_currency_rates(user_currencies: list) -> dict:
    """Выводит курсы валют"""
    logger.info('Выводим курсы валют')
    rates = {}
    for currency in user_currencies:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
        headers = {"apikey": API_KEY}
        payload: dict = {}
        response = requests.get(url, headers=headers, data=payload)
        rates[currency] = response.json().get('rates', {}).get('RUB')
    return rates


def get_stock_prices(user_stocks: list) -> dict:
    """Выводим стоимость акций из S&P500"""
    logger.info('Выводим стоимость акций из S&P500')
    stock_prices = {}
    for stock in user_stocks:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={API_KEY_STOCK2}'
        response = requests.get(url)
        print(response.text)
        if response.ok:
            stock_prices[stock] = response.json().get("Global Quote").get('05. price', None)
    return stock_prices
