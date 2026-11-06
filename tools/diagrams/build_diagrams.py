#!/usr/bin/env python3
"""Generate the illustrative SVG diagrams in assets/diagrams/.

    python tools/diagrams/build_diagrams.py

Hand-placed layouts (no layout engine) so the diagrams stay readable and
diff-able. The retail instance graph is drawn from the generated Neptune
openCypher CSVs, so it always matches the data.
"""
import csv
from pathlib import Path

from svg import (EXAMPLE, GOOD, GRAPH, INK, LINEAGE, MUTED, NEUTRAL, ONTO, SEM, WARN, Canvas)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/diagrams"
DIAGRAMS = {}


def diagram(name):
    def wrap(fn):
        DIAGRAMS[name] = fn
        return fn
    return wrap


# ---------------------------------------------------------------------------
@diagram("repo-map")
def repo_map():
    c = Canvas(960, 430, "How this repository is organised")
    c.heading("How this repository is organised", "three topics, each with concepts and implementations, sharing one example")
    c.box(300, 82, 360, 62, "foundations/", ["ontology vs KG vs graph DB · history · ontologies ⇄ semantic models"], NEUTRAL, body_size=12)
    topics = [(40, "ontologies/", ["OWL · RDFS · SKOS · SHACL", "RDF serializations · SPARQL", "COA · Fabric IQ · Palantir…"], ONTO),
              (340, "graphs/", ["property graphs · graph DBs", "Cypher · Gremlin · GQL · SQL/PGQ", "Neptune · Spanner · Neo4j…"], GRAPH),
              (640, "semantic-models/", ["semantic layers · BI models", "repositories · Apache Ossie", "Power BI · Looker · dbt…"], SEM)]
    for x, t, body, col in topics:
        c.box(x, 186, 280, 112, t, body, col)
        c.text(x + 140, 286, "concepts/ · implementations/{providers, tools}/", size=11, color=col[1])
        c.line(480, 144, x + 140, 184)
    c.box(40, 340, 640, 60, "examples/retail/", ["one Amazon-style retail domain in every format · scripts prove they agree"], EXAMPLE, body_size=12)
    c.box(700, 340, 220, 60, "reference/", ["standards · links · glossary"], NEUTRAL, body_size=12)
    for x in (180, 480):
        c.line(x, 300, x, 338, dash="4 3", both=True)
    c.line(780, 300, 600, 338, dash="4 3", both=True)
    return c


# ---------------------------------------------------------------------------
@diagram("one-domain-every-format")
def one_domain():
    c = Canvas(1000, 440, "One domain, every format")
    c.heading("One domain, every format", "rdf/retail-data.ttl is the only hand-edited data file; CI proves every format gives the same answers")
    c.box(390, 84, 220, 64, "retail-data.ttl", ["+ retail-ontology.ttl (OWL)"], EXAMPLE)
    cols = [(30, "RDF formats", ["N-Triples · N-Quads · TriG", "RDF/XML · JSON-LD", "13 SPARQL queries"], ONTO, "build_rdf_formats.py"),
            (270, "Property graph", ["29 nodes · 41 edges", "Gremlin CSV · openCypher CSV", "Cypher + Gremlin scripts"], GRAPH, "rdf_to_property_graph.py"),
            (510, "Warehouse tables", ["8 tables, star schema", "metrics.sql", "dbt seeds"], NEUTRAL, "rdf_to_tables.py"),
            (750, "Semantic models", ["Apache Ossie (+ ontology)", "dbt MetricFlow · COA metrics", "LookML · TMDL · SML · Cube…"], SEM, "")]
    for x, t, body, col, script in cols:
        c.box(x, 196, 220, 114, t, body, col)
        c.text(x + 110, 300, script or "from the warehouse tables", size=10.5, color=col[1], mono=bool(script))
        if script:
            c.line(500, 148, x + 110, 194)
    c.line(730, 253, 748, 253)
    c.rect(30, 340, 940, 70, fill=GOOD[0], stroke=GOOD[1])
    c.text(500, 368, "✓ same answers everywhere", size=15, weight="600", color=GOOD[1])
    c.text(500, 391, "Alice 1498.97 · Bob 199.98 · Carol 179.48  —  SPARQL = CSVs = SQL = Ossie = MetricFlow = COA metric SQL",
           size=12.5, color=INK)
    for x in (140, 380, 620, 860):
        c.line(x, 310, x, 338, color=GOOD[1], dash="3 3")
    return c


# ---------------------------------------------------------------------------
@diagram("layers")
def layers():
    c = Canvas(960, 452, "Ontology, knowledge graph, data model, graph database")
    c.heading("Four layers that get mixed up", "ontology ≠ knowledge graph ≠ graph data model ≠ graph database")
    rows = [("Ontology", "the meaning: classes, relationships, rules", "Orders are placed by exactly one Customer;", "subCategoryOf is transitive", ONTO),
            ("Knowledge graph", "ontology + facts (+ inferences)", "O1 placedBy Alice; Alice is a PremiumCustomer", "⇒ Alice is a Customer", GRAPH),
            ("Graph data model", "how the graph is represented", "RDF triples (subject–predicate–object)", "or labeled property graph (nodes, edges, props)", EXAMPLE),
            ("Graph database", "software that stores and queries it", "Neptune · Neo4j · Spanner Graph · Oracle", "GraphDB · Jena · Fabric Graph …", NEUTRAL)]
    c.text(470, 88, "in the retail example", size=11.5, anchor="start", color=MUTED, italic=True)
    y = 96
    for title, what, ex1, ex2, col in rows:
        c.rect(30, y, 900, 76, fill=col[0], stroke=col[1])
        c.text(50, y + 32, title, size=16, weight="700", anchor="start", color=col[1])
        c.text(50, y + 54, what, size=12.5, anchor="start", color=MUTED)
        c.text(470, y + 32, ex1, size=13, anchor="start", color=INK)
        c.text(470, y + 52, ex2, size=13, anchor="start", color=INK)
        y += 86
    return c


# ---------------------------------------------------------------------------
@diagram("history-timeline")
def history():
    c = Canvas(1000, 420, "A short history of semantics, graphs and semantic layers")
    c.heading("From Aristotle to agents", "three threads that are now converging")

    def x_of(year):
        if year < 1800:
            return 150 + (year + 350) / 2150 * 70
        if year < 1990:
            return 220 + (year - 1800) / 190 * 120
        return 340 + (year - 1990) / 36 * 620

    lanes = [("Knowledge representation & Semantic Web", ONTO, 140,
              [(-350, "Aristotle"), (1974, "Frames"), (1993, "Gruber"), (1999, "RDF"), (2004, "OWL"),
               (2008, "SPARQL"), (2012, "Google KG"), (2017, "SHACL"), (2026, "COA")]),
             ("Graph databases", GRAPH, 250,
              [(1736, "Euler"), (2010, "Neo4j 1.0"), (2011, "Cypher"), (2015, "openCypher"),
               (2018, "Neptune"), (2023, "SQL/PGQ"), (2024, "GQL")]),
             ("Semantic layers", SEM, 360,
              [(1992, "BO universe"), (2010, "DAX"), (2012, "LookML"), (2019, "Cube"),
               (2022, "dbt SL"), (2025, "OSI"), (2026, "Ossie")])]
    for name, col, y, events in lanes:
        c.text(30, y - 46, name, size=12.5, weight="600", anchor="start", color=col[1])
        c.line(150, y, 970, y, color=col[1], sw=2, arrow=False)
        for i, (yr, label) in enumerate(events):
            x = x_of(yr)
            c.circle(x, y, 5, "#fff", col[1], sw=2)
            year = str(yr) if yr > 0 else "~350 BC"
            if i % 2 == 0:      # label above the lane: name, then year above it
                c.text(x, y - 11, label, size=11.5, color=INK)
                c.text(x, y - 25, year, size=10, color=MUTED)
            else:               # label below the lane
                c.text(x, y + 22, label, size=11.5, color=INK)
                c.text(x, y + 35, year, size=10, color=MUTED)
    for x, s in ((185, "…"), (280, "1800 – 1990"), (650, "1990 – 2026")):
        c.text(x, 408, s, size=11, color=MUTED, italic=True)
    return c


# ---------------------------------------------------------------------------
@diagram("ontology-semantic-kg")
def ontology_semantic_kg():
    c = Canvas(960, 480, "How ontologies, knowledge graphs and semantic models work together")
    c.heading("Meaning, connections and numbers, together", "the ontology names things once; the KG connects them; the semantic model counts them")
    c.box(290, 82, 380, 70, "Enterprise ontology", ["OWL / Ossie ontology · IRIs · rules"], ONTO)
    c.box(40, 212, 380, 92, "Knowledge graph", ["RDF store or property graph", "entities, paths, provenance", "who · what · how connected"], GRAPH)
    c.box(540, 212, 380, 92, "Semantic models", ["Ossie · dbt · LookML · TMDL · COA metrics", "governed metrics, dimensions, joins", "how much · how many"], SEM)
    c.line(400, 152, 250, 210)
    c.label(300, 178, "mapping (R2RML · Ossie mapping)", size=11)
    c.line(560, 152, 710, 210)
    c.label(660, 178, "alignment (iri · ontologyConcepts)", size=11)
    c.box(280, 368, 400, 72, "AI agents · apps · BI", ["\"why did premium Electronics revenue drop,", "and who are those customers?\""], EXAMPLE, body_size=12)
    c.line(230, 304, 380, 366)
    c.line(730, 304, 580, 366)
    c.box(40, 368, 200, 72, "Data", ["warehouse tables", "documents"], NEUTRAL)
    c.line(140, 366, 140, 306, dash="4 3")
    c.path("M 140 440 V 456 H 940 V 258 H 924", dash="4 3")
    c.label(800, 460, "same data feeds both", size=11)
    return c


# ---------------------------------------------------------------------------
@diagram("retail-ontology")
def retail_ontology():
    c = Canvas(1060, 560, "The retail ontology")
    c.heading("The retail ontology (TBox)", "classes, object properties and subclass axioms from retail-ontology.ttl")
    W, H = 160, 58
    pos = {"Party": (70, 80), "Customer": (70, 200), "PremiumCustomer": (70, 320), "Address": (70, 450),
           "Order": (360, 200), "Review": (360, 450), "OrderLine": (630, 200), "Product": (630, 320),
           "Seller": (860, 80), "Category": (860, 320)}
    attrs = {"Party": "", "Customer": "name · email", "PremiumCustomer": "memberSince", "Address": "city · state",
             "Order": "orderDate · status", "Review": "rating · reviewText", "OrderLine": "quantity · unitPrice",
             "Product": "sku · name · price", "Seller": "name", "Category": "name"}
    for k, (x, y) in pos.items():
        c.rect(x, y, W, H, fill=ONTO[0], stroke=ONTO[1])
        c.text(x + W / 2, y + 24, k, size=14, weight="600", color=ONTO[1])
        if attrs[k]:
            c.text(x + W / 2, y + 44, attrs[k], size=11.5, color=MUTED)

    def mid(k, side):
        x, y = pos[k]
        return {"l": (x, y + H / 2), "r": (x + W, y + H / 2), "t": (x + W / 2, y), "b": (x + W / 2, y + H)}[side]

    def edge(a, sa, b, sb, label, lx=None, ly=None, dash=None):
        (x1, y1), (x2, y2) = mid(a, sa), mid(b, sb)
        c.line(x1, y1, x2, y2, color=ONTO[1] if dash else MUTED, dash=dash)
        c.label(lx if lx is not None else (x1 + x2) / 2, ly if ly is not None else (y1 + y2) / 2 + 4, label, size=11.5,
                color=ONTO[1] if dash else INK)

    edge("Customer", "t", "Party", "b", "subClassOf", dash="5 3")
    edge("PremiumCustomer", "t", "Customer", "b", "subClassOf", dash="5 3")
    c.line(860, 109, 230, 109, color=ONTO[1], dash="5 3")
    c.label(545, 113, "subClassOf", size=11.5, color=ONTO[1])
    edge("Order", "l", "Customer", "r", "placedBy")
    edge("Order", "r", "OrderLine", "l", "hasLine")
    edge("OrderLine", "b", "Product", "t", "forProduct")
    c.line(790, 349, 858, 349)
    c.label(824, 336, "inCategory", size=10.5, color=INK, bg=False)
    c.path("M 1020 335 C 1052 335, 1052 365, 1020 365", color=MUTED)
    c.text(940, 400, "subCategoryOf (transitive)", size=11, color=INK)
    c.line(770, 320, 920, 140)
    c.label(865, 220, "soldBy", size=11.5, color=INK)
    c.line(400, 258, 220, 452)
    c.label(330, 380, "shipsTo", size=11.5, color=INK)
    c.path("M 70 229 L 46 229 L 46 479 L 68 479", color=MUTED)
    c.text(38, 354, "hasAddress", size=11, color=INK, rotate=-90)
    c.line(400, 450, 205, 258)
    c.label(280, 318, "writtenBy", size=11.5, color=INK)
    c.line(520, 465, 670, 378)
    c.label(600, 432, "reviewOf", size=11.5, color=INK)
    c.text(530, 540, "dashed = rdfs:subClassOf · solid = object property (domain → range)", size=11.5, color=MUTED)
    return c


# ---------------------------------------------------------------------------
@diagram("rdf-vs-property-graph")
def rdf_vs_lpg():
    c = Canvas(980, 380, "The same fact as RDF triples and as a property graph")
    c.heading("One fact, two graph models", "\"Alice placed order O1, which contains 2 × USB-C Charger at 29.99\"")
    c.rect(24, 76, 460, 280, fill="#FCFCFD", stroke="#D0D5DD")
    c.text(254, 100, "RDF (triples): the line item must be a node", size=14, weight="600", color=ONTO[1])
    nodes = {"ex:C1": (90, 140), "ex:O1": (260, 140), "ex:O1-L2": (220, 240), "ex:P3": (410, 240)}
    for k, (x, y) in nodes.items():
        c.rect(x - 52, y - 18, 104, 36, fill=ONTO[0], stroke=ONTO[1], rx=18)
        c.text(x, y + 5, k, size=12.5, mono=True, color=ONTO[1])
    c.line(208, 140, 144, 140); c.label(176, 128, "placedBy", size=11)
    c.line(252, 158, 228, 220); c.label(282, 194, "hasLine", size=11)
    c.line(272, 240, 356, 240); c.label(314, 228, "forProduct", size=11)
    for i, (k, v) in enumerate((("quantity", '"2"'), ("unitPrice", '"29.99"'))):
        x = 110 + i * 170
        c.line(220, 258, x + 40, 312, arrow=True)
        c.rect(x, 314, 110, 30, fill="#fff", stroke=MUTED, rx=4)
        c.text(x + 55, 334, v, size=12, mono=True)
        c.label(x + 40 + (60 if i else -10), 292, k, size=11)
    c.rect(500, 76, 456, 280, fill="#FCFCFD", stroke="#D0D5DD")
    c.text(728, 100, "Property graph: the edge carries the properties", size=14, weight="600", color=GRAPH[1])
    pg = {"Alice\n:Customer": (580, 220), "O1\n:Order": (728, 220), "Charger\n:Product": (880, 220)}
    for k, (x, y) in pg.items():
        c.circle(x, y, 44, GRAPH[0], GRAPH[1], sw=2)
        a, b = k.split("\n")
        c.text(x, y - 2, a, size=12, weight="600", color=GRAPH[1])
        c.text(x, y + 15, b, size=11, color=MUTED)
    c.line(624, 220, 682, 220); c.label(653, 206, "PLACED", size=11)
    c.line(772, 220, 834, 220); c.label(803, 206, "CONTAINS", size=11)
    c.rect(735, 262, 150, 50, fill="#fff", stroke=GRAPH[1], rx=6)
    c.text(810, 282, "quantity: 2", size=12, mono=True)
    c.text(810, 301, "unitPrice: 29.99", size=12, mono=True)
    c.line(803, 228, 805, 260, color=GRAPH[1], dash="3 3", arrow=False)
    return c


# ---------------------------------------------------------------------------
@diagram("retail-instance-graph")
def retail_instance_graph():
    oc = ROOT / "graphs/implementations/providers/aws/opencypher-csv"
    nodes, edges = {}, []
    for f in sorted(oc.glob("*.csv")):
        rows = list(csv.DictReader(f.open(encoding="utf-8")))
        for r in rows:
            if ":START_ID" in r:
                edges.append((r[":START_ID"], r[":END_ID"], r[":TYPE"], r.get("quantity:Int")))
            else:
                name = r.get("name:String") or f'{r[":ID"]} · {r.get("status:String", "")}'
                nodes[r[":ID"]] = (r[":LABEL"], name)
    c = Canvas(1000, 560, "The retail knowledge graph (instance data)")
    c.heading("The retail graph: customers, orders, products, categories",
              "drawn from the generated openCypher CSVs (reviews, sellers and addresses omitted for clarity)")
    cols = {"Customer": 110, "Order": 340, "Product": 600, "Category": 870}
    colour = {"Customer": ONTO, "Order": EXAMPLE, "Product": GRAPH, "Category": SEM}
    order = {"Customer": ["C1", "C2", "C3"], "Order": ["O1", "O3", "O2", "O4"],
             "Product": ["P1", "P3", "P6", "P2", "P4", "P5"],
             "Category": ["CAT-ELECTRONICS", "CAT-COMPUTERS", "CAT-LAPTOPS", "CAT-AUDIO", "CAT-BOOKS", "CAT-KITCHEN"]}
    xy = {}
    for lab, ids in order.items():
        top, bottom = 110, 520
        step = (bottom - top) / len(ids)
        for i, nid in enumerate(ids):
            xy[nid] = (cols[lab], top + step * (i + 0.5))
        c.text(cols[lab], 96, {"Category": "Categories"}.get(lab, lab + "s"), size=13, weight="600", color=colour[lab][1])
    for a, b, t, q in edges:
        if a in xy and b in xy:
            (x1, y1), (x2, y2) = xy[a], xy[b]
            if t == "SUBCATEGORY_OF":
                c.path(f"M {x1 + 75} {y1} C {x1 + 112} {y1}, {x2 + 112} {y2}, {x2 + 77} {y2}", color=SEM[1], dash="4 3")
                continue
            dx = 72 if t in ("CONTAINS", "IN_CATEGORY", "PLACED") else 0
            c.line(x1 + 75, y1, x2 - 77, y2, color="#98A2B3", sw=1.3)
            if t == "CONTAINS" and q and q != "1":
                c.label((x1 + x2) / 2 + 10, (y1 + y2) / 2, f"×{q}", size=11, color=INK)
    for nid, (x, y) in xy.items():
        lab, name = nodes[nid]
        col = colour[lab]
        c.rect(x - 75, y - 17, 150, 34, fill=col[0], stroke=col[1], rx=17)
        short = name if len(name) <= 21 else name[:20] + "…"
        c.text(x, y + 5, short, size=11.5, color=col[1], weight="600")
    c.text(735, 545, "edges: PLACED · CONTAINS (×quantity) · IN_CATEGORY · SUBCATEGORY_OF (dashed)", size=11, color=MUTED)
    return c


# ---------------------------------------------------------------------------
@diagram("semantic-layer")
def semantic_layer():
    c = Canvas(960, 440, "What a semantic layer does")
    c.heading("A semantic layer defines each metric once", "every consumer gets the same revenue, the same joins, the same security")
    consumers = [("Dashboards", "Power BI · Looker · Tableau"), ("Notebooks / SQL", "analysts, data science"),
                 ("Spreadsheets", "Excel · Sheets"), ("AI agents", "text-to-metric · MCP")]
    for i, (t, s) in enumerate(consumers):
        x = 40 + i * 225
        c.box(x, 82, 205, 62, t, [s], EXAMPLE, body_size=11.5)
        c.line(x + 102, 146, 480, 194, dash="3 3", both=True)
    c.rect(60, 196, 840, 112, fill=SEM[0], stroke=SEM[1])
    c.text(480, 222, "Semantic model", size=16, weight="700", color=SEM[1])
    items = [("metric", "revenue = SUM(quantity × unit_price)"), ("metric", "average_order_value = revenue / order_count"),
             ("dimension", "customer · department · order month"), ("join", "order_lines → orders → customers")]
    for i, (k, v) in enumerate(items):
        x, y = 85 + (i % 2) * 400, 252 + (i // 2) * 30
        c.text(x, y, k, size=11, anchor="start", color=SEM[1], weight="600")
        c.text(x + 70, y, v, size=12, anchor="start", mono=True)
    tables = ["order_lines", "orders", "customers", "products", "categories"]
    for i, t in enumerate(tables):
        x = 70 + i * 170
        c.rect(x, 350, 140, 54, fill=NEUTRAL[0], stroke=NEUTRAL[1], rx=6)
        c.text(x + 70, 382, t, size=12.5, mono=True)
        c.line(x + 70, 348, 480, 310, dash="3 3")
    c.text(480, 425, "warehouse tables (star schema)", size=11.5, color=MUTED)
    return c


# ---------------------------------------------------------------------------
@diagram("star-schema")
def star_schema():
    c = Canvas(960, 470, "The retail star schema")
    c.heading("The retail warehouse: two facts, shared dimensions", "examples/retail/warehouse/schema.sql")
    fact = (380, 190, 200, 96)
    c.box(*fact, "order_lines", ["FACT · one row per line", "quantity · unit_price"], SEM)
    dims = {"orders": (380, 80), "products": (660, 190), "customers": (100, 80), "categories": (660, 330),
            "sellers": (660, 80), "addresses": (100, 190)}
    for k, (x, y) in dims.items():
        c.box(x, y, 200, 60, k, [], NEUTRAL)
    c.box(380, 360, 200, 70, "reviews", ["FACT · one row per review", "rating"], SEM)
    links = [((480, 190), (480, 142)), ((580, 238), (658, 220)), ((380, 110), (302, 110)), ((760, 250), (760, 328)),
             ((760, 190), (760, 142)), ((200, 140), (200, 188)), ((580, 380), (690, 252)), ((380, 395), (200, 142))]
    for (x1, y1), (x2, y2) in links:
        c.line(x1, y1, x2, y2)
    c.label(500, 168, "order_id", size=11); c.label(620, 222, "product_id", size=11)
    c.label(341, 98, "customer_id", size=11); c.label(800, 292, "category_id", size=11)
    c.label(796, 168, "seller_id", size=11); c.label(246, 168, "address_id", size=11)
    c.text(480, 456, "category_level_1/2/3 flatten the ontology's recursive subCategoryOf tree", size=11.5, color=MUTED)
    return c


# ---------------------------------------------------------------------------
@diagram("model-repositories")
def model_repositories():
    c = Canvas(1000, 420, "Metadata repository vs source repository")
    c.heading("Where a semantic model is stored and promoted", "the industry is moving from tool-managed repositories to text files in a git repo you own")
    c.text(30, 98, "Tool-managed metadata repository", size=14, weight="700", anchor="start", color=NEUTRAL[1])
    top = [("Developer", "desktop admin tool"), ("Binary model", ".rpd · .unx · .pbix"), ("BI server repository", "database inside the tool"),
           ("Promote", "upload · Object Manager · LCM")]
    for i, (t, s) in enumerate(top):
        x = 30 + i * 245
        c.box(x, 112, 210, 64, t, [s], NEUTRAL, body_size=11.5)
        if i:
            c.line(x - 33, 144, x - 2, 144)
    c.text(30, 228, "User-defined git repository (model as code)", size=14, weight="700", anchor="start", color=GOOD[1])
    bot = [("Developer branch", "TMDL · SMML · LookML · YAML"), ("Pull request + CI", "diff · review · validate"),
           ("main", "single source of truth"), ("Deploy", "dev → test → prod")]
    for i, (t, s) in enumerate(bot):
        x = 30 + i * 245
        c.box(x, 242, 210, 64, t, [s], GOOD, body_size=11.5)
        if i:
            c.line(x - 33, 274, x - 2, 274)
    c.rect(30, 330, 940, 64, fill=WARN[0], stroke=WARN[1])
    c.text(500, 356, "Git-native today: Oracle Analytics Semantic Modeler · Power BI PBIP + Fabric Git · Looker · ThoughtSpot · dbt · Cube · AtScale · Ossie",
           size=12, color=INK)
    c.text(500, 378, "Tool-managed: classic Oracle RPD (MDS XML export) · BusinessObjects CMS · Cognos Content Store · MicroStrategy · Tableau Server",
           size=12, color=INK)
    return c


# ---------------------------------------------------------------------------
@diagram("ossie-documents")
def ossie_documents():
    c = Canvas(980, 420, "The three Apache Ossie documents")
    c.heading("Apache Ossie: three documents", "an ontology and a semantic model, joined by a mapping, and portable across 20+ tools")
    c.box(40, 92, 260, 96, "retail.ontology.yaml", ["concepts · relationships", "derived_by · requires", "iri → OWL terms"], ONTO, mono_body=False)
    c.box(360, 92, 260, 96, "retail.mapping.yaml", ["fields → objects", "fields → links", "(like R2RML)"], NEUTRAL)
    c.box(680, 92, 260, 96, "retail.semantic_model.yaml", ["datasets · fields", "relationships · metrics", "ai_context · synonyms"], SEM)
    c.line(358, 140, 302, 140); c.line(622, 140, 678, 140)
    c.box(40, 240, 260, 56, "retail-ontology.ttl (OWL)", [], ONTO, title_size=13.5, dash="5 3")
    c.line(170, 188, 170, 238, color=ONTO[1], dash="4 3")
    c.label(170, 218, "34 IRIs resolve", size=11, color=ONTO[1])
    c.box(680, 240, 260, 56, "warehouse tables", [], NEUTRAL, title_size=13.5, dash="5 3")
    c.line(810, 188, 810, 238, dash="4 3")
    c.label(810, 218, "source: retail.*", size=11)
    c.rect(40, 330, 900, 62, fill=EXAMPLE[0], stroke=EXAMPLE[1])
    c.text(490, 355, "ossie-converters", size=14, weight="600", color=EXAMPLE[1])
    c.text(490, 377, "dbt · Snowflake · Databricks · Microsoft (TMDL) · Cube · Salesforce · GoodData · ThoughtSpot · Sigma · Omni · Hex …",
           size=12, color=INK)
    return c


# ---------------------------------------------------------------------------
@diagram("coa-architecture")
def coa_architecture():
    c = Canvas(1000, 470, "AWS Context Ontology Accelerator architecture")
    c.heading("AWS Context Ontology Accelerator: Scan → Model → Serve", "open source (Apache 2.0), deployed into your AWS account with CDK")
    cols = [("Scan", ["data sources: Glue, JDBC,", "Databricks, Athena", "documents (unstructured)", "schema discovery"], NEUTRAL),
            ("Model", ["induce OWL + R2RML (Bedrock)", "ground: FIBO, schema.org", "expert review & approval", "reason: HermiT / ELK", "metrics (Tier 1)"], ONTO),
            ("Serve", ["Tier 1: governed metric", "Tier 2: ontology (VKG via Ontop)", "     or NL-to-SQL", "Tier 3: documents + graph", "MCP: 6 tools for agents"], SEM)]
    for i, (t, body, col) in enumerate(cols):
        x = 30 + i * 325
        c.box(x, 84, 290, 196, t, body, col, title_size=17, body_size=12.5, body_gap=21)
        if i:
            c.line(x - 33, 182, x - 2, 182)
    c.text(500, 318, "AWS services underneath", size=13, weight="600", color=MUTED)
    svc = ["Amazon Neptune", "OpenSearch Serverless", "Amazon Bedrock", "AgentCore Runtime", "Cognito · Cedar"]
    for i, s in enumerate(svc):
        x = 30 + i * 192
        c.box(x, 334, 176, 50, s, [], GRAPH if i == 0 else NEUTRAL, title_size=13)
    c.rect(30, 404, 940, 46, fill=WARN[0], stroke=WARN[1])
    c.text(500, 432, "self-supported · ~16 CDK stacks · COA docs: Neptune + OpenSearch Serverless ≈ $930/month when idle",
           size=12.5, color=INK)
    return c


# ---------------------------------------------------------------------------
@diagram("neptune-architecture")
def neptune_architecture():
    c = Canvas(980, 430, "Amazon Neptune architecture")
    c.heading("Amazon Neptune Database", "one cluster, two graph models, all endpoints on port 8182")
    c.rect(24, 76, 932, 330, fill="#FCFCFD", stroke="#98A2B3", dash="6 4")
    c.text(44, 98, "your VPC", size=12, anchor="start", color=MUTED)
    c.box(50, 116, 230, 84, "Clients", ["EC2 · Lambda · notebook", "Gremlin · openCypher · SPARQL"], EXAMPLE, body_size=11.5)
    c.box(360, 106, 260, 56, "cluster endpoint → writer", [], GRAPH, title_size=13)
    c.box(360, 176, 260, 56, "reader endpoint → ≤15 replicas", [], GRAPH, title_size=13)
    c.line(282, 150, 358, 134); c.line(282, 160, 358, 204)
    c.rect(360, 262, 560, 70, fill=GRAPH[0], stroke=GRAPH[1])
    c.text(640, 290, "shared distributed storage", size=14, weight="600", color=GRAPH[1])
    c.text(640, 312, "quad indexes · 6 copies across 3 AZs · auto-grows", size=12)
    c.line(490, 234, 490, 260)
    c.box(680, 106, 240, 126, "Two models", ["RDF → SPARQL", "property graph →", "Gremlin + openCypher", "(models don't mix)"], ONTO, body_size=12)
    c.box(50, 262, 230, 70, "S3 + VPC endpoint", ["bulk loader: 6 formats"], NEUTRAL, body_size=11.5)
    c.line(282, 297, 358, 297)
    c.text(490, 380, "IAM auth → SigV4 (service neptune-db) · Neptune Analytics for in-memory algorithms", size=12, color=MUTED)
    return c


# ---------------------------------------------------------------------------
def landscape(name, title, sub, columns, footer=None):
    most = max(len(col[3]) for col in columns)
    panel = 76 + most * 40 + 14
    height = 80 + panel + (96 if footer else 30)
    c = Canvas(1000, height, title)
    c.heading(title, sub)
    n = len(columns)
    w = (940 - (n - 1) * 16) / n
    for i, (head, desc, col, chips) in enumerate(columns):
        x = 30 + i * (w + 16)
        c.rect(x, 80, w, panel, fill=col[0], stroke=col[1])
        c.text(x + w / 2, 106, head, size=14.5, weight="700", color=col[1])
        c.text(x + w / 2, 126, desc, size=11.5, color=MUTED)
        for j, chip in enumerate(chips):
            y = 144 + j * 40
            c.rect(x + 14, y, w - 28, 30, fill="#fff", stroke=col[1], rx=15, sw=1.2)
            c.text(x + w / 2, y + 20, chip, size=12, color=INK)
    if footer:
        c.rect(30, height - 76, 940, 50, fill=EXAMPLE[0], stroke=EXAMPLE[1])
        c.text(500, height - 46, footer, size=12.5, color=INK)
    return c


@diagram("ontology-landscape")
def ontology_landscape():
    return landscape("ontology-landscape", "Ontology products by kind", "status as of November 2026; see ontologies/implementations",
                     [("Formal (OWL / RDF)", "standards, reasoning, IRIs", ONTO,
                       ["AWS COA", "Databricks OntoBricks", "Oracle RDF Graph", "Amazon Neptune (RDF)", "SAP HANA Cloud KG engine", "Neo4j neosemantics"]),
                      ("Context graphs", "assembled or learned from metadata", GRAPH,
                       ["Google Knowledge Catalog", "Databricks Genie Ontology", "SAP Knowledge Graph"]),
                      ("Business / operational", "bound to data, apps and actions", SEM,
                       ["Microsoft Fabric IQ", "Palantir Foundry Ontology", "Ontology on Snowflake", "Azure DTDL (twins)"])],
                     footer="Apache Ossie ontology: a vendor-neutral bridge, with iri links to OWL and a mapping to semantic models")


@diagram("graph-landscape")
def graph_landscape():
    return landscape("graph-landscape", "Where graph products keep the graph", "status as of November 2026; see graphs/implementations",
                     [("Native graph DB", "graph-optimised storage", GRAPH,
                       ["Amazon Neptune", "Neo4j", "Cosmos DB (Gremlin)", "Fabric Graph"]),
                      ("Graph over tables", "property graph declared on tables", EXAMPLE,
                       ["Spanner Graph", "BigQuery Graph", "Oracle SQL/PGQ", "Snowflake KG tables"]),
                      ("RDF stores", "triples + SPARQL", ONTO,
                       ["Neptune (RDF)", "Oracle RDF Graph", "SAP HANA KG engine", "OntoBricks"]),
                      ("Graph analytics", "algorithms, batch", NEUTRAL,
                       ["Neptune Analytics", "Oracle PGX / Graph Studio", "Databricks GraphFrames", "Neo4j GDS"])])


@diagram("semantic-landscape")
def semantic_landscape():
    return landscape("semantic-landscape", "Where semantic models live", "status as of November 2026; see semantic-models/implementations",
                     [("Inside a BI tool", "one tool consumes it", NEUTRAL,
                       ["Power BI / Fabric", "Looker (LookML)", "Oracle Analytics", "Tableau Semantics", "QuickSight Topics"]),
                      ("Headless / universal", "any tool via SQL / API", SEM,
                       ["dbt Semantic Layer", "Cube", "AtScale (SML)"]),
                      ("In the data platform", "native objects + AI assistant", GRAPH,
                       ["Snowflake semantic views", "Databricks metric views", "SAP Datasphere / BDC", "AWS COA metrics"])],
                     footer="Apache Ossie: open interchange format, with converters between all three columns")


# ---------------------------------------------------------------------------
@diagram("schema-vs-data")
def schema_vs_data():
    c = Canvas(1000, 500, "Schema plus data: ontology, instance graph, knowledge graph")
    c.heading("Schema + data = knowledge graph", "what people usually mean by \"ontology\" and by \"the graph\"")
    c.rect(30, 82, 430, 196, fill=ONTO[0], stroke=ONTO[1])
    c.text(245, 108, "Schema  =  the ontology", size=16, weight="700", color=ONTO[1])
    c.text(245, 128, "TBox: classes, properties, rules · changes slowly", size=12, color=MUTED)
    for k, (ind, ln) in enumerate([(0, "retail:PremiumCustomer rdfs:subClassOf"), (1, "retail:Customer ."),
                                   (0, "retail:placedBy rdfs:domain retail:Order ;"), (1, "rdfs:range retail:Customer .")]):
        c.text(50 + ind * 58, 158 + k * 19, ln, size=12, anchor="start", mono=True)
    c.text(245, 264, "retail-ontology.ttl · 238 triples", size=11.5, color=ONTO[1])
    c.text(500, 190, "+", size=34, weight="700", color=MUTED)
    c.rect(540, 82, 430, 196, fill=GRAPH[0], stroke=GRAPH[1])
    c.text(755, 108, "Data  =  \"the graph\" (instances)", size=16, weight="700", color=GRAPH[1])
    c.text(755, 128, "ABox: individuals and facts · changes constantly", size=12, color=MUTED)
    for k, (ind, ln) in enumerate([(0, "ex:C1 a retail:PremiumCustomer ;"), (1, "retail:name \"Alice Johnson\" ."),
                                   (0, "ex:O1 retail:placedBy ex:C1 ;"), (1, "retail:orderDate \"2026-09-01\" .")]):
        c.text(560 + ind * 44, 158 + k * 19, ln, size=12, anchor="start", mono=True)
    c.text(755, 264, "retail-data.ttl · 165 triples", size=11.5, color=GRAPH[1])
    c.line(245, 280, 440, 326)
    c.line(755, 280, 560, 326)
    c.rect(250, 328, 500, 82, fill=EXAMPLE[0], stroke=EXAMPLE[1])
    c.text(500, 355, "=  Knowledge graph", size=16, weight="700", color=EXAMPLE[1])
    c.text(500, 378, "+ a reasoner adds what follows from the schema:", size=12, color=INK)
    c.text(500, 398, "ex:C1 a retail:Customer   (Alice is a Customer)", size=12, mono=True, color=EXAMPLE[1])
    c.rect(30, 428, 940, 50, fill=WARN[0], stroke=WARN[1])
    c.text(500, 450, "In RDF both halves are triples in one graph, so the line is a convention: formally an OWL ontology may include",
           size=12, color=INK)
    c.text(500, 468, "individuals too. This repo: ontology = schema · data = instance graph · knowledge graph = both.",
           size=12, color=INK)
    return c


# ---------------------------------------------------------------------------
@diagram("ecosystem-poster")
def ecosystem_poster():
    import math
    W, H = 1460, 1580
    c = Canvas(W, H, "The semantics, ontology and graphs ecosystem")
    c.text(W / 2, 62, "Semantics · Ontologies · Graphs: the ecosystem", size=34, weight="700", color=SEM[1])
    c.text(W / 2, 94, "from meaning to models to products, with one retail example implemented in every format",
           size=16, color=INK)
    cx, cy, r0, r1 = 215, 790, 118, 300
    segments = [
        ("Foundations", NEUTRAL), ("Ontologies", ONTO), ("Graphs", GRAPH),
        ("Semantic models", SEM), ("Standards", EXAMPLE), ("AI & agents", GOOD)]
    span, start = 150 / len(segments), -75
    rail_y = [290, 490, 690, 890, 1090, 1290]
    rail_x0, rail_x1 = 610, 1420
    rows = [
        ([("Ontology", ["the schema: classes,", "relationships, rules", "(TBox)"]),
          ("Instance graph", ["the data: individuals", "and facts", "(ABox)"]),
          ("Knowledge graph", ["schema + data", "+ inferences", "+ provenance"]),
          ("Semantic model", ["metrics, dimensions,", "joins over tables", "for BI and agents"])]),
        ([("Languages", ["OWL 2 · RDFS", "SKOS · SHACL", "Ossie ontology"]),
          ("Formats", ["Turtle · JSON-LD", "RDF/XML · N-Triples", "N-Quads · TriG"]),
          ("Query & reason", ["SPARQL 1.1", "OWL RL · HermiT · ELK", "SHACL validation"]),
          ("Products", ["AWS COA · Fabric IQ", "Palantir · OntoBricks", "Oracle RDF · SAP KG"])]),
        ([("Models", ["RDF triples", "labeled property", "graphs"]),
          ("Languages", ["Cypher · Gremlin", "ISO GQL · SQL/PGQ", "SPARQL"]),
          ("Databases", ["Neptune · Neo4j", "Spanner · BigQuery", "Fabric · Oracle"]),
          ("Analytics", ["Neptune Analytics", "GraphFrames · PGX", "Neo4j GDS"])]),
        ([("Building blocks", ["datasets · dimensions", "measures · metrics", "joins · hierarchies"]),
          ("BI tools", ["Power BI · Looker", "Oracle Analytics", "Tableau Semantics"]),
          ("Headless", ["dbt MetricFlow", "Cube · AtScale SML", "COA metrics"]),
          ("Data platforms", ["Snowflake semantic", "views · Databricks", "metric views · SAP"])]),
        ([("W3C", ["RDF 1.1/1.2 · OWL 2", "SPARQL 1.1 · SHACL", "SKOS · JSON-LD"]),
          ("ISO", ["GQL 39075:2024", "SQL/PGQ 9075-16", "BFO 21838-2"]),
          ("Open source", ["openCypher", "Apache TinkerPop", "R2RML · RML"]),
          ("Apache Ossie", ["semantic model +", "ontology + mapping", "20+ converters"])]),
        ([("Grounding", ["ontology terms,", "synonyms and", "ai_context for LLMs"]),
          ("GraphRAG", ["retrieve entities,", "paths and facts", "from the graph"]),
          ("Text-to-metric", ["agents pick governed", "metrics instead of", "writing SQL"]),
          ("MCP serving", ["COA · Knowledge", "Catalog · Genie", "Fabric IQ · Tableau"])]),
    ]

    def pt(r, deg):
        a = math.radians(deg)
        return cx + r * math.cos(a), cy + r * math.sin(a)

    for i, ((name, col), boxes, ry) in enumerate(zip(segments, rows, rail_y)):
        a0, a1 = start + i * span + 1.2, start + (i + 1) * span - 1.2
        (x0, y0), (x1, y1) = pt(r0, a0), pt(r1, a0)
        (x2, y2), (x3, y3) = pt(r1, a1), pt(r0, a1)
        c.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f} A {r1} {r1} 0 0 1 {x2:.1f} {y2:.1f} "
               f"L {x3:.1f} {y3:.1f} A {r0} {r0} 0 0 0 {x0:.1f} {y0:.1f} Z",
               color=col[1], sw=1.8, arrow=False, fill=col[0])
        mid = (a0 + a1) / 2
        tx, ty = pt((r0 + r1) / 2 + 6, mid)
        c.text(tx, ty + 6, name, size=17, weight="700", color=col[1], rotate=mid)
        ex, ey = pt(r1 + 4, mid)
        c.path(f"M {ex:.1f} {ey:.1f} C {ex + 50:.1f} {ey:.1f}, {rail_x0 - 50} {ry}, {rail_x0} {ry}",
               color=col[1], sw=2.2, arrow=False)
        c.line(rail_x0, ry, rail_x1, ry, color=col[1], sw=2.2, arrow=False)
        bw = (rail_x1 - rail_x0 - 3 * 18) / 4
        for j, (title, body) in enumerate(boxes):
            bx = rail_x0 + j * (bw + 18)
            c.rect(bx, ry - 150, bw, 126, fill="#ffffff", stroke=col[1], rx=10, sw=1.4)
            c.text(bx + bw / 2, ry - 122, title, size=15.5, weight="700", color=col[1])
            c.lines(bx + bw / 2, ry - 98, body, size=13, gap=19)
            c.line(bx + bw / 2, ry - 24, bx + bw / 2, ry - 5, color=col[1], sw=1.6, arrow=False)
            c.circle(bx + bw / 2, ry, 6, "#ffffff", col[1], sw=2.2)
        c.circle(rail_x0, ry, 5, col[1], col[1])
    c.circle(cx, cy, r0 - 8, "#ffffff", SEM[1], sw=2.5)
    c.text(cx, cy - 26, "✳", size=40, color=SEM[1])
    c.text(cx, cy + 12, "SEMANTICS", size=22, weight="700", color=SEM[1])
    c.text(cx, cy + 36, "ontology · graphs", size=14, color=INK)
    c.text(cx, cy + 56, "semantic models", size=14, color=INK)
    c.rect(40, 1360, W - 80, 150, fill=EXAMPLE[0], stroke=EXAMPLE[1])
    c.text(W / 2, 1396, "examples/retail: one Amazon-style domain, every format, CI-verified", size=19, weight="700",
           color=EXAMPLE[1])
    stations = ["OWL + SHACL", "RDF × 6 formats", "13 SPARQL queries", "property graph", "warehouse tables",
                "Apache Ossie", "dbt MetricFlow ✓", "COA metrics"]
    sw_ = (W - 120) / len(stations)
    c.line(70, 1455, W - 70, 1455, color=EXAMPLE[1], sw=2.2, arrow=False)
    for k, s in enumerate(stations):
        x = 60 + sw_ * (k + 0.5)
        c.circle(x, 1455, 6, "#ffffff", EXAMPLE[1], sw=2.2)
        c.text(x, 1440, s, size=13.5, weight="600", color=INK)
    c.text(W / 2, 1488, "same answers everywhere: Alice 1498.97 · Bob 199.98 · Carol 179.48",
           size=14, color=INK)
    c.text(W / 2, 1560, "github.com/rongali-naidu/semantics-ontology-graphs · status as of November 2026",
           size=13, color=MUTED)
    return c


# ---------------------------------------------------------------------------
@diagram("ontology-to-tables")
def ontology_to_tables():
    c = Canvas(1000, 540, "Mapping warehouse tables to the ontology with R2RML")
    c.heading("Mapping tables and columns to the ontology", "examples/retail/mapping/retail-r2rml.ttl (W3C R2RML)")
    c.text(170, 88, "warehouse tables", size=13, weight="700", color=NEUTRAL[1])
    c.text(500, 88, "R2RML rule", size=13, weight="700", color=MUTED)
    c.text(830, 88, "ontology / knowledge graph", size=13, weight="700", color=ONTO[1])
    groups = [("products", "retail:Product", [("product_id", "ex:P1  (IRI)", "rr:template"),
                                               ("name", "retail:name", "rr:column"),
                                               ("list_price", "retail:price  xsd:decimal", "rr:column + rr:datatype"),
                                               ("category_id", "retail:inCategory → ex:CAT-…", "FK → object property")]),
              ("customers", "retail:Customer / PremiumCustomer", [("customer_id", "ex:C1  (IRI)", "rr:template"),
                                                                    ("is_premium = 'true'", "a retail:PremiumCustomer", "rr:sqlQuery … WHERE")]),
              ("orders", "retail:Order", [("order_id", "ex:O1  (IRI)", "rr:template"),
                                          ("customer_id", "retail:placedBy → ex:C1", "FK → object property"),
                                          ("order_date", "retail:orderDate  xsd:date", "rr:column + rr:datatype")])]
    y = 104
    for table, cls, rows in groups:
        h = 30 + 27 * len(rows)
        c.rect(40, y, 260, h, fill=NEUTRAL[0], stroke=NEUTRAL[1], rx=8)
        c.text(56, y + 21, table, size=13.5, weight="700", anchor="start", color=NEUTRAL[1], mono=True)
        c.rect(700, y, 260, h, fill=ONTO[0], stroke=ONTO[1], rx=8)
        c.text(716, y + 21, cls, size=13, weight="700", anchor="start", color=ONTO[1])
        for i, (col, prop, rule) in enumerate(rows):
            ry = y + 46 + i * 27
            c.text(56, ry, col, size=12.5, anchor="start", mono=True)
            c.text(716, ry, prop, size=12.5, anchor="start", mono=True)
            c.line(302, ry - 4, 698, ry - 4, color="#98A2B3", sw=1.2)
            c.label(500, ry, rule, size=11, color=INK)
        y += h + 12
    c.rect(40, 482, 920, 38, fill=GOOD[0], stroke=GOOD[1])
    c.text(500, 506, "✓ scripts/check_r2rml.py: the mapping generates 165 triples = retail-data.ttl (checked in CI)",
           size=12.5, color=GOOD[1])
    return c


# ---------------------------------------------------------------------------
@diagram("rdbms-vs-graph")
def rdbms_vs_graph():
    c = Canvas(1000, 420, "SQL joins versus graph traversal")
    c.heading("\"Bought the earbuds, also bought…\": joins vs traversal", "same question, same answer, two ways of finding relationships")
    c.rect(24, 80, 470, 276, fill="#FCFCFD", stroke="#D0D5DD")
    c.text(259, 106, "Relational: join at query time", size=14, weight="600", color=NEUTRAL[1])
    tables = ["products", "order_lines", "orders", "orders", "order_lines", "products"]
    for i, t in enumerate(tables):
        x, y = 48 + (i % 3) * 150, 130 + (i // 3) * 110
        c.rect(x, y, 120, 44, fill=NEUTRAL[0], stroke=NEUTRAL[1], rx=6)
        c.text(x + 60, y + 27, t, size=12.5, mono=True)
    for (x1, y1, x2, y2) in [(168, 152, 196, 152), (318, 152, 346, 152), (408, 174, 408, 238), (346, 262, 318, 262), (196, 262, 168, 262)]:
        c.line(x1, y1, x2, y2, arrow=False, color=NEUTRAL[1], sw=1.6)
    for x, y in [(182, 143), (332, 143), (423, 210), (332, 254), (182, 254)]:
        c.text(x, y, "⋈", size=15, color=SEM[1], weight="700")
    c.text(259, 330, "5 joins · cost grows with table sizes and hops", size=12, color=MUTED)
    c.rect(506, 80, 470, 276, fill="#FCFCFD", stroke="#D0D5DD")
    c.text(741, 106, "Graph: follow stored edges", size=14, weight="600", color=GRAPH[1])
    nodes = [("Earbuds", 560, 170, GRAPH), ("O3", 650, 170, EXAMPLE), ("Alice", 740, 170, ONTO),
             ("O1", 830, 170, EXAMPLE), ("Laptop", 920, 170, GRAPH)]
    for name, x, y, col in nodes:
        c.circle(x, y, 32, col[0], col[1], sw=2)
        c.text(x, y + 5, name, size=12, weight="600", color=col[1])
    for (x1, x2, lab) in [(618, 592, "CONTAINS"), (708, 682, "PLACED"), (772, 798, "PLACED"), (862, 888, "CONTAINS")]:
        c.line(x1, 170, x2, 170, color=MUTED)
        c.text((x1 + x2) / 2, 128, lab, size=10, color=MUTED)
    c.rect(560, 236, 360, 58, fill="#fff", stroke=GRAPH[1], rx=6)
    c.text(740, 258, "MATCH (t)<-[:CONTAINS]-()<-[:PLACED]-(c)", size=11.5, mono=True)
    c.text(740, 278, "      -[:PLACED]->()-[:CONTAINS]->(other)", size=11.5, mono=True)
    c.text(741, 330, "cost grows with the part of the graph visited", size=12, color=MUTED)
    c.rect(24, 368, 952, 36, fill=GOOD[0], stroke=GOOD[1])
    c.text(500, 391, "same answer: Knowledge Graphs 101 · Laptop Pro 14 · USB-C Charger 65W (1 buyer each)", size=12.5, color=GOOD[1])
    return c


# ---------------------------------------------------------------------------
@diagram("data-agent")
def data_agent():
    c = Canvas(1000, 520, "What a data agent needs")
    c.heading("A data agent needs context, not just SQL access", "each component answers a different kind of question")
    c.box(250, 80, 500, 56, "\"Why did premium Electronics revenue drop, and who are those customers?\"", [],
          EXAMPLE, title_size=13.5)
    c.box(380, 160, 240, 56, "Data agent (LLM + tools)", [], NEUTRAL, title_size=14)
    c.line(500, 136, 500, 158)
    tools = [(30, "Semantic model", "how much? how many?", ["governed metrics · joins", "revenue = Σ qty × price"], SEM),
             (275, "Ontology", "what does it mean?", ["vocabulary · synonyms", "premium ⊑ customer"], ONTO),
             (520, "Knowledge graph", "where is it? how related?", ["concepts ↔ tables ↔ metrics", "lineage · key entities"], GRAPH),
             (765, "Documents", "why?", ["policies · definitions", "RAG retrieval"], NEUTRAL)]
    for x, t, q, body, col in tools:
        c.rect(x, 252, 205, 128, fill=col[0], stroke=col[1])
        c.text(x + 102, 278, t, size=15, weight="700", color=col[1])
        c.text(x + 102, 299, q, size=12.5, color=INK, italic=True)
        c.lines(x + 102, 326, body, size=11.5, gap=18, color=MUTED)
        c.line(500, 218, x + 102, 250, dash="3 3")
    c.rect(30, 408, 940, 46, fill="#F9FAFB", stroke="#D0D5DD")
    c.text(500, 436, "same data underneath: warehouse tables · graph store · documents (linked by IRIs and mappings)",
           size=12.5, color=INK)
    c.text(500, 488, "start with the semantic model for numbers · add the ontology when vocabulary diverges · add the KG when data spans many sources",
           size=12, color=MUTED, italic=True)
    for x in (132, 377, 622, 867):
        c.line(x, 382, x, 406, arrow=False, color="#98A2B3")
    return c


# ---------------------------------------------------------------------------
@diagram("ai-era")
def ai_era():
    c = Canvas(1000, 470, "Semantics and LLMs, both directions")
    c.heading("Semantics and LLMs need each other", "LLMs bring language and reasoning; semantics brings the enterprise's meaning, facts and numbers")
    c.box(30, 110, 300, 250, "LLMs / agents", ["fluent language", "reasoning and planning", "tool calling (MCP)", "",
                                                "but: no built-in knowledge", "of YOUR terms, tables,", "rules or numbers"],
          EXAMPLE, title_size=17, body_size=13, body_gap=24)
    c.rect(670, 110, 300, 250, fill="#fff", stroke=NEUTRAL[1])
    c.text(820, 140, "Semantics", size=17, weight="700", color=NEUTRAL[1])
    for i, (t, s, col) in enumerate([("Ontology", "meaning · vocabulary · rules", ONTO),
                                      ("Knowledge graph", "facts · connections · identity", GRAPH),
                                      ("Semantic model", "governed numbers", SEM)]):
        y = 158 + i * 64
        c.rect(690, y, 260, 54, fill=col[0], stroke=col[1])
        c.text(820, y + 23, t, size=14, weight="700", color=col[1])
        c.text(820, y + 42, s, size=11.5, color=INK)
    c.path("M 668 175 C 560 150, 440 150, 332 175", color=GOOD[1], sw=2.2)
    c.label(500, 135, "grounds the LLM", size=13, color=GOOD[1])
    for i, s in enumerate(["exact meaning, fewer wrong terms", "facts, paths, provenance (GraphRAG)",
                           "correct metrics (text-to-metric)", "guardrails: validate output (SHACL)"]):
        c.text(500, 172 + i * 19, s, size=11.5, color=INK)
    c.path("M 332 300 C 440 330, 560 330, 668 300", color=SEM[1], sw=2.2)
    c.label(500, 350, "helps build semantics", size=13, color=SEM[1])
    for i, s in enumerate(["draft ontologies & mappings (R2RML)", "align to FIBO / schema.org",
                           "extract entities from text"]):
        c.text(500, 262 + i * 19, s, size=11.5, color=INK)
    c.rect(30, 392, 940, 54, fill=WARN[0], stroke=WARN[1])
    c.text(500, 415, "the rule that keeps it safe:  LLM proposes  →  human approves  →  machine checks",
           size=14, weight="600", color=INK)
    c.text(500, 435, "(this repo's CI: R2RML must reproduce the graph · SHACL must pass · every format gives the same answers)",
           size=11.5, color=MUTED)
    return c


# ---------------------------------------------------------------------------
@diagram("agent-context-layers")
def agent_context_layers():
    c = Canvas(1000, 560, "What goes in the graph for a data agent, and what stays in the warehouse")
    c.heading("At scale, the graph holds meaning, not terabytes of orders",
              "a data agent plans with the context graph, computes with the semantic model, and reads facts from the warehouse")
    c.box(330, 82, 340, 50, "Data agent (LLM + tools)", [], EXAMPLE, title_size=14.5)
    cols = [(30, "Context graph (metadata KG)", ["ontology concepts · glossary", "tables · columns · mappings",
             "metric references · lineage", "owners · example queries"], ONTO, "thousands–millions of nodes", "1. understand & plan"),
            (350, "Semantic model", ["metric definitions", "joins · grain · fan-out rules", "compiles to correct SQL", "(executable)"],
             SEM, "per domain; text files", "2. compute numbers"),
            (670, "Entity graph (optional)", ["customers · products · suppliers", "identities resolved across", "systems · relationships",
             "(master data, not transactions)"], GRAPH, "millions of nodes", "3. who / how connected")]
    for x, t, body, col, size, step in cols:
        c.box(x, 186, 300, 150, t, body, col, title_size=14.5, body_size=12.5, body_gap=20)
        c.text(x + 150, 330, size, size=11, color=col[1], italic=True)
        c.line(500, 134, x + 150, 184)
        c.label(x + 150 + (40 if x < 350 else -40 if x > 350 else 0), 166, step, size=11.5, color=INK)
    c.line(330, 262, 348, 262, both=True)
    c.line(650, 262, 668, 262, both=True)
    c.rect(30, 400, 940, 76, fill=NEUTRAL[0], stroke=NEUTRAL[1])
    c.text(500, 428, "Warehouse / lakehouse: transactions stay here", size=15, weight="700", color=NEUTRAL[1])
    c.text(500, 452, "orders · order lines · events · terabytes   (graphs over tables: Spanner / BigQuery Graph, SQL/PGQ)",
           size=12.5, color=INK)
    c.line(500, 338, 500, 398)
    c.label(500, 372, "SQL", size=11.5)
    c.line(820, 398, 820, 338, dash="4 3")
    c.label(820, 372, "load master data", size=11)
    c.line(180, 398, 180, 338, dash="4 3", both=True)
    c.label(180, 372, "virtual KG: SPARQL → SQL", size=11)
    c.rect(30, 494, 940, 46, fill=WARN[0], stroke=WARN[1])
    c.text(500, 522, "the retail example loads everything into the graph only because it is tiny (165 triples); at scale, don't",
           size=12.5, color=INK)
    return c


# ---------------------------------------------------------------------------
@diagram("six-dimensions")
def six_dimensions():
    W = 1480
    c = Canvas(W, 1200, "The six dimensions of meaning, on the retail example")
    c.heading("Metadata, semantic model, knowledge base, ontology, knowledge graph or lineage?",
              "the six dimensions of a semantic layer, each shown on this repo's retail example "
              "(the knowledge graph in its two kinds)")
    cols = [("Metadata", "describes the data", NEUTRAL), ("Semantic model", "encodes business logic", SEM),
            ("Knowledge base", "captures context", GOOD), ("Ontology & taxonomy", "defines meaning", ONTO),
            ("Data graph", "entities and relationships", GRAPH), ("Semantic graph", "meaning, not records", GRAPH),
            ("Lineage", "proves trust", LINEAGE)]
    xs = [30 + i * 203 for i in range(7)]
    CW = 197
    captions = ["columns + types + meaning", "business logic → tables", "rules + verified answers",
                "tree + classes + rules", "this customer, these orders", "metric ↔ terms ↔ tables",
                "where a number came from"]
    for i, (x, (t, sub, col), cap) in enumerate(zip(xs, cols, captions)):
        c.rect(x, 84, CW, 360, fill="#fff", stroke=col[1])
        if i not in (4, 5):
            c.rect(x, 84, CW, 34, fill=col[1], stroke=col[1])
            c.text(x + CW / 2, 107, t, size=15, weight="700", color="#ffffff")
            c.text(x + CW / 2, 136, sub, size=11.5, color=MUTED, italic=True)
        else:
            c.text(x + CW / 2, 136, {4: "data graph · records", 5: "semantic graph · metadata"}[i],
                   size=11.5, weight="600", color=GRAPH[1])
        c.rect(x + 8, 418, CW - 16, 20, fill=col[0], stroke=col[0], rx=5)
        c.text(x + CW / 2, 432, cap, size=10.5, weight="600", color=col[1])
    kx = xs[4]
    c.rect(kx, 84, xs[5] + CW - kx, 34, fill=GRAPH[1], stroke=GRAPH[1])
    c.text(kx + (xs[5] + CW - kx) / 2, 107, "Knowledge graph: two kinds", size=15, weight="700", color="#ffffff")

    def mono(x, y, rows, size=10, gap=14.5, color=INK):
        for i, r in enumerate(rows):  # non-breaking spaces keep the indentation (SVG collapses spaces)
            c.text(x, y + i * gap, r.replace(" ", " "), size=size, mono=True, anchor="start", color=color)

    def pill(x, y, w, s, col, size=10, mono_=False):
        c.rect(x, y, w, 22, fill=col[0], stroke=col[1], rx=11)
        c.text(x + w / 2, y + 15, s, size=size, weight="600", color=col[1], mono=mono_)

    # 1 metadata: schema.sql types and keys, Ossie descriptions, SHACL sh:in
    x = xs[0]
    c.rect(x + 8, 148, CW - 16, 262, fill=NEUTRAL[0], stroke="#D0D5DD", rx=6)
    mono(x + 16, 168, ["customers.is_premium", "  BOOLEAN NOT NULL", "  \"paid membership\"", "",
                       "order_lines.unit_price", "  DECIMAL(10,2)", "  \"price actually paid\"", "",
                       "orders.status", "  PLACED | SHIPPED |", "  DELIVERED | CANCELLED", "",
                       "orders.customer_id", "  FK → customers"])
    # 2 semantic model: Ossie metric over physical tables
    x = xs[1]
    c.rect(x + 8, 148, CW - 16, 128, fill=SEM[0], stroke=SEM[1], rx=6)
    c.text(x + CW / 2, 164, "business layer", size=10.5, weight="600", color=SEM[1])
    mono(x + 16, 182, ["revenue =", "  SUM(quantity", "      × unit_price)", "aov = revenue", "      / order_count",
                       "dims: category_level_1›2›3", "      is_premium"], size=9.5, gap=13)
    c.line(x + CW / 2, 278, x + CW / 2, 306)
    c.label(x + CW / 2 + 32, 297, "maps to", size=10)
    c.rect(x + 8, 308, CW - 16, 102, fill="#fff", stroke=SEM[1], rx=6, dash="4 3")
    c.text(x + CW / 2, 324, "physical tables", size=10.5, weight="600", color=SEM[1])
    mono(x + 16, 344, ["order_lines", "  ⋈ orders ⋈ customers", "products ⋈ categories", "(Ossie, dbt, LookML…)"],
         size=9.5, gap=15)
    # 3 knowledge base: Ossie ai_context + verified queries with expected answers
    x = xs[2]
    c.rect(x + 8, 148, CW - 16, 134, fill=GOOD[0], stroke=GOOD[1], rx=6)
    c.text(x + CW / 2, 164, "rules (ai_context)", size=10.5, weight="600", color=GOOD[1])
    c.lines(x + CW / 2, 183, ["“Revenue means the price", "actually paid, not list price.”",
                               "“Count orders with order_count,", "never by counting lines.”",
                               "“Use category_level_1 for", "Electronics.”"], size=9.8, gap=15, color=INK)
    c.rect(x + 8, 290, CW - 16, 120, fill="#fff", stroke=GOOD[1], rx=6)
    c.text(x + CW / 2, 306, "verified queries", size=10.5, weight="600", color=GOOD[1])
    mono(x + 16, 325, ["03-order-totals…rq", "→ Alice 1498.97", "  Bob 199.98", "  Carol 179.48", "metrics.sql",
                       "→ revenue 1878.43"], size=9.5, gap=14)
    # 4 ontology & taxonomy: category tree (skos:broader) + classes and axioms
    x = xs[3]
    c.text(x + 14, 160, "taxonomy (skos:broader)", size=10.5, weight="600", color=ONTO[1], anchor="start")
    mono(x + 18, 178, ["Electronics", "├─ Computers", "│  └─ Laptops", "└─ Audio", "Books · Kitchen"],
         size=10, gap=14)
    c.line(x + 8, 252, x + CW - 8, 252, arrow=False, color="#D0D5DD", dash="3 3")
    c.text(x + 14, 270, "ontology (OWL)", size=10.5, weight="600", color=ONTO[1], anchor="start")
    c.rect(x + 8, 280, 62, 24, fill=ONTO[0], stroke=ONTO[1], rx=5)
    c.text(x + 39, 296, "Order", size=10.5, weight="600", color=ONTO[1])
    c.rect(x + 110, 280, 78, 24, fill=ONTO[0], stroke=ONTO[1], rx=5)
    c.text(x + 149, 296, "Customer", size=10.5, weight="600", color=ONTO[1])
    c.line(x + 71, 292, x + 108, 292)
    c.text(x + 90, 315, "placedBy", size=9, color=MUTED)
    c.rect(x + 88, 330, 102, 22, fill=ONTO[0], stroke=ONTO[1], rx=5)
    c.text(x + 139, 345, "PremiumCustomer", size=10, weight="600", color=ONTO[1])
    c.line(x + 149, 329, x + 149, 306)
    c.text(x + 162, 322, "⊑", size=11, color=MUTED)
    c.lines(x + CW / 2, 370, ["Order placedBy exactly 1 Customer", "Customer disjointWith Seller",
                               "subCategoryOf is transitive"], size=9.5, gap=13.5, color=INK)
    # 5 data knowledge graph: instance chain from retail-data.ttl
    x = xs[4]
    chain = [("Alice : PremiumCustomer", 150), ("O1 : Order", 202), ("Laptop Pro 14 : Product", 254),
             ("Laptops : Category", 306), ("Computers : Category", 358)]
    edges = ["PLACED", "CONTAINS {qty 1}", "IN_CATEGORY", "SUBCATEGORY_OF"]
    for i, (n, y) in enumerate(chain):
        pill(x + 18, y, 160, n, GRAPH, size=10.5)
        if i < 4:
            c.line(x + 46, y + 23, x + 46, y + 50)
            c.text(x + 54, y + 41, edges[i], size=9, color=MUTED, anchor="start")
    c.text(x + CW / 2, 402, "retail-data.ttl: 29 nodes · 41 edges", size=10, color=MUTED)
    # 6 semantic (metadata) knowledge graph: links that exist in the repo's files
    x = xs[5]
    pill(x + 28, 150, 140, "metric: revenue", GRAPH, size=10.5)
    links = [("synonym", "“sales”, “GMV”"), ("defined in", "Ossie · dbt · COA"), ("about concept", "retail:OrderLine"),
             ("computed from", "fct_order_lines"), ("column", "line_amount")]
    c.line(x + 40, 173, x + 40, 392, arrow=False, color=MUTED)
    for i, (lab, tgt) in enumerate(links):
        y = 186 + i * 44
        c.line(x + 40, y + 22, x + 76, y + 22)
        c.text(x + 80, y + 9, lab, size=9, color=MUTED, anchor="start")
        c.rect(x + 78, y + 12, 112, 22, fill="#fff", stroke=GRAPH[1], rx=5)
        c.text(x + 134, y + 27, tgt, size=9.5, color=GRAPH[1], weight="600")
    c.text(x + CW / 2, 405, "links found in the repo's files", size=9.5, color=MUTED, italic=True)
    # 7 lineage: the dbt pipeline, source tables → model → metric (run in CI)
    x = xs[6]
    c.rect(x + 18, 148, CW - 36, 40, fill="#fff", stroke=LINEAGE[1], rx=6, dash="4 3")
    c.text(x + CW / 2, 164, "sources", size=10.5, weight="600", color=LINEAGE[1])
    c.text(x + CW / 2, 180, "order_lines · orders · products", size=9.5, color=INK)
    c.line(x + CW / 2, 189, x + CW / 2, 204)
    c.rect(x + 18, 206, CW - 36, 40, fill=LINEAGE[0], stroke=LINEAGE[1], rx=6)
    c.text(x + CW / 2, 222, "fct_order_lines", size=10.5, mono=True, weight="600", color=LINEAGE[1])
    c.text(x + CW / 2, 238, "line_amount = qty × price", size=9.5, color=INK)
    c.line(x + CW / 2, 247, x + CW / 2, 268)
    c.rect(x + 18, 270, CW - 36, 40, fill=LINEAGE[0], stroke=LINEAGE[1], rx=6)
    c.text(x + CW / 2, 286, "measure revenue", size=10.5, mono=True, weight="600", color=LINEAGE[1])
    c.text(x + CW / 2, 302, "sum(line_amount)", size=9.5, color=INK)
    c.line(x + CW / 2, 311, x + CW / 2, 332)
    c.rect(x + 18, 334, CW - 36, 40, fill=LINEAGE[0], stroke=LINEAGE[1], rx=6)
    c.text(x + CW / 2, 350, "metric revenue", size=10.5, mono=True, weight="600", color=LINEAGE[1])
    c.text(x + CW / 2, 366, "= 1878.43 (CI)", size=9.5, color=INK)
    c.text(x + CW / 2, 396, "sources → dbt model → metric", size=9.5, color=MUTED, italic=True)
    c.text(x + CW / 2, 409, "(the repo's dbt project)", size=9.5, color=MUTED, italic=True)

    # one question, seven contributions
    c.rect(30, 462, W - 60, 168, fill="#F9FAFB", stroke="#D0D5DD")
    c.text(W / 2, 487, "One question, every dimension contributes: “What was revenue from premium customers in Electronics?”",
           size=14.5, weight="700", color=EXAMPLE[1])
    contrib = [["is_premium = paid membership;", "unit_price = price paid"],
               ["revenue = Σ quantity × unit_price,", "filtered: premium, Electronics"],
               ["use the price paid, not list", "price; Electronics = level 1"],
               ["premium customers ⊑ Customer;", "Laptops ⊂ Computers ⊂ Electronics"],
               ["who: Alice (orders O1, O3);", "Carol bought Books, Kitchen"],
               ["“revenue” = governed metric,", "computed from fct_order_lines"],
               ["answer ← metric revenue ←", "fct_order_lines ← 3 sources"]]
    for x, (t, _, col), lines in zip(xs, cols, contrib):
        c.rect(x, 500, CW, 70, fill=col[0], stroke=col[1], rx=6)
        c.text(x + CW / 2, 516, t, size=11, weight="700", color=col[1])
        c.lines(x + CW / 2, 535, lines, size=9.8, gap=15, color=INK)
    c.rect(38, 582, W - 76, 36, fill=GOOD[0], stroke=GOOD[1], rx=6)
    c.text(W / 2, 605, "answer: 1498.97, all from Alice Johnson's orders: Laptop Pro 14, 2 × USB-C Charger 65W (O1) "
           "and Wireless Earbuds X (O3)", size=12.5, weight="600", color=GOOD[1])

    # comparison table
    rows = [("Purpose",
             [["describe tables and columns:", "types, meaning, owners"],
              ["define metrics, dimensions", "and joins once, for every", "tool and agent"],
              ["capture rules, definitions", "and verified Q&A the data", "itself doesn't say"],
              ["define what things are, how", "they relate, and the rules", "(a taxonomy: just the tree)"],
              ["store real entities and their", "relationships: customers,", "orders, products"],
              ["store meaning, not records:", "terms, metrics, concepts,", "tables, owners, lineage"],
              ["show where a number came", "from and what depends on it"]]),
            ("Form",
             [["catalog entries: schema,", "descriptions, constraints"],
              ["datasets, fields, metrics,", "joins over physical tables"],
              ["documents, instructions,", "example questions + SQL"],
              ["classes, properties, axioms", "(TBox); taxonomy = broader /", "narrower concept tree"],
              ["instances (ABox) as triples", "or a property graph"],
              ["a metadata graph linking", "glossary, semantic model,", "ontology and catalog"],
              ["a DAG: sources → models →", "metrics, down to columns"]]),
            ("Standards",
             [["DCAT, Dublin Core;", "catalog APIs"],
              ["Apache Ossie, MetricFlow,", "LookML, TMDL, semantic views"],
              ["none: docs, Ossie ai_context,", "verified queries"],
              ["OWL 2, RDFS, SHACL;", "SKOS for taxonomies"],
              ["RDF + SPARQL, or property", "graph + Cypher / ISO GQL"],
              ["RDF, SKOS, DCAT, PROV-O;", "or a catalog's graph API"],
              ["OpenLineage, W3C PROV-O"]]),
            ("Reasoning",
             [["none; lookup and search"],
              ["no logical inference;", "computes aggregates without", "double counting"],
              ["none; retrieved (RAG) and", "applied by the LLM"],
              ["a reasoner infers and checks:", "Alice is a Customer; a", "Customer + Seller is an error"],
              ["traversal and paths; inference", "only when backed by an", "ontology"],
              ["navigate meaning: which", "metric, which tables, whose,", "how fresh"],
              ["impact analysis: what breaks", "if a source changes"]]),
            ("In this repo",
             [["schema.sql, Ossie field", "descriptions, SHACL sh:in"],
              ["Ossie model, dbt MetricFlow,", "LookML, TMDL, COA metrics"],
              ["Ossie ai_context; .rq files", "with expected answers"],
              ["retail-ontology.ttl,", "retail-shapes.ttl, category", "tree (skos:broader)"],
              ["retail-data.ttl, property", "graph, Neptune load files"],
              ["links in Ossie mapping, COA", "ontologyConcepts; the graph", "itself isn't built here"],
              ["dbt: sources →", "fct_order_lines → revenue", "(run in CI)"]]),
            ("Typical tools",
             [["Unity Catalog, Glue Data", "Catalog, Dataplex, DataHub"],
              ["dbt, Looker, Power BI, Cube,", "AtScale, Snowflake"],
              ["wikis, vector stores; Genie", "instructions, Cortex verified", "queries"],
              ["Protégé, TopBraid, AWS COA;", "PoolParty for taxonomies"],
              ["Neptune, Neo4j, GraphDB,", "Stardog, Spanner Graph"],
              ["Knowledge Catalog, AWS COA,", "Fabric IQ, Genie Ontology,", "DataHub"],
              ["OpenLineage / Marquez, dbt", "docs, catalog lineage views"]])]
    tx = [156 + i * 184 for i in range(7)]
    TW = 178
    y = 646
    c.rect(30, y, 120, 30, fill=NEUTRAL[0], stroke=NEUTRAL[1], rx=6)
    c.text(90, y + 20, "Aspect", size=12.5, weight="700", color=NEUTRAL[1])
    for x, (t, _, col) in zip(tx, cols):
        c.rect(x, y, TW, 30, fill=col[1], stroke=col[1], rx=6)
        c.text(x + TW / 2, y + 20, t, size=12, weight="700", color="#ffffff")
    y += 36
    for label, cells in rows:
        h = max(len(cl) for cl in cells) * 14 + 14
        c.rect(30, y, 120, h, fill=NEUTRAL[0], stroke="#D0D5DD", rx=6)
        c.text(90, y + h / 2 + 4, label, size=12, weight="700", color=INK)
        for x, cl in zip(tx, cells):
            c.rect(x, y, TW, h, fill="#fff", stroke="#D0D5DD", rx=6)
            top = y + (h - len(cl) * 14) / 2 + 11
            c.lines(x + TW / 2, top, cl, size=10, gap=14, color=INK)
        y += h + 6
    c.rect(30, y + 6, W - 60, 34, fill=WARN[0], stroke=WARN[1])
    c.text(W / 2, y + 28, "they overlap: give each piece of meaning one source of truth, and make the others reference it",
           size=12.5, weight="600", color=INK)
    c.h = y + 56
    return c


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        (OUT / f"{name}.svg").write_text(fn().svg(), encoding="utf-8")
    print(f"wrote {len(DIAGRAMS)} diagrams to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
