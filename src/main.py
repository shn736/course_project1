from typing import Any, List, Dict
import pandas as pd
from datetime import datetime, timedelta


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

# print(transactions)


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

target_date = "2020-05-20 15:30:00"
result = filter_and_sort_transactions(transactions, target_date)
print(result)