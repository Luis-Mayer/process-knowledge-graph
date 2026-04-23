from pathlib import Path
from rdflib import Graph
from pyshacl import validate

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_GRAPH = BASE_DIR / "output" / "process_graph.ttl"
SHAPES = BASE_DIR / "ontology" / "shapes.ttl"


def load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(path, format="turtle")  # load RDF/Turtle file into graph
    return g


def main():
    # load generated process graph
    data_graph = load_graph(DATA_GRAPH)

    # load SHACL constraints
    shapes_graph = load_graph(SHAPES)

    # run SHACL validation
    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        debug=False,
    )

    print("\n=== SHACL VALIDATION RESULT ===")
    print("Conforms:", conforms)
    print(results_text)


if __name__ == "__main__":
    main()