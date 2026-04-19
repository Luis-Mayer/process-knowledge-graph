from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, RDFS


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "purchase_request_process.json"
OUTPUT_PATH = BASE_DIR / "output" / "process_graph.ttl"

EX = Namespace("http://example.org/process-kg/")


def load_process_data(path: Path) -> dict:
    """Load process data from a JSON file."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_graph(data: dict) -> Graph:
    """Build a simple RDF graph from process data."""
    graph = Graph()
    graph.bind("ex", EX)
    graph.bind("rdfs", RDFS)

    # Define basic classes
    graph.add((EX.Process, RDF.type, RDFS.Class))
    graph.add((EX.Task, RDF.type, RDFS.Class))
    graph.add((EX.Role, RDF.type, RDFS.Class))
    graph.add((EX.System, RDF.type, RDFS.Class))
    graph.add((EX.Decision, RDF.type, RDFS.Class))

    # Define basic properties
    graph.add((EX.hasTask, RDF.type, RDF.Property))
    graph.add((EX.hasDecision, RDF.type, RDF.Property))
    graph.add((EX.performedBy, RDF.type, RDF.Property))
    graph.add((EX.precedes, RDF.type, RDF.Property))
    graph.add((EX.usesSystem, RDF.type, RDF.Property))
    graph.add((EX.condition, RDF.type, RDF.Property))
    graph.add((EX.trueNext, RDF.type, RDF.Property))
    graph.add((EX.falseNext, RDF.type, RDF.Property))

    # Create process node
    process_uri = EX[data["process_id"]]
    graph.add((process_uri, RDF.type, EX.Process))
    graph.add((process_uri, RDFS.label, Literal(data["process_name"])))

    # Create role nodes
    for role in data.get("roles", []):
        role_uri = EX[role["id"]]
        graph.add((role_uri, RDF.type, EX.Role))
        graph.add((role_uri, RDFS.label, Literal(role["name"])))

    # Create system nodes
    for system in data.get("systems", []):
        system_uri = EX[system["id"]]
        graph.add((system_uri, RDF.type, EX.System))
        graph.add((system_uri, RDFS.label, Literal(system["name"])))

    # Create task nodes and relations
    for task in data.get("tasks", []):
        task_uri = EX[task["id"]]
        graph.add((task_uri, RDF.type, EX.Task))
        graph.add((task_uri, RDFS.label, Literal(task["name"])))

        # Process -> Task
        graph.add((process_uri, EX.hasTask, task_uri))

        # Task -> Role
        performed_by = task.get("performed_by")
        if performed_by:
            graph.add((task_uri, EX.performedBy, EX[performed_by]))

        # Task -> next Task or Decision
        next_task = task.get("next_task")
        if next_task:
            graph.add((task_uri, EX.precedes, EX[next_task]))

        # Task -> System
        uses_system = task.get("uses_system")
        if uses_system:
            graph.add((task_uri, EX.usesSystem, EX[uses_system]))

    # Create decision nodes and relations
    for decision in data.get("decisions", []):
        decision_uri = EX[decision["id"]]
        graph.add((decision_uri, RDF.type, EX.Decision))
        graph.add((decision_uri, RDFS.label, Literal(decision["name"])))
        graph.add((process_uri, EX.hasDecision, decision_uri))

        condition = decision.get("condition")
        if condition:
            graph.add((decision_uri, EX.condition, Literal(condition)))

        true_next = decision.get("true_next")
        if true_next:
            graph.add((decision_uri, EX.trueNext, EX[true_next]))

        false_next = decision.get("false_next")
        if false_next:
            graph.add((decision_uri, EX.falseNext, EX[false_next]))

    return graph


def main() -> None:
    """Load input data, build RDF graph, and save it as Turtle."""
    data = load_process_data(DATA_PATH)
    graph = build_graph(data)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=OUTPUT_PATH, format="turtle")

    print(f"Graph saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()