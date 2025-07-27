import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Callable, Any

logger = logging.getLogger('reports')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('../logs/reports.log')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


# Декоратор для записи результатов в файл
def report_decorator(filename: Optional[str] = None) -> Callable:
    if filename is None:
        filename = f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        print(filename)

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Вызов оригинальной функции
            result = func(*args, **kwargs)
            print(result)
            # Запись результата в файл
            with open(filename, 'w') as f:
                json.dump(result.to_dict(orient='records'), f, indent=4)
            logger.info(f'Results written to {filename}')
            return result

        return wrapper

    return decorator


# Функция для получения трат по категории
@report_decorator()  # Декоратор без параметров
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    # Преобразование даты
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    date = datetime.strptime(date, '%Y-%m-%d')

    # Вычисление даты трех месяцев назад
    three_months_ago = date - timedelta(days=90)

    # Фильтрация транзакций
    filtered_transactions = transactions[
        (transactions['category'] == category)
        & (transactions['date'] >= three_months_ago.strftime('%Y-%m-%d'))
        & (transactions['date'] <= date.strftime('%Y-%m-%d'))]

    # Подсчет сумм
    total_spending = filtered_transactions['amount'].sum()

    # Подготовка результата для возврата
    result_list = pd.DataFrame({
        'category': [category],
        'total_spending': [total_spending],
        'date': [str(date.date())]
    })
    print(result_list)
    return result_list


# Пример использования
if __name__ == "__main__":
    # Пример данных
    data = {
        'date': ['2025-05-10', '2025-05-15', '2025-06-20', '2025-07-25'],
        'amount': [100, 200, 300, 150],
        'category': ['Food', 'Food', 'Transport', 'Food']
    }
    transactions_df = pd.DataFrame(data)

    # Запрос трат по категории
    result = spending_by_category(transactions_df, 'Food')
    print(result)
