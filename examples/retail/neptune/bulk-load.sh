#!/usr/bin/env bash
# ===========================================================================
# Load the retail example into Amazon Neptune with the BULK LOADER.
#
# The bulk loader reads files from S3 (it never takes data in the request
# body). One load job = one S3 prefix + one format.
#
#   format value   files in this repo                    query with
#   ------------   -----------------------------------   -------------------
#   csv            neptune/gremlin-csv/*.csv             Gremlin + openCypher
#   opencypher     neptune/opencypher-csv/*.csv          openCypher + Gremlin
#   turtle         neptune/rdf/*.ttl                     SPARQL
#   ntriples       neptune/rdf/retail-data.nt            SPARQL
#   nquads         neptune/rdf/retail-data.nq            SPARQL (named graphs)
#   rdfxml         neptune/rdf/retail-data.rdf           SPARQL
#
# JSON-LD and TriG are NOT bulk-load formats: convert them first
# (python scripts/build_rdf_formats.py writes .nt / .nq for you).
#
# Property-graph data (Gremlin/openCypher) and RDF data are stored
# separately in Neptune Database: SPARQL cannot see CSV-loaded data and
# vice versa. Load ONE of the CSV formats (they produce the same graph).
#
# Prereqs
#   * Neptune cluster in a VPC + an S3 VPC endpoint (gateway)
#   * IAM role with s3:GetObject/ListBucket attached to the cluster
#     ("Manage IAM roles" in the console / aws neptune add-role-to-db-cluster)
#   * Run from a host that can reach the cluster (EC2/Cloud9/notebook in VPC)
# Docs: https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load.html
# ===========================================================================
set -euo pipefail

NEPTUNE_ENDPOINT="${NEPTUNE_ENDPOINT:?set NEPTUNE_ENDPOINT, e.g. my-cluster.cluster-abc123.us-east-1.neptune.amazonaws.com}"
BUCKET="${BUCKET:?set BUCKET, e.g. my-graph-data-bucket}"
REGION="${AWS_REGION:-us-east-1}"
LOADER_ROLE_ARN="${LOADER_ROLE_ARN:?set LOADER_ROLE_ARN, e.g. arn:aws:iam::123456789012:role/NeptuneLoadFromS3}"
HERE="$(cd "$(dirname "$0")" && pwd)"
LOADER="https://${NEPTUNE_ENDPOINT}:8182/loader"

# --- 1. Upload the files to S3 -------------------------------------------
aws s3 sync "${HERE}/gremlin-csv"    "s3://${BUCKET}/retail/gremlin-csv/"
aws s3 sync "${HERE}/opencypher-csv" "s3://${BUCKET}/retail/opencypher-csv/"
aws s3 sync "${HERE}/rdf"            "s3://${BUCKET}/retail/rdf/"

# --- 2. Start load jobs -----------------------------------------------------
# If IAM database authentication is ON, plain curl will get 403: use awscurl
#   pip install awscurl;  alias curl='awscurl --service neptune-db --region $REGION'
# or the AWS CLI 'neptunedata' commands shown at the bottom of this file.

start_load() {   # $1 = S3 prefix, $2 = format, $3 = extra JSON (optional)
  curl -sS -X POST "${LOADER}" -H 'Content-Type: application/json' -d @- <<EOF
{
  "source": "s3://${BUCKET}/retail/$1",
  "format": "$2",
  "iamRoleArn": "${LOADER_ROLE_ARN}",
  "region": "${REGION}",
  "failOnError": "FALSE",
  "parallelism": "MEDIUM",
  "updateSingleCardinalityProperties": "FALSE",
  "queueRequest": "TRUE"${3:+,
  $3}
}
EOF
  echo
}

# Property graph - pick ONE of these two:
start_load "gremlin-csv/"    "csv"
# start_load "opencypher-csv/" "opencypher"

# RDF - the ontology (TBox) and the data (ABox) as Turtle.
# Ontology goes into its own named graph so it is easy to replace later.
start_load "rdf/retail-ontology.ttl" "turtle" \
  '"parserConfiguration": {"namedGraphUri": "https://example.org/retail/graph/ontology"}'
start_load "rdf/retail-data.ttl" "turtle" \
  '"parserConfiguration": {"namedGraphUri": "https://example.org/retail/graph/data"}'

# Other RDF formats (same triples - load any ONE instead of the .ttl above):
# start_load "rdf/retail-data.nt"  "ntriples"
# start_load "rdf/retail-data.rdf" "rdfxml"
# start_load "rdf/retail-data.nq"  "nquads"   # keeps catalog/customers/orders/reviews graphs
#
# Without namedGraphUri, triples from turtle/ntriples/rdfxml go to Neptune's
# default graph  http://aws.amazon.com/neptune/vocab/v01/DefaultNamedGraph

# --- 3. Check status ------------------------------------------------------
#   curl -sS "${LOADER}"                                        # list job ids
#   curl -sS "${LOADER}/<loadId>?details=true&errors=true&page=1&errorsPerPage=10"
#   curl -sS -X DELETE "${LOADER}/<loadId>"                     # cancel
#
# --- Same thing with the AWS CLI (signs requests for IAM auth) ------------
#   aws neptunedata start-loader-job \
#     --endpoint-url "https://${NEPTUNE_ENDPOINT}:8182" \
#     --source "s3://${BUCKET}/retail/gremlin-csv/" --format csv \
#     --s3-bucket-region "${REGION}" --iam-role-arn "${LOADER_ROLE_ARN}"
#   aws neptunedata get-loader-job-status --endpoint-url "https://${NEPTUNE_ENDPOINT}:8182" --load-id <loadId>
#
# --- Or from a Neptune notebook (graph-notebook) ---------------------------
#   %load        -> interactive bulk-load form
#   %load_status <loadId>
