from typing import Any, List, Dict
import pandas as pd
from datetime import datetime, timedelta


def main(date_str):
    # Настройки
    user_settings = load_user_settings('../user_settings.json')
    user_currencies = user_settings['user_currencies']
    user_stocks = user_settings['user_stocks']

    # Определение диапазона дат
    request_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    start_date = request_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_date = request_date

    # Загрузка транзакций
    transactions = load_transactions('../data/operations.xlsx')

    # Фильтрация транзакций по дате
    #filtered_transactions = filter_transactions(transactions, start_date, end_date)

    # Получение данных по картам
    cards_data = calculate_card_data(transactions)

    # Получение Топ-5 транзакций
    top_transactions = get_top_transactions(transactions)

    # Получение курсов валют
    currency_rates = get_currency_rates(user_currencies)

    # Получение стоимости акций
    stock_prices = get_stock_prices(user_stocks)

    # Формирование JSON-ответа
    response = {
        "greeting": get_greeting(),
        "cards": cards_data,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(response, ensure_ascii=False, indent=4)
