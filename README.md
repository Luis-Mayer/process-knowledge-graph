# Process Knowledge Graph

A small Python project for representing business process information as an RDF knowledge graph and querying it with SPARQL.

The project is inspired by the idea that business process knowledge is often stored in unstructured or semi-structured documentation. By representing process steps, roles, systems, and dependencies as graph relationships, the process becomes machine-readable and easier to query.

## Current Scope

The current prototype:

- reads a JSON-based process definition
- creates an RDF graph using RDFLib
- models processes, tasks, roles, systems, and decisions
- stores the graph in Turtle format
- runs SPARQL queries against the generated graph

The sample process is a simplified purchase request approval workflow.

## Project Structure

```
.
├── data/
│   └── purchase_request_process.json
├── docs/
│   └── related_work.md
├── ontology/
│   └── shapes.ttl
├── output/
│   └── process_graph.ttl
├── queries/
│   ├── decisions.rq
│   ├── tasks_by_role.rq
│   └── tasks_using_systems.rq
├── src/
│   ├── build_graph.py
│   ├── run_query.py
│   └── validate_graph.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Setup

This project uses `uv` for dependency management.

```bash
uv sync
```

## Build the RDF Graph

Generate an RDF graph from the sample process definition:

```bash
uv run python src/build_graph.py
```

This reads the sample process from:

```
data/purchase_request_process.json
```

and writes the generated graph to:

```
output/process_graph.ttl
```

## Run SPARQL Queries

List tasks by responsible role:

```bash
uv run python src/run_query.py tasks_by_role
```

List tasks that use business systems:

```bash
uv run python src/run_query.py tasks_using_systems
```

## Process Input Format

The input process is defined as JSON:

```json
{
  "process_id": "purchase_request",
  "process_name": "Purchase Request Approval",
  "roles": [
    { "id": "purchaser", "name": "Purchaser" }
  ],
  "systems": [
    { "id": "erp", "name": "ERP System" }
  ],
  "tasks": [
    {
      "id": "task_1",
      "name": "Submit purchase request",
      "performed_by": "purchaser",
      "uses_system": null,
      "next_task": "task_2"
    }
  ],
  "decisions": [
    {
      "id": "decision_1",
      "name": "Check request value",
      "condition": "Request value exceeds approval threshold",
      "true_next": "task_3",
      "false_next": "task_4"
    }
  ]
}
```

## Graph Model

The current graph model uses a lightweight vocabulary.

### Classes

- `ex:Process`
- `ex:Task`
- `ex:Role`
- `ex:System`
- `ex:Decision`

### Properties

- `ex:hasTask`
- `ex:hasDecision`
- `ex:performedBy`
- `ex:precedes`
- `ex:usesSystem`
- `ex:condition`
- `ex:trueNext`
- `ex:falseNext`

### Example

Turtle output:

```turtle
@prefix ex: <http://example.org/process-kg/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:task_1 a ex:Task ;
    rdfs:label "Submit purchase request" ;
    ex:performedBy ex:purchaser ;
    ex:precedes ex:task_2 .
```

## Example Queries

The repository currently includes three SPARQL queries:

- `decisions.rq`: shows decision logic with conditions and branching paths
- `tasks_by_role.rq`: shows which role performs which task
- `tasks_using_systems.rq`: shows which tasks use which systems

## SHACL Validation (Data Quality Constraints)

The project includes initial SHACL shapes to define data quality constraints for the knowledge graph.

Currently implemented constraints:

- Each Task must have exactly one `ex:performedBy` relationship
- Each Decision must define:
    - a condition (ex:condition)
    - a true branch (ex:trueNext)
    - a false branch (ex:falseNext)

Future extensions may include additional constraints for more complex process structures and validation rules.

## Motivation

This project is a small prototype for connecting business process modeling with semantic data modeling. It demonstrates how process knowledge can be represented as a machine-readable graph and queried in a structured way.

The prototype also includes simple decision logic to represent branching process paths, which makes it closer to real-world process modeling.

## Possible Extensions

- Extending decision logic with multiple branches and gateway types
- Creating a formal OWL ontology in the `ontology/` directory
- Mapping BPMN XML elements to RDF triples
- Adding SHACL validation for process consistency
- Exporting the graph to graph databases or visualization tools