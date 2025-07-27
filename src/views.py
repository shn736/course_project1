from typing import Any

from src.utils import load_user_settings, reading_operations_excel, filter_and_sort_transactions, calculate_card_data
from src.utils import get_top_transactions, get_currency_rates, get_stock_prices, get_greeting
import json


def main(target_date: str) -> str:
    # Настройки
    user_settings = load_user_settings('../user_settings.json')
    user_currencies = user_settings['user_currencies']
    user_stocks = user_settings['user_stocks']
    # Загрузка транзакций
    transactions = reading_operations_excel(transactions_excel='../data/operations.xlsx')
    # Фильтрация транзакций по дате
    filtered_transactions = filter_and_sort_transactions(transactions, target_date)
    # Получение данных по картам
    cards_data = calculate_card_data(filtered_transactions)
    # Получение Топ-5 транзакций
    top_transactions = get_top_transactions(filtered_transactions)
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


if __name__ == "__main__":
    result = main("2020-05-30 15:30:00")
    print(result)
