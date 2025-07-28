import json
import re
import logging
from typing import List, Dict

logger = logging.getLogger('services')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('C:/Users/shn-7/PycharmProjects/course_project1/logs/services.log')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def filter_transfers(transactions: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Фильтрует транзакции по критериям: категория 'Переводы'
    и наличие имени и первой буквы фамилии с точкой в описании."""
    filtered_transactions = []
    pattern = r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.$'
    logger.info('Фильтрует транзакции')
    for transaction in transactions:
        if transaction.get('category') == 'Переводы':
            description = transaction.get('description', '')
            if re.match(pattern, description):
                logger.info(f"Добавление транзакции: {transaction}")
                filtered_transactions.append(transaction)

    return filtered_transactions


def get_json_transfers(transactions: List[Dict[str, str]]) -> str:
    """Возвращает JSON со всеми отфильтрованными транзакциями."""
    logger.info('Возвращает JSON со всеми отфильтрованными транзакциями.')
    filtered_data = filter_transfers(transactions)
    return json.dumps(filtered_data, ensure_ascii=False)


if __name__ == "__main__":
    transactions = [
        {"category": "Переводы", "description": "Валерий А."},
        {"category": "Переводы", "description": "Сергей З."},
        {"category": "Покупка", "description": "Книга"},
        {"category": "Переводы", "description": "Артем П."},
        {"category": "Переводы", "description": "Недопустимое Имя"},
    ]

    json_result = get_json_transfers(transactions)
    print(json_result)
