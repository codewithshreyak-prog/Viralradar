import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table, Input, Output


ALERTS_PATH = "data/processed/viral_alerts.csv"
POSTS_PATH = "data/processed/enriched_posts.csv"

app = Dash(__name__)
app.title = "ViralRadar"


def load_data():
    alerts = pd.read_csv(ALERTS_PATH)
    posts = pd.read_csv(POSTS_PATH)

    alerts["spike_multiplier"] = alerts["spike_multiplier"].round(2)
    alerts["spike_percentage"] = alerts["spike_percentage"].round(2)
    alerts["avg_score"] = alerts["avg_score"].round(2)
    alerts["avg_comments"] = alerts["avg_comments"].round(2)
    alerts["avg_sentiment_score"] = alerts["avg_sentiment_score"].round(3)

    return alerts, posts


def create_card(title, value, subtitle):
    return html.Div(
        style={
            "background": "linear-gradient(135deg, #111827, #1e293b)",
            "border": "1px solid #334155",
            "borderRadius": "18px",
            "padding": "22px",
            "boxShadow": "0 10px 25px rgba(0,0,0,0.35)",
        },
        children=[
            html.Div(
                title,
                style={
                    "fontSize": "14px",
                    "color": "#94a3b8",
                    "fontWeight": "600",
                },
            ),
            html.Div(
                str(value),
                style={
                    "fontSize": "32px",
                    "fontWeight": "800",
                    "marginTop": "8px",
                    "color": "#f8fafc",
                },
            ),
            html.Div(
                subtitle,
                style={
                    "fontSize": "13px",
                    "color": "#64748b",
                    "marginTop": "6px",
                },
            ),
        ],
    )


def style_fig(fig):
    fig.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="#e5e7eb",
        title_font_color="#f8fafc",
        title_font_size=19,
        margin=dict(l=35, r=25, t=55, b=35),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor="#1f2937")
    fig.update_yaxes(gridcolor="#1f2937")
    return fig


app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "background": "radial-gradient(circle at top left, #1e3a8a 0, #020617 34%, #020617 100%)",
        "color": "#f8fafc",
        "minHeight": "100vh",
        "padding": "30px",
    },
    children=[
        dcc.Interval(
            id="interval-refresh",
            interval=10 * 1000,
            n_intervals=0,
        ),

        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "marginBottom": "25px",
            },
            children=[
                html.Div(
                    children=[
                        html.H1(
                            "📡 ViralRadar",
                            style={
                                "fontSize": "46px",
                                "margin": "0",
                                "fontWeight": "900",
                                "letterSpacing": "-1px",
                            },
                        ),
                        html.P(
                            "Early viral trend detection using sentiment, engagement, and spike analytics",
                            style={
                                "color": "#cbd5e1",
                                "fontSize": "17px",
                                "marginTop": "8px",
                            },
                        ),
                    ]
                ),
                html.Div(
                    "LIVE DEMO MODE",
                    style={
                        "backgroundColor": "#dc2626",
                        "color": "white",
                        "padding": "10px 16px",
                        "borderRadius": "999px",
                        "fontWeight": "800",
                        "fontSize": "13px",
                        "boxShadow": "0 0 18px rgba(220,38,38,0.55)",
                    },
                ),
            ],
        ),

        html.Div(id="kpi-cards"),

        html.Div(
            id="top-alert",
            style={
                "background": "linear-gradient(135deg, #7f1d1d, #111827)",
                "border": "1px solid #ef4444",
                "borderRadius": "18px",
                "padding": "22px",
                "marginBottom": "22px",
                "boxShadow": "0 10px 25px rgba(127,29,29,0.35)",
            },
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1.1fr 0.9fr",
                "gap": "22px",
                "marginBottom": "22px",
            },
            children=[
                html.Div(
                    style={
                        "backgroundColor": "#111827",
                        "border": "1px solid #334155",
                        "borderRadius": "18px",
                        "padding": "12px",
                    },
                    children=[dcc.Graph(id="spike-chart")],
                ),
                html.Div(
                    style={
                        "backgroundColor": "#111827",
                        "border": "1px solid #334155",
                        "borderRadius": "18px",
                        "padding": "12px",
                    },
                    children=[dcc.Graph(id="sentiment-chart")],
                ),
            ],
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "22px",
                "marginBottom": "22px",
            },
            children=[
                html.Div(
                    style={
                        "backgroundColor": "#111827",
                        "border": "1px solid #334155",
                        "borderRadius": "18px",
                        "padding": "12px",
                    },
                    children=[dcc.Graph(id="mentions-chart")],
                ),
                html.Div(
                    style={
                        "backgroundColor": "#111827",
                        "border": "1px solid #334155",
                        "borderRadius": "18px",
                        "padding": "12px",
                    },
                    children=[dcc.Graph(id="engagement-chart")],
                ),
            ],
        ),

        html.Div(
            style={
                "backgroundColor": "#111827",
                "border": "1px solid #334155",
                "borderRadius": "18px",
                "padding": "22px",
                "boxShadow": "0 10px 25px rgba(0,0,0,0.35)",
            },
            children=[
                html.H2(
                    "🚨 Viral Alerts",
                    style={
                        "marginTop": "0",
                        "marginBottom": "6px",
                    },
                ),
                html.P(
                    "Topics are flagged when recent mentions rise above their expected baseline.",
                    style={
                        "color": "#94a3b8",
                        "marginTop": "0",
                    },
                ),
                html.Div(id="alerts-table"),
            ],
        ),
    ],
)


@app.callback(
    [
        Output("kpi-cards", "children"),
        Output("top-alert", "children"),
        Output("spike-chart", "figure"),
        Output("mentions-chart", "figure"),
        Output("sentiment-chart", "figure"),
        Output("engagement-chart", "figure"),
        Output("alerts-table", "children"),
    ],
    Input("interval-refresh", "n_intervals"),
)
def update_dashboard(n):
    alerts, posts = load_data()

    viral_alerts = alerts[alerts["viral_status"] == "VIRAL_ALERT"]
    viral_count = viral_alerts.shape[0]
    total_topics = alerts["topic"].nunique()
    total_posts = posts.shape[0]

    top_row = alerts.iloc[0]
    top_topic = top_row["topic"]
    top_spike = top_row["spike_multiplier"]
    top_percent = top_row["spike_percentage"]

    kpi_cards = html.Div(
        style={
            "display": "grid",
            "gridTemplateColumns": "repeat(4, 1fr)",
            "gap": "18px",
            "marginBottom": "22px",
        },
        children=[
            create_card("Total Posts", total_posts, "Analyzed in current dataset"),
            create_card("Detected Topics", total_topics, "Unique monitored topics"),
            create_card("Viral Alerts", viral_count, "Topics above spike threshold"),
            create_card("Highest Spike", f"{top_spike}x", f"{top_topic} is leading"),
        ],
    )

    top_alert = html.Div(
        children=[
            html.Div(
                "🔥 Top Viral Signal",
                style={
                    "color": "#fecaca",
                    "fontSize": "14px",
                    "fontWeight": "700",
                },
            ),
            html.H2(
                top_topic,
                style={
                    "margin": "8px 0 4px 0",
                    "fontSize": "30px",
                },
            ),
            html.Div(
                f"Spike multiplier: {top_spike}x | Spike percentage: {top_percent}%",
                style={
                    "color": "#fca5a5",
                    "fontSize": "16px",
                },
            ),
            html.P(
                "This topic is showing abnormal growth compared to its recent baseline activity.",
                style={
                    "color": "#e5e7eb",
                    "marginBottom": "0",
                },
            ),
        ]
    )

    spike_fig = px.bar(
        alerts,
        x="topic",
        y="spike_multiplier",
        color="viral_status",
        title="Spike Multiplier by Topic",
        text="spike_multiplier",
    )
    spike_fig.update_traces(textposition="outside")
    spike_fig.update_layout(
        xaxis_title="",
        yaxis_title="Spike Multiplier",
    )
    style_fig(spike_fig)

    mentions_fig = px.bar(
        alerts,
        x="topic",
        y="recent_mentions",
        color="viral_status",
        title="Recent Mentions by Topic",
        text="recent_mentions",
    )
    mentions_fig.update_traces(textposition="outside")
    mentions_fig.update_layout(
        xaxis_title="",
        yaxis_title="Recent Mentions",
    )
    style_fig(mentions_fig)

    sentiment_fig = px.pie(
        posts,
        names="sentiment",
        hole=0.45,
        title="Sentiment Distribution",
    )
    style_fig(sentiment_fig)

    engagement_fig = px.scatter(
        alerts,
        x="avg_score",
        y="avg_comments",
        size="recent_mentions",
        color="viral_status",
        hover_name="topic",
        title="Engagement Signal: Score vs Comments",
    )
    engagement_fig.update_layout(
        xaxis_title="Average Score",
        yaxis_title="Average Comments",
    )
    style_fig(engagement_fig)

    table = dash_table.DataTable(
        data=alerts.to_dict("records"),
        columns=[
            {"name": "Topic", "id": "topic"},
            {"name": "Recent Mentions", "id": "recent_mentions"},
            {"name": "Expected Mentions", "id": "expected_mentions"},
            {"name": "Spike Multiplier", "id": "spike_multiplier"},
            {"name": "Spike %", "id": "spike_percentage"},
            {"name": "Avg Sentiment", "id": "avg_sentiment_score"},
            {"name": "Avg Score", "id": "avg_score"},
            {"name": "Avg Comments", "id": "avg_comments"},
            {"name": "Status", "id": "viral_status"},
        ],
        page_size=10,
        style_table={
            "overflowX": "auto",
        },
        style_header={
            "backgroundColor": "#0f172a",
            "color": "#f8fafc",
            "fontWeight": "bold",
            "border": "1px solid #334155",
        },
        style_cell={
            "backgroundColor": "#111827",
            "color": "#e5e7eb",
            "border": "1px solid #334155",
            "padding": "12px",
            "textAlign": "left",
            "fontSize": "14px",
        },
        style_data_conditional=[
            {
                "if": {"filter_query": "{viral_status} = VIRAL_ALERT"},
                "backgroundColor": "#450a0a",
                "color": "#fecaca",
                "fontWeight": "700",
            }
        ],
    )

    return (
        kpi_cards,
        top_alert,
        spike_fig,
        mentions_fig,
        sentiment_fig,
        engagement_fig,
        table,
    )


if __name__ == "__main__":
    app.run(debug=True, port=8060)