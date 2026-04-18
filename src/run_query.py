from __future__ import annotations

import argparse
from pathlib import Path

from rdflib import Graph


BASE_DIR = Path(__file__).resolve().parent.parent
GRAPH_PATH = BASE_DIR / "output" / "process_graph.ttl"
QUERY_DIR = BASE_DIR / "queries"


def load_graph(path: Path) -> Graph:
    """Load an RDF graph from a Turtle file."""
    graph = Graph()
    graph.parse(path, format="turtle")
    return graph


def load_query(query_name: str) -> str:
    """Load a SPARQL query by name from the queries directory."""
    query_path = QUERY_DIR / f"{query_name}.rq"

    if not query_path.exists():
        available_queries = sorted(path.stem for path in QUERY_DIR.glob("*.rq"))
        raise FileNotFoundError(
            f"Query '{query_name}' not found. "
            f"Available queries: {', '.join(available_queries)}"
        )

    with query_path.open("r", encoding="utf-8") as file:
        return file.read()
   
    
def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run a SPARQL query against the generated process graph."
    )
    parser.add_argument(
        "query",
        help="Name of the query file without extension, e.g. tasks_by_role",
    )
    return parser.parse_args()


def main() -> None:
    """Run a selected SPARQL query against the generated process graph."""
    args = parse_args()

    graph = load_graph(GRAPH_PATH)
    query = load_query(args.query)

    results = graph.query(query)

    print(f"Results for query: {args.query}")
    print("-" * 40)

    for row in results:
        print(" | ".join(str(value) for value in row))


if __name__ == "__main__":
    main()