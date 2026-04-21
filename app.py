# -*- coding: utf-8 -*-
# تطبيق Dash - شاشة مقسمة:
# اليسار: صورة كاملة
# اليمين: أعلى (تعليمات) + أسفل (حاسبة انحناء الأرض)

import dash
from dash import html, dcc, Input, Output
import math

app = dash.Dash(__name__)
server = app.server

# ثابت انحناء الأرض (نصف القطر بالكيلومترات)
R_km = 6371.0

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
        'fontFamily': 'Arial, sans-serif',
        'overflow': 'hidden'
    },
    children=[
        # القسم الأيسر: الصورة (تملأ المساحة المتاحة)
        html.Div(
            style={
                'flex': '1',  # يأخذ نفس مساحة القسم الأيمن
                'backgroundColor': '#000',
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '0',
                'margin': '0'
            },
            children=[
                html.Img(
                    src='/ASdddd112.jpg',  # استخدم المسار الصحيح (أو غيره إلى الرابط المباشر)
                    style={
                        'width': '100%',
                        'height': '100%',
                        'objectFit': 'cover',  # تغطي كامل المنطقة بدون تشويه (قد تقص)
                        # إذا أردت الصورة كاملة بدون قص استخدم 'contain'
                    }
                )
            ]
        ),
        # القسم الأيمن: يحتوي على جزئين متساويين (أعلى وأسفل)
        html.Div(
            style={
                'flex': '1',
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
                # الجزء العلوي: التعليمات (نصف الارتفاع)
                html.Div(
                    style={
                        'flex': '1',
                        'backgroundColor': '#1e1e2f',
                        'padding': '20px',
                        'overflowY': 'auto',
                        'borderBottom': '2px solid #333'
                    },
                    children=[
                        html.H3("📘 تعليمات:", style={'color': '#4CAF50', 'marginTop': '0'}),
                        html.Ul([
                            html.Li("أدخل المسافة (بالكيلومتر أو الميل)."),
                            html.Li("اضغط على زر 'احسب الانحناء'."),
                            html.Li("ستظهر قيمة الانخفاض الناتج عن انحناء الأرض بالأمتار والأقدام."),
                            html.Li("القيمة النظرية لا تأخذ في الاعتبار الانكسار الجوي."),
                            html.Li("يمكنك استخدام التكبير والتدوير بالماوس لرؤية الصورة بشكل أفضل.")
                        ], style={'paddingRight': '20px'})
                    ]
                ),
                # الجزء السفلي: حاسبة الانحناء (نصف الارتفاع)
                html.Div(
                    style={
                        'flex': '1',
                        'backgroundColor': '#0d0d1a',
                        'padding': '20px',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'overflowY': 'auto'
                    },
                    children=[
                        html.H1("🌍 حاسبة انحناء الأرض", style={'textAlign': 'center', 'fontSize': '1.8rem', 'marginBottom': '15px'}),
                        html.Label("أدخل المسافة:", style={'fontSize': '18px'}),
                        dcc.Input(
                            id='distance-input',
                            type='number',
                            value=10,
                            step=0.1,
                            style={
                                'width': '80%',
                                'padding': '10px',
                                'fontSize': '18px',
                                'margin': '10px 0',
                                'borderRadius': '8px',
                                'border': 'none',
                                'backgroundColor': '#2a2a3a',
                                'color': 'white',
                                'textAlign': 'center'
                            }
                        ),
                        html.Label("الوحدة:", style={'fontSize': '18px', 'marginTop': '5px'}),
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
                                        'padding': '10px 20px',
                                        'fontSize': '18px',
                                        'border': 'none',
                                        'borderRadius': '8px',
                                        'cursor': 'pointer',
                                        'margin': '15px 0',
                                        'width': '60%'
                                    }),
                        html.Div(id='result-container',
                                 style={
                                     'backgroundColor': '#1e1e2f',
                                     'padding': '15px',
                                     'borderRadius': '12px',
                                     'width': '90%',
                                     'textAlign': 'center',
                                     'border': '1px solid #444',
                                     'marginTop': '10px'
                                 }),
                        html.Div(id='horizon-container',
                                 style={'marginTop': '15px', 'fontSize': '14px', 'color': '#aaa', 'textAlign': 'center'})
                    ]
                )
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
        html.H4(f"المسافة: {distance:.2f} {unit_name}", style={'margin': '0 0 8px 0'}),
        html.P("📉 مقدار الانحناء (الانخفاض):", style={'margin': '5px', 'fontSize': '15px'}),
        html.H3(f"{drop_m:.2f} متر", style={'color': '#ffaa00', 'margin': '5px'}),
        html.P(f"أي ما يعادل {drop_ft:.2f} قدم", style={'fontSize': '13px', 'color': '#ccc'}),
        html.Hr(style={'width': '80%', 'borderColor': '#555'}),
        html.P("ملاحظة: الحساب النظري يهمل الانكسار الجوي.", style={'fontSize': '11px', 'color': '#888'})
    ])
    
    eye_height = 1.7
    horizon_km = horizon_distance(eye_height)
    horizon_miles = horizon_km * 0.621371
    horizon_text = html.Div([
        html.P(f"👁️ لشخص ارتفاع عينيه {eye_height} متر، المسافة إلى الأفق ≈ {horizon_km:.2f} كم ({horizon_miles:.2f} ميل).")
    ])
    return result_text, horizon_text

if __name__ == '__main__':
    app.run(debug=True)
