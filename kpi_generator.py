import pandas as pd
import numpy as np


def generate_kpis(df):

    kpis = {}

    # Find numerical columns
    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    # If there are no numerical columns
    if not numeric_columns:
        return kpis

    # Generate KPIs for numerical columns
    for column in numeric_columns:

        series = df[column].dropna()

        if series.empty:
            continue

        kpis[column] = {
            "sum": float(series.sum()),
            "average": float(series.mean()),
            "minimum": float(series.min()),
            "maximum": float(series.max()),
            "count": int(series.count())
        }

    return kpis