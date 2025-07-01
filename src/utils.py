import json
import datetime
import random
import pandas as pd
from typing import Any


def get_greeting(current_time):
    """Возвращает приветствие в зависимости от времени суток."""
    if current_time.hour < 6:
        return "Доброй ночи"
    elif 6 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"

print(get_greeting(current_time=datetime.datetime.now().time()))

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

#print(reading_operations_excel(transactions_excel='../data/operations.xlsx'))
transactions = reading_operations_excel(transactions_excel='../data/operations.xlsx')

def get_card_details(transactions):
    """Возвращает последние 4 цифры карты, сумму расходов и кешбэк."""
    card_info = {}
    total_spent = 0

    for transaction in transactions:
        if type(transaction['Номер карты']) == str:
            card_last4 = transaction['Номер карты'][-4:]
            amount = transaction['Сумма операции']
            total_spent += amount

            if card_last4 not in card_info:
                card_info[card_last4] = {
                    "total_spent": 0,
                    "transactions": []
                }

            card_info[card_last4]["total_spent"] += amount
            card_info[card_last4]["transactions"].append(transaction)

        # Добавляем кешбэк
        for card in card_info.values():
            card['Кэшбэк'] = card["total_spent"] // 100  # 1 рубль за 100 рублей

        return card_info

print(get_card_details(transactions))

def get_top_transactions(transactions, top_n=5):
    """Возвращает топ-N транзакций по сумме платежа."""
    return sorted(transactions, key=lambda x: x["Сумма операции"], reverse=True)[:top_n]

print(get_top_transactions(transactions))
def get_currency_rates():
    """Возвращает пример курсов валют (можно получить данные из API для реальных данных)."""
    return {
        "USD": round(random.uniform(60, 100), 2),
        "EUR": round(random.uniform(70, 120), 2),
        "JPY": round(random.uniform(0.5, 1.5), 2)
    }


def get_sp500_stock_prices():
    """Возвращает пример цен акций из S&P500 (можно получить данные из API для реальных данных)."""
    return {
        "AAPL": round(random.uniform(100, 200), 2),
        "GOOGL": round(random.uniform(1000, 3000), 2),
        "AMZN": round(random.uniform(1500, 3500), 2),
        "MSFT": round(random.uniform(200, 300), 2),
        "TSLA": round(random.uniform(600, 900), 2),
    }


def main(date_time_str):
    # Парсинг входной строки с датой и временем
    current_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
