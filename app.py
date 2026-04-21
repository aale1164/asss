# -*- coding: utf-8 -*-
# تطبيق Dash - تصميم مقسم إلى 6 حاويات في القسم الأيمن
# مع تصغير حجم الحاسبة بنسبة 25%

import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import math

app = dash.Dash(__name__)
server = app.server

R_km = 6371.0

def curvature_drop(distance_km):
    if distance_km < 0:
        return 0.0
    return (distance_km ** 2) / (2 * R_km) * 1000

def create_curvature_graph(distance_km, drop_m):
    distances = [i * 0.5 for i in range(int(distance_km * 2) + 1)]
    drops = [curvature_drop(d) for d in distances]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=distances, y=drops, mode='lines+markers',
                             name='الانحناء', line=dict(color='#4CAF50', width=2)))
    fig.add_vline(x=distance_km, line_dash="dash", line_color="red",
                  annotation_text=f"المسافة: {distance_km} كم", annotation_position="top right")
    fig.add_hline(y=drop_m, line_dash="dash", line_color="orange",
                  annotation_text=f"الانخفاض: {drop_m:.2f} م", annotation_position="bottom right")
    
    fig.update_layout(
        title="منحنى انحناء الأرض",
        xaxis_title="المسافة (كم)",
        yaxis_title="الانخفاض (متر)",
        template="plotly_dark",
        height=250,
        margin=dict(l=40, r=40, t=40, b=30),
        font=dict(color='white')
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
        'overflow': 'hidden',
        'backgroundColor': '#000'
    },
    children=[
        # القسم الأيسر: الصورة
        html.Div(
            style={
                'flex': '1',
                'backgroundColor': '#000',
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '0',
                'margin': '0',
                'height': '100vh'
            },
            children=[
                html.Img(
                    src='/ASdddd112.jpg',  # استخدم المسار الصحيح
                    style={
                        'width': '100%',
                        'height': '100%',
                        'objectFit': 'cover'
                    }
                )
            ]
        ),
        # القسم الأيمن: 6 حاويات
        html.Div(
            style={
                'width': '30%',
                'display': 'flex',
                'flexDirection': 'column',
                'backgroundColor': '#0d0d1a',
                'height': '100vh',
                'overflow': 'auto',
                'padding': '0',
                'margin': '0'
            },
            children=[
                # الحاوية 1: التعليمات (نص أبيض)
                html.Div(
                    style={
                        'flex': '1',
                        'backgroundColor': '#1e1e2f',
                        'borderBottom': '1px solid #333',
                        'padding': '10px',
                        'position': 'relative',
                        'overflow': 'auto'
                    },
                    children=[
                        html.Div("1", style={'position': 'absolute', 'top': 5, 'left': 5, 'color': '#888', 'fontSize': '12px'}),
                        html.H4("📘 تعليمات:", style={'color': 'white', 'marginTop': '0', 'marginBottom': '8px'}),
                        html.Ul([
                            html.Li("أدخل المسافة (كيلومتر أو ميل).", style={'color': 'white'}),
                            html.Li("اضغط على زر 'احسب الانحناء'.", style={'color': 'white'}),
                            html.Li("ستظهر قيمة الانخفاض بالأمتار والأقدام.", style={'color': 'white'}),
                            html.Li("الرسم البياني يتغير تلقائياً.", style={'color': 'white'}),
                            html.Li("القيمة النظرية تهمل الانكسار الجوي.", style={'color': 'white'})
                        ], style={'paddingRight': '15px', 'margin': '0'})
                    ]
                ),
                # الحاوية 2: حاسبة الانحناء (مصغرة بنسبة 25%)
                html.Div(
                    style={
                        'flex': '1',
                        'backgroundColor': '#0d0d1a',
                        'borderBottom': '1px solid #333',
                        'padding': '6px',
                        'position': 'relative',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'justifyContent': 'center',
                        'overflow': 'auto'
                    },
                    children=[
                        html.Div("2", style={'position': 'absolute', 'top': 3, 'left': 5, 'color': '#888', 'fontSize': '10px'}),
                        html.H5("🌍 حاسبة الانحناء", style={'textAlign': 'center', 'margin': '0 0 5px 0', 'color': '#ddd', 'fontSize': '0.9rem'}),
                        html.Label("المسافة:", style={'fontSize': '9px', 'color': 'white'}),
                        dcc.Input(
                            id='distance-input',
                            type='number',
                            value=10,
                            step=0.1,
                            style={
                                'width': '85%',
                                'padding': '3px',
                                'fontSize': '9px',
                                'margin': '3px 0',
                                'borderRadius': '3px',
                                'border': 'none',
                                'backgroundColor': '#2a2a3a',
                                'color': 'white',
                                'textAlign': 'center'
                            }
                        ),
                        html.Label("الوحدة:", style={'fontSize': '9px', 'marginTop': '3px', 'color': 'white'}),
                        dcc.RadioItems(
                            id='unit-selector',
                            options=[
                                {'label': ' كيلومتر', 'value': 'km'},
                                {'label': ' ميل', 'value': 'mile'}
                            ],
                            value='km',
                            labelStyle={'display': 'inline-block', 'margin': '2px', 'fontSize': '8px', 'color': 'white'},
                            style={'textAlign': 'center'}
                        ),
                        html.Button("احسب", id='calc-button', n_clicks=0,
                                    style={
                                        'backgroundColor': '#4CAF50',
                                        'color': 'white',
                                        'padding': '2px 6px',
                                        'fontSize': '9px',
                                        'border': 'none',
                                        'borderRadius': '3px',
                                        'cursor': 'pointer',
                                        'margin': '5px 0',
                                        'width': '45%'
                                    }),
                        html.Div(id='result-container',
                                 style={
                                     'backgroundColor': '#1e1e2f',
                                     'padding': '4px',
                                     'borderRadius': '4px',
                                     'width': '95%',
                                     'textAlign': 'center',
                                     'border': '1px solid #555',
                                     'fontSize': '8px',
                                     'marginTop': '3px',
                                     'color': 'white'
                                 }),
                        html.Div(id='horizon-container',
                                 style={'fontSize': '7px', 'color': '#aaa', 'textAlign': 'center', 'marginTop': '3px'})
                    ]
                ),
                # الحاوية 3: الرسم البياني
                html.Div(
                    id='graph-container',
                    style={
                        'flex': '1',
                        'backgroundColor': '#0d0d1a',
                        'borderBottom': '1px solid #333',
                        'padding': '5px',
                        'position': 'relative',
                        'overflow': 'hidden'
                    },
                    children=[
                        html.Div("3", style={'position': 'absolute', 'top': 5, 'left': 5, 'color': '#888', 'fontSize': '12px', 'zIndex': 10}),
                        dcc.Graph(id='curvature-graph', config={'displayModeBar': False}, style={'height': '100%', 'width': '100%'})
                    ]
                ),
                # الحاوية 4: فارغة
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#111', 'borderBottom': '1px solid #333', 'position': 'relative'},
                    children=[html.Div("4", style={'position': 'absolute', 'top': 5, 'left': 5, 'color': '#555', 'fontSize': '12px'})]
                ),
                # الحاوية 5: فارغة
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#111', 'borderBottom': '1px solid #333', 'position': 'relative'},
                    children=[html.Div("5", style={'position': 'absolute', 'top': 5, 'left': 5, 'color': '#555', 'fontSize': '12px'})]
                ),
                # الحاوية 6: فارغة
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#111', 'position': 'relative'},
                    children=[html.Div("6", style={'position': 'absolute', 'top': 5, 'left': 5, 'color': '#555', 'fontSize': '12px'})]
                )
            ]
        )
    ]
)

@app.callback(
    [Output('result-container', 'children'),
     Output('horizon-container', 'children'),
     Output('curvature-graph', 'figure')],
    [Input('calc-button', 'n_clicks'),
     Input('distance-input', 'value'),
     Input('unit-selector', 'value')]
)
def update_all(n_clicks, dist_val, unit_val):
    if dist_val is None:
        dist_val = 0
    distance = float(dist_val)
    unit = unit_val if unit_val else 'km'
    
    if unit == 'mile':
        distance_km = distance * 1.60934
        unit_name = 'ميل'
    else:
        distance_km = distance
        unit_name = 'كم'
    
    drop_m = curvature_drop(distance_km)
    drop_ft = drop_m * 3.28084
    
    result_text = html.Div([
        html.P(f"📏 المسافة: {distance:.2f} {unit_name}", style={'margin': '0 0 2px 0', 'fontWeight': 'bold', 'fontSize': '8px'}),
        html.P("📉 الانخفاض:", style={'margin': '1px', 'fontSize': '8px'}),
        html.H5(f"{drop_m:.2f} متر", style={'color': '#ffaa00', 'margin': '1px', 'fontSize': '9px'}),
        html.P(f"{drop_ft:.2f} قدم", style={'fontSize': '7px', 'margin': '1px'})
    ])
    
    eye_height = 1.7
    horizon_km = math.sqrt(2 * R_km * (eye_height / 1000))
    horizon_miles = horizon_km * 0.621371
    horizon_text = html.Div([
        html.P(f"👁️ الأفق ≈ {horizon_km:.1f} كم ({horizon_miles:.1f} ميل)", style={'margin': '0', 'fontSize': '7px'})
    ])
    
    fig = create_curvature_graph(distance_km, drop_m)
    return result_text, horizon_text, fig

if __name__ == '__main__':
    app.run(debug=True)
