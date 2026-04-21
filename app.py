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

        cur_top = (obj_h / (dist * 1000)) * (eye_h + obj_h / 2)
        cur_bottom = (obj_h / (dist * 1000)) * (eye_h - obj_h / 2)

        fig.add_trace(go.Scatter(x=[dist], y=[cur_top], mode="markers", marker=dict(size=10, color="cyan")))
        fig.add_trace(go.Scatter(x=[dist], y=[cur_bottom], mode="markers", marker=dict(size=10, color="red")))

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


# ===================== LAYOUT =====================
app.layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "row",
        "height": "85vh",
        "overflow": "hidden"
    },
    children=[

        # ===== لوحة التحكم =====
        html.Div(
            style={
                "flex": "0 0 24%",
                "padding": "15px",
                "backgroundColor": "#f5f7fa",
                "overflowY": "auto",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.15)"
            },
            children=[

                html.H2("🎛️ اختر النموذج من الأسفل"),

                dcc.Dropdown(
                    id="model",
                    options=[
                        {"label": "مسطح", "value": "flat"},
                        {"label": "كروي", "value": "curved"}
                    ],
                    value="flat"
                ),

                html.Br(),

                html.Label("ارتفاع الجسم"),
                dcc.Slider(id="obj", min=1, max=100, value=50),

                html.Label("ارتفاع العين"),
                dcc.Slider(id="eye", min=0.1, max=10, value=1.7),

                html.Label("المسافة"),
                dcc.Slider(id="dist", min=1, max=100, value=20),

                html.Label("التكبير"),
                dcc.Slider(id="zoom", min=0, max=5, value=0),

                html.Label("الارتفاع"),
                dcc.Slider(id="alt", min=0, max=50, value=10),

                html.Div(id="info", style={"marginTop": "15px"}),

                html.Hr(),
                html.P("برمجة وتطوير: عدناني"),
                html.P("X (Twitter): @aale1164")
            ]
        ),

        # ===== الرسم البياني =====
        html.Div(
            style={
                "flex": "1",
                "padding": "10px",
                "height": "85vh"
            },
            children=[
                dcc.Graph(
                    id="graph",
                    style={
                        "height": "100%",
                        "width": "100%"
                    }
                )
            ]
        )

    ]
)


# ===================== CALLBACK =====================
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
        html.P(f"الأفق: {math.sqrt(2 * R_KM * (eye / 1000)):.2f} كم"),
        html.P(f"زاوية الأفق: {horizon_dip_deg(alt):.2f}°")
    ])

    return fig, info


# ===================== مهم للنشر =====================
server = app.server
