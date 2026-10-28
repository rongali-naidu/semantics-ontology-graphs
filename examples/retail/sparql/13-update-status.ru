# U2. DELETE/INSERT ... WHERE: mark every SHIPPED order as DELIVERED.
PREFIX rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:    <http://www.w3.org/2002/07/owl#>
PREFIX xsd:    <http://www.w3.org/2001/XMLSchema#>
PREFIX retail: <https://example.org/retail/ontology#>
PREFIX ex:     <https://example.org/retail/data/>

DELETE { ?o retail:status "SHIPPED" }
INSERT { ?o retail:status "DELIVERED" }
WHERE  { ?o a retail:Order ; retail:status "SHIPPED" }
