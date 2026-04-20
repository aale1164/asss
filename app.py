# -*- coding: utf-8 -*-
# تطبيق Dash لعرض خريطة غليسون فقط (بدون الخريطة الجغرافية السابقة) مع الشمس والقمر والنجوم

import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

# ============================================
# إنشاء تطبيق Dash مع تعريف server للنشر
# ============================================
app = dash.Dash(__name__)
server = app.server

# ============================================
# إنشاء الشكل (Figure) الخاص بـ Plotly
# ============================================
fig = go.Figure()

# 1. نقطة وهمية لتفعيل الخريطة (مخفية)
fig.add_trace(go.Scattergeo(
    lon=[0], lat=[0],
    mode='markers',
    marker=dict(size=0.1, opacity=0),
    showlegend=False
))

# 2. إعدادات الإسقاط الجغرافي (سمتي مسطح - مركزه القطب الشمالي)
# تم إزالة جميع عناصر الخريطة السابقة (السواحل، اليابسة، المحيطات، الدول، البحيرات)
fig.update_geos(
    projection_type="azimuthal equidistant",
    projection_rotation=dict(lon=0, lat=90, roll=0),
    showcoastlines=False,      # إزالة السواحل
    showland=False,             # إزالة اليابسة
    showocean=False,            # إزالة المحيطات
    showcountries=False,        # إزالة الحدود
    showlakes=False,            # إزالة البحيرات
    showrivers=False,           # إزالة الأنهار
    lataxis_showgrid=True,      # إبقاء شبكة خطوط العرض
    lonaxis_showgrid=True,      # إبقاء شبكة خطوط الطول
    lataxis_gridcolor="white",
    lonaxis_gridcolor="white",
    lataxis_gridwidth=0.5,
    lonaxis_gridwidth=0.5,
    lataxis_range=[-90, 90],
    lonaxis_range=[-180, 180],
    bgcolor='black'
)

# 3. إضافة صورة خريطة غليسون كخلفية كاملة (بديل الخريطة السابقة)
fig.add_layout_image(
    dict(
        source="https://upload.wikimedia.org/wikipedia/commons/3/30/Gleason%27s_new_standard_map_of_the_world_-_on_the_projection_of_J._S._Christopher%2C_Modern_College%2C_Blackheath%2C_England%3B_scientifically_and_practically_correct%3B_as_%22it_is.%22_%2810143175716%29.jpg",
        xref="x",
        yref="y",
        x=-180,
        y=90,
        sizex=360,
        sizey=180,
        sizing="stretch",
        opacity=0.9,
        layer="below"
    )
)

# 4. إضافة الشمس (نقطة ذهبية)
fig.add_trace(go.Scattergeo(
    lon=[0], lat=[45],
    mode='markers',
    marker=dict(size=20, color='gold', symbol='circle',
                line=dict(width=2, color='orange')),
    name='الشمس ☀️'
))

# 5. إضافة القمر (نقطة فضية)
fig.add_trace(go.Scattergeo(
    lon=[-120], lat=[20],
    mode='markers',
    marker=dict(size=10, color='silver', symbol='circle',
                line=dict(width=1, color='gray')),
    name='القمر 🌙'
))

# 6. إضافة النجوم (150 نقطة عشوائية بيضاء)
np.random.seed(42)
star_lons = np.random.uniform(-180, 180, 150)
star_lats = np.random.uniform(-90, 90, 150)
fig.add_trace(go.Scattergeo(
    lon=star_lons, lat=star_lats,
    mode='markers',
    marker=dict(size=2.5, color='white', opacity=0.8),
    name='النجوم ✨'
))

# 7. إضافة نقطة القطب الشمالي (مركز الخريطة)
fig.add_trace(go.Scattergeo(
    lon=[0], lat=[90],
    mode='markers',
    marker=dict(size=6, color='red', symbol='x', line=dict(width=2)),
    name='القطب الشمالي'
))

# 8. تنسيق الشكل العام
fig.update_layout(
    title=dict(
        text='🗺️ خريطة غليسون 1892 (الإسقاط السمتي) - مع الشمس والقمر والنجوم',
        x=0.5,
        font=dict(size=18, color='white')
    ),
    geo=dict(bgcolor='black'),
    paper_bgcolor='black',
    height=750,
    margin=dict(l=0, r=0, t=60, b=0),
    legend=dict(
        font=dict(color='white'),
        bgcolor='rgba(0,0,0,0.6)',
        x=0.02,
        y=0.98
    )
)

# ============================================
# تصميم واجهة التطبيق
# ============================================
app.layout = html.Div([
    dcc.Graph(figure=fig, config={'displayModeBar': True}),
    html.Div(
        "خريطة غليسون الأصلية (1892) - تم إزالة الخريطة الجغرافية السابقة بالكامل | يمكنك التكبير والتدوير",
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
