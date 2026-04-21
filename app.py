import dash
from dash import html

app = dash.Dash(__name__)
server = app.server  # مهم للنشر

app.layout = html.Div([
    html.H1("Hello World 🔥"),
    html.P("إذا شفت هذي الصفحة، النشر اشتغل 100%")
])

# لا تستخدم debug في السيرفر
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)
