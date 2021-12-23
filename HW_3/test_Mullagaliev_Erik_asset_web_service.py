import pytest
from task_Mullagaliev_Erik_asset_web_service import (
    app, 
    parse_cbr_currency_base_daily,
    parse_cbr_key_indicators,
)

CURRENCY_BASE_OUTPUT_RESULT = {
    'AUD': 56.9065, 'AZN': 44.4127, 'AMD': 0.144485, 'BYN': 29.2821,
    'BGN': 46.9816, 'BRL': 14.6235, 'HUF': 0.254265, 'KRW': 0.0681688,
    'HKD': 9.73339, 'DKK': 12.3566, 'USD': 75.4571, 'EUR': 91.9822,
    'INR': 1.02294, 'KZT': 0.179088, 'CAD': 58.5438, 'KGS': 0.930621,
    'CNY': 11.541, 'MDL': 4.3781300000000005, 'TMT': 21.59, 'NOK': 8.66526,
    'PLN': 20.4264, 'RON': 18.8676, 'XDR': 108.8099, 'SGD': 56.5561,
    'TJS': 6.6628799999999995, 'TRY': 9.87607, 'UZS': 0.00720439, 'UAH': 2.65297,
    'GBP': 101.1955, 'CZK': 3.49857, 'SEK': 9.08618, 'CHF': 84.8882,
    'ZAR': 5.169, 'JPY': 0.729265,
}
KEY_INDICATORS_OUTPUT_RESULT = {
    'USD': 75.4571, 'EUR': 91.9822, 'Au': 4529.59, 
    'Ag': 62.52, 'Pt': 2459.96, 'Pd': 5667.14
}

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_can_parse_currency_base_output():
    with open("cbr_text.html") as fin:
        currency_base_search_output_html = fin.read()
    documents = parse_cbr_currency_base_daily(currency_base_search_output_html)
    assert 34 == len(documents)
    assert CURRENCY_BASE_OUTPUT_RESULT == documents

def test_can_parse_key_indicators_output():
    with open("cbr_key.html") as fin:
        key_indicators_search_output_html = fin.read()
    documents = parse_cbr_key_indicators(key_indicators_search_output_html)
    assert 6 == len(documents)
    assert KEY_INDICATORS_OUTPUT_RESULT == documents
