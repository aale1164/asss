# -*- coding: utf-8 -*-
# تطبيق Dash لعرض خريطة غليسون (الإسقاط السمتي متساوي المسافات) مع الشمس والقمر والنجوم
# يعمل على Render و Hugging Face Spaces وغيرها من خدمات الاستضافة

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
fig.update_geos(
    projection_type="azimuthal equidistant",
    projection_rotation=dict(lon=0, lat=90, roll=0),
    showcoastlines=True,
    coastlinecolor="DarkBlue",
    showland=True,
    landcolor="LightGreen",
    showocean=True,
    oceancolor="LightBlue",
    showcountries=True,
    countrycolor="gray",
    showlakes=True,
    lakecolor="LightBlue",
    lataxis_showgrid=True,
    lonaxis_showgrid=True,
    lataxis_gridcolor="white",
    lonaxis_gridcolor="white",
    lataxis_range=[-90, 90],
    lonaxis_range=[-180, 180]
)

# 3. إضافة صورة خريطة غليسون كخلفية (اختياري، قد لا تظهر بشكل مثالي)
# ملاحظة: إضافة الصور في geo ليس مدعوماً رسمياً، لكن يمكن تجربته
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
        opacity=0.7,
        layer="below"
    )
)

# 4. إضافة الشمس (نقطة ذهبية مع هالة)
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

# 6. إضافة النجوم (100 نقطة عشوائية بيضاء)
np.random.seed(42)
star_lons = np.random.uniform(-180, 180, 100)
star_lats = np.random.uniform(-90, 90, 100)
fig.add_trace(go.Scattergeo(
    lon=star_lons, lat=star_lats,
    mode='markers',
    marker=dict(size=3, color='white', opacity=0.7),
    name='النجوم ✨'
))

# 7. إضافة نقطة القطب الشمالي (مركز الخريطة)
fig.add_trace(go.Scattergeo(
    lon=[0], lat=[90],
    mode='markers',
    marker=dict(size=6, color='white', symbol='x'),
    name='القطب الشمالي'
))

# 8. تنسيق الشكل العام
fig.update_layout(
    title=dict(
        text='🌍 خريطة غليسون (الإسقاط السمتي متساوي المسافات) - مع الشمس والقمر والنجوم',
        x=0.5,
        font=dict(size=18, color='white')
    ),
    geo=dict(bgcolor='black'),
    paper_bgcolor='black',
    height=700,
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
        "خريطة غليسون (1892) - الإسقاط السمتي متساوي المسافات | يمكنك التكبير والتدوير بالماوس",
        style={
            'textAlign': 'center',
            'color': 'white',
            'marginTop': '10px',
            'fontSize': '14px'
        }
    )
])

# ============================================
# تشغيل التطبيق (للتجربة المحلية)
# ============================================
if __name__ == '__main__':
    app.run(debug=True)
