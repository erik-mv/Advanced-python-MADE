"""
This app is Web-server for
CBR CURRENCY BASE DAILY
"""
import requests
from flask import Flask, request, abort, jsonify
from lxml import etree


app = Flask(__name__)
bank = []


CBR_CURRENCY_BASE_DAILY = "https://www.cbr.ru/eng/currency_base/daily/"
CBR_KEY_INDICATORS = "https://www.cbr.ru/eng/key-indicators/"


@app.route("/cbr/daily")
def api_cbr_currency_base_daily():
    """
    This function route api
    cbr currency base daily
    """
    try:
        currency_responce = requests.get(CBR_CURRENCY_BASE_DAILY)
    except TypeError:
        abort(500)
    if not currency_responce.ok:
        abort(500)
    documents = parse_cbr_currency_base_daily(currency_responce.text)
    return documents
# http://127.0.0.1:5000/cbr/daily


def parse_cbr_currency_base_daily(currency_responce_output):
    """
    This function parse
    cbr currency base daily
    """
    root = etree.fromstring(currency_responce_output, etree.HTMLParser())
    documents_raw_collection = root.xpath("//table[@class='data']")
    documents_collection = {}
    for document in documents_raw_collection:
        number_td = len(document.xpath(".//td[1]"))
        for i in range(number_td):
            char_сode = "".join(document.xpath(".//td[2]")[i].itertext())
            unit = "".join(document.xpath(".//td[3]")[i].itertext())
            rate = "".join(document.xpath(".//td[5]")[i].itertext())
            documents_collection[char_сode] = float(rate) / float(unit)
    return documents_collection


@app.route("/cbr/key_indicators")
def api_cbr_key_indicators():
    """
    This function route api
    cbr key indicators
    """
    try:
        key_responce = requests.get(CBR_KEY_INDICATORS)
    except TypeError:
        abort(500)
    if not key_responce.ok:
        abort(500)
    documents = parse_cbr_key_indicators(key_responce.text)
    return documents
# http://127.0.0.1:5000/cbr/key_indicators


def parse_cbr_key_indicators(key_responce_output):
    """
    This function parse
    cbr key indicators
    """
    root = etree.fromstring(key_responce_output, etree.HTMLParser())
    documents_raw_collection = root.xpath(
        "//div[@class='table key-indicator_table']")
    documents_collection = {}
    for document in documents_raw_collection:
        number_div = len(document.xpath(
            ".//div[@class='d-flex title-subinfo']"))
        flag = 1
        if number_div < len(document.xpath(
            ".//td[contains(concat(' ', @class, ' '), 'mono-num')]"
        )):
            flag = 0
        for i in range(number_div):
            char_сode = "".join(document.xpath(
                ".//div[@class='d-flex title-subinfo']"
            )[i][1].itertext())
            if flag:
                rate = "".join(document.xpath(
                    ".//td[contains(concat(' ', @class, ' '), 'mono-num')]"
                )[i].itertext())
            else:
                rate = "".join(document.xpath(
                    ".//td[contains(concat(' ', @class, ' '), 'mono-num')]"
                )[2 * i + 1].itertext())
            rate = rate.replace(",", "")
            documents_collection[char_сode] = float(rate)
    return documents_collection


@app.errorhandler(404)
def page_do_not_found(error):
    """
    This function route
    error 404
    """
    error_list = error
    error_list = error_list or error
    return "This route is not found", 404


@app.errorhandler(500)
def page_do_not_unavailable(error):
    """
    This function route
    error 503
    """
    error_list = error
    error_list = error_list or error
    return "CBR service is unavailable", 503


@app.route("/api/asset/add/<string:char_code>/<string:name>/<int:capital>/<int:interest>")
@app.route("/api/asset/add/<string:char_code>/<string:name>/<int:capital>/<float:interest>")
@app.route("/api/asset/add/<string:char_code>/<string:name>/<float:capital>/<int:interest>")
@app.route("/api/asset/add/<string:char_code>/<string:name>/<float:capital>/<float:interest>")
def asset_add(char_code, name, capital, interest):
    """
    This function route
    add item for list bank
    """
    number_item_bank = len(bank)
    for i in range(number_item_bank):
        if name == bank[i][1]:
            return f"Asset '{name}' is already exist", 403
    bank.append([char_code, name, capital, interest])
    bank.sort()
    return f"Asset '{name}' was successfully added", 200
# http://127.0.0.1:5000/api/asset/add/AZN/myEUR/1000/0.5
# http://127.0.0.1:5000/api/asset/add/EUR/myREUR/2000/0.6
# http://127.0.0.1:5000/api/asset/add/AMD/bamyREUR/2000/0.6
# http://127.0.0.1:5000/api/asset/add/AUD/amyREUR/2000/0.6
# http://127.0.0.1:5000/api/asset/add/USD/dollars/120.0/5.6
# http://127.0.0.1:5000/api/asset/add/EUR/euro/12.0/1.2
# http://127.0.0.1:5000/api/asset/add/Ag/Silver/50.5/10.1
# http://127.0.0.1:5000/api/asset/add/INR/Indian/10.5/99.1
# http://127.0.0.1:5000/api/asset/add/JPY/Yen/1.5/1.7


@app.route("/api/asset/list")
def asset_list():
    """
    This function route
    bild list bank
    """
    return jsonify(bank), 200
# http://127.0.0.1:5000/api/asset/list


@app.route("/api/asset/cleanup")
def asset_cleanup():
    """
    This function route
    clear list bank
    """
    bank.clear()
    return "Asset list was cleanup", 200
# http://127.0.0.1:5000/api/asset/cleanup


@app.route("/api/asset/get")
def asset_get():
    """
    This function route
    get list for name to bank
    """
    result = []
    user_name = request.args.getlist("name")
    number_item_bank = len(bank)
    number_item_name = len(user_name)
    for i in range(number_item_bank):
        for j in range(number_item_name):
            if user_name[j] == bank[i][1]:
                result.append(bank[i])
    result.sort()
    return jsonify(result)
# http://127.0.0.1:5000/api/asset/get?name=myEUR&name=amyREUR


@app.route("/api/asset/calculate_revenue")
def asset_calculate_revenue():
    """
    This function route
    calculate revenue for bank
    """
    try:
        currency_responce = requests.get(CBR_CURRENCY_BASE_DAILY)
    except TypeError:
        abort(500)
    if not currency_responce.ok:
        abort(500)
    documents = parse_cbr_currency_base_daily(currency_responce.text)
    try:
        key_responce = requests.get(CBR_KEY_INDICATORS)
    except TypeError:
        abort(500)
    if not key_responce.ok:
        abort(500)
    documents.update(parse_cbr_key_indicators(key_responce.text))
    user_period = request.args.getlist("period")
    number_item_bank = len(bank)
    number_item_period = len(user_period)
    for i in range(number_item_period):
        user_period[i] = int(user_period[i])
    result = {}
    for i in range(number_item_period):
        revenue = 0
        for j in range(number_item_bank):
            for document in documents:
                if document == bank[j][0]:
                    revenue += bank[j][2] * documents[bank[j][0]] * (
                        (1.0 + bank[j][3]) ** user_period[i] - 1.0
                    )
        result[user_period[i]] = revenue
    return result
# http://127.0.0.1:5000/api/asset/calculate_revenue?period=1&period=2&period=5&period=10
# http://127.0.0.1:5000/api/asset/calculate_revenue?period=1&period=2&period=5
