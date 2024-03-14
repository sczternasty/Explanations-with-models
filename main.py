from GraphGeneration import generate_graph
from LoadOntology import loadOntology
from TableauMethod import tableauMethod
from UnfoldTBox import unfold_tbox
import os

ontology_name = input("Type in ontology name: ")

while not(os.path.isfile(os.path.join(os.getcwd(), ontology_name))):
    print("Error: File not found")
    ontology_name = input("Type in ontology name: ")

axioms = loadOntology(ontology_name)
unfold_input = input("For which concept you want to unfold (if necessary add quotation marks): ")
#max_iter = int(input("Choose maximum number of iterations: "))
complex_concept = unfold_tbox(unfold_input, axioms)


ABox_dict = tableauMethod(complex_concept)

graph = generate_graph(ABox_dict)
graph.render('example_graph', format='png', cleanup=True)
graph.view()