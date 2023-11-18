"""This module includes the functions to make datasets for bank marketing ML applications.

Examples
--------
    >>> from bank_marketing.data.make_datasets import make_bank_marketing_dataframe
    >>> bank_db_file = r"/path/to/bank_marketing.db"
    >>> socio_eco_data_file = r"/path/to/socio_economic_indices_data.csv"
    >>> df = make_bank_marketing_dataframe(bank_db_file, socio_eco_data_file)

"""
import os
from typing import Tuple

import pandas as pd
from bank_marketing.sqlite_db.bank_marketing_dal import BankMarketingDAL


def extract_credit_features(row: pd.Series) -> Tuple[str, str]:
    """Deduce if the customer has any credit or any default of payment
        based on two columns: status and default penalites that are present
        in loans and mortgages data tables.

    Args:
    ----
        row (pd.Series): mortgage/loan entry (row) for one customer

    Returns:
    -------
        Tuple[str, str]: has loan (yes/no/unknown), had default (yes/no/unknown)
    """
    loan, default = None, None
    if row["status"] == "paid":
        loan = "no"
    elif row["status"] == "ongoing":
        loan = "yes"
    elif row["status"] == "unknown":
        loan = "unknown"
    if row["default_penalties"] != row["default_penalties"] or not (row["default_penalties"]):
        default = "unknown"
    elif row["default_penalties"] == 0:
        default = "no"
    elif row["default_penalties"] > 0:
        default = "yes"
    return loan, default


def merge_defaults(row: pd.Series) -> str:
    """Merge two default columns resulting from the fusion of loans and mortgages dataframes

    Args:
    ----
        row (pd.Series): entry (row) for one customer aggregated data

    Returns:
    -------
        str: has default overall (yes/no/unknown)
    """
    if row["default_x"] == "yes" or row["default_y"] == "yes":
        return "yes"
    elif row["default_x"] == "unknown" or row["default_y"] == "unknown":
        return "unknown"
    elif row["default_x"] == "no" and row["default_y"] == "no":
        return "no"
    raise ValueError


def make_bank_marketing_dataframe(bank_db_file: os.PathLike, socio_eco_data_file: os.PathLike) -> pd.DataFrame:
    """Extract and build data from bank database and socio economical indices data files

    Args:
    ----
        bank_db_file (os.PathLike): Bank database sqlite file path
        socio_eco_data_file (os.PathLike): Socio-Economical CSV data file path

    Returns:
    -------
        pd.DataFrame: customers dataframe (personal infos + loans +
                                           mortgages + campaign missions +
                                           socio economical indices)
    """
    socio_eco_df = pd.read_csv(socio_eco_data_file, sep=";")
    bank_marketing_dl = BankMarketingDAL(bank_db_file)
    loans_df = bank_marketing_dl.loans.fetch_all(to_dataframe=True)
    mortgages_df = bank_marketing_dl.mortgages.fetch_all(to_dataframe=True)
    mortgages_df[["housing", "default"]] = mortgages_df.apply(extract_credit_features, axis=1, result_type="expand")
    loans_df[["loan", "default"]] = loans_df.apply(extract_credit_features, axis=1, result_type="expand")
    customers_df = bank_marketing_dl.customers.fetch_all(to_dataframe=True)
    campaign_missions_df = bank_marketing_dl.campaign_missions.fetch_all_done(to_dataframe=True)
    dataframe = pd.merge(customers_df, campaign_missions_df, left_on="id", right_on="customer_id")
    dataframe = pd.merge(dataframe, socio_eco_df, left_on="comm_date", right_on="date")
    dataframe = pd.merge(dataframe, mortgages_df[["customer_id", "housing", "default"]], on="customer_id")
    dataframe = pd.merge(dataframe, loans_df[["customer_id", "loan", "default"]], on="customer_id")
    dataframe["default"] = dataframe.apply(merge_defaults, axis=1)
    dataframe = dataframe.drop(columns=["default_x", "default_y"])
    return dataframe
