# -*- coding: utf-8 -*-
# تطبيق Dash - 6 مربعات متساوية (3 أعمدة × صفين)
# العمود الأيسر: أعلى = رسم بياني، أسفل = فارغ
# العمود الأوسط: أعلى = حاسبة انحناء الأرض، أسفل = فارغ
# العمود الأيمن: أعلى = تعليمات، أسفل = فارغ

import dash
from dash import html, dcc, Input, Output
import math
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)
server = app.server

# ==================== ثوابت الانحناء ====================
R_km = 6371.0

def curvature_drop(distance_km):
    if distance_km < 0:
        return 0.0
    return (distance_km ** 2) / (2 * R_km) * 1000

def horizon_distance(observer_height_m):
    if observer_height_m < 0:
        return 0.0
    return math.sqrt(2 * R_km * (observer_height_m / 1000))

# ==================== رسم بياني (منحنى الانحناء) ====================
def create_curvature_graph(max_distance_km=100, current_distance_km=None, current_drop_m=None):
    distances = np.linspace(0, max_distance_km, 200)
    drops = [curvature_drop(d) for d in distances]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=distances, y=drops, mode='lines', name='الانحناء',
                             line=dict(color='#4CAF50', width=3)))
    if current_distance_km is not None and current_drop_m is not None and current_distance_km <= max_distance_km:
        fig.add_trace(go.Scatter(x=[current_distance_km], y=[current_drop_m], mode='markers',
                                 marker=dict(color='red', size=12, symbol='circle'),
                                 name=f'المسافة: {current_distance_km:.1f} كم'))
    fig.update_layout(
        title="منحنى انحناء الأرض",
        xaxis_title="المسافة (كم)",
        yaxis_title="الانخفاض (متر)",
        template="plotly_dark",
        margin=dict(l=40, r=20, t=50, b=40),
        paper_bgcolor='#0d0d1a',
        plot_bgcolor='#1e1e2f',
        font=dict(color='white', size=12)
    )
    return fig

# ==================== تخطيط الصفحة (6 مربعات متساوية) ====================
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
        # العمود الأيسر
        html.Div(
            style={'flex': '1', 'display': 'flex', 'flexDirection': 'column', 'backgroundColor': '#0d0d1a'},
            children=[
                # المربع العلوي الأيسر: الرسم البياني
                html.Div(
                    style={'flex': '1', 'padding': '10px', 'borderBottom': '1px solid #333', 'overflow': 'hidden'},
                    children=[
                        dcc.Graph(
                            id='curvature-graph',
                            figure=create_curvature_graph(),
                            config={'displayModeBar': True},
                            style={'height': '100%', 'width': '100%'}
                        )
                    ]
                ),
                # المربع السفلي الأيسر: فارغ
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#1e1e2f', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'},
                    children=[html.Div("", style={'color': '#555'})]  # فارغ
                )
            ]
        ),
        # العمود الأوسط
        html.Div(
            style={'flex': '1', 'display': 'flex', 'flexDirection': 'column', 'backgroundColor': '#0d0d1a'},
            children=[
                # المربع العلوي الأوسط: حاسبة انحناء الأرض
                html.Div(
                    style={'flex': '1', 'padding': '15px', 'borderBottom': '1px solid #333', 'overflowY': 'auto'},
                    children=[
                        html.Div(
                            style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%'},
                            children=[
                                html.H3("🌍 حاسبة انحناء الأرض", style={'textAlign': 'center', 'fontSize': '1.3rem', 'marginBottom': '15px', 'fontWeight': 'bold'}),
                                html.Label("أدخل المسافة:", style={'fontSize': '1rem', 'fontWeight': 'bold'}),
                                dcc.Input(
                                    id='distance-input',
                                    type='number',
                                    value=10,
                                    step=0.1,
                                    style={
                                        'width': '80%',
                                        'padding': '8px',
                                        'fontSize': '1rem',
                                        'margin': '8px 0',
                                        'borderRadius': '8px',
                                        'border': 'none',
                                        'backgroundColor': '#2a2a3a',
                                        'color': 'white',
                                        'textAlign': 'center',
                                        'fontWeight': 'bold'
                                    }
                                ),
                                html.Label("الوحدة:", style={'fontSize': '1rem', 'marginTop': '5px', 'fontWeight': 'bold'}),
                                dcc.RadioItems(
                                    id='unit-selector',
                                    options=[
                                        {'label': ' كيلومتر (km)', 'value': 'km'},
                                        {'label': ' ميل (mile)', 'value': 'mile'}
                                    ],
                                    value='km',
                                    labelStyle={'display': 'inline-block', 'margin': '8px', 'fontSize': '0.9rem', 'fontWeight': 'bold'},
                                    style={'textAlign': 'center'}
                                ),
                                html.Button("احسب الانحناء", id='calc-button', n_clicks=0,
                                            style={
                                                'backgroundColor': '#4CAF50',
                                                'color': 'white',
                                                'padding': '8px 16px',
                                                'fontSize': '1rem',
                                                'border': 'none',
                                                'borderRadius': '8px',
                                                'cursor': 'pointer',
                                                'margin': '15px 0',
                                                'width': '60%',
                                                'fontWeight': 'bold'
                                            }),
                                html.Div(id='result-container',
                                         style={
                                             'backgroundColor': '#1e1e2f',
                                             'padding': '12px',
                                             'borderRadius': '10px',
                                             'width': '90%',
                                             'textAlign': 'center',
                                             'border': '1px solid #444',
                                             'marginTop': '10px',
                                             'fontSize': '0.9rem',
                                             'fontWeight': 'bold'
                                         })
                            ]
                        )
                    ]
                ),
                # المربع السفلي الأوسط: فارغ
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#1e1e2f', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'},
                    children=[html.Div("", style={'color': '#555'})]
                )
            ]
        ),
        # العمود الأيمن
        html.Div(
            style={'flex': '1', 'display': 'flex', 'flexDirection': 'column', 'backgroundColor': '#0d0d1a'},
            children=[
                # المربع العلوي الأيمن: التعليمات
                html.Div(
                    style={
                        'flex': '1',
                        'padding': '15px',
                        'borderBottom': '1px solid #333',
                        'overflowY': 'auto',
                        'fontFamily': 'Tharwat Emara Ruqaa, "Traditional Arabic", Tahoma, sans-serif',
                        'fontWeight': 'bold',
                        'textAlign': 'right',
                        'direction': 'rtl'
                    },
                    children=[
                        html.H3("📘 تعليمات:", style={'color': '#4CAF50', 'marginTop': '0', 'marginBottom': '15px'}),
                        html.Ul([
                            html.Li("أدخل المسافة (كيلومتر أو ميل) في الحاسبة بالعمود الأوسط."),
                            html.Li("اضغط على زر 'احسب الانحناء'."),
                            html.Li("ستظهر قيمة الانخفاض الناتج عن انحناء الأرض بالأمتار والأقدام."),
                            html.Li("القيمة النظرية لا تأخذ في الاعتبار الانكسار الجوي."),
                            html.Li("الرسم البياني بالعمود الأيسر يوضح المنحنى حتى 100 كم."),
                            html.Li("يمكنك استخدام التكبير والتدوير بالماوس لرؤية التفاصيل.")
                        ], style={'paddingRight': '20px', 'fontSize': '1rem'})
                    ]
                ),
                # المربع السفلي الأيمن: فارغ
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#1e1e2f', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'},
                    children=[html.Div("", style={'color': '#555'})]
                )
            ]
        )
    ]
)

# ==================== تحديث النتائج والرسم البياني ====================
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
        html.P(f"المسافة: {distance:.2f} {unit_name}", style={'margin': '0 0 8px 0', 'fontWeight': 'bold'}),
        html.P("📉 مقدار الانحناء (الانخفاض):", style={'margin': '5px', 'fontWeight': 'bold'}),
        html.H4(f"{drop_m:.2f} متر", style={'color': '#ffaa00', 'margin': '5px', 'fontWeight': 'bold'}),
        html.P(f"أي ما يعادل {drop_ft:.2f} قدم", style={'fontSize': '0.85rem', 'margin': '5px', 'fontWeight': 'bold'}),
        html.Hr(style={'margin': '8px 0'}),
        html.P(f"👁️ مسافة الأفق (ارتفاع {eye_height} م) ≈ {horizon_km:.2f} كم ({horizon_miles:.2f} ميل)",
               style={'fontSize': '0.8rem', 'margin': '5px', 'color': '#aaa', 'fontWeight': 'bold'})
    ])
    
    fig = create_curvature_graph(max_distance_km=100, current_distance_km=distance_km, current_drop_m=drop_m)
    return result_text, fig

if __name__ == '__main__':
    app.run(debug=True)
