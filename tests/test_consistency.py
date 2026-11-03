"""Every format describes the same data and gives the same answers."""
import check_consistency as cc
import check_semantic_model as cs


def test_rdf_serializations_are_isomorphic():
    cc.check_rdf_formats()        # asserts internally


def test_property_graph_csvs_match_sparql():
    expected = cc.sparql_answers()
    for folder, cols in [(cc.AWS / "opencypher-csv", (":ID", ":LABEL", ":TYPE", ":START_ID", ":END_ID")),
                         (cc.AWS / "gremlin-csv", ("~id", "~label", "~label", "~from", "~to"))]:
        assert cc.pg_answers(*cc.load_pg(folder, *cols)) == expected


def test_warehouse_metrics_match_sparql():
    cs.check_warehouse(cs.load_warehouse())


def test_ossie_model_metrics_and_references():
    cs.check_ossie(cs.load_warehouse(), None)


def test_coa_metric_definitions():
    cs.check_coa(cs.load_warehouse())
