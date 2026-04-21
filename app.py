# -*- coding: utf-8 -*-
# تطبيق Dash متكامل: المحاكي الموحد للأرض (المنظور الخطي + الانحناء الكروي)
# يجمع أفضل ميزات الكودين السابقين مع إمكانية النشر على Render

import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import numpy as np
import math

app = dash.Dash(__name__)
server = app.server

# --- الثوابت والدوال الحسابية ---
R_KM = 6371.0

def curvature_drop_m(distance_km):
    """الانخفاض الهندسي (بالمتر) لمسافة معينة (نموذج كروي)"""
    return (distance_km ** 2) / (2 * R_KM) * 1000

def horizon_distance_km(observer_height_m):
    """مسافة الأفق بالكيلومترات لراصد ارتفاعه بالأمتار"""
    return math.sqrt(2 * R_KM * (observer_height_m / 1000))

def horizon_dip_deg(altitude_km):
    """زاوية انخفاض الأفق (بالدرجات) عند ارتفاع معين فوق سطح الأرض"""
    if altitude_km <= 0:
        return 0.0
    cos_theta = R_KM / (R_KM + altitude_km)
    if cos_theta > 1:
        cos_theta = 1
    elif cos_theta < -1:
        cos_theta = -1
    dip_rad = np.arccos(cos_theta)
    return np.degrees(dip_rad)

# --- دالة إنشاء الرسم البياني حسب النموذج المختار ---
def create_figure(model, obj_height, eye_height, distance_km, zoom, altitude_km):
    """
    model: 'flat' (المنظور الخطي) أو 'curved' (النموذج الكروي)
    """
    max_dist_km = max(distance_km * 2, 10)
    distances = np.linspace(0.1, max_dist_km, 200)
    fig = go.Figure()
    
    # --- مستوى العين الهندسي المرجعي (y=0) ---
    fig.add_hline(y=0, line_width=2, line_color="lime", line_dash="dash",
                  annotation_text="مستوى العين", annotation_position="bottom right")
    
    if model == 'flat':
        # ---------- نموذج المنظور الخطي (سطح مستوٍ) ----------
        # الزاوية الرأسية للجسم (تقريب)
        angular_size = obj_height / (distances * 1000)  # راديان
        # إحداثيات قمة وقاعدة الجسم (مركزه عند مستوى العين)
        top_y = angular_size * (eye_height + obj_height/2)
        bottom_y = angular_size * (eye_height - obj_height/2)
        
        # نقطة التلاشي (حيث تصبح الزاوية أقل من حد الرؤية ~0.02°)
        vanishing_angle_deg = 0.02
        vanishing_dist_km = obj_height / (2 * math.tan(math.radians(vanishing_angle_deg))) / 1000
        
        # إخفاء الجسم بعد نقطة التلاشي
        mask = distances > vanishing_dist_km
        top_y[mask] = 0
        bottom_y[mask] = 0
        
        # رسم منطقة الجسم
        fig.add_trace(go.Scatter(x=distances, y=top_y, mode='lines',
                                 line=dict(color='cyan', width=2), name='قمة الجسم (مسطح)'))
        fig.add_trace(go.Scatter(x=distances, y=bottom_y, mode='lines',
                                 line=dict(color='red', width=2), name='قاعدة الجسم (مسطح)',
                                 fill='tonexty'))
        # موقع الجسم الحالي مع الزوم
        curr_top = (obj_height / (distance_km * 1000)) * (eye_height + obj_height/2) * (1+zoom)
        curr_bottom = (obj_height / (distance_km * 1000)) * (eye_height - obj_height/2) * (1+zoom)
        if distance_km > vanishing_dist_km:
            curr_top = curr_bottom = 0
        fig.add_trace(go.Scatter(x=[distance_km], y=[curr_top], mode='markers',
                                 marker=dict(size=10, color='cyan'), name='القمة الحالية'))
        fig.add_trace(go.Scatter(x=[distance_km], y=[curr_bottom], mode='markers',
                                 marker=dict(size=10, color='red'), name='القاعدة الحالية'))
        # الأفق المسطح (عند y=0)
        fig.add_hline(y=0, line_width=3, line_color="white", name='الأفق (مسطح)')
        # نقطة التلاشي
        fig.add_vline(x=vanishing_dist_km, line_dash="dot", line_color="gray",
                      annotation_text=f"نقطة التلاشي ≈ {vanishing_dist_km:.1f} كم",
                      annotation_position="top right")
        title = f"🌍 نموذج الأرض المسطحة - المنظور الخطي (جسم {obj_height} م، عين {eye_height} م)"
    
    else:  # model == 'curved'
        # ---------- نموذج الأرض الكروية (الانحناء والأفق المنخفض) ----------
        drop = curvature_drop_m(distances)          # الانخفاض بالمتر
        visible_height = np.maximum(0, obj_height - drop)
        fig.add_trace(go.Scatter(x=distances, y=visible_height, mode='lines',
                                 line=dict(color='orange', width=3), name='الارتفاع المرئي (كروي)',
                                 fill='tozeroy'))
        # الجسم الحالي مع الزوم
        current_drop = curvature_drop_m(distance_km)
        curr_visible = max(0, (obj_height - current_drop) * (1+zoom))
        fig.add_trace(go.Scatter(x=[distance_km], y=[curr_visible], mode='markers',
                                 marker=dict(size=12, color='red'), name='الجسم الحالي'))
        # الأفق الكروي المنخفض (بزاوية dip)
        dip_deg = horizon_dip_deg(altitude_km)
        horizon_y = -dip_deg   # تمثيل الزاوية على محور y
        fig.add_hline(y=horizon_y, line_width=3, line_color="blue", line_dash="dot",
                      annotation_text=f"الأفق الكروي (انخفاض {dip_deg:.2f}°)", annotation_position="bottom right")
        title = f"🌍 نموذج الأرض الكروية - الانحناء والأفق (ارتفاع {altitude_km} كم)"
    
    # --- تنسيق عام للشكل ---
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(color='white', size=16)),
        xaxis=dict(title="المسافة (كم)", range=[0, max_dist_km], gridcolor='#444', color='white'),
        yaxis=dict(title="الارتفاع المرئي / الزاوية (م)", gridcolor='#444', color='white'),
        plot_bgcolor='black',
        paper_bgcolor='black',
        legend=dict(font=dict(color='white'), bgcolor='rgba(0,0,0,0.6)'),
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode='closest'
    )
    return fig

# --- واجهة المستخدم ---
app.layout = html.Div(
    style={
        'display': 'flex',
        'flexDirection': 'row',
        'height': '100vh',
        'width': '100vw',
        'backgroundColor': '#000',
        'fontFamily': 'Arial, sans-serif',
        'color': 'white',
        'padding': '20px',
        'gap': '20px'
    },
    children=[
        # العمود الأيمن: أدوات التحكم
        html.Div(
            style={'flex': '1', 'backgroundColor': '#111', 'borderRadius': '12px', 'padding': '15px', 'overflowY': 'auto'},
            children=[
                html.H2("🎛️ لوحة التحكم", style={'textAlign': 'center'}),
                html.Hr(),
                html.Label("نموذج المحاكاة:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='model-select',
                    options=[
                        {'label': ' المنظور الخطي (أرض مسطحة)', 'value': 'flat'},
                        {'label': ' الانحناء الكروي (أرض كروية)', 'value': 'curved'}
                    ],
                    value='flat',
                    clearable=False,
                    style={'backgroundColor': '#222', 'color': 'black', 'marginBottom': '15px'}
                ),
                html.Label("ارتفاع الجسم (متر):", style={'fontWeight': 'bold'}),
                dcc.Slider(id='obj-height', min=1, max=100, step=1, value=50,
                           marks={i: str(i) for i in [1, 50, 100]}, tooltip={"placement": "bottom"}),
                html.Label("ارتفاع العين (متر):", style={'fontWeight': 'bold'}),
                dcc.Slider(id='eye-height', min=0.1, max=10, step=0.1, value=1.7,
                           marks={i: str(i) for i in [0.1, 5, 10]}, tooltip={"placement": "bottom"}),
                html.Label("المسافة (كم):", style={'fontWeight': 'bold'}),
                dcc.Slider(id='distance', min=1, max=100, step=1, value=20,
                           marks={i: str(i) for i in [1, 50, 100]}, tooltip={"placement": "bottom"}),
                html.Label("عامل التكبير (الزوم):", style={'fontWeight': 'bold'}),
                dcc.Slider(id='zoom', min=0, max=5, step=0.2, value=0,
                           marks={i: str(i) for i in [0, 2, 5]}, tooltip={"placement": "bottom"}),
                html.Label("الارتفاع الحالي (كم) – يؤثر على الأفق الكروي:", style={'fontWeight': 'bold'}),
                dcc.Slider(id='altitude', min=0, max=50, step=0.5, value=10,
                           marks={i: str(i) for i in [0, 25, 50]}, tooltip={"placement": "bottom"}),
                html.Div(id='info-panel', style={'marginTop': '20px', 'backgroundColor': '#1e1e2f', 'padding': '10px', 'borderRadius': '8px'})
            ]
        ),
        # العمود الأيسر: الرسم البياني
        html.Div(
            style={'flex': '2', 'backgroundColor': '#0d0d1a', 'borderRadius': '12px', 'padding': '10px'},
            children=[
                dcc.Graph(id='main-graph', config={'displayModeBar': True}, style={'height': '90vh'})
            ]
        )
    ]
)

# --- تحديث الرسم البياني ولوحة المعلومات ---
@app.callback(
    [Output('main-graph', 'figure'),
     Output('info-panel', 'children')],
    [Input('model-select', 'value'),
     Input('obj-height', 'value'),
     Input('eye-height', 'value'),
     Input('distance', 'value'),
     Input('zoom', 'value'),
     Input('altitude', 'value')]
)
def update_app(model, obj_h, eye_h, dist, zoom, alt):
    # إنشاء الشكل
    fig = create_figure(model, obj_h, eye_h, dist, zoom, alt)
    # لوحة معلومات إضافية
    drop_km = curvature_drop_m(dist)
    horizon_km = horizon_distance_km(eye_h)
    info = html.Div([
        html.H5("📊 معلومات مرجعية:", style={'margin': '0 0 5px 0'}),
        html.P(f"• الانخفاض الهندسي لمسافة {dist} كم ≈ {drop_km:.2f} متر (في النموذج الكروي).", style={'fontSize': 12}),
        html.P(f"• مسافة الأفق لارتفاع العين {eye_h} م ≈ {horizon_km:.2f} كم.", style={'fontSize': 12}),
        html.P(f"• زاوية انخفاض الأفق عند ارتفاع {alt} كم ≈ {horizon_dip_deg(alt):.2f} درجة.", style={'fontSize': 12})
    ])
    return fig, info

if __name__ == '__main__':
    app.run(debug=True)
