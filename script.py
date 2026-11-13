import pandas as pd
from rdflib import Graph, Namespace, Literal, RDF
import networkx as nx
import matplotlib.pyplot as plt


df = pd.read_csv("wafers.csv").dropna()
EX = Namespace("http://example.org/semi/")
g = Graph()

for _, r in df.iterrows():
    w = EX[f"wafer_{r.wafer_id}"]
    g.add((w, RDF.type, EX.Wafer))
    g.add((w, EX.belongsTo, EX[f"batch_{r.batch}"]))
    g.add((w, EX.processedBy, EX[f"machine_{r.machine}"]))
    g.add((w, EX.defectCount, Literal(int(r.defect_count))))

q = """
PREFIX ex: <http://example.org/semi/>
SELECT ?w ?m ?d WHERE {
  ?w ex:processedBy ?m ; ex:defectCount ?d .
  FILTER(?d > 5)
}"""
for row in g.query(q):
    print(row)
    G = nx.DiGraph()
    for _, r in df.iterrows():
        w = f"wafer_{r.wafer_id}"
        G.add_edge(w, f"batch_{r.batch}", label="belongsTo")
        G.add_edge(w, f"machine_{r.machine}", label="processedBy")

    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color="lightblue",
            node_size=1500, font_size=8, arrows=True)
    nx.draw_networkx_edge_labels(G, pos,
                                 edge_labels=nx.get_edge_attributes(G, "label"), font_size=7)
    plt.show()