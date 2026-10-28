# U1. SPARQL 1.1 UPDATE: Bob orders a Mechanical Keyboard.
# Run against an update endpoint (Neptune: POST /sparql with update=...).
PREFIX rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:    <http://www.w3.org/2002/07/owl#>
PREFIX xsd:    <http://www.w3.org/2001/XMLSchema#>
PREFIX retail: <https://example.org/retail/ontology#>
PREFIX ex:     <https://example.org/retail/data/>

INSERT DATA {
  ex:O5 a retail:Order ;
        retail:placedBy ex:C2 ;
        retail:orderDate "2026-10-20"^^xsd:date ;
        retail:status "PLACED" ;
        retail:paymentMethod "CARD" ;
        retail:shipsTo ex:A2 ;
        retail:hasLine ex:O5-L1 .
  ex:O5-L1 a retail:OrderLine ;
        retail:forProduct ex:P6 ;
        retail:quantity "1"^^xsd:positiveInteger ;
        retail:unitPrice "89.00"^^xsd:decimal .
}
