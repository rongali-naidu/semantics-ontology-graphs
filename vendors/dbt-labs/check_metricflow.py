#!/usr/bin/env python3
"""Run MetricFlow queries on the dbt project and compare with the known answers.

    cd vendors/dbt-labs/retail_dbt && DBT_PROFILES_DIR=. dbt build
    python ../check_metricflow.py          (run from retail_dbt/)

The expected values are the SPARQL answers over the RDF graph
(examples/retail/sparql/03-order-totals-per-customer.rq) and the totals in
examples/retail/warehouse/metrics.sql.
"""
import csv
import subprocess
import sys
import tempfile
from decimal import Decimal
from pathlib import Path

CHECKS = [
    (["--metrics", "revenue,units_sold,order_count,average_order_value,buyer_count,discount_amount"],
     [{"revenue": "1878.43", "units_sold": "9", "order_count": "4",
       "average_order_value": "469.61", "buyer_count": "3", "discount_amount": "10.00"}]),
    (["--metrics", "revenue,order_count", "--group-by", "customer__customer_name"],
     [{"customer__customer_name": "Alice Johnson", "revenue": "1498.97", "order_count": "2"},
      {"customer__customer_name": "Bob Smith", "revenue": "199.98", "order_count": "1"},
      {"customer__customer_name": "Carol Diaz", "revenue": "179.48", "order_count": "1"}]),
    (["--metrics", "revenue", "--group-by", "product__category_level_1"],
     [{"product__category_level_1": "Books", "revenue": "149.97"},
      {"product__category_level_1": "Electronics", "revenue": "1648.96"},
      {"product__category_level_1": "Kitchen", "revenue": "79.50"}]),
    (["--metrics", "premium_revenue"], [{"premium_revenue": "1678.45"}]),
]


def norm(v: str) -> str:
    try:
        return str(Decimal(v).quantize(Decimal("0.01")))
    except Exception:
        return v


def main() -> int:
    failed = 0
    for args, expected in CHECKS:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "result.csv"
            subprocess.run(["mf", "query", *args, "--csv", str(out), "--quiet"], check=True)
            with out.open() as f:
                rows = [{k: norm(v) for k, v in r.items()} for r in csv.DictReader(f)]
        want = [{k: norm(v) for k, v in r.items()} for r in expected]
        key = lambda r: sorted(r.items())
        ok = sorted(rows, key=key) == sorted(want, key=key)
        print(("ok  " if ok else "FAIL"), "mf query", " ".join(args))
        if not ok:
            print("    got     ", rows, "\n    expected", want)
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
