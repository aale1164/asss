app.layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "row",
        "height": "100vh",
        "overflow": "hidden"
    },
    children=[

        # ===== لوحة التحكم =====
        html.Div(
            style={
                "flex": "0 0 24%",
                "padding": "15px",
                "backgroundColor": "#f5f7fa",
                "overflowY": "auto",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.15)"
            },
            children=[
                html.H2("🎛️ اختر النموذج من الأسفل"),

                dcc.Dropdown(
                    id="model",
                    options=[
                        {"label": "مسطح", "value": "flat"},
                        {"label": "كروي", "value": "curved"}
                    ],
                    value="flat"
                ),

                html.Br(),

                html.Label("ارتفاع الجسم"),
                dcc.Slider(id="obj", min=1, max=100, value=50),

                html.Label("ارتفاع العين"),
                dcc.Slider(id="eye", min=0.1, max=10, value=1.7),

                html.Label("المسافة"),
                dcc.Slider(id="dist", min=1, max=100, value=20),

                html.Label("التكبير"),
                dcc.Slider(id="zoom", min=0, max=5, value=0),

                html.Label("الارتفاع"),
                dcc.Slider(id="alt", min=0, max=50, value=10),

                html.Div(id="info", style={"marginTop": "15px"}),

                html.Hr(),
                html.P("برمجة وتطوير: عدناني"),
                html.P("X: @aale1164")
            ]
        ),

        # ===== الرسم البياني (يمين - ثابت أعلى) =====
        html.Div(
            style={
                "flex": "1",
                "padding": "10px",
                "height": "100vh"
            },
            children=[
                dcc.Graph(
                    id="graph",
                    style={
                        "height": "100%",
                        "width": "100%"
                    }
                )
            ]
        )

    ]
)
