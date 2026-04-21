# -*- coding: utf-8 -*-
# تطبيق Dash - شاشة مقسمة (يسار: صورة 54.jpg، يمين: حاسبة انحناء الأرض)

import dash
from dash import html, dcc, Input, Output
import math

app = dash.Dash(__name__)
server = app.server

# ثوابت انحناء الأرض
R_km = 6371.0  # نصف القطر بالكيلومترات

def curvature_drop(distance_km):
    """حساب الانخفاض بسبب الانحناء بالأمتار"""
    if distance_km < 0:
        return 0.0
    return (distance_km ** 2) / (2 * R_km) * 1000

def horizon_distance(observer_height_m):
    """مسافة الأفق بالكيلومترات لراصد ارتفاعه بالأمتار"""
    if observer_height_m < 0:
        return 0.0
    return math.sqrt(2 * R_km * (observer_height_m / 1000))

# تنسيق الصفحة
app.layout = html.Div(
    style={
        'display': 'flex',
        'flexDirection': 'row',
        'height': '100vh',
        'width': '100vw',
        'margin': '0',
        'padding': '0',
        'fontFamily': 'Arial, sans-serif'
    },
    children=[
        # القسم الأيسر: الصورة (بحجم نصف القسم تقريباً)
        html.Div(
            style={
                'flex': '1',
                'backgroundColor': '#1e1e2f',
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '20px'
            },
            children=[
                html.Img(
                    src='/54.jpg',   # الصورة موجودة في جذر المستودع
                    style={
                        'maxWidth': '50%',      # نصف عرض القسم الأيسر
                        'maxHeight': '50%',     # نصف ارتفاع القسم الأيسر
                        'width': 'auto',
                        'height': 'auto',
                        'objectFit': 'contain',
                        'borderRadius': '12px',
                        'boxShadow': '0 6px 12px rgba(0,0,0,0.4)'
                    }
                ),
                html.P("خريطة غليسون (1892)", style={'color': '#aaa', 'marginTop': '20px', 'fontSize': '14px'})
            ]
        ),
        # القسم الأيمن: حاسبة انحناء الأرض
        html.Div(
            style={
                'flex': '1',
                'backgroundColor': '#0d0d1a',
                'color': 'white',
                'padding': '30px',
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center',
                'alignItems': 'center',
                'overflowY': 'auto'
            },
            children=[
                html.H1("🌍 حاسبة انحناء الأرض", style={'textAlign': 'center', 'marginBottom': '30px'}),
                html.Hr(style={'width': '80%', 'borderColor': '#444'}),
                html.Label("أدخل المسافة:", style={'fontSize': '18px', 'marginTop': '20px'}),
                dcc.Input(
                    id='distance-input',
                    type='number',
                    value=10,
                    step=0.1,
                    style={
                        'width': '80%',
                        'padding': '12px',
                        'fontSize': '18px',
                        'margin': '10px 0',
                        'borderRadius': '8px',
                        'border': 'none',
                        'backgroundColor': '#2a2a3a',
                        'color': 'white',
                        'textAlign': 'center'
                    }
                ),
                html.Label("الوحدة:", style={'fontSize': '18px', 'marginTop': '10px'}),
                dcc.RadioItems(
                    id='unit-selector',
                    options=[
                        {'label': ' كيلومتر (km)', 'value': 'km'},
                        {'label': ' ميل (mile)', 'value': 'mile'}
                    ],
                    value='km',
                    labelStyle={'display': 'inline-block', 'margin': '10px', 'fontSize': '16px'},
                    style={'textAlign': 'center'}
                ),
                html.Button("احسب الانحناء", id='calc-button', n_clicks=0,
                            style={
                                'backgroundColor': '#4CAF50',
                                'color': 'white',
                                'padding': '12px 24px',
                                'fontSize': '18px',
                                'border': 'none',
                                'borderRadius': '8px',
                                'cursor': 'pointer',
                                'margin': '20px 0',
                                'width': '60%'
                            }),
                html.Div(id='result-container',
                         style={
                             'backgroundColor': '#1e1e2f',
                             'padding': '20px',
                             'borderRadius': '12px',
                             'width': '80%',
                             'marginTop': '20px',
                             'textAlign': 'center',
                             'border': '1px solid #444'
                         }),
                html.Div(id='horizon-container',
                         style={'marginTop': '20px', 'fontSize': '14px', 'color': '#aaa'})
            ]
        )
    ]
)

@app.callback(
    [Output('result-container', 'children'),
     Output('horizon-container', 'children')],
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
    
    result_text = html.Div([
        html.H3(f"المسافة: {distance:.2f} {unit_name}", style={'margin': '0 0 10px 0'}),
        html.P("📉 مقدار الانحناء (الانخفاض):", style={'fontSize': '16px', 'margin': '5px'}),
        html.H2(f"{drop_m:.2f} متر", style={'color': '#ffaa00', 'margin': '5px'}),
        html.P(f"أي ما يعادل {drop_ft:.2f} قدم", style={'fontSize': '14px', 'color': '#ccc'}),
        html.Hr(style={'width': '80%', 'borderColor': '#555'}),
        html.P("ملاحظة: هذا الحساب يهمل تأثير الانكسار الجوي. القيمة تمثل الانخفاض الهندسي النظري.",
               style={'fontSize': '12px', 'color': '#888'})
    ])
    
    eye_height = 1.7
    horizon_km = horizon_distance(eye_height)
    horizon_miles = horizon_km * 0.621371
    horizon_text = html.Div([
        html.P(f"👁️ لشخص ارتفاع عينيه {eye_height} متر، المسافة إلى الأفق ≈ {horizon_km:.2f} كم ({horizon_miles:.2f} ميل).",
               style={'margin': '5px'})
    ])
    return result_text, horizon_text

if __name__ == '__main__':
    app.run(debug=True)
