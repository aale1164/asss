# -*- coding: utf-8 -*-
# تطبيق Dash المطور لمحاكاة الانحناء والمنظور - نسخة المطورين
# تم تعديل الألوان لتكون واضحة وجذابة في لوحة التحكم

import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import numpy as np
import math

app = dash.Dash(__name__)
server = app.server

R_KM = 6371.0

# --- الدوال الرياضية ---
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
    fig.add_hline(y=0, line_width=2, line_color="#4CAF50", line_dash="dash", annotation_text="مستوى العين")
    
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
        title = "🌍 نموذج الأرض المسطحة - المنظور الخطي"
    else:
        drop = curvature_drop_m(distances)
        visible = np.maximum(0, obj_h - drop)
        fig.add_trace(go.Scatter(x=distances, y=visible, mode='lines', line=dict(color='orange', width=3), name='الارتفاع المرئي', fill='tozeroy'))
        cur_visible = max(0, (obj_h - curvature_drop_m(dist)) * (1+zoom))
        fig.add_trace(go.Scatter(x=[dist], y=[cur_visible], mode='markers', marker=dict(size=12, color='red'), name='الجسم الحالي'))
        dip = horizon_dip_deg(alt)
        fig.add_hline(y=-dip, line_width=3, line_color="blue", line_dash="dot", annotation_text=f"الأفق الكروي (انخفاض {dip:.2f}°)")
        title = "🌍 نموذج الأرض الكروية - الانحناء والأفق"
    
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(color='white', size=20)),
        xaxis=dict(title="المسافة (كم)", range=[0, max_dist], gridcolor='#333', color='white'),
        yaxis=dict(title="الارتفاع/الزاوية", gridcolor='#333', color='white'),
        plot_bgcolor='black', paper_bgcolor='black',
        legend=dict(font=dict(color='white'), bgcolor='rgba(0,0,0,0.6)'),
        margin=dict(l=40, r=40, t=80, b=40)
    )
    return fig

# --- واجهة التطبيق ---
app.layout = html.Div([
    html.Style('''
        /* تغيير لون أرقام الشرائح (الماركس) لتكون واضحة جدا
