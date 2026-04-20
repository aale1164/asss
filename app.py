# -*- coding: utf-8 -*-
# تطبيق Dash لعرض إسقاط سمتي فارغ (بدون خريطة غليسون، شمس، قمر، نجوم)

import dash
from dash import html, dcc
import plotly.graph_objects as go

# ============================================
# إنشاء تطبيق Dash مع تعريف server للنشر
# ============================================
app = dash.Dash(__name__)
server = app.server

# ============================================
# إنشاء الشكل (Figure) فارغ تماماً باستثناء الإسقاط الجغرافي
# ============================================
fig = go.Figure()

# نقطة وهمية مخفية لإظهار الخريطة (بدون أي علامات)
fig.add_trace(go.Scattergeo(
    lon=[0], lat=[0],
    mode='markers',
    marker=dict(size=0.1, opacity=0),
    showlegend=False
))

# إعدادات الإسقاط الجغرافي (سمتي مسطح - مركزه القطب الشمالي) بدون أي عناصر خرائطية
fig.update_geos(
    projection_type="azimuthal equidistant",
    projection_rotation=dict(lon=0, lat=90, roll=0),
    showcoastlines=False,
    showland=False,
    showocean=False,
    showcountries=False,
    showlakes=False,
    showrivers=False,
    # إظهار شبكة خطوط الطول والعرض فقط (بيضاء)
    lataxis_showgrid=True,
    lonaxis_showgrid=True,
    lataxis_gridcolor="white",
    lonaxis_gridcolor="white",
    lataxis_gridwidth=0.5,
    lonaxis_gridwidth=0.5,
    lataxis_range=[-90, 90],
    lonaxis_range=[-180, 180],
    bgcolor='black'
)

# تنسيق الشكل العام
fig.update_layout(
    title=dict(
        text='🗺️ إسقاط سمتي متساوي المسافات (خريطة فارغة) - تم إزالة كل العناصر',
        x=0.5,
        font=dict(size=18, color='white')
    ),
    geo=dict(bgcolor='black'),
    paper_bgcolor='black',
    height=700,
    margin=dict(l=0, r=0, t=60, b=0)
)

# ============================================
# تصميم واجهة التطبيق
# ============================================
app.layout = html.Div([
    dcc.Graph(figure=fig, config={'displayModeBar': True}),
    html.Div(
        "لا توجد خريطة غليسون، ولا شمس، ولا قمر، ولا نجوم. فقط شبكة خطوط الطول والعرض.",
        style={
            'textAlign': 'center',
            'color': '#aaa',
            'marginTop': '10px',
            'fontSize': '13px'
        }
    )
])

# ============================================
# تشغيل التطبيق
# ============================================
if __name__ == '__main__':
    app.run(debug=True)
