# -*- coding: utf-8 -*-
# تطبيق Dash - شاشة مقسمة:
# اليسار: صورة
# اليمين: أعلى تعليمات، وسط حاسبة، أسفل رسم بياني لانحناء الأرض

import dash
from dash import html, dcc, Input, Output
import math
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)
server = app.server

R_km = 6371.0

def curvature_drop(distance_km):
    if distance_km < 0:
        return 0.0
    return (distance_km ** 2) / (2 * R_km) * 1000

def horizon_distance(observer_height_m):
    if observer_height_m < 0:
        return 0.0
    return math.sqrt(2 * R_km * (observer_height_m / 1000))

# دالة لإنشاء الرسم البياني (منحنى الانحناء)
def create_curvature_graph(max_distance_km=100):
    distances = np.linspace(0, max_distance_km, 200)
    drops = [curvature_drop(d) for d in distances]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=distances, y=drops, mode='lines', name='الانحناء', line=dict(color='#4CAF50', width=2)))
    fig.update_layout(
        title="منحنى انحناء الأرض",
        xaxis_title="المسافة (كم)",
        yaxis_title="الانخفاض (متر)",
        template="plotly_dark",
        height=250,
        margin=dict(l=40, r=20, t=40, b=30),
        paper_bgcolor='#0d0d1a',
        plot_bgcolor='#1e1e2f',
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
        'overflow': 'hidden'
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
                'margin': '0'
            },
            children=[
                html.Img(
                    src='/ASdddd112.jpg',
                    style={'width': '100%', 'height': '100%', 'objectFit': 'cover'}
                )
            ]
        ),
        # القسم الأيمن: عمودي (تعليمات، حاسبة، رسم بياني)
        html.Div(
            style={
                'width': '30%',
                'display': 'flex',
                'flexDirection': 'column',
                'backgroundColor': '#0d0d1a',
                'color': 'white',
                'padding': '0',
                'margin': '0',
                'height': '100vh',
                'overflow': 'hidden'
            },
            children=[
                # التعليمات (25% من الارتفاع)
                html.Div(
                    style={
                        'flex': '0.25',
                        'backgroundColor': '#1e1e2f',
                        'padding': '8px',
                        'overflowY': 'auto',
                        'borderBottom': '1px solid #333',
                        'fontFamily': 'Tharwat Emara Ruqaa, "Traditional Arabic", Tahoma, sans-serif',
                        'fontWeight': 'bold',
                        'textAlign': 'right',
                        'direction': 'rtl',
                        'paddingRight': '20px',
                    },
                    children=[
                        html.H4("📘 تعليمات:", style={'color': '#4CAF50', 'marginTop': '0', 'marginBottom': '5px'}),
                        html.Ul([
                            html.Li("أدخل المسافة (كيلومتر أو ميل)."),
                            html.Li("اضغط على زر 'احسب الانحناء'."),
                            html.Li("ستظهر قيمة الانخفاض."),
                            html.Li("القيمة النظرية لا تأخذ في الاعتبار الانكسار الجوي."),
                            html.Li("الرسم البياني يوضح منحنى الانحناء حتى 100 كم.")
                        ], style={'paddingRight': '15px', 'margin': '0', 'fontSize': '0.8rem'})
                    ]
                ),
                # الحاسبة (35% من الارتفاع)
                html.Div(
                    style={
                        'flex': '0.35',
                        'backgroundColor': '#0d0d1a',
                        'padding': '8px',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'overflowY': 'auto'
                    },
                    children=[
                        html.H3("🌍 حاسبة انحناء الأرض", style={'textAlign': 'center', 'fontSize': '1.1rem', 'marginBottom': '5px'}),
                        html.Label("أدخل المسافة:", style={'fontSize': '0.85rem'}),
                        dcc.Input(
                            id='distance-input',
                            type='number',
                            value=10,
                            step=0.1,
                            style={
                                'width': '80%',
                                'padding': '5px',
                                'fontSize': '0.85rem',
                                'margin': '5px 0',
                                'borderRadius': '6px',
                                'border': 'none',
                                'backgroundColor': '#2a2a3a',
                                'color': 'white',
                                'textAlign': 'center'
                            }
                        ),
                        html.Label("الوحدة:", style={'fontSize': '0.85rem', 'marginTop': '3px'}),
                        dcc.RadioItems(
                            id='unit-selector',
                            options=[
                                {'label': ' كيلومتر (km)', 'value': 'km'},
                                {'label': ' ميل (mile)', 'value': 'mile'}
                            ],
                            value='km',
                            labelStyle={'display': 'inline-block', 'margin': '4px', 'fontSize': '0.75rem'},
                            style={'textAlign': 'center'}
                        ),
                        html.Button("احسب الانحناء", id='calc-button', n_clicks=0,
                                    style={
                                        'backgroundColor': '#4CAF50',
                                        'color': 'white',
                                        'padding': '4px 8px',
                                        'fontSize': '0.85rem',
                                        'border': 'none',
                                        'borderRadius': '6px',
                                        'cursor': 'pointer',
                                        'margin': '6px 0',
                                        'width': '60%'
                                    }),
                        html.Div(id='result-container',
                                 style={
                                     'backgroundColor': '#1e1e2f',
                                     'padding': '6px',
                                     'borderRadius': '8px',
                                     'width': '90%',
                                     'textAlign': 'center',
                                     'border': '1px solid #444',
                                     'marginTop': '5px',
                                     'fontSize': '0.75rem'
                                 })
                    ]
                ),
                # الرسم البياني (40% من الارتفاع)
                html.Div(
                    style={
                        'flex': '0.4',
                        'backgroundColor': '#0d0d1a',
                        'padding': '5px',
                        'overflow': 'hidden'
                    },
                    children=[
                        dcc.Graph(
                            id='curvature-graph',
                            figure=create_curvature_graph(100),
                            config={'displayModeBar': False},
                            style={'height': '100%', 'width': '100%'}
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    [Output('result-container', 'children'),
     Output('curvature-graph', 'figure')],
    [Input('calc-button', 'n_clicks'),
     Input('distance-input', 'value'),
     Input('unit-selector', 'value')]
)
def update_results(n_clicks, dist_val, unit_val):
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
    
    eye_height = 1.7
    horizon_km = horizon_distance(eye_height)
    horizon_miles = horizon_km * 0.621371
    
    result_text = html.Div([
        html.P(f"المسافة: {distance:.2f} {unit_name}", style={'margin': '0 0 4px 0', 'fontWeight': 'bold'}),
        html.P("📉 مقدار الانحناء (الانخفاض):", style={'margin': '2px'}),
        html.H4(f"{drop_m:.2f} متر", style={'color': '#ffaa00', 'margin': '2px'}),
        html.P(f"أي ما يعادل {drop_ft:.2f} قدم", style={'fontSize': '0.7rem', 'margin': '2px'}),
        html.Hr(style={'margin': '4px 0'}),
        html.P(f"👁️ مسافة الأفق (ارتفاع {eye_height} م) ≈ {horizon_km:.2f} كم ({horizon_miles:.2f} ميل)", 
               style={'fontSize': '0.7rem', 'margin': '2px', 'color': '#aaa'})
    ])
    
    # تحديث الرسم البياني: نضيف نقطة حمراء عند المسافة المدخلة
    max_dist = 100
    distances = np.linspace(0, max_dist, 200)
    drops = [curvature_drop(d) for d in distances]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=distances, y=drops, mode='lines', name='الانحناء', line=dict(color='#4CAF50', width=2)))
    # إضافة نقطة للمسافة الحالية (إذا كانت ضمن النطاق)
    if distance_km <= max_dist:
        fig.add_trace(go.Scatter(x=[distance_km], y=[drop_m], mode='markers', 
                                 marker=dict(color='red', size=8, symbol='circle'),
                                 name=f'المسافة: {distance_km:.1f} كم'))
    fig.update_layout(
        title="منحنى انحناء الأرض",
        xaxis_title="المسافة (كم)",
        yaxis_title="الانخفاض (متر)",
        template="plotly_dark",
        height=250,
        margin=dict(l=40, r=20, t=40, b=30),
        paper_bgcolor='#0d0d1a',
        plot_bgcolor='#1e1e2f',
        font=dict(color='white')
    )
    return result_text, fig

if __name__ == '__main__':
    app.run(debug=True)
