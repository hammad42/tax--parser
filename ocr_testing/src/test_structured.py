import pandas as pd
import pytest
from structured import parse_ocr_json

@pytest.fixture
def sample_ocr_data():
    return [
        {"bounding_box": [[24, 3], [167, 3], [167, 18], [24, 18]], "text": "InvoiceNumber", "confidence": 0.99},
        {"bounding_box": [[23, 37], [209, 37], [209, 52], [23, 52]], "text": "12345", "confidence": 0.99},
        {"bounding_box": [[22, 81], [180, 82], [180, 100], [22, 99]], "text": "Total Amount:", "confidence": 0.95},
        {"bounding_box": [[21, 117], [87, 117], [87, 136], [21, 136]], "text": "500.00", "confidence": 0.99},
    ]

def test_parse_ocr_json_all_keys_found(sample_ocr_data):
    user_keys = ["InvoiceNumber", "Total Amount"]
    df = parse_ocr_json(sample_ocr_data, user_keys)
    assert not df.empty
    assert df.iloc[0]["InvoiceNumber"] == "12345"
    assert df.iloc[0]["Total Amount"] == "500.00"

def test_parse_ocr_json_some_keys_not_found(sample_ocr_data):
    user_keys = ["InvoiceNumber", "NonExistentKey"]
    df = parse_ocr_json(sample_ocr_data, user_keys)
    assert not df.empty
    assert df.iloc[0]["InvoiceNumber"] == "12345"
    assert df.iloc[0]["NonExistentKey"] == ""

def test_parse_ocr_json_empty_ocr_data():
    user_keys = ["InvoiceNumber", "Total Amount"]
    df = parse_ocr_json([], user_keys)
    assert "InvoiceNumber" in df.columns
    assert "Total Amount" in df.columns
    assert df.iloc[0]["InvoiceNumber"] == ""
    assert df.iloc[0]["Total Amount"] == ""

def test_parse_ocr_json_empty_user_keys(sample_ocr_data):
    user_keys = []
    df = parse_ocr_json(sample_ocr_data, user_keys)
    assert df.empty