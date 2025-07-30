import json
import pytest
from unittest.mock import patch, mock_open
from src.utils import (
    get_greeting,
    load_user_settings,
    filter_and_sort_transactions,
    calculate_card_data,
    get_top_transactions,
    get_currency_rates,
    get_stock_prices,
)


@pytest.fixture
def mock_transactions():
    """Фикстура для тестирования операций."""
    return [
        {'Номер карты': '1234567890123456', 'Сумма операции': 100, 'Дата операции': '01.10.2023 14:00:00'},
        {'Номер карты': '1234567890123456', 'Сумма операции': 200, 'Дата операции': '02.10.2023 15:00:00'},
        {'Номер карты': '6543210987654321', 'Сумма операции': 300, 'Дата операции': '30.09.2023 16:00:00'},
    ]


@pytest.fixture
def mock_file_data():
    """Фикстура для загрузки пользовательских настроек."""
    return json.dumps({'setting1': 'value1', 'setting2': 'value2'})


def test_load_user_settings(mock_file_data):
    """Тестируем загрузку пользовательских настроек."""
    with patch("builtins.open", mock_open(read_data=mock_file_data)):
        settings = load_user_settings("fake_path.json")
        assert settings == {'setting1': 'value1', 'setting2': 'value2'}


def test_filter_and_sort_transactions(mock_transactions):
    """Тестируем фильтрацию и сортировку транзакций."""
    result = filter_and_sort_transactions(mock_transactions, '2023-10-02 17:00:00')
    assert result == [
        {'Номер карты': '1234567890123456', 'Сумма операции': 200, 'Дата операции': '02.10.2023 15:00:00'},
    ]


def test_calculate_card_data(mock_transactions):
    """Тестируем расчёт данных по картам."""
    result = calculate_card_data(mock_transactions)
    assert result == {
        '3456': {'Общая сумма расходов': 300, 'Кешбэк': 3},
        '4321': {'Общая сумма расходов': 300, 'Кешбэк': 3},
    }


def test_get_top_transactions(mock_transactions):
    """Тестируем получение топ-N транзакций."""
    result = get_top_transactions(mock_transactions, top_n=2)
    assert result == [
        {'Номер карты': '6543210987654321', 'Сумма операции': 300, 'Дата операции': '30.09.2023 16:00:00'},
        {'Номер карты': '1234567890123456', 'Сумма операции': 200, 'Дата операции': '02.10.2023 15:00:00'},
    ]


@patch('requests.get')
def test_get_currency_rates(mock_get):
    """Тестируем получение курсов валют."""
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {'rates': {'RUB': 70.0}}

    rates = get_currency_rates(['USD', 'EUR'])
    assert rates['USD'] == 70.0
    assert rates['EUR'] == 70.0


@patch('requests.get')
def test_get_stock_prices(mock_get):
    """Тестируем получение цен акций."""
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {'Global Quote': {'05. price': '150.00'}}

    prices = get_stock_prices(['AAPL', 'GOOGL'])
    assert prices['AAPL'] == '150.00'
    assert prices['GOOGL'] == '150.00'


@pytest.mark.parametrize("hour, expected_greeting", [
    (6, "Доброе утро"),
    (12, "Добрый день"),
    (15, "Добрый день"),
    (18, "Добрый вечер"),
    (22, "Добрый вечер"),
    (0, "Доброй ночи"),
    (4, "Доброй ночи"),
])
def test_get_greeting(hour, expected_greeting):
    """тестируем время суток"""
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value.hour = hour
        assert get_greeting() == expected_greeting
