from py4j.java_gateway import JavaGateway, GatewayParameters

def loadOntology(name):
    gateway = JavaGateway()
    parser = gateway.getOWLParser()
    ontology = parser.parseFile(name)
    gateway.convertToBinaryConjunctions(ontology)
    tbox = ontology.tbox()
    axioms = tbox.getAxioms()
    return axioms