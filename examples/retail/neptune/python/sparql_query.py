#!/usr/bin/env python3
"""Run a SPARQL query (or update) against Neptune over HTTPS.

    python sparql_query.py ../../sparql/03-order-totals-per-customer.rq
    python sparql_query.py ../../sparql/12-insert-new-order.ru      # .ru = update
    python sparql_query.py ../../sparql/02-*.rq --explain           # query plan

Neptune SPARQL endpoint:  POST https://<endpoint>:8182/sparql
  form field  query=...   (SELECT/ASK/CONSTRUCT/DESCRIBE)
  form field  update=...  (INSERT/DELETE/LOAD/CLEAR ...)
  Accept header picks the result format, e.g.
    application/sparql-results+json | text/csv | text/tab-separated-values
    text/turtle | application/n-triples (for CONSTRUCT/DESCRIBE)
"""
import sys
from pathlib import Path
from urllib.parse import urlencode

import requests

from common import HTTPS_URL, signed_headers


def run(text: str, is_update: bool, explain: bool = False, accept: str = "application/sparql-results+json"):
    url = f"{HTTPS_URL}/sparql"
    form = {"update" if is_update else "query": text}
    if explain:
        form["explain"] = "dynamic"     # static | dynamic | details
        accept = "text/plain"
    body = urlencode(form)
    headers = signed_headers("POST", url, body, {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": accept,
    })
    resp = requests.post(url, data=body, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp


def print_table(result: dict) -> None:
    if "boolean" in result:
        print(result["boolean"])
        return
    cols = result["head"]["vars"]
    print(" | ".join(cols))
    for b in result["results"]["bindings"]:
        print(" | ".join(b.get(c, {}).get("value", "") for c in cols))


if __name__ == "__main__":
    path = Path(sys.argv[1])
    text = path.read_text()
    is_update = path.suffix == ".ru"
    explain = "--explain" in sys.argv
    resp = run(text, is_update, explain)
    if is_update or explain or "CONSTRUCT" in text:
        print(resp.text)
    else:
        print_table(resp.json())
