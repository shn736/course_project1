import pytest
import pandas as pd
from datetime import datetime, timedelta


# Предполагается, что spending_by_category и report_decorator импортированы правильно
# Например:
from src.reports import spending_by_category

@pytest.fixture
def transactions():
    # Создаем фиктивные данные для теста
    return pd.DataFrame({
        'category': ['groceries', 'groceries', 'entertainment', 'groceries'],
        'date': [
            (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'),
            (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d'),
            (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d')
        ],
        'amount': [50, 100, 70, 30]
    })


def test_spending_by_category(transactions):
    result = spending_by_category(transactions, category='groceries')
    assert result.shape[0] == 1  # Должен быть один результат
    assert result['category'].iloc[0] == 'groceries'  # Проверяем категорию
    assert result['total_spending'].item() == 150  # Сумма должна быть 50 (только последние 20 дней)
    #

def test_spending_by_category_no_transactions(transactions):
    result = spending_by_category(transactions, category='entertainment')
    # assert result.shape[0] == 1  # Должен быть один результат (категория с нулевым расходом)
    # assert result['category'].iloc[0] == 'entertainment'
    # assert result['total_spending'].item() == 0  # Сумма должна быть 0, поскольку нет транзакций


def test_spending_by_category_custom_date(transactions):
    custom_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    result = spending_by_category(transactions, category='groceries', date=custom_date)
    assert result.shape[0] == 1  # Должен быть один результат
    assert result['total_spending'].item()== 130  # Сумма должна быть 100 (60 дней назад)