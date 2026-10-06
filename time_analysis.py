import pandas as pd
import numpy as np


def find_date_column(df):

    for column in df.columns:

        # Already a datetime column
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            return column

        # Try converting text to dates
        if (
            df[column].dtype == "object"
            or pd.api.types.is_string_dtype(df[column])
        ):

            converted = pd.to_datetime(
                df[column],
                errors="coerce",
                format="mixed"
            )

            valid_ratio = converted.notna().mean()

            if valid_ratio >= 0.8:
                return column

    return None


def find_numeric_columns(df):

    return df.select_dtypes(
        include=np.number
    ).columns.tolist()


def analyze_time_data(df):

    date_column = find_date_column(df)

    if date_column is None:
        return {
            "error": "No date column detected."
        }

    numeric_columns = find_numeric_columns(df)

    if not numeric_columns:
        return {
            "error": "No numerical columns detected."
        }

    data = df.copy()

    data[date_column] = pd.to_datetime(
        data[date_column],
        errors="coerce",
        format="mixed"
    )

    data = data.dropna(
        subset=[date_column]
    )

    if data.empty:
        return {
            "error": "No valid dates found."
        }

    results = {
        "date_column": date_column,
        "numeric_columns": numeric_columns
    }

    # -----------------------------------------
    # Monthly analysis
    # -----------------------------------------

    monthly = {}

    for column in numeric_columns:

        monthly_data = (
            data.groupby(
                data[date_column].dt.to_period("M")
            )[column]
            .sum()
            .sort_index()
        )

        monthly[column] = {
            str(period): float(value)
            for period, value in monthly_data.items()
        }

    results["monthly"] = monthly

    # -----------------------------------------
    # Yearly analysis
    # -----------------------------------------

    yearly = {}

    for column in numeric_columns:

        yearly_data = (
            data.groupby(
                data[date_column].dt.year
            )[column]
            .sum()
            .sort_index()
        )

        yearly[column] = {
            str(year): float(value)
            for year, value in yearly_data.items()
        }

    results["yearly"] = yearly

    # -----------------------------------------
    # Best and worst month
    # -----------------------------------------

    best_worst = {}

    for column in numeric_columns:

        monthly_data = (
            data.groupby(
                data[date_column].dt.to_period("M")
            )[column]
            .sum()
            .sort_index()
        )

        if not monthly_data.empty:

            best_period = monthly_data.idxmax()
            worst_period = monthly_data.idxmin()

            best_worst[column] = {
                "best_month": str(best_period),
                "best_value": float(
                    monthly_data.max()
                ),
                "worst_month": str(worst_period),
                "worst_value": float(
                    monthly_data.min()
                )
            }

    results["best_worst"] = best_worst

    return results