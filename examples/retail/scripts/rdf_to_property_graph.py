#!/usr/bin/env python3
"""Convert the RDF retail data into a labeled property graph (LPG).

    pip install rdflib
    python scripts/rdf_to_property_graph.py

This is the RDF -> property graph mapping explained in
docs/07-property-graphs.md, written out as code:

  RDF                                   Property graph
  ------------------------------------  ------------------------------------
  resource with rdf:type                node with a label
  literal-valued triple                 node property
  resource-valued triple                edge (relationship)
  retail:OrderLine (a reified link)     CONTAINS edge with properties
                                        {quantity, unitPrice}
  retail:PremiumCustomer subclass       Customer label + premium=true
  Order placedBy Customer               (Customer)-[:PLACED]->(Order)
  Review writtenBy Customer             (Customer)-[:WROTE]->(Review)

Writes (all from the same in-memory graph, so they always agree):
  neptune/gremlin-csv/      Neptune bulk-load "csv" format   (Gremlin)
  neptune/opencypher-csv/   Neptune bulk-load "opencypher" format
  property-graph/cypher/01-create-retail-graph.cypher
  property-graph/gremlin/01-create-retail-graph.groovy
"""
import csv
from collections import defaultdict
from pathlib import Path

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF

ROOT = Path(__file__).resolve().parent.parent
RETAIL = Namespace("https://example.org/retail/ontology#")
EX = "https://example.org/retail/data/"

LABEL_FOR_CLASS = {
    RETAIL.Customer: "Customer",
    RETAIL.PremiumCustomer: "Customer",
    RETAIL.Address: "Address",
    RETAIL.Seller: "Seller",
    RETAIL.Product: "Product",
    RETAIL.Category: "Category",
    RETAIL.Order: "Order",
    RETAIL.Review: "Review",
}

# property name -> (Gremlin CSV type, openCypher CSV type)
PROPERTY_TYPES = {
    "name": ("String", "String"),
    "email": ("String", "String"),
    "premium": ("Bool", "Bool"),
    "memberSince": ("Date", "DateTime"),
    "sku": ("String", "String"),
    "price": ("Double", "Double"),        # no decimal type in Neptune CSV
    "orderDate": ("Date", "DateTime"),
    "status": ("String", "String"),
    "paymentMethod": ("String", "String"),
    "city": ("String", "String"),
    "state": ("String", "String"),
    "postalCode": ("String", "String"),
    "country": ("String", "String"),
    "rating": ("Int", "Int"),
    "reviewText": ("String", "String"),
    "quantity": ("Int", "Int"),
    "unitPrice": ("Double", "Double"),
}

# RDF predicate -> (edge label, reverse direction?)
EDGE_FOR_PREDICATE = {
    RETAIL.placedBy: ("PLACED", True),
    RETAIL.hasAddress: ("HAS_ADDRESS", False),
    RETAIL.shipsTo: ("SHIPS_TO", False),
    RETAIL.inCategory: ("IN_CATEGORY", False),
    RETAIL.subCategoryOf: ("SUBCATEGORY_OF", False),
    RETAIL.soldBy: ("SOLD_BY", False),
    RETAIL.writtenBy: ("WROTE", True),
    RETAIL.reviewOf: ("REVIEWS", False),
}

NODE_ORDER = ["Category", "Seller", "Product", "Address", "Customer", "Order", "Review"]


def local(iri) -> str:
    return str(iri).removeprefix(EX)


def build(g: Graph):
    nodes = {}                       # id -> {"label": str, "props": dict}
    edges = []                       # dicts: id, from, to, label, props

    for s, t in g.subject_objects(RDF.type):
        if t not in LABEL_FOR_CLASS:
            continue
        props = {}
        for p, o in g.predicate_objects(s):
            if isinstance(o, Literal):
                props[str(p).removeprefix(str(RETAIL))] = o.toPython()
        if LABEL_FOR_CLASS[t] == "Customer":
            props["premium"] = (t == RETAIL.PremiumCustomer)
        nodes[local(s)] = {"label": LABEL_FOR_CLASS[t], "props": props}

    for p, (label, reverse) in EDGE_FOR_PREDICATE.items():
        for s, o in g.subject_objects(p):
            a, b = (local(o), local(s)) if reverse else (local(s), local(o))
            edges.append({"id": f"{a}-{label}-{b}", "from": a, "to": b,
                          "label": label, "props": {}})

    # Collapse each OrderLine node into an Order-[:CONTAINS]->Product edge
    for order, line in g.subject_objects(RETAIL.hasLine):
        edges.append({
            "id": local(line), "from": local(order),
            "to": local(g.value(line, RETAIL.forProduct)), "label": "CONTAINS",
            "props": {"quantity": int(g.value(line, RETAIL.quantity)),
                      "unitPrice": float(g.value(line, RETAIL.unitPrice))},
        })

    edges.sort(key=lambda e: (e["label"], e["id"]))
    return nodes, edges


def csv_value(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v)


def by_label(nodes):
    groups = defaultdict(list)
    for nid, n in sorted(nodes.items()):
        groups[n["label"]].append((nid, n["props"]))
    return groups


def prop_columns(groups_items):
    cols = []
    for _, props in groups_items:
        for k in props:
            if k not in cols:
                cols.append(k)
    return sorted(cols, key=list(PROPERTY_TYPES).index)


def write_csv(path: Path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def write_neptune_csv(nodes, edges):
    groups = by_label(nodes)
    plain = [e for e in edges if not e["props"]]
    contains = [e for e in edges if e["props"]]
    edge_cols = ["quantity", "unitPrice"]

    # ---- Gremlin CSV:  ~id, ~label, name:Type(single) ...
    gdir = ROOT / "neptune/gremlin-csv"
    for label in NODE_ORDER:
        items = groups[label]
        cols = prop_columns(items)
        header = ["~id", "~label"] + [f"{c}:{PROPERTY_TYPES[c][0]}(single)" for c in cols]
        rows = [[nid, label] + [csv_value(p[c]) if c in p else "" for c in cols]
                for nid, p in items]
        write_csv(gdir / f"vertices-{label.lower()}.csv", header, rows)
    write_csv(gdir / "edges.csv", ["~id", "~from", "~to", "~label"],
              [[e["id"], e["from"], e["to"], e["label"]] for e in plain])
    write_csv(gdir / "edges-contains.csv",
              ["~id", "~from", "~to", "~label"] + [f"{c}:{PROPERTY_TYPES[c][0]}" for c in edge_cols],
              [[e["id"], e["from"], e["to"], e["label"]] + [csv_value(e["props"][c]) for c in edge_cols]
               for e in contains])

    # ---- openCypher CSV:  :ID, :LABEL, name:Type ...
    odir = ROOT / "neptune/opencypher-csv"
    for label in NODE_ORDER:
        items = groups[label]
        cols = prop_columns(items)
        header = [":ID", ":LABEL"] + [f"{c}:{PROPERTY_TYPES[c][1]}" for c in cols]
        rows = [[nid, label] + [csv_value(p[c]) if c in p else "" for c in cols]
                for nid, p in items]
        write_csv(odir / f"nodes-{label.lower()}.csv", header, rows)
    write_csv(odir / "relationships.csv", [":ID", ":START_ID", ":END_ID", ":TYPE"],
              [[e["id"], e["from"], e["to"], e["label"]] for e in plain])
    write_csv(odir / "relationships-contains.csv",
              [":ID", ":START_ID", ":END_ID", ":TYPE"] + [f"{c}:{PROPERTY_TYPES[c][1]}" for c in edge_cols],
              [[e["id"], e["from"], e["to"], e["label"]] + [csv_value(e["props"][c]) for c in edge_cols]
               for e in contains])


def cypher_literal(k, v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return f"{v:.2f}" if isinstance(v, float) else str(v)
    if k in ("memberSince", "orderDate"):
        return f"datetime('{v}T00:00:00Z')"
    return "'" + str(v).replace("'", "\\'") + "'"


def var(nid: str) -> str:
    return "n_" + nid.replace("-", "_")


def write_cypher(nodes, edges):
    groups = by_label(nodes)
    lines = [
        "// GENERATED by scripts/rdf_to_property_graph.py - do not edit by hand.",
        "// One CREATE statement for the whole retail graph (works in Neo4j and",
        "// Amazon Neptune openCypher). `~id` is the element id in Neptune; in",
        "// Neo4j it is simply a property, so MATCH (n {`~id`:'O1'}) works in both.",
        "CREATE",
    ]
    parts = []
    for label in NODE_ORDER:
        for nid, props in groups[label]:
            body = ", ".join([f"`~id`: '{nid}'"] +
                             [f"{k}: {cypher_literal(k, v)}" for k, v in sorted(props.items())])
            parts.append(f"  ({var(nid)}:{label} {{{body}}})")
    for e in edges:
        body = ""
        if e["props"]:
            body = " {" + ", ".join(f"{k}: {cypher_literal(k, v)}" for k, v in e["props"].items()) + "}"
        parts.append(f"  ({var(e['from'])})-[:{e['label']}{body}]->({var(e['to'])})")
    lines.append(",\n".join(parts) + ";")
    path = ROOT / "property-graph/cypher/01-create-retail-graph.cypher"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def gremlin_literal(k, v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return f"{v:.2f}"
    if isinstance(v, int):
        return str(v)
    if k in ("memberSince", "orderDate"):
        return f"datetime('{v}T00:00:00Z')"
    return "'" + str(v).replace("'", "\\'") + "'"


def write_gremlin(nodes, edges):
    groups = by_label(nodes)
    lines = [
        "// GENERATED by scripts/rdf_to_property_graph.py - do not edit by hand.",
        "// A single traversal that creates the whole retail graph.",
        "// Works on Amazon Neptune (string ids are kept as ~id) and on",
        "// TinkerGraph / Gremlin Server 3.7+ (datetime() needs TinkerPop 3.7+).",
        "g",
    ]
    for label in NODE_ORDER:
        for nid, props in groups[label]:
            chain = "".join(f".property('{k}', {gremlin_literal(k, v)})" for k, v in sorted(props.items()))
            lines.append(f"  .addV('{label}').property(T.id, '{nid}'){chain}.as('{nid}')")
    for e in edges:
        chain = "".join(f".property('{k}', {gremlin_literal(k, v)})" for k, v in e["props"].items())
        lines.append(f"  .addE('{e['label']}').from('{e['from']}').to('{e['to']}')"
                     f".property(T.id, '{e['id']}'){chain}")
    lines.append("  .iterate()")
    path = ROOT / "property-graph/gremlin/01-create-retail-graph.groovy"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    g = Graph().parse(ROOT / "rdf/retail-data.ttl")
    nodes, edges = build(g)
    write_neptune_csv(nodes, edges)
    write_cypher(nodes, edges)
    write_gremlin(nodes, edges)
    print(f"nodes: {len(nodes)}  edges: {len(edges)}")


if __name__ == "__main__":
    main()
