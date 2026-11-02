// ===========================================================================
// Neo4j + the OWL ontology, via neosemantics (n10s)
// https://neo4j.com/labs/neosemantics/
// n10s imports RDF/OWL into a property graph, so the SAME ontology and data
// used by the SPARQL examples can live in Neo4j next to the Cypher model.
// ===========================================================================

// 1. One-time setup
CREATE CONSTRAINT n10s_unique_uri IF NOT EXISTS FOR (r:Resource) REQUIRE r.uri IS UNIQUE;
// IGNORE drops namespaces so instance labels (Customer) match class names
CALL n10s.graphconfig.init({handleVocabUris: 'IGNORE', handleRDFTypes: 'LABELS'});

// 2. Import the ontology (classes -> :Class nodes, subClassOf -> :SCO edges)
CALL n10s.onto.import.fetch(
  'https://raw.githubusercontent.com/rongali-naidu/semantics-ontology-graphs/main/examples/retail/ontology/retail-ontology.ttl',
  'Turtle');

// 3. Import the instance data (resources -> nodes, rdf:type -> labels)
CALL n10s.rdf.import.fetch(
  'https://raw.githubusercontent.com/rongali-naidu/semantics-ontology-graphs/main/examples/retail/rdf/retail-data.ttl',
  'Turtle');

// 4. Inference from the imported ontology: all customers incl. PremiumCustomer
//    (= SPARQL 08-all-customers-via-subclass.rq)
CALL n10s.inference.nodesLabelled('Customer', {catNameProp: 'name', catLabel: 'Class', subCatRel: 'SCO'})
YIELD node
RETURN node.name AS customer;   // Alice Johnson, Bob Smith, Carol Diaz

// 5. Validate the graph with the SHACL shapes
CALL n10s.validation.shacl.import.fetch(
  'https://raw.githubusercontent.com/rongali-naidu/semantics-ontology-graphs/main/examples/retail/ontology/retail-shapes.ttl',
  'Turtle');
CALL n10s.validation.shacl.validate();
