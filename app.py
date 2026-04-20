# -*- coding: utf-8 -*-
# تطبيق Dash فارغ تماماً (بدون أي خطوط أو شبكات أو عناصر)

import dash
from dash import html, dcc
import plotly.graph_objects as go

app = dash.Dash(__name__)
server = app.server

# شكل فارغ تماماً بدون أي إسقاط جغرافي
fig = go.Figure()

# لا نضيف أي traces ولا أي إعدادات جغرافية
fig.update_layout(
    title=dict(text='', x=0.5),
    paper_bgcolor='black',
    plot_bgcolor='black',
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    margin=dict(l=0, r=0, t=0, b=0),
    geo=dict(visible=False)  # إخفاء أي إسقاط جغرافي بالكامل
)

app.layout = html.Div([
    dcc.Graph(figure=fig, config={'displayModeBar': False}),
    html.Div(
        "لا توجد خطوط كرة ولا شبكة ولا خرائط.",
        style={'textAlign': 'center', 'color': 'white', 'marginTop': '20px'}
    )
])

if __name__ == '__main__':
    app.run(debug=True)
