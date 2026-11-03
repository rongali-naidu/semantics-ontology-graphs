#!/usr/bin/env python3
"""Run Gremlin against Neptune - WebSocket (gremlinpython) or HTTPS (boto3).

    python gremlin_query.py ws       # gremlinpython bytecode over wss://.../gremlin
    python gremlin_query.py boto3    # string query via neptunedata.execute_gremlin_query
"""
import sys

from common import ENDPOINT, PORT, neptunedata_client, signed_headers

STRING_QUERY = (
    "g.V().has('Category','name','Electronics')"
    ".emit().repeat(__.in('SUBCATEGORY_OF'))"
    ".in('IN_CATEGORY').dedup().order().by('name').values('name')"
)


def via_websocket():
    from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
    from gremlin_python.process.anonymous_traversal import traversal
    from gremlin_python.process.graph_traversal import __
    from gremlin_python.process.traversal import Order

    url = f"wss://{ENDPOINT}:{PORT}/gremlin"
    # Sign the HTTP upgrade request (https:// form of the same URL) for IAM auth
    headers = signed_headers("GET", f"https://{ENDPOINT}:{PORT}/gremlin")
    conn = DriverRemoteConnection(url, "g", headers=headers)
    g = traversal().with_remote(conn)
    try:
        # Same traversal as STRING_QUERY, written in Python (bytecode)
        names = (g.V().has("Category", "name", "Electronics")
                  .emit().repeat(__.in_("SUBCATEGORY_OF"))
                  .in_("IN_CATEGORY").dedup()
                  .order().by("name", Order.asc)
                  .values("name").to_list())
        # Spend per customer (Q3)
        spend = (g.V().has_label("Customer")
                  .project("customer", "totalSpent")
                  .by("name")
                  .by(__.out("PLACED").out_e("CONTAINS")
                        .project("q", "p").by("quantity").by("unitPrice")
                        .math("q * p").sum_())
                  .to_list())
        return names, spend
    finally:
        conn.close()


def via_boto3():
    r = neptunedata_client().execute_gremlin_query(gremlinQuery=STRING_QUERY)
    return r["result"]


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "ws"
    print({"ws": via_websocket, "boto3": via_boto3}[mode]())

# Query plans:  POST /gremlin/explain  or  /gremlin/profile  with {"gremlin": "..."}
#   aws neptunedata execute-gremlin-explain-query --gremlin-query "..." --endpoint-url ...
