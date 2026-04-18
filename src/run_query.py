from __future__ import annotations

from pathlib import Path

from rdflib import Graph


BASE_DIR = Path(__file__).resolve().parent.parent
GRAPH_PATH = BASE_DIR / "output" / "process_graph.ttl"
QUERY_PATH = BASE_DIR / "queries" / "tasks_by_role.rq"


def load_graph(path: Path) -> Graph:
    """Load an RDF graph from a Turtle file."""
    graph = Graph()
    graph.parse(path, format="turtle")
    return graph


def load_query(path: Path) -> str:
    """Load a SPARQL query from a file."""
    with path.open("r", encoding="utf-8") as file:
        return file.read()


def main() -> None:
    """Run a SPARQL query against the generated process graph."""
    graph = load_graph(GRAPH_PATH)
    query = load_query(QUERY_PATH)

    results = graph.query(query)

    print("Tasks by role:")
    print("-" * 40)

    for row in results:
        print(f"{row.roleLabel}: {row.taskLabel}")


if __name__ == "__main__":
    main()