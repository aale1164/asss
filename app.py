# -*- coding: utf-8 -*-
# تطبيق Dash - 6 مربعات متساوية
# المربعات: 1 تعليمات، 2 حاسبة انحناء، 3 رسم بياني للانحناء، 4 فارغ،
# 5 محاكاة المنظور الخطي، 6 محاكاة مستوى الأفق

import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import math
import numpy as np

app = dash.Dash(__name__)
server = app.server

# ---- ثوابت انحناء الأرض ----
R_KM = 6371.0

def curvature_drop(distance_km):
    if distance_km < 0:
        return 0.0
    return (distance_km ** 2) / (2 * R_KM) * 1000

def create_curvature_graph(distance_km, drop_m):
    max_dist = max(distance_km, 1)
    distances = [i * 0.5 for i in range(int(max_dist * 2) + 1)]
    drops = [curvature_drop(d) for d in distances]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=distances, y=drops, mode='lines+markers',
                             name='الانحناء النظري',
                             line=dict(color='#4CAF50', width=2),
                             marker=dict(size=3)))
    fig.add_vline(x=distance_km, line_dash="dash", line_color="red",
                  annotation_text=f"{distance_km:.1f} كم", annotation_position="top right")
    fig.add_hline(y=drop_m, line_dash="dash", line_color="orange",
                  annotation_text=f"{drop_m:.2f} م", annotation_position="bottom right")
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=5, r=5, t=30, b=5),
        font=dict(color='white', size=8),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=7)),
        xaxis_title="كم", yaxis_title="متر",
        title="منحنى الانحناء", title_font_size=10
    )
    return fig

# ---- دوال للمربع 5 (المنظور الخطي) ----
def perspective_simulation(distance_km, object_height_m, model):
    # model: 'flat' or 'curved'
    distances = np.linspace(0.1, max(distance_km, 1)*2, 100)
    if model == 'flat':
        # المنظور الخطي: الارتفاع الظاهري يتناسب عكسياً مع المسافة
        apparent_height = object_height_m / (distances * 1000)  # تبسيط
        # نقطة التلاشي عند 0
        vanishing_dist = object_height_m / (2 * math.tan(math.radians(0.02))) / 1000
        title = "نموذج الأرض المسطحة: المنظور الخطي"
        color = 'cyan'
    else:
        # نموذج كروي: الانخفاض بسبب الانحناء
        drop_curvature = (distances**2) / (2 * R_KM) * 1000
        apparent_height = np.maximum(0, object_height_m - drop_curvature)
        title = "نموذج الأرض الكروية: الانحناء"
        color = 'orange'
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=distances, y=apparent_height, mode='lines',
                             line=dict(color=color, width=2), name='الارتفاع المرئي (م)'))
    # موقع الجسم الحالي
    if model == 'flat':
        curr_height = object_height_m / (distance_km * 1000)
        curr_height = max(0, curr_height)
    else:
        curr_height = max(0, object_height_m - (distance_km**2)/(2*R_KM)*1000)
    fig.add_trace(go.Scatter(x=[distance_km], y=[curr_height], mode='markers',
                             marker=dict(size=8, color='red'), name='الجسم الحالي'))
    fig.update_layout(
        template="plotly_dark", margin=dict(l=5, r=5, t=35, b=5),
        font=dict(color='white', size=8),
        xaxis_title="المسافة (كم)", yaxis_title="الارتفاع المرئي (م)",
        title=title, title_font_size=10,
        height=200, width=None
    )
    return fig

# ---- دالة للمربع 6 (مستوى الأفق) ----
def horizon_simulation(altitude_km):
    R = 6371
    # زاوية انخفاض الأفق (dip angle) بالدرجات
    if altitude_km <= 0:
        dip_deg = 0
    else:
        dip_rad = math.acos(R / (R + altitude_km))
        dip_deg = math.degrees(dip_rad)
    # رسم خط الأفق للنموذجين
    fig = go.Figure()
    # الأفق المسطح: ثابت عند 0
    fig.add_trace(go.Scatter(x=[0, 10], y=[0, 0], mode='lines',
                             line=dict(color='white', width=3), name='أفق الأرض المسطحة'))
    # الأفق الكروي: منخفض بمقدار dip_deg
    fig.add_trace(go.Scatter(x=[0, 10], y=[-dip_deg, -dip_deg], mode='lines',
                             line=dict(color='lightblue', width=3, dash='dot'), name='أفق الأرض الكروية'))
    # إضافة نص توضيحي
    fig.add_annotation(x=8, y=-dip_deg+0.1, text=f"انخفاض {dip_deg:.2f}°", showarrow=False,
                       font=dict(size=8, color='lightblue'), bgcolor='rgba(0,0,0,0.6)')
    fig.update_layout(
        template="plotly_dark", margin=dict(l=5, r=5, t=30, b=5),
        font=dict(color='white', size=8),
        xaxis=dict(visible=False, range=[0,10]), yaxis_title="الزاوية (درجة)",
        title=f"مقارنة مستوى الأفق (ارتفاع {altitude_km} كم)", title_font_size=10,
        height=200, width=None
    )
    return fig

# ---- التصميم العام ----
common_style = {'position': 'relative', 'padding': '8px', 'overflow': 'auto', 'display': 'flex', 'flexDirection': 'column'}

app.layout = html.Div(
    style={
        'display': 'grid',
        'gridTemplateRows': '1fr 1fr',
        'gridTemplateColumns': '1fr 1fr 1fr',
        'height': '100vh',
        'width': '100vw',
        'gap': '2px',
        'backgroundColor': '#000',
        'margin': '0',
        'padding': '0',
        'direction': 'rtl'
    },
    children=[
        # ---- الصف العلوي ----
        # مربع 3: تعليمات
        html.Div(
            style={**common_style, 'backgroundColor': '#1e1e2f', 'textAlign': 'right'},
            children=[
                html.Div("3", style={'position': 'absolute', 'top': 5, 'right': 8, 'color': '#aaa', 'fontSize': 16}),
                html.H5("📘 تعليمات:", style={'color': 'white', 'marginTop': 25, 'fontSize': 14}),
                html.Ul([
                    html.Li("أدخل المسافة واضغط احسب.", style={'fontSize': 12}),
                    html.Li("الرسم البياني يوضح الانحناء.", style={'fontSize': 12}),
                    html.Li("المربعان 5 و6 تفاعليان.", style={'fontSize': 12}),
                ], style={'paddingRight': '15px'})
            ]
        ),
        # مربع 2: حاسبة الانحناء
        html.Div(
            style={**common_style, 'backgroundColor': '#0d0d1a', 'textAlign': 'right', 'justifyContent': 'center'},
            children=[
                html.Div("2", style={'position': 'absolute', 'top': 5, 'right': 8, 'color': '#aaa', 'fontSize': 16}),
                html.H6("🌍 حاسبة الانحناء", style={'textAlign': 'center', 'color': 'white', 'margin': '5px 0', 'fontSize': 14}),
                html.Label("المسافة:", style={'fontSize': 10}),
                dcc.Input(id='dist-input', type='number', value=10, step=0.5, style={'width': '85%', 'padding': '3px', 'fontSize': 10, 'margin': '3px 0', 'backgroundColor': '#2a2a3a', 'color': 'white', 'border': 'none', 'borderRadius': '3px'}),
                html.Label("الوحدة:", style={'fontSize': 10}),
                dcc.RadioItems(id='unit-select', options=[{'label':' كم','value':'km'},{'label':' ميل','value':'mile'}], value='km', labelStyle={'display':'inline-block','margin':'3px','fontSize':9}),
                html.Button("احسب", id='calc-btn', n_clicks=0, style={'backgroundColor':'#4CAF50','color':'white','padding':'2px 8px','fontSize':10,'margin':'5px 0','border':'none','borderRadius':'3px','cursor':'pointer'}),
                html.Div(id='res-div', style={'backgroundColor':'#1e1e2f','padding':'4px','borderRadius':'4px','marginTop':'5px','fontSize':10,'color':'white','textAlign':'center'})
            ]
        ),
        # مربع 1: رسم بياني الانحناء
        html.Div(
            style={**common_style, 'backgroundColor': '#0d0d1a', 'padding': '3px'},
            children=[
                html.Div("1", style={'position': 'absolute', 'top': 5, 'right': 8, 'color': '#aaa', 'fontSize': 16}),
                dcc.Graph(id='curvature-graph', config={'displayModeBar': False}, style={'height': '95%', 'width': '100%'})
            ]
        ),
        # ---- الصف السفلي ----
        # مربع 6 (كان 4 سابقاً، الآن رقم 6): محاكاة مستوى الأفق
        html.Div(
            style={**common_style, 'backgroundColor': '#111', 'textAlign': 'right'},
            children=[
                html.Div("6", style={'position': 'absolute', 'top': 5, 'right': 8, 'color': '#aaa', 'fontSize': 16}),
                html.P("📐 مستوى الأفق", style={'textAlign': 'center', 'fontSize': 12, 'margin': '0 0 5px 0'}),
                html.Label("الارتفاع (كم):", style={'fontSize': 9}),
                dcc.Slider(id='altitude-slider', min=0, max=20, step=0.5, value=10,
                           marks={i: str(i) for i in range(0,21,5)}, tooltip={"placement": "bottom", "always_visible": False}),
                dcc.Graph(id='horizon-graph', config={'displayModeBar': False}, style={'height': '150px', 'width': '100%'}),
                html.Div("توضيح: الأفق المسطح ثابت، الكروي ينخفض مع الارتفاع.", style={'fontSize': 8, 'color': '#aaa', 'textAlign': 'center', 'marginTop': '4px'})
            ]
        ),
        # مربع 5: محاكاة المنظور الخطي
        html.Div(
            style={**common_style, 'backgroundColor': '#111', 'textAlign': 'right'},
            children=[
                html.Div("5", style={'position': 'absolute', 'top': 5, 'right': 8, 'color': '#aaa', 'fontSize': 16}),
                html.P("👁️ المنظور الخطي", style={'textAlign': 'center', 'fontSize': 12, 'margin': '0 0 5px 0'}),
                html.Label("المسافة (كم):", style={'fontSize': 9}),
                dcc.Slider(id='persp-distance', min=1, max=100, step=1, value=20,
                           marks={i: str(i) for i in range(0,101,20)}, tooltip={"placement": "bottom"}),
                html.Label("ارتفاع الجسم (م):", style={'fontSize': 9}),
                dcc.Slider(id='object-height', min=1, max=100, step=5, value=50,
                           marks={i: str(i) for i in range(0,101,20)}),
                html.Label("النموذج:", style={'fontSize': 9}),
                dcc.RadioItems(id='persp-model', options=[{'label':'مسطح','value':'flat'},{'label':'كروي','value':'curved'}], value='flat', labelStyle={'display':'inline-block','margin':'3px','fontSize':9}),
                dcc.Graph(id='persp-graph', config={'displayModeBar': False}, style={'height': '140px', 'width': '100%'}),
                html.Div("توضيح: المسافة تؤثر على الارتفاع الظاهري.", style={'fontSize': 8, 'color': '#aaa', 'textAlign': 'center', 'marginTop': '4px'})
            ]
        ),
        # مربع 4 (فارغ) - نضعه أخيراً ليظهر في أقصى اليسار
        html.Div(
            style={**common_style, 'backgroundColor': '#111', 'textAlign': 'right'},
            children=[html.Div("4", style={'position': 'absolute', 'top': 5, 'right': 8, 'color': '#888', 'fontSize': 16})]
        )
    ]
)

# ---- Callbacks ----
# تحديث حاسبة الانحناء والرسم البياني
@app.callback(
    Output('res-div', 'children'),
    Output('curvature-graph', 'figure'),
    Input('calc-btn', 'n_clicks'),
    Input('dist-input', 'value'),
    Input('unit-select', 'value')
)
def update_curvature(n_clicks, dist_val, unit):
    if dist_val is None:
        dist_val = 0
    dist = float(dist_val)
    if unit == 'mile':
        dist_km = dist * 1.60934
        unit_label = 'ميل'
    else:
        dist_km = dist
        unit_label = 'كم'
    drop_m = curvature_drop(dist_km)
    drop_ft = drop_m * 3.28084
    result = html.Div([
        html.P(f"📏 المسافة: {dist:.2f} {unit_label}", style={'margin': '0', 'fontSize': 10}),
        html.P(f"📉 الانخفاض: {drop_m:.2f} م", style={'margin': '0', 'color': '#ffaa00', 'fontSize': 10}),
        html.P(f"≈ {drop_ft:.2f} قدم", style={'margin': '0', 'fontSize': 8})
    ])
    fig = create_curvature_graph(dist_km, drop_m)
    return result, fig

# تحديث المربع 5 (المنظور)
@app.callback(
    Output('persp-graph', 'figure'),
    Input('persp-distance', 'value'),
    Input('object-height', 'value'),
    Input('persp-model', 'value')
)
def update_perspective(distance, obj_height, model):
    if distance is None: distance = 20
    if obj_height is None: obj_height = 50
    fig = perspective_simulation(distance, obj_height, model)
    return fig

# تحديث المربع 6 (مستوى الأفق)
@app.callback(
    Output('horizon-graph', 'figure'),
    Input('altitude-slider', 'value')
)
def update_horizon(altitude):
    if altitude is None: altitude = 10
    fig = horizon_simulation(altitude)
    return fig

if __name__ == '__main__':
    app.run(debug=True)
