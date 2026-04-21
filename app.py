# -*- coding: utf-8 -*-
import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import numpy as np
import math
import os

app = dash.Dash(__name__)
server = app.server

R_KM = 6371.0

def curvature_drop_m(distance_km):
    return (distance_km ** 2) / (2 * R_KM) * 1000

def horizon_dip_deg(altitude_km):
    if altitude_km <= 0:
        return 0.0
    cos_theta = R_KM / (R_KM + altitude_km)
    cos_theta = max(min(cos_theta, 1), -1)
    return np.degrees(np.arccos(cos_theta))

def create_figure(model, obj_h, eye_h, dist, zoom, alt):
    max_dist = max(dist * 2, 10)
    distances = np.linspace(0.1, max_dist, 200)

    fig = go.Figure()
    fig.add_hline(y=0, line_color="lime", line_dash="dash", annotation_text="مستوى العين")

    if model == "flat":
        angular = obj_h / (distances * 1000)
        top = angular * (eye_h + obj_h / 2)
        bottom = angular * (eye_h - obj_h / 2)

        fig.add_trace(go.Scatter(x=distances, y=top, name="القمة", line=dict(color="cyan")))
        fig.add_trace(go.Scatter(x=distances, y=bottom, name="القاعدة", fill="tonexty", line=dict(color="red")))

        fig.add_trace(go.Scatter(x=[dist], y=[top[len(top)//2]], mode="markers", marker=dict(size=10, color="cyan")))
        fig.add_trace(go.Scatter(x=[dist], y=[bottom[len(bottom)//2]], mode="markers", marker=dict(size=10, color="red")))

        title = "نموذج الأرض المسطحة"

    else:
        drop = curvature_drop_m(distances)
        visible = np.maximum(0, obj_h - drop)

        fig.add_trace(go.Scatter(x=distances, y=visible, name="المرئي", line=dict(color="orange")))

        cur = max(0, obj_h - curvature_drop_m(dist))
        fig.add_trace(go.Scatter(x=[dist], y=[cur], mode="markers", marker=dict(size=10, color="red")))

        dip = horizon_dip_deg(alt)
        fig.add_hline(y=-dip, line_color="blue", line_dash="dot")

        title = "نموذج الأرض الكروية"

    fig.update_layout(
        title=title,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(color="white"),
        yaxis=dict(color="white"),
        legend=dict(font=dict(color="white"))
    )

    return fig


app.layout = html.Div([
    html.Div([
        html.H2("لوحة التحكم"),

        dcc.Dropdown(
            id="model",
            options=[
                {"label": "مسطح", "value": "flat"},
                {"label": "كروي", "value": "curved"}
            ],
            value="flat"
        ),

        dcc.Slider(id="obj", min=1, max=100, value=50),
        dcc.Slider(id="eye", min=0.1, max=10, value=1.7),
        dcc.Slider(id="dist", min=1, max=100, value=20),
        dcc.Slider(id="zoom", min=0, max=5, value=0),
        dcc.Slider(id="alt", min=0, max=50, value=10),

        html.Div(id="info")

    ], style={"width": "30%", "display": "inline-block"}),

    html.Div([
        dcc.Graph(id="graph")
    ], style={"width": "68%", "display": "inline-block"})
])


@app.callback(
    [Output("graph", "figure"), Output("info", "children")],
    [Input("model", "value"),
     Input("obj", "value"),
     Input("eye", "value"),
     Input("dist", "value"),
     Input("zoom", "value"),
     Input("alt", "value")]
)
def update(model, obj, eye, dist, zoom, alt):
    fig = create_figure(model, obj, eye, dist, zoom, alt)

    info = html.Div([
        html.P(f"الانخفاض: {curvature_drop_m(dist):.2f} م"),
        html.P(f"الأفق: {math.sqrt(2*R_KM*(eye/1000)):.2f} كم"),
        html.P(f"زاوية الأفق: {horizon_dip_deg(alt):.2f}°")
    ])

    return fig, info


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
