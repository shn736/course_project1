import json
import pytest
from unittest import mock

# Предполагая, что ваша функция json_answer находится в модуле my_module
from src.views import json_answer

# Пример данных, которые могут возвращаться загружаемыми функциями
mock_user_settings = {
    'user_currencies': ['USD', 'EUR'],
    'user_stocks': ['AAPL', 'GOOGL']
}
mock_transactions = [
    {'date': '2023-10-01', 'amount': 100, 'currency': 'USD'},
    {'date': '2023-10-02', 'amount': 200, 'currency': 'EUR'},
]
mock_filtered_transactions = [
    {'date': '2023-10-01', 'amount': 100, 'currency': 'USD'}
]
mock_card_data = {'balance': 300}
mock_top_transactions = [{'date': '2023-10-01', 'amount': 100}]
mock_currency_rates = {'USD': 1.0, 'EUR': 0.85}
mock_stock_prices = {'AAPL': 150.0, 'GOOGL': 2800.0}
mock_greeting = "Hello!"


def test_json_answer():
    with mock.patch('src.views.load_user_settings', return_value=mock_user_settings), \
            mock.patch('src.views.reading_operations_excel', return_value=mock_transactions), \
            mock.patch('src.views.filter_and_sort_transactions', return_value=mock_filtered_transactions), \
            mock.patch('src.views.calculate_card_data', return_value=mock_card_data), \
            mock.patch('src.views.get_top_transactions', return_value=mock_top_transactions), \
            mock.patch('src.views.get_currency_rates', return_value=mock_currency_rates), \
            mock.patch('src.views.get_stock_prices', return_value=mock_stock_prices), \
            mock.patch('src.views.get_greeting', return_value=mock_greeting):
        target_date = "2023-10-01"
        result = json_answer(target_date)

        expected_response = {
            "greeting": mock_greeting,
            "cards": mock_card_data,
            "top_transactions": mock_top_transactions,
            "currency_rates": mock_currency_rates,
            "stock_prices": mock_stock_prices,
        }

        assert json.loads(result) == expected_response
