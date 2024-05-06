import plotly.express as px
from plotly.graph_objects import Figure
import pandas as pd


def generate_total_required_cash_graph(
    data: pd.DataFrame, total_table: pd.DataFrame, home_report: int
) -> Figure:
    fig = px.area(
        data,
        x="Offer",
        y="Expense cost",
        labels={"Expense cost": "Cost", "Offer": "Offer"},
        color="Expense",
        category_orders={"Expense": ["Legal fees", "Deposit", "LBTT", "Offers over"]},
        color_discrete_map={  # replaces default color mapping by value
            "Legal fees": "#636EFA",
            "Deposit": "#EF553B",
            "LBTT": "#00CC96",
            "Offers over": "#AB63FA",
        },
        hover_data={
            "Expense cost": ":3f",
            "Offer": False,
        },
        custom_data=["Offer", "Expense cost", "Expense"],
    )
    total_line = px.line(
        total_table,
        x="Offer",
        y="Total cash required",
        hover_data={"Offer": False, "Total cash required": ":f"},
        custom_data=["Offer", "Total cash required"],
    )
    total_line.update_traces(name="Total cash required")
    fig.add_traces(total_line.data)
    fig.add_vline(
        x=home_report,
        line_width=2,
        line_dash="dash",
        line_color="green",
        annotation_text=f"Home report value: £{round(home_report // 1000)}k",
    )
    fig.update_annotations(borderwidth=5)
    fig.update_layout(
        height=700,
        yaxis_title="Total cash required",
        hovermode="x unified",
    )  #
    fig.update_traces(hovertemplate="£%{customdata[1]:f}")
    return fig
