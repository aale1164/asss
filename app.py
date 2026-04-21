# -*- coding: utf-8 -*-
# تطبيق Dash - شاشة مقسمة:
# اليسار: صورة بحجم القسم بالكامل (بدون أي حواجز)
# اليمين: تعليمات + حاسبة انحناء الأرض

import dash
from dash import html, dcc, Input, Output
import math

app = dash.Dash(__name__)
server = app.server

# ثوابت انحناء الأرض
R_km = 6371.0

def curvature_drop(distance_km):
    if distance_km < 0:
        return 0.0
    return (distance_km ** 2) / (2 * R_km) * 1000

def horizon_distance(observer_height_m):
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
        # القسم الأيسر: الصورة فقط (تملأ القسم بالكامل)
        html.Div(
            style={
                'flex': '1',
                'backgroundColor': 'black',  # خلفية سوداء في حال الصورة لا تغطي كل شيء
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '0',
                'margin': '0',
                'overflow': 'hidden'  # لمنع أي تمرير غير مرغوب
            },
            children=[
                html.Img(
                    src='/ASdddd112.jpg',   # الصورة في جذر المشروع (أو استخدم الرابط المباشر)
                    style={
                        'width': '100%',      # تغطي كامل عرض القسم
                        'height': '100%',     # تغطي كامل ارتفاع القسم
                        'objectFit': 'cover',  # تغطي المساحة بدون تشويه (قد تقص أطراف الصورة)
                        # إذا أردت رؤية الصورة كاملة بدون قص استخدم 'contain' بدل 'cover'
                        # ولكن قد تظهر خلفية سوداء على الجوانب
                    }
                )
            ]
        ),
        # القسم الأيمن: تعليمات + حاسبة الانحناء
        html.Div(
            style={
                'flex': '1',
                'backgroundColor': '#0d0d1a',
                'color': 'white',
                'padding': '20px',
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'flex-start',  # محاذاة من الأعلى
                'alignItems': 'center',
                'overflowY': 'auto',
                'fontFamily': 'Arial, sans-serif'
            },
            children=[
                # صندوق التعليمات
                html.Div(
                    style={
                        'backgroundColor': '#1e1e2f',
                        'padding': '15px',
                        'borderRadius': '10px',
                        'marginBottom': '25px',
                        'width': '90%',
                        'textAlign': 'right',
                        'borderRight': '4px solid #4CAF50'
                    },
                    children=[
                        html.H3("📘 تعليمات:", style={'margin': '0 0 10px 0', 'color': '#4CAF50'}),
                        html.Ul([
                            html.Li("أدخل المسافة (بالكيلومتر أو الميل)."),
                            html.Li("اضغط على زر 'احسب الانحناء'."),
                            html.Li("ستظهر قيمة الانخفاض الناتج عن انحناء الأرض بالأمتار والأقدام."),
                            html.Li("القيمة النظرية لا تأخذ في الاعتبار الانكسار الجوي."),
                            html.Li("يمكنك استخدام زر التكبير والتدوير بالماوس لرؤية الصورة بشكل أفضل.")
                        ], style={'margin': '0', 'paddingRight': '20px'})
                    ]
                ),
                # حاسبة الانحناء
                html.H1("🌍 حاسبة انحناء الأرض", style={'textAlign': 'center', 'marginBottom': '20px'}),
                html.Hr(style={'width': '80%', 'borderColor': '#444'}),
                html.Label("أدخل المسافة:", style={'fontSize': '18px', 'marginTop': '10px'}),
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
                             'marginTop': '10px',
                             'textAlign': 'center',
                             'border': '1px solid #444'
                         }),
                html.Div(id='horizon-container',
                         style={'marginTop': '20px', 'fontSize': '14px', 'color': '#aaa', 'textAlign': 'center'})
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
