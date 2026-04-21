# -*- coding: utf-8 -*-
# صفحة مقسمة إلى 6 مربعات متساوية تمامًا في الحجم
# المربعات: 3 تعليمات، 2 حاسبة انحناء، 1 رسم بياني،
# 6 محاكاة المنظور الخطي، 5 محاكاة مستوى الأفق، 4 فارغ

import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import math
import numpy as np

app = dash.Dash(__name__)
server = app.server

R_KM = 6371.0

# --- دوال حاسبة الانحناء ---
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
                             marker=dict(size=4)))
    fig.add_vline(x=distance_km, line_dash="dash", line_color="red",
                  annotation_text=f"المسافة: {distance_km:.1f} كم",
                  annotation_position="top right")
    fig.add_hline(y=drop_m, line_dash="dash", line_color="orange",
                  annotation_text=f"الانخفاض: {drop_m:.2f} م",
                  annotation_position="bottom right")
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(color='white', size=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9)),
        xaxis_title="المسافة (كم)",
        yaxis_title="الانخفاض (متر)",
        title="منحنى انحناء الأرض"
    )
    return fig

# --- دوال محاكاة المنظور الخطي (للمربع 5) ---
def perspective_simulation(object_height_m, eye_height_m, initial_distance_km, zoom_factor, simulation_model):
    horizon_y = 0
    fig = go.Figure()
    fig.add_hline(y=horizon_y, line_width=2, line_color="black", line_dash="dash", name='مستوى العين')
    
    max_dist_km = max(initial_distance_km * 2, 1)
    distances_km = np.linspace(0.1, max_dist_km, 200)
    
    if simulation_model == "المنظور الخطي (سطح مستوٍ)":
        # حساب الزاوية الرأسية
        angular_sizes_rad = object_height_m / (distances_km * 1000)
        object_top_y = eye_height_m + (object_height_m / 2)
        object_bottom_y = eye_height_m - (object_height_m / 2)
        y_top = angular_sizes_rad * object_top_y
        y_bottom = angular_sizes_rad * object_bottom_y
        
        vanishing_angle_deg = 0.02
        vanishing_dist_km = object_height_m / (2 * np.tan(np.radians(vanishing_angle_deg))) / 1000
        mask = distances_km > vanishing_dist_km
        y_top[mask] = 0
        y_bottom[mask] = 0
        
        fig.add_trace(go.Scatter(x=distances_km, y=y_top, mode='lines', line=dict(color='blue', width=2),
                                 name='قمة الجسم (سطح مستوٍ)', stackgroup='one'))
        fig.add_trace(go.Scatter(x=distances_km, y=y_bottom, mode='lines', line=dict(color='red', width=2),
                                 name='قاعدة الجسم (سطح مستوٍ)', fill='tonexty'))
        
        current_y_top = object_height_m / (initial_distance_km * 1000) * object_top_y * (1 + zoom_factor)
        current_y_bottom = object_height_m / (initial_distance_km * 1000) * object_bottom_y * (1 + zoom_factor)
        if initial_distance_km > vanishing_dist_km:
            current_y_top = 0
            current_y_bottom = 0
        
        fig.add_trace(go.Scatter(x=[initial_distance_km], y=[current_y_top], mode='markers', marker=dict(size=12, color='blue'),
                                 name='موقع القمة الحالي'))
        fig.add_trace(go.Scatter(x=[initial_distance_km], y=[current_y_bottom], mode='markers', marker=dict(size=12, color='red'),
                                 name='موقع القاعدة الحالي'))
        
        vanishing_text = f"نقطة التلاشي: {vanishing_dist_km:.1f} كم (جسم ارتفاعه {object_height_m} م)"
        fig.add_annotation(x=max_dist_km * 0.8, y=0.05, text=vanishing_text, showarrow=False,
                           bgcolor='white', opacity=0.8, font=dict(size=10))
    else:
        drop_m = (distances_km**2) / (2 * 6371) * 1000
        visible_heights_m = object_height_m - drop_m
        visible_heights_m[visible_heights_m < 0] = 0
        fig.add_trace(go.Scatter(x=distances_km, y=visible_heights_m, mode='lines', line=dict(color='blue', width=3),
                                 name='الارتفاع المرئي (سطح منحني)', fill='tozeroy'))
        current_visible_height = object_height_m - (initial_distance_km**2 / (2 * 6371) * 1000)
        current_visible_height = max(0, current_visible_height) * (1 + zoom_factor)
        fig.add_trace(go.Scatter(x=[initial_distance_km], y=[current_visible_height], mode='markers', marker=dict(size=15, color='blue'),
                                 name='الجسم الحالي'))
    
    title_text = f"محاكاة المنظور الخطي: جسم {object_height_m} م، ارتفاع العين {eye_height_m} م، زوم x{1+zoom_factor}"
    fig.update_layout(title=dict(text=title_text, x=0.5, font=dict(size=14, color='white')),
                      xaxis=dict(title="المسافة (كم)", range=[0, max_dist_km], showgrid=True),
                      yaxis=dict(title="الارتفاع المرئي (تقريبي)", range=[-0.05, 0.2], showgrid=True),
                      plot_bgcolor='black', paper_bgcolor='black',
                      legend=dict(font=dict(color='white'), bgcolor='rgba(0,0,0,0.5)'),
                      margin=dict(l=40, r=40, t=50, b=30), height=250)
    return fig

# --- دوال محاكاة مستوى الأفق (للمربع 6) ---
def horizon_simulation(altitude_km, eye_height_m):
    fig = go.Figure()
    fig.add_hline(y=0, line_width=2, line_color="lime", line_dash="dash", name='مستوى العين الهندسي')
    flat_horizon_y = 0
    R_earth_km = 6371
    cos_theta = R_earth_km / (R_earth_km + altitude_km)
    if cos_theta > 1: cos_theta = 1
    elif cos_theta < -1: cos_theta = -1
    dip_angle_rad = np.arccos(cos_theta)
    dip_angle_deg = np.degrees(dip_angle_rad)
    spherical_horizon_y = -dip_angle_deg
    fig.add_trace(go.Scatter(x=[0, 10], y=[flat_horizon_y, flat_horizon_y],
                             mode='lines', line=dict(color='white', width=4),
                             name='الأفق (نموذج مسطح)'))
    fig.add_trace(go.Scatter(x=[0, 10], y=[spherical_horizon_y, spherical_horizon_y],
                             mode='lines', line=dict(color='blue', width=4, dash='dot'),
                             name='الأفق (نموذج كروي)'))
    fig.add_annotation(x=8, y=0.05, text=f"الأفق المسطح: مستوى العين", showarrow=False, bgcolor='white', opacity=0.8)
    if spherical_horizon_y != 0:
        fig.add_annotation(x=8, y=spherical_horizon_y - 0.1, text=f"الأفق الكروي: انخفاض ({dip_angle_deg:.2f}°)",
                           showarrow=False, bgcolor='white', opacity=0.8, font=dict(color='blue'))
    title_text = f"محاكاة مستوى الأفق - الارتفاع: {altitude_km} كم"
    fig.update_layout(title=dict(text=title_text, x=0.5, font=dict(size=14, color='white')),
                      xaxis=dict(visible=False, range=[0, 10]),
                      yaxis=dict(title="الزاوية الرأسية (درجة)", range=[-10, 2], showgrid=True),
                      plot_bgcolor='black', paper_bgcolor='black',
                      legend=dict(font=dict(color='white'), bgcolor='rgba(0,0,0,0.5)'),
                      margin=dict(l=40, r=40, t=50, b=30), height=250)
    return fig

# --- النمط الموحد للمربعات ---
common_style = {
    'position': 'relative',
    'padding': '10px',
    'overflow': 'auto',
    'display': 'flex',
    'flexDirection': 'column'
}

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
        # ---- الصف العلوي (من اليمين إلى اليسار) ----
        # مربع 3: تعليمات
        html.Div(
            style={**common_style, 'backgroundColor': '#1e1e2f', 'textAlign': 'right'},
            children=[
                html.Div("3", style={'position': 'absolute', 'top': 10, 'right': 10, 'color': '#aaa', 'fontSize': 20}),
                html.H4("📘 تعليمات:", style={'color': 'white', 'marginTop': 35, 'textAlign': 'right'}),
                html.Ul([
                    html.Li("أدخل المسافة (كم أو ميل) في المربع 2."),
                    html.Li("اضغط على زر 'احسب' لرؤية الانحناء."),
                    html.Li("استخدم أشرطة التمرير في المربعين 5 و6."),
                    html.Li("الرسوم البيانية تتفاعل تلقائياً.")
                ], style={'color': 'white', 'paddingRight': '20px'})
            ]
        ),
        # مربع 2: حاسبة الانحناء
        html.Div(
            style={**common_style, 'backgroundColor': '#0d0d1a', 'textAlign': 'right', 'justifyContent': 'center'},
            children=[
                html.Div("2", style={'position': 'absolute', 'top': 10, 'right': 10, 'color': '#aaa', 'fontSize': 20}),
                html.H5("🌍 حاسبة الانحناء", style={'textAlign': 'center', 'color': 'white', 'marginTop': 30}),
                html.Label("المسافة:", style={'fontSize': 12, 'color': 'white', 'display': 'block', 'textAlign': 'right'}),
                dcc.Input(id='dist-input', type='number', value=10, step=0.5,
                          style={'width': '90%', 'padding': '5px', 'margin': '5px 0', 'backgroundColor': '#2a2a3a', 'color': 'white', 'border': 'none', 'borderRadius': '4px', 'textAlign': 'right'}),
                html.Label("الوحدة:", style={'fontSize': 12, 'color': 'white', 'display': 'block', 'textAlign': 'right'}),
                dcc.RadioItems(id='unit-select', options=[{'label': ' كيلومتر', 'value': 'km'}, {'label': ' ميل', 'value': 'mile'}],
                               value='km', labelStyle={'display': 'inline-block', 'margin': '5px', 'color': 'white'}),
                html.Button("احسب", id='calc-btn', n_clicks=0,
                            style={'backgroundColor': '#4CAF50', 'color': 'white', 'padding': '5px 12px', 'margin': '10px 0', 'border': 'none', 'borderRadius': '4px', 'cursor': 'pointer'}),
                html.Div(id='res-div', style={'backgroundColor': '#1e1e2f', 'padding': '8px', 'borderRadius': '6px', 'marginTop': '10px', 'fontSize': 12, 'color': 'white', 'textAlign': 'center'})
            ]
        ),
        # مربع 1: رسم بياني انحناء
        html.Div(
            style={**common_style, 'backgroundColor': '#0d0d1a', 'padding': '5px', 'overflow': 'hidden'},
            children=[
                html.Div("1", style={'position': 'absolute', 'top': 10, 'right': 10, 'color': '#aaa', 'fontSize': 20, 'zIndex': 10}),
                dcc.Graph(id='graph-curvature', config={'displayModeBar': False}, style={'height': '100%', 'width': '100%'})
            ]
        ),
        # ---- الصف السفلي ----
        # مربع 6: محاكاة المنظور الخطي
        html.Div(
            style={**common_style, 'backgroundColor': '#111', 'padding': '5px', 'overflow': 'hidden'},
            children=[
                html.Div("6", style={'position': 'absolute', 'top': 10, 'right': 10, 'color': '#aaa', 'fontSize': 20}),
                html.H6("🎛️ محاكاة المنظور الخطي", style={'color': 'white', 'textAlign': 'center', 'marginTop': 25}),
                html.Label("ارتفاع الجسم (م):", style={'fontSize': 10, 'color': 'white'}),
                dcc.Slider(id='obj-height', min=1, max=100, step=1, value=50,
                           tooltip={"placement": "bottom", "always_visible": True}),
                html.Label("ارتفاع العين (م):", style={'fontSize': 10, 'color': 'white'}),
                dcc.Slider(id='eye-height', min=0.1, max=10, step=0.1, value=1.7,
                           tooltip={"placement": "bottom", "always_visible": True}),
                html.Label("المسافة (كم):", style={'fontSize': 10, 'color': 'white'}),
                dcc.Slider(id='persp-dist', min=1, max=100, step=1, value=20,
                           tooltip={"placement": "bottom", "always_visible": True}),
                html.Label("عامل الزوم:", style={'fontSize': 10, 'color': 'white'}),
                dcc.Slider(id='zoom-factor', min=0, max=10, step=0.5, value=0,
                           tooltip={"placement": "bottom", "always_visible": True}),
                html.Label("النموذج:", style={'fontSize': 10, 'color': 'white'}),
                dcc.Dropdown(id='persp-model',
                             options=[{"label": "المنظور الخطي (سطح مستوٍ)", "value": "المنظور الخطي (سطح مستوٍ)"},
                                      {"label": "نموذج المقارنة (كروي)", "value": "نموذج المقارنة (كروي)"}],
                             value="المنظور الخطي (سطح مستوٍ)", clearable=False,
                             style={'backgroundColor': '#2a2a3a', 'color': 'black'}),
                dcc.Graph(id='graph-perspective', config={'displayModeBar': False}, style={'height': '180px', 'marginTop': '10px'})
            ]
        ),
        # مربع 5: محاكاة مستوى الأفق
        html.Div(
            style={**common_style, 'backgroundColor': '#111', 'padding': '5px', 'overflow': 'hidden'},
            children=[
                html.Div("5", style={'position': 'absolute', 'top': 10, 'right': 10, 'color': '#aaa', 'fontSize': 20}),
                html.H6("🌄 محاكاة مستوى الأفق", style={'color': 'white', 'textAlign': 'center', 'marginTop': 25}),
                html.Label("الارتفاع (كم):", style={'fontSize': 10, 'color': 'white'}),
                dcc.Slider(id='horizon-alt', min=0.1, max=100, step=0.1, value=10,
                           tooltip={"placement": "bottom", "always_visible": True}),
                html.Label("ارتفاع العين (م):", style={'fontSize': 10, 'color': 'white'}),
                dcc.Slider(id='horizon-eye', min=0.1, max=10, step=0.1, value=1.7,
                           tooltip={"placement": "bottom", "always_visible": True}),
                dcc.Graph(id='graph-horizon', config={'displayModeBar': False}, style={'height': '220px', 'marginTop': '10px'})
            ]
        ),
        # مربع 4: فارغ
        html.Div(
            style={**common_style, 'backgroundColor': '#111', 'textAlign': 'right'},
            children=[html.Div("4", style={'position': 'absolute', 'top': 10, 'right': 10, 'color': '#888', 'fontSize': 20})]
        )
    ]
)

# --- Callbacks ---
@app.callback(
    Output('res-div', 'children'),
    Output('graph-curvature', 'figure'),
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
        html.P(f"📏 المسافة: {dist:.2f} {unit_label}", style={'margin': '0 0 5px 0', 'textAlign': 'right'}),
        html.P(f"📉 الانخفاض: {drop_m:.2f} متر", style={'margin': '0', 'color': '#ffaa00', 'textAlign': 'right'}),
        html.P(f"≈ {drop_ft:.2f} قدم", style={'margin': '2px 0 0 0', 'fontSize': 10, 'textAlign': 'right'})
    ])
    fig = create_curvature_graph(dist_km, drop_m)
    return result, fig

@app.callback(
    Output('graph-perspective', 'figure'),
    Input('obj-height', 'value'),
    Input('eye-height', 'value'),
    Input('persp-dist', 'value'),
    Input('zoom-factor', 'value'),
    Input('persp-model', 'value')
)
def update_perspective(obj_h, eye_h, dist_km, zoom, model):
    fig = perspective_simulation(obj_h, eye_h, dist_km, zoom, model)
    return fig

@app.callback(
    Output('graph-horizon', 'figure'),
    Input('horizon-alt', 'value'),
    Input('horizon-eye', 'value')
)
def update_horizon(alt_km, eye_m):
    fig = horizon_simulation(alt_km, eye_m)
    return fig

if __name__ == '__main__':
    app.run(debug=True)
