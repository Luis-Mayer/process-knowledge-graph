from pathlib import Path
from rdflib import Graph
from pyshacl import validate

BASE_DIR = Path(__file__).resolve().parent.parent
SHAPES = BASE_DIR / "ontology" / "shapes.ttl"


def load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(path, format="turtle")
    return g


def validate_graph(data_graph_path: Path):
    data_graph = load_graph(data_graph_path)
    shapes_graph = load_graph(SHAPES)

    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        debug=False,
    )

    return {
        "conforms": conforms,
        "report": results_text
    }


def main():
    result = validate_graph(BASE_DIR / "output" / "process_graph.ttl")

    print("\n=== SHACL VALIDATION RESULT ===")
    print("Conforms:", result["conforms"])
    print(result["report"])


if __name__ == "__main__":
    main()