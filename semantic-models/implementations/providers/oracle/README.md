# Oracle: semantic models

> **Verification:** ⚪ design only. This folder maps the retail model onto
> Oracle's layers; there is no model file yet (see [ROADMAP](../../../../ROADMAP.md)).
> Last reviewed 2026-11-03.

| Concept | Oracle product | Retail example |
|---|---|---|
| Semantic model (classic) | **Oracle Analytics RPD** (OBIEE / OAS / OAC): Physical, Business Model and Mapping, Presentation layers | mapping below |
| Semantic model (modern) | **Oracle Analytics Semantic Modeler**: SMML (JSON) files in a **user-defined Git repository** | mapping below |
| Self-service models | Oracle Analytics datasets | — |
| Open format | Apache Ossie: check the converter list | — |

Oracle also appears in
[graphs (property graphs, PGX)](../../../../graphs/implementations/providers/oracle/README.md) and
[ontologies (RDF Graph)](../../../../ontologies/implementations/providers/oracle/README.md).

How Oracle stores and promotes the semantic model (RPD file, MUDE, MDS XML,
Semantic Modeler + Git) is covered in
[semantic models concepts 3](../../../concepts/03-semantic-model-repositories.md#31-oracle-analytics-oac--oas-formerly-obiee).

## The retail model in Oracle's three layers

| Layer | Object | Definition |
|---|---|---|
| **Physical** | database + connection pool `Retail` | points at schema `retail` ([`schema.sql`](../../../../examples/retail/warehouse/schema.sql)) |
| | physical tables | `order_lines`, `orders`, `customers`, `addresses`, `products`, `categories`, `sellers`, `reviews` |
| | physical joins | `order_lines.order_id = orders.order_id`, `order_lines.product_id = products.product_id`, `orders.customer_id = customers.customer_id`, `products.category_id = categories.category_id`, ... |
| **Business Model and Mapping** | logical fact **Fact – Order Lines** (sources: `order_lines` + `orders`) | logical columns with aggregation rules: `Revenue` = SUM(`quantity * unit_price`), `Units Sold` = SUM(`quantity`), `Order Count` = COUNT DISTINCT(`order_id`), `Discount Amount` = SUM(`quantity * (list_price - unit_price)`) |
| | derived measure | `Average Order Value` = `Revenue / Order Count` (calculated from logical columns, so it is right at every level) |
| | logical dimension **Customer** | `Customer Name`, `Is Premium`, `City`, `State`; hierarchy *Total → State → City → Customer* |
| | logical dimension **Product** | `Product Name`, `SKU`, `Seller`; level-based hierarchy *Total → Department (category_level_1) → Level 2 → Level 3 → Product* |
| | logical dimension **Time** | from `orders.order_date`: *Year → Quarter → Month → Day* (time dimension for AGO / TODATE functions) |
| | logical fact **Fact – Reviews** | `Average Rating` = AVG(`rating`); joins to Product and Customer only |
| **Presentation** | subject area **Retail Orders** | folders *Measures*, *Customer*, *Product*, *Time* |

The two-fact design (order lines, reviews sharing Product and Customer)
avoids the chasm trap described in
[chapter 1](../../../concepts/01-what-is-a-semantic-model.md#12-the-hard-problems-a-semantic-model-solves).

Docs: [Oracle Analytics Cloud](https://docs.oracle.com/en/cloud/paas/analytics-cloud/) ·
[Oracle Database graph](https://docs.oracle.com/en/database/oracle/property-graph/)
