# -*- coding: utf-8 -*-
# صفحة مقسمة إلى 6 مربعات متساوية (صفين، 3 أعمدة)
# الترقيم من اليمين إلى اليسار:
# الصف العلوي: 1 تعليمات، 2 حاسبة، 3 رسم بياني
# الصف السفلي: 4 فارغ، 5 فارغ، 6 فارغ

import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import math

app = dash.Dash(__name__)
server = app.server

R_KM = 6371.0

def curvature_drop(distance_km):
    if distance_km < 0:
        return 0.0
    return (distance_km ** 2) / (2 * R_KM) * 1000

def create_graph(distance_km, drop_m):
    max_dist = max(distance_km, 1)
    distances = [i * 0.5 for i in range(int(max_dist * 2) + 1)]
    drops = [curvature_drop(d) for d in distances]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=distances, y=drops, mode='lines+markers', line=dict(color='#4CAF50', width=2)))
    fig.add_vline(x=distance_km, line_dash="dash", line_color="red",
                  annotation_text=f"{distance_km:.1f} كم", annotation_position="top right")
    fig.add_hline(y=drop_m, line_dash="dash", line_color="orange",
                  annotation_text=f"{drop_m:.2f} م", annotation_position="bottom right")
    fig.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=30, b=10),
                      font=dict(color='white', size=9))
    return fig

app.layout = html.Div(
    style={
        'display': 'grid',
        'gridTemplateRows': '1fr 1fr',      # صفان متساويان
        'gridTemplateColumns': '1fr 1fr 1fr', # 3 أعمدة متساوية
        'height': '100vh',
        'width': '100vw',
        'gap': '2px',
        'backgroundColor': '#000',
        'margin': '0',
        'padding': '0'
    },
    children=[
        # ---- الصف العلوي (من اليمين إلى اليسار) ----
        # العمود 3 (أقصى اليمين) -> المربع 1: تعليمات
        html.Div(
            style={'backgroundColor': '#1e1e2f', 'position': 'relative', 'padding': '10px', 'overflow': 'auto'},
            children=[
                html.Div("1", style={'position': 'absolute', 'top': 10, 'right': 10, 'color': '#aaa', 'fontSize': 20}),
                html.H4("📘 تعليمات:", style={'color': 'white', 'marginTop': 35}),
                html.Ul([
                    html.Li("أدخل المسافة (كم أو ميل).", style={'color': 'white'}),
                    html.Li("اضغط على زر 'احسب'.", style={'color': 'white'}),
                    html.Li("ستظهر قيمة الانخفاض بالأمتار.", style={'color': 'white'}),
                    html.Li("الرسم البياني يتغير تلقائياً.", style={'color': 'white'}),
                    html.Li("الحساب نظري (بدون انكسار جوي).", style={'color': 'white'})
                ], style={'color': 'white'})
            ]
        ),
        # العمود 2 (الوسط) -> المربع 2: حاسبة
        html.Div(
            style={'backgroundColor': '#0d0d1a', 'position': 'relative', 'padding': '10px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'},
            children=[
                html.Div("2", style={'position': 'absolute', 'top': 10, 'right': 10, 'color': '#aaa', 'fontSize': 20}),
                html.H5("🌍 حاسبة الانحناء", style={'textAlign': 'center', 'color': 'white', 'marginTop': 30}),
                html.Label("المسافة:", style={'fontSize': 12, 'color': 'white'}),
                dcc.Input(id='dist-input', type='number', value=10, step=0.5,
                          style={'width': '90%', 'padding': '5px', 'margin': '5px 0', 'backgroundColor': '#2a2a3a', 'color': 'white', 'border': 'none', 'borderRadius': '4px'}),
                html.Label("الوحدة:", style={'fontSize': 12, 'color': 'white'}),
                dcc.RadioItems(id='unit-select', options=[{'label': ' كيلومتر', 'value': 'km'}, {'label': ' ميل', 'value': 'mile'}],
                               value='km', labelStyle={'display': 'inline-block', 'margin': '5px', 'color': 'white'}),
                html.Button("احسب", id='calc-btn', n_clicks=0,
                            style={'backgroundColor': '#4CAF50', 'color': 'white', 'padding': '5px 12px', 'margin': '10px 0', 'border': 'none', 'borderRadius': '4px', 'cursor': 'pointer'}),
                html.Div(id='res-div', style={'backgroundColor': '#1e1e2f', 'padding': '8px', 'borderRadius': '6px', 'marginTop': '10px', 'fontSize': 12, 'color': 'white', 'textAlign': 'center'})
            ]
        ),
        # العمود 1 (أقصى اليسار) -> المربع 3: رسم بياني
        html.Div(
            style={'backgroundColor': '#0d0d1a', 'position': 'relative', 'padding': '5px'},
            children=[
                html.Div("3", style={'position': 'absolute', 'top': 10, 'right': 10, 'color': '#aaa', 'fontSize': 20, 'zIndex': 10}),
                dcc.Graph(id='graph', config={'displayModeBar': False}, style={'height': '100%'})
            ]
        ),
        # ---- الصف السفلي (من اليمين إلى اليسار) ----
        # المربع 4 (فارغ)
        html.Div(
            style={'backgroundColor': '#111', 'position': 'relative'},
            children=[html.Div("4", style={'position': 'absolute', 'top': 10, 'right': 10, 'color': '#888', 'fontSize': 20})]
        ),
        # المربع 5 (فارغ)
        html.Div(
            style={'backgroundColor': '#111', 'position': 'relative'},
            children=[html.Div("5", style={'position': 'absolute', 'top': 10, 'right': 10, 'color': '#888', 'fontSize': 20})]
        ),
        # المربع 6 (فارغ)
        html.Div(
            style={'backgroundColor': '#111', 'position': 'relative'},
            children=[html.Div("6", style={'position': 'absolute', 'top': 10, 'right': 10, 'color': '#888', 'fontSize': 20})]
        )
    ]
)

@app.callback(
    Output('res-div', 'children'),
    Output('graph', 'figure'),
    Input('calc-btn', 'n_clicks'),
    Input('dist-input', 'value'),
    Input('unit-select', 'value')
)
def update(n_clicks, dist_val, unit):
    if dist_val is None:
        dist_val = 0
    dist = float(dist_val)
    if unit == 'mile':
        dist_km = dist * 1.60934
        unit_label = 'ميل'
    else:
        dist_km = dist
        unit_label = 'كم'
    drop_m = curvature_drop(dist_km)
    drop_ft = drop_m * 3.28084
    result = html.Div([
        html.P(f"📏 المسافة: {dist:.2f} {unit_label}", style={'margin': '0 0 5px 0'}),
        html.P(f"📉 الانخفاض: {drop_m:.2f} متر", style={'margin': '0', 'color': '#ffaa00'}),
        html.P(f"≈ {drop_ft:.2f} قدم", style={'margin': '2px 0 0 0', 'fontSize': 10})
    ])
    fig = create_graph(dist_km, drop_m)
    return result, fig

if __name__ == '__main__':
    app.run(debug=True)
