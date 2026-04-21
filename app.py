# -*- coding: utf-8 -*-
# تطبيق Dash - فقط حاسبة انحناء الأرض والرسم البياني
# تم إزالة جميع المربعات الأخرى

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

def create_curvature_graph(distance_km, drop_m):
    max_dist = max(distance_km, 1)
    distances = [i * 0.5 for i in range(int(max_dist * 2) + 1)]
    drops = [curvature_drop(d) for d in distances]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=distances, y=drops, mode='lines+markers',
                             name='الانحناء النظري',
                             line=dict(color='#4CAF50', width=2),
                             marker=dict(size=3)))
    fig.add_vline(x=distance_km, line_dash="dash", line_color="red",
                  annotation_text=f"{distance_km:.1f} كم", annotation_position="top right")
    fig.add_hline(y=drop_m, line_dash="dash", line_color="orange",
                  annotation_text=f"{drop_m:.2f} م", annotation_position="bottom right")
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(color='white', size=10, family='Arial', weight='bold'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=8, weight='bold')),
        xaxis_title="المسافة (كم)",
        yaxis_title="الانخفاض (متر)",
        title="منحنى انحناء الأرض",
        title_font_size=12
    )
    return fig

app.layout = html.Div(
    style={
        'display': 'flex',
        'flexDirection': 'row',
        'height': '100vh',
        'width': '100vw',
        'margin': '0',
        'padding': '0',
        'fontFamily': 'Arial, sans-serif',
        'fontWeight': 'bold',
        'color': 'white',
        'backgroundColor': '#000'
    },
    children=[
        # القسم الأيمن: حاسبة الانحناء
        html.Div(
            style={
                'flex': '1',
                'backgroundColor': '#0d0d1a',
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '20px',
                'margin': '10px',
                'borderRadius': '12px'
            },
            children=[
                html.H2("🌍 حاسبة انحناء الأرض", style={'textAlign': 'center', 'color': 'white', 'marginBottom': '20px', 'fontWeight': 'bold'}),
                html.Label("أدخل المسافة:", style={'fontSize': 14, 'fontWeight': 'bold'}),
                dcc.Input(
                    id='dist-input',
                    type='number',
                    value=10,
                    step=0.5,
                    style={
                        'width': '80%',
                        'padding': '8px',
                        'fontSize': 14,
                        'margin': '10px 0',
                        'backgroundColor': '#2a2a3a',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '6px',
                        'fontWeight': 'bold',
                        'textAlign': 'center'
                    }
                ),
                html.Label("الوحدة:", style={'fontSize': 14, 'fontWeight': 'bold'}),
                dcc.RadioItems(
                    id='unit-select',
                    options=[
                        {'label': ' كيلومتر (km)', 'value': 'km'},
                        {'label': ' ميل (mile)', 'value': 'mile'}
                    ],
                    value='km',
                    labelStyle={'display': 'inline-block', 'margin': '10px', 'fontSize': 12, 'fontWeight': 'bold', 'color': 'white'},
                    style={'textAlign': 'center'}
                ),
                html.Button(
                    "احسب الانحناء",
                    id='calc-btn',
                    n_clicks=0,
                    style={
                        'backgroundColor': '#4CAF50',
                        'color': 'white',
                        'padding': '8px 16px',
                        'fontSize': 14,
                        'border': 'none',
                        'borderRadius': '6px',
                        'cursor': 'pointer',
                        'margin': '15px 0',
                        'width': '60%',
                        'fontWeight': 'bold'
                    }
                ),
                html.Div(
                    id='result-div',
                    style={
                        'backgroundColor': '#1e1e2f',
                        'padding': '12px',
                        'borderRadius': '8px',
                        'width': '80%',
                        'textAlign': 'center',
                        'marginTop': '15px',
                        'border': '1px solid #444'
                    }
                )
            ]
        ),
        # القسم الأيسر: الرسم البياني
        html.Div(
            style={
                'flex': '1',
                'backgroundColor': '#0d0d1a',
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '20px',
                'margin': '10px',
                'borderRadius': '12px'
            },
            children=[
                dcc.Graph(
                    id='curvature-graph',
                    config={'displayModeBar': True},
                    style={'width': '100%', 'height': '100%'}
                )
            ]
        )
    ]
)

@app.callback(
    Output('result-div', 'children'),
    Output('curvature-graph', 'figure'),
    Input('calc-btn', 'n_clicks'),
    Input('dist-input', 'value'),
    Input('unit-select', 'value')
)
def update_curvature(n_clicks, dist_val, unit):
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
        html.P(f"📏 المسافة: {dist:.2f} {unit_label}", style={'margin': '0 0 5px 0', 'fontSize': 14, 'fontWeight': 'bold'}),
        html.P(f"📉 الانخفاض: {drop_m:.2f} متر", style={'margin': '0', 'color': '#ffaa00', 'fontSize': 14, 'fontWeight': 'bold'}),
        html.P(f"≈ {drop_ft:.2f} قدم", style={'margin': '5px 0 0 0', 'fontSize': 12, 'fontWeight': 'bold'})
    ])
    fig = create_curvature_graph(dist_km, drop_m)
    return result, fig

if __name__ == '__main__':
    app.run(debug=True)
