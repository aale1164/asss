# -*- coding: utf-8 -*-
# تطبيق Dash يعرض خريطة غليسون في الجانب الأيمن فقط

import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)
server = app.server

# ============================================
# إنشاء خريطة غليسون (الإسقاط السمتي)
# ============================================
fig_gleason = go.Figure()

# نقطة وهمية
fig_gleason.add_trace(go.Scattergeo(
    lon=[0], lat=[0],
    mode='markers',
    marker=dict(size=0.1, opacity=0),
    showlegend=False
))

# إعدادات الإسقاط السمتي مع إظهار شبكة خفيفة
fig_gleason.update_geos(
    projection_type="azimuthal equidistant",
    projection_rotation=dict(lon=0, lat=90, roll=0),
    showcoastlines=False,
    showland=False,
    showocean=False,
    showcountries=False,
    lataxis_showgrid=True,
    lonaxis_showgrid=True,
    lataxis_gridcolor="white",
    lonaxis_gridcolor="white",
    lataxis_gridwidth=0.5,
    lonaxis_gridwidth=0.5,
    bgcolor='black'
)

# إضافة صورة خريطة غليسون كخلفية
fig_gleason.add_layout_image(
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

# تنسيق الشكل
fig_gleason.update_layout(
    title=dict(text='خريطة غليسون (1892)', x=0.5, font=dict(color='white', size=14)),
    geo=dict(bgcolor='black'),
    paper_bgcolor='black',
    height=600,
    margin=dict(l=0, r=0, t=40, b=0),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False)
)

# ============================================
# تصميم واجهة التطبيق: خريطة غليسون في اليمين فقط
# ============================================
app.layout = html.Div(
    style={'display': 'flex', 'flexDirection': 'row', 'height': '100vh', 'backgroundColor': 'black'},
    children=[
        # الجهة اليسرى (فارغة أو يمكن إضافة نص)
        html.Div(
            style={'flex': '1', 'backgroundColor': 'black', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'},
            children=[
                html.Div(
                    "الجهة اليسرى (فارغة)",
                    style={'color': 'white', 'fontSize': '20px'}
                )
            ]
        ),
        # الجهة اليمنى: خريطة غليسون
        html.Div(
            style={'flex': '1', 'backgroundColor': 'black', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'},
            children=[
                dcc.Graph(figure=fig_gleason, config={'displayModeBar': True}, style={'width': '100%', 'height': '100%'})
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
