import pandas as pd
from typing import Tuple
from lbtt import compute_lbtt


def generate_base_offer_dataframe(home_report: float) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Offer": list(
                range(
                    round(int(home_report * 0.9), -3),
                    round(int(home_report * 1.2), -3),
                    1000,
                )
            )
        }
    )


def generate_offers_data(
    home_report: int, mortgage_deposit: int, legal_fees: float, ftb_status: bool
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    deposit_table = generate_base_offer_dataframe(home_report=home_report)
    deposit_table["Expense cost"] = mortgage_deposit
    deposit_table["Expense"] = "Deposit"

    legal_fee_table = generate_base_offer_dataframe(home_report=home_report)
    legal_fee_table["Expense cost"] = legal_fees
    legal_fee_table["Expense"] = "Legal fees"

    lbtt_table = generate_base_offer_dataframe(home_report=home_report)
    lbtt_table["Expense cost"] = lbtt_table["Offer"].apply(
        lambda offer: compute_lbtt(offer, ftb=ftb_status)
    )
    lbtt_table["Expense"] = "LBTT"

    oo_table = generate_base_offer_dataframe(home_report=home_report)
    oo_table["Expense cost"] = oo_table["Offer"].apply(
        lambda offer: max(offer - home_report, 0)
    )
    oo_table["Expense"] = "Offers over"

    total_table = generate_base_offer_dataframe(home_report=home_report)
    total_table["Total cash required"] = (
        deposit_table["Expense cost"]
        + legal_fee_table["Expense cost"]
        + lbtt_table["Expense cost"]
        + oo_table["Expense cost"]
    )

    data = pd.concat([deposit_table, lbtt_table, oo_table, legal_fee_table], axis=0)
    return data, total_table
