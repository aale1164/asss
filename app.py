# -*- coding: utf-8 -*-
# تطبيق Dash - شاشة مقسمة:
# اليسار: صورة بحجم كامل
# اليمين: أعلى (تعليمات) + أسفل (حاسبة) - حجمه 50% من عرضه الأصلي

import dash
from dash import html, dcc, Input, Output
import math

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
        # القسم الأيسر: الصورة (يأخذ المساحة المتبقية)
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
                    src='/ASdddd112.jpg',  # استخدم المسار الصحيح
                    style={
                        'width': '100%',
                        'height': '100%',
                        'objectFit': 'cover',
                    }
                )
            ]
        ),
        # القسم الأيمن: تم تصغير عرضه إلى 50% من المساحة الأصلية
        html.Div(
            style={
                'width': '25%',            # جعل العرض 25% بدلاً من 50% من الشاشة الكاملة (نصف الحجم الأصلي)
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
                # الجزء العلوي: التعليمات (نصف ارتفاع القسم الأيمن)
                html.Div(
                    style={
                        'flex': '1',
                        'backgroundColor': '#1e1e2f',
                        'padding': '10px',
                        'overflowY': 'auto',
                        'borderBottom': '1px solid #333',
                        'fontSize': '0.9rem'
                    },
                    children=[
                        html.H4("📘 تعليمات:", style={'color': '#4CAF50', 'marginTop': '0', 'marginBottom': '8px'}),
                        html.Ul([
                            html.Li("أدخل المسافة (كيلومتر أو ميل)."),
                            html.Li("اضغط على زر 'احسب الانحناء'."),
                            html.Li("ستظهر قيمة الانخفاض الناتج عن انحناء الأرض بالأمتار والأقدام."),
                            html.Li("القيمة النظرية لا تأخذ في الاعتبار الانكسار الجوي."),
                            html.Li("يمكنك استخدام التكبير والتدوير بالماوس لرؤية الصورة بشكل أفضل.")
                        ], style={'paddingRight': '15px', 'margin': '0'})
                    ]
                ),
                # الجزء السفلي: حاسبة الانحناء (نصف ارتفاع القسم الأيمن)
                html.Div(
                    style={
                        'flex': '1',
                        'backgroundColor': '#0d0d1a',
                        'padding': '10px',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'overflowY': 'auto'
                    },
                    children=[
                        html.H3("🌍 حاسبة انحناء الأرض", style={'textAlign': 'center', 'fontSize': '1.2rem', 'marginBottom': '10px'}),
                        html.Label("أدخل المسافة:", style={'fontSize': '0.9rem'}),
                        dcc.Input(
                            id='distance-input',
                            type='number',
                            value=10,
                            step=0.1,
                            style={
                                'width': '80%',
                                'padding': '6px',
                                'fontSize': '0.9rem',
                                'margin': '5px 0',
                                'borderRadius': '6px',
                                'border': 'none',
                                'backgroundColor': '#2a2a3a',
                                'color': 'white',
                                'textAlign': 'center'
                            }
                        ),
                        html.Label("الوحدة:", style={'fontSize': '0.9rem', 'marginTop': '5px'}),
                        dcc.RadioItems(
                            id='unit-selector',
                            options=[
                                {'label': ' كيلومتر (km)', 'value': 'km'},
                                {'label': ' ميل (mile)', 'value': 'mile'}
                            ],
                            value='km',
                            labelStyle={'display': 'inline-block', 'margin': '5px', 'fontSize': '0.8rem'},
                            style={'textAlign': 'center'}
                        ),
                        html.Button("احسب الانحناء", id='calc-button', n_clicks=0,
                                    style={
                                        'backgroundColor': '#4CAF50',
                                        'color': 'white',
                                        'padding': '6px 12px',
                                        'fontSize': '0.9rem',
                                        'border': 'none',
                                        'borderRadius': '6px',
                                        'cursor': 'pointer',
                                        'margin': '10px 0',
                                        'width': '70%'
                                    }),
                        html.Div(id='result-container',
                                 style={
                                     'backgroundColor': '#1e1e2f',
                                     'padding': '8px',
                                     'borderRadius': '8px',
                                     'width': '90%',
                                     'textAlign': 'center',
                                     'border': '1px solid #444',
                                     'marginTop': '5px',
                                     'fontSize': '0.8rem'
                                 }),
                        html.Div(id='horizon-container',
                                 style={'marginTop': '8px', 'fontSize': '0.7rem', 'color': '#aaa', 'textAlign': 'center'})
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
        html.P(f"المسافة: {distance:.2f} {unit_name}", style={'margin': '0 0 5px 0', 'fontWeight': 'bold'}),
        html.P("📉 مقدار الانحناء (الانخفاض):", style={'margin': '2px'}),
        html.H4(f"{drop_m:.2f} متر", style={'color': '#ffaa00', 'margin': '2px'}),
        html.P(f"أي ما يعادل {drop_ft:.2f} قدم", style={'fontSize': '0.7rem', 'margin': '2px'}),
        html.Hr(style={'margin': '5px 0'}),
        html.P("ملاحظة: الحساب النظري يهمل الانكسار الجوي.", style={'fontSize': '0.6rem', 'margin': '2px'})
    ])
    
    eye_height = 1.7
    horizon_km = horizon_distance(eye_height)
    horizon_miles = horizon_km * 0.621371
    horizon_text = html.Div([
        html.P(f"👁️ مسافة الأفق (ارتفاع {eye_height} م) ≈ {horizon_km:.2f} كم ({horizon_miles:.2f} ميل)", style={'margin': '0'})
    ])
    return result_text, horizon_text

if __name__ == '__main__':
    app.run(debug=True)
