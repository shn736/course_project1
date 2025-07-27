import pytest
import json
from src.services import get_json_transfers


def test_get_json_transfers():
    transactions = [
        {"category": "Переводы", "description": "Валерий А."},
        {"category": "Переводы", "description": "Сергей З."},
        {"category": "Покупка", "description": "Книга"},
        {"category": "Переводы", "description": "Артем П."},
        {"category": "Переводы", "description": "Недопустимое Имя"}
    ]

    expected_result = json.dumps([
        {"category": "Переводы", "description": "Валерий А."},
        {"category": "Переводы", "description": "Сергей З."},
        {"category": "Переводы", "description": "Артем П."}
    ], ensure_ascii=False)

    assert get_json_transfers(transactions) == expected_result
