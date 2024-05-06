import streamlit as st
from src.footer import FOOTER
from src.data import generate_offers_data
from src.graph import generate_total_required_cash_graph

APP_TITLE = "Scottish offer calculator"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=":home:",
    layout="wide",
    menu_items={
        "Source code": "https://github.com/stuartburrell/scottish-offer-calculator",
        "Report a bug": "https://github.com/stuartburrell/scottish-offer-calculator/issues",
    },
)

st.sidebar.title(APP_TITLE)
st.sidebar.header("About")
st.sidebar.markdown(
    "This calculator helps you decide how much to offer on your new home, taking into account the different costs in Scotland."
)

st.sidebar.markdown("## Your purchase details")
ftb_status = st.sidebar.toggle("First-time buyer")
home_report = st.sidebar.number_input(
    "Home report value (£)",
    value=585_000,
    help="The valuation stated in the home report.",
    step=1000,
)
legal_fees = st.sidebar.number_input(
    "Legal fees (£)", value=1600, help="The conveyancing costs, not including LBTT."
)
ltv = st.sidebar.slider("Mortgage LTV (%)", value=90)
st.sidebar.markdown("## Mortgage summary")
mortgage_deposit = (1 - ltv / 100) * home_report
st.sidebar.markdown(f"**Deposit amount:** £{round(mortgage_deposit):,}")
st.sidebar.markdown(f"**Loan amount:** £{round(home_report - mortgage_deposit):,}")
st.sidebar.markdown(FOOTER, unsafe_allow_html=True)

data, total_table = generate_offers_data(
    home_report=home_report,
    mortgage_deposit=mortgage_deposit,
    legal_fees=legal_fees,
    ftb_status=ftb_status,
)

fig = generate_total_required_cash_graph(
    data=data, total_table=total_table, home_report=home_report
)
st.plotly_chart(fig, use_container_width=True)
