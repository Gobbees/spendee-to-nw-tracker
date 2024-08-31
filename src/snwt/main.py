import os
import argparse
from datetime import datetime
import pandas as pd

DEFAULT_FILE_NAME_DATE_TIME = datetime.now().strftime("%Y%m%dT%H%M%S")
DEFAULT_OUTPUT_INCOME_FILE_NAME = f"output-income-{DEFAULT_FILE_NAME_DATE_TIME}.csv"
DEFAULT_OUTPUT_EXPENSES_FILE_NAME = f"output-expenses-{DEFAULT_FILE_NAME_DATE_TIME}.csv"

OUTPUT_COLUMN_ORDER = ["Month", "Day", "Note", "Amount", "Category name", "Labels"]


def main():
    parser = argparse.ArgumentParser(
        prog="snwt - Spendee to Net-Worth-Tracker",
        description="Convers Spendee exports to personal net worth tracker",
    )

    parser.add_argument("input_file_path")
    parser.add_argument(
        "-out-income",
        "--output-income",
        default=DEFAULT_OUTPUT_INCOME_FILE_NAME,
    )
    parser.add_argument(
        "-out-expenses",
        "--output-expenses",
        default=DEFAULT_OUTPUT_EXPENSES_FILE_NAME,
    )
    args = parser.parse_args()
    print(args.input_file_path, args.output_income)

    if not os.path.isfile(args.input_file_path):
        raise Exception(
            f"Provided input file path {args.input_file_path} is not a file"
        )
    elif not args.input_file_path.endswith(".csv"):
        raise Exception(
            f"Provided input file path {args.input_file_path} is not a CSV file"
        )

    df = pd.read_csv(args.input_file_path)

    # date
    df["Month"] = pd.to_datetime(df["Date"]).apply(lambda date: date.month)
    df["Day"] = pd.to_datetime(df["Date"]).apply(lambda date: date.day)

    # cleanup df
    df.drop(columns=["Date", "Wallet", "Author", "Currency"], inplace=True)

    # split df
    income_df = df[df["Type"] == "Income"].copy()
    expenses_df = df[df["Type"] == "Expense"].copy()
    expenses_df["Amount"] = -df["Amount"]

    # cleanup both dfs
    income_df.drop(columns=["Type"], inplace=True)
    expenses_df.drop(columns=["Type"], inplace=True)

    # export
    income_df.to_csv(args.output_income, columns=OUTPUT_COLUMN_ORDER, index=False)
    expenses_df.to_csv(args.output_expenses, columns=OUTPUT_COLUMN_ORDER, index=False)
