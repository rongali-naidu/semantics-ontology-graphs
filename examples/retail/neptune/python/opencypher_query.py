#!/usr/bin/env python3
"""Run openCypher against Neptune - three ways.

    python opencypher_query.py https    # raw HTTPS  POST /openCypher
    python opencypher_query.py boto3    # boto3 neptunedata.execute_open_cypher_query
    python opencypher_query.py bolt     # neo4j driver over Bolt (port 8182)
"""
import json
import sys
from urllib.parse import urlencode

import requests

from common import ENDPOINT, HTTPS_URL, IAM_AUTH, PORT, neptunedata_client, signed_headers

# Q5 from ../../property-graph/cypher/02-queries.cypher, parameterised
QUERY = """
MATCH (target:Product {name: $product})<-[:CONTAINS]-(:Order)<-[:PLACED]-(c:Customer),
      (c)-[:PLACED]->(:Order)-[:CONTAINS]->(other:Product)
WHERE other <> target
RETURN other.name AS product, count(DISTINCT c) AS buyers
ORDER BY buyers DESC, product
"""
PARAMS = {"product": "Wireless Earbuds X"}


def via_https():
    url = f"{HTTPS_URL}/openCypher"
    body = urlencode({"query": QUERY, "parameters": json.dumps(PARAMS)})
    headers = signed_headers("POST", url, body, {"Content-Type": "application/x-www-form-urlencoded"})
    r = requests.post(url, data=body, headers=headers, timeout=60)
    r.raise_for_status()
    return r.json()["results"]


def via_boto3():
    client = neptunedata_client()
    r = client.execute_open_cypher_query(openCypherQuery=QUERY, parameters=json.dumps(PARAMS))
    return r["results"]


def via_bolt():
    from neo4j import GraphDatabase
    if IAM_AUTH:
        raise SystemExit("Bolt + IAM needs a SigV4 auth token; see "
                         "https://docs.aws.amazon.com/neptune/latest/userguide/access-graph-opencypher-bolt.html")
    # Without IAM auth, Neptune ignores the username/password.
    driver = GraphDatabase.driver(f"bolt://{ENDPOINT}:{PORT}", auth=("neptune", "ignored"), encrypted=True)
    with driver.session() as s:
        rows = [r.data() for r in s.run(QUERY, PARAMS)]
    driver.close()
    return rows


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "boto3"
    rows = {"https": via_https, "boto3": via_boto3, "bolt": via_bolt}[mode]()
    for row in rows:
        print(row)

# Query plans:  POST /openCypher/explain  with  query=...&explain=dynamic
