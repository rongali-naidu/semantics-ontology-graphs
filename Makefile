# Common tasks. `make help` lists them.
PYTHON       ?= python3
RETAIL       := examples/retail
DBT_DIR      := semantic-models/implementations/tools/dbt/retail_dbt
# Apache Ossie spec the Ossie files are validated against (see
# examples/retail/semantic-model/ossie/README.md)
OSSIE_COMMIT := 10116f936e628944eadaa70ec7578caf23912e96
OSSIE_REPO   ?= .cache/ossie

.PHONY: help install generate diagrams check-r2rml check check-graph check-semantic check-ossie check-links check-generated dbt clean

help:            ## list targets
	@grep -E '^[a-z0-9-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-16s %s\n", $$1, $$2}'

install:         ## install the Python check dependencies
	$(PYTHON) -m pip install -r requirements.txt

# Data flow: rdf/retail-data.ttl (source of truth) is the ONLY hand-edited data file.
#   build_rdf_formats.py     -> examples/retail/rdf/*.{nt,nq,trig,rdf,jsonld}, graphs/implementations/providers/aws/rdf/
#   rdf_to_property_graph.py -> graphs/implementations/providers/aws/{gremlin,opencypher}-csv/, property-graph/*/01-create-*
#   rdf_to_tables.py         -> examples/retail/warehouse/data/, semantic-models/implementations/tools/dbt/retail_dbt/seeds/
generate:        ## regenerate every derived file from rdf/retail-data.ttl
	cd $(RETAIL) && $(PYTHON) scripts/build_rdf_formats.py && \
	  $(PYTHON) scripts/rdf_to_property_graph.py && $(PYTHON) scripts/rdf_to_tables.py
	$(PYTHON) tools/diagrams/build_diagrams.py

diagrams:        ## regenerate the SVG diagrams in assets/diagrams/
	$(PYTHON) tools/diagrams/build_diagrams.py

check: check-links check-graph check-semantic  ## run all fast checks (no network, no dbt)

check-graph:     ## SPARQL + SHACL + OWL reasoning demo + RDF/property-graph consistency
	cd $(RETAIL) && $(PYTHON) scripts/run_sparql_local.py --shacl > /dev/null && \
	  $(PYTHON) scripts/run_sparql_local.py --reason > /dev/null && \
	  $(PYTHON) scripts/demo_reasoning.py && \
	  $(PYTHON) scripts/check_consistency.py

check-r2rml:     ## run the R2RML mapping on the warehouse = retail-data.ttl (needs examples/retail/mapping/requirements.txt)
	cd $(RETAIL) && $(PYTHON) scripts/check_r2rml.py

check-semantic:  ## warehouse metrics + Ossie model vs SPARQL answers
	cd $(RETAIL) && $(PYTHON) scripts/check_semantic_model.py

$(OSSIE_REPO):
	git init -q $(OSSIE_REPO)
	git -C $(OSSIE_REPO) fetch -q --depth 1 https://github.com/apache/ossie.git $(OSSIE_COMMIT)
	git -C $(OSSIE_REPO) checkout -q FETCH_HEAD

check-ossie: $(OSSIE_REPO)  ## + validate Ossie files against the pinned official schemas
	cd $(RETAIL) && $(PYTHON) scripts/check_semantic_model.py --ossie-repo $(abspath $(OSSIE_REPO))

check-links:     ## relative links and anchors in all Markdown files
	$(PYTHON) tools/check_links.py

check-generated: generate  ## fail if committed derived files are out of date
	git diff --exit-code -- examples ontologies graphs semantic-models assets

dbt:             ## build the dbt project and check MetricFlow results (needs semantic-models/implementations/tools/dbt/requirements.txt)
	cd $(DBT_DIR) && DBT_PROFILES_DIR=. dbt build && DBT_PROFILES_DIR=. mf validate-configs && \
	  DBT_PROFILES_DIR=. $(PYTHON) ../check_metricflow.py

clean:           ## remove caches and build output
	rm -rf .cache $(DBT_DIR)/target $(DBT_DIR)/logs $(DBT_DIR)/*.duckdb
	find . -name __pycache__ -prune -exec rm -rf {} +
