# -*- coding: utf-8 -*-
# تطبيق Dash يعرض إسقاطاً سمتيًا فارغًا تماماً (بدون أي خطوط أو عناصر)

import dash
from dash import html, dcc
import plotly.graph_objects as go

# ============================================
# إنشاء تطبيق Dash مع تعريف server للنشر
# ============================================
app = dash.Dash(__name__)
server = app.server

# ============================================
# إنشاء شكل فارغ تماماً
# ============================================
fig = go.Figure()

# نقطة وهمية مخفية (ضرورية لتفعيل الإسقاط)
fig.add_trace(go.Scattergeo(
    lon=[0], lat=[0],
    mode='markers',
    marker=dict(size=0.1, opacity=0),
    showlegend=False
))

# إعدادات الإسقاط الجغرافي مع إخفاء خطوط الطول والعرض
fig.update_geos(
    projection_type="azimuthal equidistant",
    projection_rotation=dict(lon=0, lat=90, roll=0),
    showcoastlines=False,
    showland=False,
    showocean=False,
    showcountries=False,
    showlakes=False,
    showrivers=False,
    # إخفاء شبكة خطوط الطول والعرض تماماً
    lataxis_showgrid=False,
    lonaxis_showgrid=False,
    lataxis_showline=False,
    lonaxis_showline=False,
    lataxis_tickvals=[],      # إخفاء علامات خطوط العرض
    lonaxis_tickvals=[],      # إخفاء علامات خطوط الطول
    lataxis_visible=False,    # إخفاء محور خطوط العرض بالكامل
    lonaxis_visible=False,    # إخفاء محور خطوط الطول بالكامل
    bgcolor='black'
)

# تنسيق الشكل العام
fig.update_layout(
    title=dict(
        text='إسقاط سمتي فارغ - تم إزالة كل العناصر بما فيها خطوط الطول والعرض',
        x=0.5,
        font=dict(size=16, color='white')
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
        "خريطة فارغة تماماً: لا خريطة غليسون، لا شمس، لا قمر، لا نجوم، ولا خطوط طول وعرض.",
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
