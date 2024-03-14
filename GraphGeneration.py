import graphviz
import re
from py4j.java_gateway import JavaGateway
gateway = JavaGateway()
formatter = gateway.getSimpleDLFormatter()

def generate_graph(dictionary):
    dot = graphviz.Digraph(graph_attr={'ranksep': '.5', 'nodesep': '1.5', 'overlap': 'false'})
    preprocessed_dictionary = {}

    for x, y in dictionary.items():
        for d in y:
            if d.getClass().getSimpleName() == "ConceptName" or d.getClass().getSimpleName() == "RoleName":
                preprocessed_dictionary[x] = preprocessed_dictionary.get(x, []) + [
                    re.sub(r'[^a-zA-Z]', '', formatter.format(d))]

    for key, value in preprocessed_dictionary.items():
        if isinstance(key, tuple):
            node1 = key[0]
            node2 = key[1]
            dot.edge(str(node1), str(node2), label=str(value[0]), fontsize='10', arrowsize="0.5")
        else:
            dot.node(str(key), label=', '.join(value), xlabel=str(key), shape='box', style='rounded', fontsize='10',
                     xlp='')

    return dot