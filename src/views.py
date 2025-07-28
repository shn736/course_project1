from src.utils import load_user_settings, reading_operations_excel, filter_and_sort_transactions, calculate_card_data
from src.utils import get_top_transactions, get_currency_rates, get_stock_prices, get_greeting
import json


def json_answer(target_date: str) -> str:
    """Функция для страницы «Главная»"""
    user_settings = load_user_settings('../user_settings.json')
    user_currencies = user_settings['user_currencies']
    user_stocks = user_settings['user_stocks']
    transactions = reading_operations_excel(transactions_excel='../data/operations.xlsx')
    filtered_transactions = filter_and_sort_transactions(transactions, target_date)
    cards_data = calculate_card_data(filtered_transactions)
    top_transactions = get_top_transactions(filtered_transactions)
    currency_rates = get_currency_rates(user_currencies)
    stock_prices = get_stock_prices(user_stocks)
    response = {
        "greeting": get_greeting(),
        "cards": cards_data,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(response, ensure_ascii=False, indent=4)
