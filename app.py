# -*- coding: utf-8 -*-
# تطبيق Dash - خريطة غليسون في الجهة اليمنى فقط، مكبرة، بدون أي خطوط أو شبكات

import dash
from dash import html, dcc
import plotly.graph_objects as go

app = dash.Dash(__name__)
server = app.server

# ============================================
# إعداد خريطة غليسون (الإسقاط السمتي متساوي المسافات)
# بدون خطوط الطول والعرض، بدون شبكات، مع تكبير مناسب
# ============================================

fig = go.Figure()

# نقطة وهمية مخفية بالكامل (لإرضاء Plotly)
fig.add_trace(go.Scattergeo(
    lon=[0], lat=[0],
    mode='markers',
    marker=dict(size=0.01, opacity=0),
    showlegend=False,
    hoverinfo='none'
))

# إعدادات الإسقاط الجغرافي - إزالة كل شيء ما عدا الصورة
fig.update_geos(
    projection_type="azimuthal equidistant",
    projection_rotation=dict(lon=0, lat=90, roll=0),
    # إخفاء جميع العناصر الجغرافية
    showcoastlines=False,
    showland=False,
    showocean=False,
    showcountries=False,
    showlakes=False,
    showrivers=False,
    showframe=False,
    # إخفاء خطوط الطول والعرض (الشبكة البيضاء)
    lataxis_showgrid=False,
    lonaxis_showgrid=False,
    lataxis_showline=False,
    lonaxis_showline=False,
    lataxis_tickvals=[],
    lonaxis_tickvals=[],
    lataxis_visible=False,
    lonaxis_visible=False,
    # تحديد نطاق للخريطة بحيث تظهر مكبرة (بدون قص مفرط)
    lataxis_range=[-70, 90],     # يظهر من خط عرض -70 إلى القطب الشمالي
    lonaxis_range=[-150, 150],   # يظهر خطوط الطول من -150 إلى 150
    bgcolor='black'
)

# إضافة صورة خريطة غليسون (طبقة تحت كل شيء)
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
        layer="below",
        opacity=1.0
    )
)

# تنسيق المخطط العام: إزالة الهوامش وجعل الخلفية سوداء فقط حول الخريطة
fig.update_layout(
    title='',
    geo=dict(bgcolor='black'),
    paper_bgcolor='black',
    margin=dict(l=0, r=0, t=0, b=0),
    height=700,
    width=None,
    xaxis=dict(visible=False),
    yaxis=dict(visible=False)
)

# ============================================
# واجهة التطبيق: خريطة غليسون في النصف الأيمن فقط
# ============================================
app.layout = html.Div(
    style={
        'display': 'flex',
        'flexDirection': 'row',
        'height': '100vh',
        'width': '100vw',
        'backgroundColor': 'black',
        'margin': '0',
        'padding': '0',
        'overflow': 'hidden'
    },
    children=[
        # الجهة اليسرى (فارغة تماماً)
        html.Div(
            style={
                'flex': '1',
                'backgroundColor': 'black',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center'
            },
            children=[
                html.Div(
                    "",  # فارغ
                    style={'color': '#333', 'fontSize': '16px'}
                )
            ]
        ),
        # الجهة اليمنى: خريطة غليسون مكبرة
        html.Div(
            style={
                'flex': '1',
                'backgroundColor': 'black',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center',
                'padding': '0'
            },
            children=[
                dcc.Graph(
                    figure=fig,
                    config={'displayModeBar': True, 'responsive': True},
                    style={'width': '100%', 'height': '100%', 'border': 'none'}
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
