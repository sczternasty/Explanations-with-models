from GraphGeneration import generate_graph
from LoadOntology import loadOntology
from TableauMethod import tableauMethod
from UnfoldTBox import unfold_tbox
import os

ontology_name = input("Ontology name: ")

while not(os.path.isfile(os.path.join(os.getcwd(), ontology_name))):
    print("Error: File not found")
    ontology_name = input("Ontology name: ")
concept_name = input("Concept name (if necessary add quotation marks): ")
max_depth = int(input("Maximum depth: "))

axioms = loadOntology(ontology_name)
complex_concept = unfold_tbox(concept_name, axioms, max_depth)
ABox_dict = tableauMethod(complex_concept)
graph = generate_graph(ABox_dict)
graph.render(concept_name + " graph", format='png', cleanup=True)
graph.view()

