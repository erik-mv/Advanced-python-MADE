import logging.config
import yaml

from flask import Flask, request, abort, jsonify, render_template
from lxml import etree
import requests


logging.config.dictConfig(yaml.safe_load("""
version: 1
formatters:
    simple:
        format: "Hi from out logger, %(levelname)s from %(name)s: %(message)s"
handlers:
    stream_handler:
        class: logging.StreamHandler
        stream: ext://sys.stderr
        level: DEBUG
        formatter: simple
    file_handler:
        class: logging.FileHandler
        filename: wiki_search_app.log
        level: DEBUG
        formatter: simple
loggers:
    wiki_search_app:
        level: DEBUG
        propagate: False
        handlers:
            - file_handler   
    werkzeug:
        level: DEBUG
        propagate: False
        handlers:
            - file_handler
            - stream_handler
root:
    level: DEBUG
    handlers:
        - stream_handler
"""))


app = Flask(__name__)
WIKI_BASE_URL = "https://en.wikipedia.org"
WIKI_BASE_SEARCH_URL = f"{WIKI_BASE_URL}/w/index.php?search="

@app.route("/search")
def wiki_proxy_search():
    user_query = request.args.get("query", "")
    wiki_responce = requests.get(WIKI_BASE_SEARCH_URL + user_query)
    return wiki_responce.text, wiki_responce.status_code


@app.route("/pretty_search")
def pretty_wiki_proxy_search():
    user_query = request.args.get("query", "")
    wiki_responce = requests.get(WIKI_BASE_SEARCH_URL + user_query)
    if not wiki_responce.ok:
        abort(503)

    documents = parse_wiki_search_output(wiki_responce.text)
    return render_template(
        "wiki_search_result.html",
        query=user_query,
        documents=documents,
        wikipedia_base_url=WIKI_BASE_URL, 
    )


@app.route("/api/search")
def api_wiki_proxy_search():
    user_query = request.args.get("query", "")
    wiki_responce = requests.get(WIKI_BASE_SEARCH_URL + user_query)
    app.logger.debug("got query: %s", user_query)
    if not wiki_responce.ok:
        abort(503)

    documents = parse_wiki_search_output(wiki_responce.text)
    app.logger.debug("found %s documents for query: %s", len(documents), user_query)
    return jsonify({
        "documents": documents,
        "version": 1.0,
    })


def parse_wiki_search_output(wikipedia_search_output):
    root = etree.fromstring(wikipedia_search_output, etree.HTMLParser())
    documents_raw_collection = root.xpath("//li[@class='mw-search-result']")
    documents_collection = []
    for document in documents_raw_collection:
        title = document.xpath(".//a[1]/@title")[0]
        link = document.xpath(".//a[1]/@href")[0]
        snippet = "".join(document.xpath(".//div[@class='searchresult']")[0].itertext())
        documents_collection.append([title, link, snippet])

    return documents_collection