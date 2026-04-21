# -*- coding: utf-8 -*-
# تطبيق Dash - شاشة مقسمة إلى نصفين (يمين ويسار) فقط، بدون أي محتوى إضافي

import dash
from dash import html

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    style={
        'display': 'flex',
        'flexDirection': 'row',
        'height': '100vh',
        'width': '100vw',
        'margin': '0',
        'padding': '0',
        'backgroundColor': 'black'
    },
    children=[
        # النصف الأيسر
        html.Div(
            style={
                'flex': '1',
                'backgroundColor': 'black',
                'margin': '0',
                'padding': '0'
            }
        ),
        # النصف الأيمن
        html.Div(
            style={
                'flex': '1',
                'backgroundColor': 'black',
                'margin': '0',
                'padding': '0'
            }
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
