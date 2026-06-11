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


app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "backgroundColor": "#0f172a",
        "color": "white",
        "padding": "25px",
        "minHeight": "100vh",
    },
    children=[
        html.H1("📡 ViralRadar", style={"textAlign": "center", "fontSize": "42px"}),
        html.P(
            "Real-time viral trend detection dashboard for Reddit-style social media data",
            style={"textAlign": "center", "fontSize": "18px", "color": "#cbd5e1"},
        ),

        dcc.Interval(id="interval-refresh", interval=10 * 1000, n_intervals=0),

        html.Div(id="kpi-cards"),

        html.Br(),

        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"},
            children=[
                dcc.Graph(id="spike-chart"),
                dcc.Graph(id="mentions-chart"),
            ],
        ),

        html.Br(),

        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"},
            children=[
                dcc.Graph(id="sentiment-chart"),
                dcc.Graph(id="engagement-chart"),
            ],
        ),

        html.Br(),

        html.H2("🚨 Viral Alerts Table"),
        html.Div(id="alerts-table"),
    ],
)


@app.callback(
    [
        Output("kpi-cards", "children"),
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

    viral_count = alerts[alerts["viral_status"] == "VIRAL_ALERT"].shape[0]
    total_topics = alerts["topic"].nunique()
    top_topic = alerts.iloc[0]["topic"]
    top_spike = alerts.iloc[0]["spike_multiplier"]

    kpi_cards = html.Div(
        style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "15px"},
        children=[
            create_card("Total Topics", total_topics),
            create_card("Viral Alerts", viral_count),
            create_card("Top Topic", top_topic),
            create_card("Highest Spike", f"{top_spike}x"),
        ],
    )

    spike_fig = px.bar(
        alerts,
        x="topic",
        y="spike_multiplier",
        color="viral_status",
        title="Spike Multiplier by Topic",
    )
    style_fig(spike_fig)

    mentions_fig = px.bar(
        alerts,
        x="topic",
        y="recent_mentions",
        color="viral_status",
        title="Recent Mentions by Topic",
    )
    style_fig(mentions_fig)

    sentiment_fig = px.pie(
        posts,
        names="sentiment",
        title="Overall Sentiment Distribution",
    )
    style_fig(sentiment_fig)

    engagement_fig = px.scatter(
        alerts,
        x="avg_score",
        y="avg_comments",
        size="recent_mentions",
        color="viral_status",
        hover_name="topic",
        title="Engagement: Score vs Comments",
    )
    style_fig(engagement_fig)

    table = dash_table.DataTable(
        data=alerts.to_dict("records"),
        columns=[{"name": col, "id": col} for col in alerts.columns],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": "#1e293b",
            "color": "white",
            "fontWeight": "bold",
        },
        style_cell={
            "backgroundColor": "#0f172a",
            "color": "white",
            "border": "1px solid #334155",
            "padding": "10px",
            "textAlign": "left",
        },
        style_data_conditional=[
            {
                "if": {"filter_query": "{viral_status} = VIRAL_ALERT"},
                "backgroundColor": "#7f1d1d",
                "color": "white",
            }
        ],
    )

    return kpi_cards, spike_fig, mentions_fig, sentiment_fig, engagement_fig, table


def create_card(title, value):
    return html.Div(
        style={
            "backgroundColor": "#1e293b",
            "padding": "20px",
            "borderRadius": "14px",
            "textAlign": "center",
            "boxShadow": "0 4px 12px rgba(0,0,0,0.3)",
        },
        children=[
            html.H4(title, style={"color": "#94a3b8"}),
            html.H2(str(value), style={"color": "white"}),
        ],
    )


def style_fig(fig):
    fig.update_layout(
        paper_bgcolor="#1e293b",
        plot_bgcolor="#1e293b",
        font_color="white",
        title_font_size=20,
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True, port=8060)
