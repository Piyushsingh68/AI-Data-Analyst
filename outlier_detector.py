import pandas as pd
import numpy as np


def detect_outliers(df):

    outliers = {}

    # Find numerical columns
    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    for column in numeric_columns:

        # Remove missing values
        values = df[column].dropna()

        # Need enough values for meaningful detection
        if len(values) < 4:
            continue

        # Calculate Q1 and Q3
        Q1 = values.quantile(0.25)
        Q3 = values.quantile(0.75)

        # Calculate IQR
        IQR = Q3 - Q1

        # Calculate boundaries
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Find outliers
        outlier_values = values[
            (values < lower_bound) |
            (values > upper_bound)
        ]

        if len(outlier_values) > 0:

            outliers[column] = {
                "count": int(len(outlier_values)),
                "values": outlier_values.tolist(),
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound)
            }

    return outliers