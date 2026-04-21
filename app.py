# -*- coding: utf-8 -*-
# تطبيق Dash - 6 مربعات متساوية مع خطوط عربية عريضة بيضاء
# وتصغير حجم المحاكاة في المربعين 5 و 6 بنسبة 30%

import dash
from dash import html, dcc, Input, Output
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
        font=dict(color='white', size=8, family='Arial', weight='bold'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=7, weight='bold')),
        xaxis_title="كم", yaxis_title="متر",
        title="منحنى الانحناء", title_font_size=10
    )
    return fig

# ---- دوال للمربع 5 (المنظور الخطي) بحجم مصغر 30% ----
def perspective_simulation(distance_km, object_height_m, model):
    distances = np.linspace(0.1, max(distance_km, 1)*2, 100)
    if model == 'flat':
        apparent_height = object_height_m / (distances * 1000) * 100  # تكبير مرئي
        vanishing_dist = object_height_m / (2 * math.tan(math.radians(0.02))) / 1000
        title = "نموذج مسطح: المنظور الخطي"
        color = 'cyan'
    else:
        drop_curvature = (distances**2) / (2 * R_KM) * 1000
        apparent_height = np.maximum(0, object_height_m - drop_curvature)
        title = "نموذج كروي: الانحناء"
        color = 'orange'
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=distances, y=apparent_height, mode='lines',
                             line=dict(color=color, width=2), name='الارتفاع المرئي (م)'))
    if model == 'flat':
        curr_height = object_height_m / (distance_km * 1000) * 100
        curr_height = max(0, curr_height)
    else:
        curr_height = max(0, object_height_m - (distance_km**2)/(2*R_KM)*1000)
    fig.add_trace(go.Scatter(x=[distance_km], y=[curr_height], mode='markers',
                             marker=dict(size=6, color='red'), name='الجسم الحالي'))
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=5, r=5, t=25, b=5),
        font=dict(color='white', size=7, weight='bold'),
        xaxis_title="كم", yaxis_title="م",
        title=title, title_font_size=9,
        height=120, width=None
    )
    return fig

# ---- دالة للمربع 6 (مستوى الأفق) بحجم مصغر 30% ----
def horizon_simulation(altitude_km):
    R = 6371
    if altitude_km <= 0:
        dip_deg = 0
    else:
        dip_rad = math.acos(R / (R + altitude_km))
        dip_deg = math.degrees(dip_rad)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 10], y=[0, 0], mode='lines',
                             line=dict(color='white', width=2), name='أفق الأرض المسطحة'))
    fig.add_trace(go.Scatter(x=[0, 10], y=[-dip_deg, -dip_deg], mode='lines',
                             line=dict(color='lightblue', width=2, dash='dot'), name='أفق الأرض الكروية'))
    fig.add_annotation(x=8, y=-dip_deg+0.1, text=f"انخفاض {dip_deg:.2f}°", showarrow=False,
                       font=dict(size=7, color='lightblue', weight='bold'), bgcolor='rgba(0,0,0,0.6)')
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=5, r=5, t=25, b=5),
        font=dict(color='white', size=7, weight='bold'),
        xaxis=dict(visible=False, range=[0,10]), yaxis_title="الزاوية (درجة)",
        title=f"مقارنة مستوى الأفق (ارتفاع {altitude_km} كم)", title_font_size=9,
        height=120, width=None
    )
    return fig

# ---- التصميم العام مع خطوط عريضة بيضاء ----
common_style = {
    'position': 'relative',
    'padding': '6px',
    'overflow': 'auto',
    'display': 'flex',
    'flexDirection': 'column',
    'fontWeight': 'bold',
    'color': 'white'
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
        'direction': 'rtl',
        'fontFamily': 'Arial, sans-serif',
        'fontWeight': 'bold',
        'color': 'white'
    },
    children=[
        # ---- الصف العلوي ----
        # مربع 3: تعليمات
        html.Div(
            style={**common_style, 'backgroundColor': '#1e1e2f', 'textAlign': 'right'},
            children=[
                html.Div("3", style={'position': 'absolute', 'top': 5, 'right': 8, 'color': '#aaa', 'fontSize': 14, 'fontWeight': 'bold'}),
                html.H5("📘 تعليمات:", style={'color': 'white', 'marginTop': 25, 'fontSize': 13, 'fontWeight': 'bold'}),
                html.Ul([
                    html.Li("أدخل المسافة واضغط احسب.", style={'fontSize': 11, 'fontWeight': 'bold'}),
                    html.Li("الرسم البياني يوضح الانحناء.", style={'fontSize': 11, 'fontWeight': 'bold'}),
                    html.Li("المربعان 5 و6 تفاعليان.", style={'fontSize': 11, 'fontWeight': 'bold'}),
                ], style={'paddingRight': '15px'})
            ]
        ),
        # مربع 2: حاسبة الانحناء
        html.Div(
            style={**common_style, 'backgroundColor': '#0d0d1a', 'textAlign': 'right', 'justifyContent': 'center'},
            children=[
                html.Div("2", style={'position': 'absolute', 'top': 5, 'right': 8, 'color': '#aaa', 'fontSize': 14, 'fontWeight': 'bold'}),
                html.H6("🌍 حاسبة الانحناء", style={'textAlign': 'center', 'color': 'white', 'margin': '5px 0', 'fontSize': 13, 'fontWeight': 'bold'}),
                html.Label("المسافة:", style={'fontSize': 10, 'fontWeight': 'bold'}),
                dcc.Input(id='dist-input', type='number', value=10, step=0.5,
                          style={'width': '85%', 'padding': '3px', 'fontSize': 10, 'margin': '3px 0',
                                 'backgroundColor': '#2a2a3a', 'color': 'white', 'border': 'none',
                                 'borderRadius': '3px', 'fontWeight': 'bold'}),
                html.Label("الوحدة:", style={'fontSize': 10, 'fontWeight': 'bold'}),
                dcc.RadioItems(id='unit-select', options=[{'label':' كم','value':'km'},{'label':' ميل','value':'mile'}],
                               value='km', labelStyle={'display':'inline-block','margin':'3px','fontSize':9, 'fontWeight':'bold', 'color':'white'}),
                html.Button("احسب", id='calc-btn', n_clicks=0,
                            style={'backgroundColor':'#4CAF50','color':'white','padding':'2px 8px','fontSize':10,
                                   'margin':'5px 0','border':'none','borderRadius':'3px','cursor':'pointer','fontWeight':'bold'}),
                html.Div(id='res-div', style={'backgroundColor':'#1e1e2f','padding':'4px','borderRadius':'4px',
                                              'marginTop':'5px','fontSize':10,'color':'white','textAlign':'center','fontWeight':'bold'})
            ]
        ),
        # مربع 1: رسم بياني الانحناء
        html.Div(
            style={**common_style, 'backgroundColor': '#0d0d1a', 'padding': '3px'},
            children=[
                html.Div("1", style={'position': 'absolute', 'top': 5, 'right': 8, 'color': '#aaa', 'fontSize': 14, 'fontWeight': 'bold'}),
                dcc.Graph(id='curvature-graph', config={'displayModeBar': False}, style={'height': '95%', 'width': '100%'})
            ]
        ),
        # ---- الصف السفلي ----
        # مربع 6: محاكاة مستوى الأفق (مصغر 30%)
        html.Div(
            style={**common_style, 'backgroundColor': '#111', 'textAlign': 'right'},
            children=[
                html.Div("6", style={'position': 'absolute', 'top': 5, 'right': 8, 'color': '#aaa', 'fontSize': 14, 'fontWeight': 'bold'}),
                html.P("📐 مستوى الأفق", style={'textAlign': 'center', 'fontSize': 11, 'margin': '0 0 5px 0', 'fontWeight': 'bold'}),
                html.Label("الارتفاع (كم):", style={'fontSize': 9, 'fontWeight': 'bold'}),
                dcc.Slider(id='altitude-slider', min=0, max=20, step=0.5, value=10,
                           marks={i: str(i) for i in range(0,21,5)},
                           tooltip={"placement": "bottom", "always_visible": False},
                           updatemode='drag'),
                dcc.Graph(id='horizon-graph', config={'displayModeBar': False}, style={'height': '130px', 'width': '100%'}),
                html.Div("توضيح: الأفق المسطح ثابت، الكروي ينخفض مع الارتفاع.",
                         style={'fontSize': 8, 'color': '#aaa', 'textAlign': 'center', 'marginTop': '4px', 'fontWeight': 'bold'})
            ]
        ),
        # مربع 5: محاكاة المنظور الخطي (مصغر 30%)
        html.Div(
            style={**common_style, 'backgroundColor': '#111', 'textAlign': 'right'},
            children=[
                html.Div("5", style={'position': 'absolute', 'top': 5, 'right': 8, 'color': '#aaa', 'fontSize': 14, 'fontWeight': 'bold'}),
                html.P("👁️ المنظور الخطي", style={'textAlign': 'center', 'fontSize': 11, 'margin': '0 0 5px 0', 'fontWeight': 'bold'}),
                html.Label("المسافة (كم):", style={'fontSize': 9, 'fontWeight': 'bold'}),
                dcc.Slider(id='persp-distance', min=1, max=100, step=1, value=20,
                           marks={i: str(i) for i in range(0,101,20)},
                           tooltip={"placement": "bottom"}, updatemode='drag'),
                html.Label("ارتفاع الجسم (م):", style={'fontSize': 9, 'fontWeight': 'bold'}),
                dcc.Slider(id='object-height', min=1, max=100, step=5, value=50,
                           marks={i: str(i) for i in range(0,101,20)}),
                html.Label("النموذج:", style={'fontSize': 9, 'fontWeight': 'bold'}),
                dcc.RadioItems(id='persp-model', options=[{'label':'مسطح','value':'flat'},{'label':'كروي','value':'curved'}],
                               value='flat', labelStyle={'display':'inline-block','margin':'3px','fontSize':9, 'fontWeight':'bold', 'color':'white'}),
                dcc.Graph(id='persp-graph', config={'displayModeBar': False}, style={'height': '130px', 'width': '100%'}),
                html.Div("توضيح: المسافة تؤثر على الارتفاع الظاهري.",
                         style={'fontSize': 8, 'color': '#aaa', 'textAlign': 'center', 'marginTop': '4px', 'fontWeight': 'bold'})
            ]
        ),
        # مربع 4 (فارغ)
        html.Div(
            style={**common_style, 'backgroundColor': '#111', 'textAlign': 'right'},
            children=[html.Div("4", style={'position': 'absolute', 'top': 5, 'right': 8, 'color': '#888', 'fontSize': 14, 'fontWeight': 'bold'})]
        )
    ]
)

# ---- Callbacks ----
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
        html.P(f"📏 المسافة: {dist:.2f} {unit_label}", style={'margin': '0', 'fontSize': 10, 'fontWeight': 'bold'}),
        html.P(f"📉 الانخفاض: {drop_m:.2f} م", style={'margin': '0', 'color': '#ffaa00', 'fontSize': 10, 'fontWeight': 'bold'}),
        html.P(f"≈ {drop_ft:.2f} قدم", style={'margin': '0', 'fontSize': 8, 'fontWeight': 'bold'})
    ])
    fig = create_curvature_graph(dist_km, drop_m)
    return result, fig

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
