# -*- coding: utf-8 -*-
# تطبيق Dash - خريطة غليسون فقط، بدون أي خطوط طول أو عرض أو شبكات أو عناصر إضافية

import dash
from dash import html, dcc
import plotly.graph_objects as go

app = dash.Dash(__name__)
server = app.server

# ============================================
# إنشاء خريطة غليسون (الإسقاط السمتي متساوي المسافات)
# مع إخفاء كل شيء ما عدا الصورة
# ============================================
fig = go.Figure()

# لا نضيف أي traces (لا نقاط وهمية ولا شيء)
# نكتفي بتعيين الإسقاط الجغرافي مع إخفاء جميع الخطوط والعناصر

fig.update_geos(
    projection_type="azimuthal equidistant",
    projection_rotation=dict(lon=0, lat=90, roll=0),
    # إخفاء كل العناصر الجغرافية
    showcoastlines=False,
    showland=False,
    showocean=False,
    showcountries=False,
    showlakes=False,
    showrivers=False,
    showframe=False,
    # إخفاء خطوط الطول والعرض بشكل مطلق
    lataxis_showgrid=False,
    lonaxis_showgrid=False,
    lataxis_showline=False,
    lonaxis_showline=False,
    lataxis_tickvals=[],
    lonaxis_tickvals=[],
    lataxis_visible=False,
    lonaxis_visible=False,
    # إخفاء أي تسميات أو أرقام
    showlakes=False,
    # تحديد نطاق الخريطة لتبدو واضحة (ليست صغيرة ولا مقطوعة)
    lataxis_range=[-85, 90],
    lonaxis_range=[-175, 175],
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

# تنسيق المخطط: إزالة الهوامش والعناوين
fig.update_layout(
    title='',
    geo=dict(bgcolor='black'),
    paper_bgcolor='black',
    margin=dict(l=0, r=0, t=0, b=0),
    height=700,
    width=None,
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    plot_bgcolor='black'
)

# ============================================
# تصميم الواجهة: خريطة غليسون في الجهة اليمنى فقط
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
        # الجهة اليسرى (فارغة تمامًا)
        html.Div(
            style={
                'flex': '1',
                'backgroundColor': 'black'
            }
        ),
        # الجهة اليمنى: الخريطة فقط
        html.Div(
            style={
                'flex': '1',
                'backgroundColor': 'black',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center'
            },
            children=[
                dcc.Graph(
                    figure=fig,
                    config={'displayModeBar': True, 'responsive': True},
                    style={'width': '100%', 'height': '100%'}
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
