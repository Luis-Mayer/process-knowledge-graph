import sys
from pathlib import Path

# Damit Imports funktionieren wenn via "uv run streamlit run src/app.py" gestartet
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import json
from rdflib import Graph
import networkx as nx
import tempfile

from build_graph import build_graph
from validate_graph import validate_graph


st.set_page_config(layout="wide")
st.title("Process Knowledge Graph UI")

# -------- Upload --------
uploaded_file = st.file_uploader("Upload Process JSON", type="json")

if uploaded_file:
    process_data = json.load(uploaded_file)
    st.success("JSON geladen")

    # -------- Build Graph --------
    if st.button("Build RDF Graph"):
        g = build_graph(process_data)

        tmp_file = Path(tempfile.gettempdir()) / "graph.ttl"
        g.serialize(destination=tmp_file, format="turtle")

        st.session_state["graph_path"] = str(tmp_file)
        st.success("Graph erstellt")

    # -------- Validation --------
    if "graph_path" in st.session_state:
        if st.button("Run Validation"):
            results = validate_graph(st.session_state["graph_path"])
            st.subheader("Validation Results")
            st.write(results)

    # -------- Visualization --------
    if "graph_path" in st.session_state:
        if st.button("Show Graph"):
            g = Graph()
            g.parse(st.session_state["graph_path"], format="turtle")

            nx_graph = nx.DiGraph()
            for s, p, o in g:
                nx_graph.add_edge(str(s), str(o), label=str(p))

            nodes = []
            node_ids = {}
            for i, node in enumerate(nx_graph.nodes):
                label = node.split("/")[-1].split("#")[-1]
                node_ids[node] = i
                nodes.append({"id": i, "label": label, "title": node})

            edges = []
            for u, v, data in nx_graph.edges(data=True):
                label = data.get("label", "").split("/")[-1].split("#")[-1]
                edges.append({
                    "from": node_ids[u],
                    "to": node_ids[v],
                    "label": label,
                })

            nodes_json = json.dumps(nodes)
            edges_json = json.dumps(edges)
            n_nodes = len(nodes)
            n_edges = len(edges)

            html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #0f1117; font-family: sans-serif; }}
  #graph {{ width: 100%; height: 570px; }}
  #status {{
    color: #94a3b8; font-size: 12px; background: #1e293b;
    padding: 5px 14px; text-align: center;
  }}
</style>
</head>
<body>
<div id="status">Lade Graph...</div>
<div id="graph"></div>
<script>
  const NODES_DATA = {nodes_json};
  const EDGES_DATA = {edges_json};

  function initGraph() {{
    document.getElementById("status").textContent =
      "{n_nodes} Nodes · {n_edges} Edges  —  ziehen zum verschieben, scrollen zum zoomen";

    const nodes = new vis.DataSet(NODES_DATA);
    const edges = new vis.DataSet(EDGES_DATA);

    const options = {{
      nodes: {{
        shape: "dot",
        size: 16,
        color: {{
          background: "#3b82f6",
          border: "#1d4ed8",
          highlight: {{ background: "#60a5fa", border: "#1e40af" }}
        }},
        font: {{ color: "#f1f5f9", size: 13 }},
        borderWidth: 2,
      }},
      edges: {{
        color: {{ color: "#475569", highlight: "#7dd3fc" }},
        font: {{ color: "#94a3b8", size: 10, align: "middle", background: "#0f1117" }},
        arrows: {{ to: {{ enabled: true, scaleFactor: 0.8 }} }},
        smooth: {{ type: "curvedCW", roundness: 0.2 }},
        width: 1.5,
      }},
      physics: {{
        stabilization: {{ iterations: 200, fit: true }},
        barnesHut: {{
          gravitationalConstant: -6000,
          springLength: 140,
          springConstant: 0.04,
          damping: 0.09,
        }},
      }},
      interaction: {{
        hover: true,
        tooltipDelay: 100,
        zoomView: true,
        dragView: true,
      }},
    }};

    const network = new vis.Network(
      document.getElementById("graph"),
      {{ nodes, edges }},
      options
    );

    network.once("stabilizationIterationsDone", () => {{
      network.fit({{ animation: {{ duration: 600, easingFunction: "easeInOutQuad" }} }});
    }});
  }}

  // vis.js dynamisch laden — erst DANN initGraph aufrufen
  const script = document.createElement("script");
  script.src = "https://unpkg.com/vis-network@9.1.9/dist/vis-network.min.js";
  script.onload = initGraph;
  script.onerror = () => {{
    document.getElementById("status").textContent =
      "Fehler: vis.js konnte nicht geladen werden (kein Internet?)";
  }};
  document.head.appendChild(script);
</script>
</body>
</html>"""

            st.session_state["graph_html"] = html

if "graph_html" in st.session_state:
    st.subheader("Graph Visualization")
    st.components.v1.html(
        st.session_state["graph_html"],
        height=620,
        scrolling=False,
    )
