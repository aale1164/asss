# -*- coding: utf-8 -*-
import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import numpy as np
import math

app = dash.Dash(__name__)
server = app.server

R_KM = 6371.0

def curvature_drop_m(distance_km):
    return (distance_km ** 2) / (2 * R_KM) * 1000

def horizon_dip_deg(altitude_km):
    if altitude_km <= 0:
        return 0.0
    cos_theta = R_KM / (R_KM + altitude_km)
    if cos_theta > 1:
        cos_theta = 1
    elif cos_theta < -1:
        cos_theta = -1
    dip_rad = np.arccos(cos_theta)
    return np.degrees(dip_rad)

def create_figure(model, obj_h, eye_h, dist, zoom, alt):
    max_dist = max(dist * 2, 10)
    distances = np.linspace(0.1, max_dist, 200)
    fig = go.Figure()
    fig.add_hline(y=0, line_width=2, line_color="lime", line_dash="dash", annotation_text="مستوى العين")
    
    if model == 'flat':
        angular = obj_h / (distances * 1000)
        top = angular * (eye_h + obj_h/2)
        bottom = angular * (eye_h - obj_h/2)
        vanish_deg = 0.02
        vanish_km = obj_h / (2 * math.tan(math.radians(vanish_deg))) / 1000
        top[distances > vanish_km] = 0
        bottom[distances > vanish_km] = 0
        fig.add_trace(go.Scatter(x=distances, y=top, mode='lines', line=dict(color='cyan', width=2), name='القمة'))
        fig.add_trace(go.Scatter(x=distances, y=bottom, mode='lines', line=dict(color='red', width=2), name='القاعدة', fill='tonexty'))
        cur_top = (obj_h / (dist * 1000)) * (eye_h + obj_h/2) * (1+zoom)
        cur_bottom = (obj_h / (dist * 1000)) * (eye_h - obj_h/2) * (1+zoom)
        if dist > vanish_km:
            cur_top = cur_bottom = 0
        fig.add_trace(go.Scatter(x=[dist], y=[cur_top], mode='markers', marker=dict(size=10, color='cyan'), name='القمة الحالية'))
        fig.add_trace(go.Scatter(x=[dist], y=[cur_bottom], mode='markers', marker=dict(size=10, color='red'), name='القاعدة الحالية'))
        fig.add_vline(x=vanish_km, line_dash="dot", line_color="gray", annotation_text=f"نقطة التلاشي {vanish_km:.1f} كم")
        title = "نموذج الأرض المسطحة - المنظور الخطي"
    else:
        drop = curvature_drop_m(distances)
        visible = np.maximum(0, obj_h - drop)
        fig.add_trace(go.Scatter(x=distances, y=visible, mode='lines', line=dict(color='orange', width=3), name='الارتفاع المرئي', fill='tozeroy'))
        cur_visible = max(0, (obj_h - curvature_drop_m(dist)) * (1+zoom))
        fig.add_trace(go.Scatter(x=[dist], y=[cur_visible], mode='markers', marker=dict(size=12, color='red'), name='الجسم الحالي'))
        dip = horizon_dip_deg(alt)
        fig.add_hline(y=-dip, line_width=3, line_color="blue", line_dash="dot", annotation_text=f"الأفق الكروي (انخفاض {dip:.2f}°)")
        title = "نموذج الأرض الكروية - الانحناء والأفق"
    
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(color='white', size=16)),
        xaxis=dict(title="المسافة (كم)", range=[0, max_dist], gridcolor='#444', color='white'),
        yaxis=dict(title="الارتفاع المرئي (م)", gridcolor='#444', color='white'),
        plot_bgcolor='black', paper_bgcolor='black',
        legend=dict(font=dict(color='white'), bgcolor='rgba(0,0,0,0.6)'),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

app.layout = html.Div([
    # CSS قوي وحاسم لتغيير ألوان أرقام الشرائح إلى الأسود مع خلفية فاتحة
    html.Style('''
        /* العنصر الذي يحتوي على رقم العلامة */
        .rc-slider-mark-text {
            color: black !important;
            font-size: 12px !important;
            font-weight: bold !important;
            background-color: #e0e0e0 !important;  /* خلفية رمادية فاتحة لضمان التباين */
            padding: 2px 5px !important;
            border-radius: 4px !important;
            border: 1px solid #aaa !important;
            white-space: nowrap !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
        }
        /* إزالة أي خلفية بيضاء افتراضية */
        .rc-slider-mark {
            background-color: transparent !important;
        }
        /* نافذة القيمة المنبثقة */
        .rc-slider-tooltip-inner {
            background-color: #333 !important;
            color: white !important;
            font-weight: bold !important;
        }
        /* باقي عناصر الشريط */
        .rc-slider-dot { border-color: #aaa !important; }
        .rc-slider-handle { border-color: #4CAF50 !important; background-color: #4CAF50 !important; }
        .rc-slider-track { background-color: #4CAF50 !important; }
        .rc-slider-rail { background-color: #555 !important; }
        label, .control-label { color: white !important; font-weight: bold !important; }
        .Select-control, .Select-menu-outer { background-color: #222 !important; color: white !important; }
        .Select-value-label { color: white !important; }
        .Select-option { background-color: #222 !important; color: white !important; }
        .Select-option.is-focused { background-color: #4CAF50 !important; }
    '''),
    html.Div(
        style={'display': 'flex', 'flexDirection': 'row', 'height': '100vh', 'padding': '20px', 'gap': '20px', 'backgroundColor': '#000', 'color': 'white'},
        children=[
            html.Div(
                style={'flex': '1', 'backgroundColor': '#111', 'borderRadius': '12px', 'padding': '15px', 'overflowY': 'auto'},
                children=[
                    html.H2("لوحة التحكم", style={'textAlign': 'center'}),
                    html.Hr(),
                    html.Label("نموذج المحاكاة:"),
                    dcc.Dropdown(id='model', options=[{'label':' أرض مسطحة','value':'flat'},{'label':' أرض كروية','value':'curved'}], value='flat', clearable=False),
                    html.Label("ارتفاع الجسم (م):"),
                    dcc.Slider(id='obj', min=1, max=100, step=1, value=50, marks={1:'1',25:'25',50:'50',75:'75',100:'100'}),
                    html.Label("ارتفاع العين (م):"),
                    dcc.Slider(id='eye', min=0.1, max=10, step=0.1, value=1.7, marks={0.1:'0.1',2:'2',5:'5',8:'8',10:'10'}),
                    html.Label("المسافة (كم):"),
                    dcc.Slider(id='dist', min=1, max=100, step=1, value=20, marks={1:'1',25:'25',50:'50',75:'75',100:'100'}),
                    html.Label("عامل التكبير:"),
                    dcc.Slider(id='zoom', min=0, max=5, step=0.2, value=0, marks={0:'0',1:'1',2:'2',3:'3',4:'4',5:'5'}),
                    html.Label("الارتفاع الحالي (كم):"),
                    dcc.Slider(id='alt', min=0, max=50, step=0.5, value=10, marks={0:'0',10:'10',20:'20',30:'30',40:'40',50:'50'}),
                    html.Div(id='info', style={'marginTop':'20px','backgroundColor':'#1e1e2f','padding':'10px','borderRadius':'8px'})
                ]
            ),
            html.Div(style={'flex': '2', 'backgroundColor': '#0d0d1a', 'borderRadius': '12px', 'padding': '10px'}, children=[dcc.Graph(id='graph', style={'height':'85vh'})])
        ]
    )
])

@app.callback(
    [Output('graph', 'figure'), Output('info', 'children')],
    [Input('model', 'value'), Input('obj', 'value'), Input('eye', 'value'), Input('dist', 'value'), Input('zoom', 'value'), Input('alt', 'value')]
)
def update(model, obj, eye, dist, zoom, alt):
    obj = obj or 50
    eye = eye or 1.7
    dist = dist or 20
    zoom = zoom or 0
    alt = alt or 10
    fig = create_figure(model, obj, eye, dist, zoom, alt)
    info = html.Div([
        html.P(f"الانخفاض لـ {dist} كم = {curvature_drop_m(dist):.2f} متر"),
        html.P(f"الأفق (عين {eye} م) = {math.sqrt(2*R_KM*(eye/1000)):.2f} كم"),
        html.P(f"زاوية الأفق عند {alt} كم = {horizon_dip_deg(alt):.2f}°")
    ])
    return fig, info
