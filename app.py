# -*- coding: utf-8 -*-
import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import numpy as np
import math

app = dash.Dash(__name__)
server = app.server

R_KM = 6371.0

# ================= الحسابات =================
def curvature_drop_m(distance_km):
    return (distance_km ** 2) / (2 * R_KM) * 1000

def horizon_dip_deg(altitude_km):
    if altitude_km <= 0:
        return 0.0
    cos_theta = R_KM / (R_KM + altitude_km)
    cos_theta = max(min(cos_theta, 1), -1)
    return np.degrees(np.arccos(cos_theta))

# ================= الرسم =================
def create_figure(model, obj_h, eye_h, dist, zoom, alt):
    max_dist = max(dist * 2, 10)
    x = np.linspace(0.1, max_dist, 200)

    fig = go.Figure()
    fig.add_hline(y=0, line_color="lime", line_dash="dash")

    if model == "flat":
        y = obj_h / (x * 1000) * eye_h
        fig.add_trace(go.Scatter(x=x, y=y, line=dict(color="cyan"), name="Flat"))
        title = "Flat Model"
    else:
        drop = curvature_drop_m(x)
        y = np.maximum(0, obj_h - drop)
        fig.add_trace(go.Scatter(x=x, y=y, line=dict(color="orange"), name="Curved"))
        title = "Curved Model"

    fig.update_layout(
        title=title,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# ================= LAYOUT =================
app.layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "row",
        "height": "100vh"
    },
    children=[

        dcc.Store(id="sidebar-state", data=True),

        # ===== SIDEBAR =====
        html.Div(
            id="sidebar",
            style={
                "width": "320px",
                "transition": "0.3s",
                "backgroundColor": "#f5f7fa",
                "padding": "15px",
                "overflowY": "auto"
            },
            children=[

                html.Button(
                    "☰",
                    id="toggle-btn",
                    style={
                        "fontSize": "20px",
                        "padding": "5px 10px",
                        "marginBottom": "10px",
                        "cursor": "pointer"
                    }
                ),

                html.H3("Control Panel"),

                dcc.Dropdown(
                    id="model",
                    options=[
                        {"label": "Flat", "value": "flat"},
                        {"label": "Curved", "value": "curved"}
                    ],
                    value="flat"
                ),

                html.Br(),

                html.Label("Object Height"),
                dcc.Slider(id="obj", min=1, max=100, value=50),

                html.Label("Eye Height"),
                dcc.Slider(id="eye", min=0.1, max=10, value=1.7),

                html.Label("Distance"),
                dcc.Slider(id="dist", min=1, max=100, value=20),

                html.Label("Zoom"),
                dcc.Slider(id="zoom", min=0, max=5, value=0),

                html.Label("Altitude"),
                dcc.Slider(id="alt", min=0, max=50, value=10),
            ]
        ),

        # ===== CHART =====
        html.Div(
            style={"flex": 1, "padding": "10px"},
            children=[
                dcc.Graph(id="graph", style={"height": "95vh"})
            ]
        )
    ]
)

# ================= TOGGLE SIDEBAR =================
@app.callback(
    Output("sidebar", "style"),
    Output("sidebar-state", "data"),
    Input("toggle-btn", "n_clicks"),
    State("sidebar-state", "data"),
    prevent_initial_call=True
)
def toggle_sidebar(n, state):
    state = not state

    if state:
        return {
            "width": "320px",
            "transition": "0.3s",
            "backgroundColor": "#f5f7fa",
            "padding": "15px",
            "overflowY": "auto"
        }, state
    else:
        return {
            "width": "60px",
            "transition": "0.3s",
            "backgroundColor": "#f5f7fa",
            "padding": "10px",
            "overflow": "hidden"
        }, state

# ================= UPDATE =================
@app.callback(
    Output("graph", "figure"),
    Input("model", "value"),
    Input("obj", "value"),
    Input("eye", "value"),
    Input("dist", "value"),
    Input("zoom", "value"),
    Input("alt", "value")
)
def update(m, o, e, d, z, a):
    return create_figure(m, o, e, d, z, a)

# ================= RUN =================
if __name__ == "__main__":
    app.run_server(debug=False)
