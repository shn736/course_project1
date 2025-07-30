import pandas as pd
from src.views import json_answer
from src.reports import spending_by_category
from src.services import get_json_transfers


result = json_answer("2020-05-30 15:30:00")
print(result)

data = {
    'date': ['2025-05-10', '2025-05-15', '2025-06-20', '2025-07-25'],
    'amount': [100, 200, 300, 150],
    'category': ['Food', 'Food', 'Transport', 'Food']
}
transactions_df = pd.DataFrame(data)
result = spending_by_category(transactions_df, 'Food')
print(result)

transactions = [
    {"category": "Переводы", "description": "Валерий А."},
    {"category": "Переводы", "description": "Сергей З."},
    {"category": "Покупка", "description": "Книга"},
    {"category": "Переводы", "description": "Артем П."},
    {"category": "Переводы", "description": "Недопустимое Имя"},]

json_result = get_json_transfers(transactions)
print(json_result)
