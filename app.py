# -*- coding: utf-8 -*-
# تطبيق Dash - ثلاث أعمدة:
# العمود الأيسر: صورة
# العمود الأوسط: تعليمات فقط
# العمود الأيمن: رسم بياني مكبر بالأعلى + حاسبة انحناء الأرض بالأسفل

import dash
from dash import html, dcc, Input, Output
import math
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)
server = app.server

# ثوابت الانحناء
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
def create_curvature_graph(max_distance_km=100, current_distance_km=None, current_drop_m=None):
    distances = np.linspace(0, max_distance_km, 200)
    drops = [curvature_drop(d) for d in distances]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=distances, y=drops, mode='lines', name='الانحناء',
                             line=dict(color='#4CAF50', width=3)))  # زيادة العرض
    if current_distance_km is not None and current_drop_m is not None and current_distance_km <= max_distance_km:
        fig.add_trace(go.Scatter(x=[current_distance_km], y=[current_drop_m], mode='markers',
                                 marker=dict(color='red', size=12, symbol='circle'),
                                 name=f'المسافة: {current_distance_km:.1f} كم'))
    fig.update_layout(
        title="منحنى انحناء الأرض (مكبر)",
        xaxis_title="المسافة (كم)",
        yaxis_title="الانخفاض (متر)",
        template="plotly_dark",
        height=500,  # حجم مكبر
        margin=dict(l=40, r=20, t=50, b=40),
        paper_bgcolor='#0d0d1a',
        plot_bgcolor='#1e1e2f',
        font=dict(color='white', size=12)
    )
    return fig

# تصميم الصفحة
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
        # العمود الأيسر: الصورة
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
                    src='/ASdddd112.jpg',  # ضع المسار الصحيح
                    style={'width': '100%', 'height': '100%', 'objectFit': 'cover'}
                )
            ]
        ),
        # العمود الأوسط: التعليمات فقط (بعد نقل الحاسبة والرسم البياني)
        html.Div(
            style={
                'flex': '0.8',
                'backgroundColor': '#1e1e2f',
                'padding': '15px',
                'overflowY': 'auto',
                'borderLeft': '1px solid #333',
                'fontFamily': 'Tharwat Emara Ruqaa, "Traditional Arabic", Tahoma, sans-serif',
                'fontWeight': 'bold',
                'textAlign': 'right',
                'direction': 'rtl'
            },
            children=[
                html.H3("📘 تعليمات:", style={'color': '#4CAF50', 'marginTop': '0'}),
                html.Ul([
                    html.Li("أدخل المسافة (كيلومتر أو ميل) في الحاسبة على اليمين."),
                    html.Li("اضغط على زر 'احسب الانحناء'."),
                    html.Li("ستظهر قيمة الانخفاض الناتج عن انحناء الأرض بالأمتار والأقدام."),
                    html.Li("القيمة النظرية لا تأخذ في الاعتبار الانكسار الجوي."),
                    html.Li("الرسم البياني المكبر يوضح المنحنى حتى 100 كم."),
                    html.Li("يمكنك استخدام التكبير والتدوير بالماوس لرؤية الصورة بشكل أفضل.")
                ], style={'paddingRight': '20px'})
            ]
        ),
        # العمود الأيمن: رسم بياني مكبر (أعلى) + حاسبة (أسفل)
        html.Div(
            style={
                'flex': '1.2',
                'display': 'flex',
                'flexDirection': 'column',
                'backgroundColor': '#0d0d1a',
                'color': 'white',
                'padding': '10px',
                'margin': '0',
                'height': '100vh',
                'overflow': 'hidden'
            },
            children=[
                # الرسم البياني (مكبر)
                html.Div(
                    style={
                        'flex': '2',
                        'marginBottom': '10px',
                        'minHeight': '400px'
                    },
                    children=[
                        dcc.Graph(
                            id='curvature-graph',
                            figure=create_curvature_graph(),
                            config={'displayModeBar': True},
                            style={'height': '100%', 'width': '100%'}
                        )
                    ]
                ),
                # الحاسبة (أسفل الرسم البياني)
                html.Div(
                    style={
                        'flex': '1',
                        'backgroundColor': '#0d0d1a',
                        'padding': '10px',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'borderTop': '1px solid #333',
                        'overflowY': 'auto'
                    },
                    children=[
                        html.H3("🌍 حاسبة انحناء الأرض", style={'textAlign': 'center', 'fontSize': '1.2rem', 'marginBottom': '10px'}),
                        html.Label("أدخل المسافة:", style={'fontSize': '1rem'}),
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
                                'textAlign': 'center'
                            }
                        ),
                        html.Label("الوحدة:", style={'fontSize': '1rem', 'marginTop': '5px'}),
                        dcc.RadioItems(
                            id='unit-selector',
                            options=[
                                {'label': ' كيلومتر (km)', 'value': 'km'},
                                {'label': ' ميل (mile)', 'value': 'mile'}
                            ],
                            value='km',
                            labelStyle={'display': 'inline-block', 'margin': '8px', 'fontSize': '0.9rem'},
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
                                        'width': '60%'
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
                                     'fontSize': '0.9rem'
                                 })
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
        html.P(f"المسافة: {distance:.2f} {unit_name}", style={'margin': '0 0 8px 0', 'fontWeight': 'bold'}),
        html.P("📉 مقدار الانحناء (الانخفاض):", style={'margin': '5px'}),
        html.H4(f"{drop_m:.2f} متر", style={'color': '#ffaa00', 'margin': '5px'}),
        html.P(f"أي ما يعادل {drop_ft:.2f} قدم", style={'fontSize': '0.85rem', 'margin': '5px'}),
        html.Hr(style={'margin': '8px 0'}),
        html.P(f"👁️ مسافة الأفق (ارتفاع {eye_height} م) ≈ {horizon_km:.2f} كم ({horizon_miles:.2f} ميل)",
               style={'fontSize': '0.8rem', 'margin': '5px', 'color': '#aaa'})
    ])
    
    # تحديث الرسم البياني مع حجم مكبر ونقطة حمراء
    fig = create_curvature_graph(max_distance_km=100, current_distance_km=distance_km, current_drop_m=drop_m)
    return result_text, fig

if __name__ == '__main__':
    app.run(debug=True)
