"""
Interactive Plotly graph visualizations for impactx.
"""

from typing import Dict, Any, List, Optional
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from dashboard.components.theme import get_plotly_layout, get_axis_layout

LANGUAGE_COLORS = {
    "Python": "#3B82F6",
    "JavaScript": "#F59E0B",
    "TypeScript": "#06B6D4",
    "Java": "#EC4899",
    "HTML": "#EF4444",
    "CSS": "#8B5CF6",
    "Unknown": "#6B7280",
}

def build_network_graph(
    G: nx.DiGraph,
    theme: str = "dark",
    max_nodes: int = 300,
    highlight_node: Optional[str] = None,
    pageranks: Optional[Dict[str, float]] = None,
) -> go.Figure:
    """
    Renders interactive 2D network graph of dependencies with NetworkX layout.
    Node size scaled by PageRank, color by language.
    """
    if G.number_of_nodes() == 0:
        fig = go.Figure()
        fig.update_layout(title="No dependency graph data available", **get_plotly_layout(theme))
        return fig

    # Subgraph if too large
    if G.number_of_nodes() > max_nodes:
        top_nodes = sorted(G.nodes(), key=lambda n: G.degree(n), reverse=True)[:max_nodes]
        G = G.subgraph(top_nodes).copy()

    # Calculate layout positions
    pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

    # Edge traces
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_color = "rgba(139, 92, 246, 0.35)" if theme == "dark" else "rgba(99, 102, 241, 0.45)"
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1.0, color=edge_color),
        hoverinfo="none",
        mode="lines",
    )

    # Node traces
    node_x = []
    node_y = []
    node_colors = []
    node_sizes = []
    node_text = []
    node_customdata = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        node_data = G.nodes[node]
        lang = node_data.get("language", "Unknown")
        color = LANGUAGE_COLORS.get(lang, "#8B5CF6")
        
        # Highlight selected node
        if highlight_node and node == highlight_node:
            color = "#10B981"  # Emerald highlight

        pr = (pageranks or {}).get(node, 0.01)
        size = max(10, min(36, 12 + pr * 300))
        if highlight_node and node == highlight_node:
            size = 40

        in_deg = G.in_degree(node)
        out_deg = G.out_degree(node)
        loc = node_data.get("lines_of_code", 0)

        tooltip = (
            f"<b>{node}</b><br>"
            f"Language: {lang}<br>"
            f"Type: {node_data.get('type', 'file')}<br>"
            f"Lines of Code: {loc}<br>"
            f"Dependents (In-degree): {in_deg}<br>"
            f"Dependencies (Out-degree): {out_deg}<br>"
            f"PageRank: {pr:.4f}"
        )

        node_colors.append(color)
        node_sizes.append(size)
        node_text.append(node)
        node_customdata.append(tooltip)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text" if G.number_of_nodes() < 40 else "markers",
        text=[n.split("/")[-1] for n in G.nodes()] if G.number_of_nodes() < 40 else None,
        textposition="top center",
        hoverinfo="text",
        hovertext=node_customdata,
        marker=dict(
            showscale=False,
            color=node_colors,
            size=node_sizes,
            line=dict(width=1.5, color="#FFFFFF" if theme == "dark" else "#0F172A"),
        ),
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    layout_cfg = get_plotly_layout(theme)
    fig.update_layout(
        showlegend=False,
        hovermode="closest",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        **layout_cfg,
    )
    return fig

def build_language_pie(lang_dist: Dict[str, int], theme: str = "dark") -> go.Figure:
    """Builds a sleek donut chart for language distribution."""
    labels = list(lang_dist.keys())
    values = list(lang_dist.values())
    colors = [LANGUAGE_COLORS.get(l, "#6366F1") for l in labels]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker=dict(colors=colors, line=dict(color="#121422" if theme == "dark" else "#FFFFFF", width=2)),
                textinfo="label+percent",
                hoverinfo="label+value+percent",
            )
        ]
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        **get_plotly_layout(theme),
    )
    return fig

def build_roc_curve(roc_data: Dict[str, List[float]], auc_score: float, theme: str = "dark") -> go.Figure:
    """Builds interactive ROC curve visualization."""
    fpr = roc_data.get("fpr", [0, 1])
    tpr = roc_data.get("tpr", [0, 1])

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=fpr,
            y=tpr,
            mode="lines",
            name=f"ROC Curve (AUC = {auc_score:.3f})",
            line=dict(color="#8B5CF6", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Random Baseline",
            line=dict(color="rgba(148, 163, 184, 0.4)" if theme == "dark" else "rgba(100, 116, 139, 0.5)", width=2, dash="dash"),
        )
    )
    axis_cfg = get_axis_layout(theme)
    layout = get_plotly_layout(theme)
    fig.update_layout(
        xaxis=dict(title="False Positive Rate (1 - Specificity)", range=[0, 1], **axis_cfg),
        yaxis=dict(title="True Positive Rate (Recall)", range=[0, 1.05], **axis_cfg),
        **layout,
    )
    return fig

def build_feature_importance_bar(importances: Dict[str, float], theme: str = "dark", top_n: int = 12) -> go.Figure:
    """Builds horizontal bar chart for feature importances."""
    sorted_items = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:top_n]
    names = [x[0].replace("_", " ").title() for x in sorted_items][::-1]
    scores = [x[1] for x in sorted_items][::-1]

    fig = go.Figure(
        go.Bar(
            x=scores,
            y=names,
            orientation="h",
            marker=dict(
                color=scores,
                colorscale="Purples" if theme == "dark" else "Blues",
                line=dict(width=0),
            ),
        )
    )
    axis_cfg = get_axis_layout(theme)
    layout = get_plotly_layout(theme)
    fig.update_layout(
        xaxis=dict(title="Importance Weight", **axis_cfg),
        yaxis=dict(title="", **axis_cfg),
        **layout,
    )
    return fig

def build_confusion_matrix_heatmap(cm: List[List[int]], theme: str = "dark") -> go.Figure:
    """Builds heatmap for 2x2 confusion matrix."""
    z = cm if len(cm) == 2 else [[0, 0], [0, 0]]
    x = ["Predicted Negative", "Predicted Positive"]
    y = ["Actual Negative", "Actual Positive"]

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=x,
            y=y,
            colorscale="Purples" if theme == "dark" else "Blues",
            text=z,
            texttemplate="%{text}",
            textfont={"size": 16, "family": "Inter"},
            showscale=False,
        )
    )
    axis_cfg = get_axis_layout(theme)
    layout = get_plotly_layout(theme)
    fig.update_layout(
        xaxis=dict(**axis_cfg),
        yaxis=dict(**axis_cfg),
        **layout,
    )
    return fig
