from pathlib import Path
from rdflib import Graph
import networkx as nx
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
GRAPH_PATH = BASE_DIR / "output" / "process_graph.ttl"


def load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(path, format="turtle")
    return g


def rdf_to_networkx(g: Graph) -> nx.DiGraph:
    nx_graph = nx.DiGraph()

    for s, p, o in g:
        s = str(s)
        p = str(p)
        o = str(o)

        nx_graph.add_node(s)
        nx_graph.add_node(o)
        nx_graph.add_edge(s, o, label=p)

    return nx_graph


def draw_graph(nx_graph: nx.DiGraph):
    plt.figure(figsize=(12, 8))

    if len(nx_graph.nodes) == 0:
        print("Graph ist leer → nichts zu zeichnen")
        return

    pos = nx.spring_layout(nx_graph, k=0.8)

    nx.draw(
        nx_graph,
        pos,
        with_labels=True,
        node_size=1200,
        font_size=7,
        arrows=True
    )

    plt.title("Process Knowledge Graph")
    plt.show()


def main():
    g = load_graph(GRAPH_PATH)

    print("RDF Triples:", len(g))

    nx_graph = rdf_to_networkx(g)

    print("Nodes:", len(nx_graph.nodes))
    print("Edges:", len(nx_graph.edges))

    draw_graph(nx_graph)


if __name__ == "__main__":
    main()