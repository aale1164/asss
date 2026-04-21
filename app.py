# -*- coding: utf-8 -*-
import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import numpy as np
import math
import os

app = dash.Dash(__name__)
server = app.server

R_KM = 6371.0

def curvature_drop_m(distance_km):
    return (distance_km ** 2) / (2 * R_KM) * 1000

def horizon_dip_deg(altitude_km):
    if altitude_km <= 0:
        return 0.0
    cos_theta = R_KM / (R_KM + altitude_km)
    cos_theta = max(min(cos_theta, 1), -1)
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

        fig.add_trace(go.Scatter(x=distances, y=top, mode='lines', line=dict(color='#00E5FF', width=2), name='القمة'))
        fig.add_trace(go.Scatter(x=distances, y=bottom, mode='lines', line=dict(color='#FF4D4D', width=2), name='القاعدة', fill='tonexty'))

        cur_top = (obj_h / (dist * 1000)) * (eye_h + obj_h/2) * (1+zoom)
        cur_bottom = (obj_h / (dist * 1000)) * (eye_h - obj_h/2) * (1+zoom)

        if dist > vanish_km:
            cur_top = cur_bottom = 0

        fig.add_trace(go.Scatter(x=[dist], y=[cur_top], mode='markers', marker=dict(size=10, color='#00E5FF'), name='القمة الحالية'))
        fig.add_trace(go.Scatter(x=[dist], y=[cur_bottom], mode='markers', marker=dict(size=10, color='#FF4D4D'), name='القاعدة الحالية'))

        fig.add_vline(x=vanish_km, line_dash="dot", line_color="gray", annotation_text=f"نقطة التلاشي {vanish_km:.1f} كم")

        title = "نموذج الأرض المسطحة - المنظور"

    else:
        drop = curvature_drop_m(distances)
        visible = np.maximum(0, obj_h - drop)

        fig.add_trace(go.Scatter(x=distances, y=visible, mode='lines', line=dict(color='#FFA500', width=3), name='الارتفاع المرئي', fill='tozeroy'))

        cur_visible = max(0, (obj_h - curvature_drop_m(dist)) * (1+zoom))
        fig.add_trace(go.Scatter(x=[dist], y=[cur_visible], mode='markers', marker=dict(size=12, color='#FF4D4D'), name='الجسم الحالي'))

        dip = horizon_dip_deg(alt)
        fig.add_hline(y=-dip, line_width=3, line_color="#3b82f6", line_dash="dot", annotation_text=f"الأفق ({dip:.2f}°)")

        title = "نموذج الأرض الكروية - الانحناء"

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(color='white')),
        xaxis=dict(title="المسافة (كم)", range=[0, max_dist], gridcolor='#333', color='white'),
        yaxis=dict(title="الارتفاع (م)", gridcolor='#333', color='white'),
        plot_bgcolor='#0d0d1a',
        paper_bgcolor='#0d0d1a',
        legend=dict(font=dict(color='white')),
    )

    return fig


app.layout = html.Div([

    html.Style('''
        body { background-color: #0b0f19; }

        .control-panel {
            background: linear-gradient(135deg, #f5f7fa, #e4e7ec);
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        }

        .control-panel, .control-panel * {
            color: #1f2937;
        }

        .rc-slider-track { background-color: #3b82f6; }
        .rc-slider-rail { background-color: #cbd5e1; }

        .rc-slider-handle {
            border: solid 3px #3b82f6;
            background-color: #fff;
        }

        .rc-slider-mark-text {
            color: #111;
            background-color: #fff;
            padding: 3px 6px;
            border-radius: 6px;
            border: 1px solid #d1d5db;
            font-size: 12px;
        }

        .rc-slider-tooltip-inner {
            background-color: #111827;
            color: #fff;
        }

        .Select-control, .Select-menu-outer {
            background-color: #fff;
            color: #111;
        }

        .Select-option.is-focused {
            background-color: #3b82f6;
            color: #fff;
        }

        .info-box {
            background: #fff;
            border-radius: 10px;
            padding: 10px;
        }
    '''),

    html.Div(
        style={'display': 'flex', 'height': '100vh', 'padding': '20px', 'gap': '20px'},
        children=[

            html.Div(
                className="control-panel",
                style={'flex': '1', 'borderRadius': '12px', 'padding': '15px'},
                children=[
                    html.H2("🎛️ لوحة التحكم"),
                    html.Label("النموذج"),
                    dcc.Dropdown(id='model', options=[
                        {'label':'مسطح','value':'flat'},
                        {'label':'كروي','value':'curved'}
                    ], value='flat'),

                    dcc.Slider(id='obj', min=1, max=100, value=50),
                    dcc.Slider(id='eye', min=0.1, max=10, value=1.7),
                    dcc.Slider(id='dist', min=1, max=100, value=20),
                    dcc.Slider(id='zoom', min=0, max=5, value=0),
                    dcc.Slider(id='alt', min=0, max=50, value=10),

                    html.Div(id='info', className="info-box")
                ]
            ),

            html.Div(
                style={'flex': '2'},
                children=[dcc.Graph(id='graph')]
            )
        ]
    )
])


@app.callback(
    [Output('graph', 'figure'), Output('info', 'children')],
    [Input('model', 'value'), Input('obj', 'value'),
     Input('eye', 'value'), Input('dist', 'value'),
     Input('zoom', 'value'), Input('alt', 'value')]
)
def update(model, obj, eye, dist, zoom, alt):
    fig = create_figure(model, obj, eye, dist, zoom, alt)

    info = html.Div([
        html.P(f"الانخفاض: {curvature_drop_m(dist):.2f} متر"),
        html.P(f"الأفق: {math.sqrt(2*R_KM*(eye/1000)):.2f} كم"),
        html.P(f"زاوية الأفق: {horizon_dip_deg(alt):.2f}°")
    ])

    return fig, info


# 🔥 هذا أهم تعديل للـ Deploy
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port, debug=False)
