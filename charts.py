import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =====================================================
# DATE COLUMN DETECTION
# =====================================================

def find_date_columns(df):

    datetime_columns = []

    for column in df.columns:

        # Already a datetime column
        if pd.api.types.is_datetime64_any_dtype(df[column]):

            datetime_columns.append(column)

            continue

        # Try converting text/object columns
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

            # Consider it a date column if
            # at least 80% of values are valid dates
            if valid_ratio >= 0.8:

                datetime_columns.append(column)

    return datetime_columns


# =====================================================
# GENERATE CHARTS
# =====================================================

def generate_charts(df):

    charts = []

    # =================================================
    # DETECT NUMERICAL COLUMNS
    # =================================================

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()


    # =================================================
    # DETECT CATEGORICAL COLUMNS
    # =================================================

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()


    # =================================================
    # DETECT DATE COLUMNS
    # =================================================

    datetime_columns = find_date_columns(df)


    # =================================================
    # 1. CATEGORICAL + NUMERICAL
    # BAR CHART
    # =================================================

    if categorical_columns and numeric_columns:

        category = categorical_columns[0]

        number = numeric_columns[0]

        grouped_data = (
            df.groupby(category)[number]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
        )

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        grouped_data.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            f"{number} by {category}"
        )

        ax.set_xlabel(
            category
        )

        ax.set_ylabel(
            number
        )

        plt.xticks(
            rotation=45
        )

        plt.tight_layout()

        charts.append(
            ("bar", fig)
        )


    # =================================================
    # 2. DATE + NUMERICAL
    # LINE CHART
    # =================================================

    if datetime_columns and numeric_columns:

        date_column = datetime_columns[0]

        number = numeric_columns[0]


        data = df.copy()

        data[date_column] = pd.to_datetime(
            data[date_column],
            errors="coerce",
            format="mixed"
        )

        data = data.dropna(
            subset=[date_column]
        )


        date_data = (
            data.groupby(date_column)[number]
            .sum()
            .sort_index()
        )


        if len(date_data) >= 2:

            fig, ax = plt.subplots(
                figsize=(8, 5)
            )

            date_data.plot(
                kind="line",
                marker="o",
                ax=ax
            )

            ax.set_title(
                f"{number} over Time"
            )

            ax.set_xlabel(
                date_column
            )

            ax.set_ylabel(
                number
            )

            plt.xticks(
                rotation=45
            )

            plt.tight_layout()

            charts.append(
                ("line", fig)
            )


    # =================================================
    # 3. ACTUAL VALUES + TREND LINE
    # =================================================

    if datetime_columns and numeric_columns:

        date_column = datetime_columns[0]

        number = numeric_columns[0]


        data = df.copy()


        # Convert date column
        data[date_column] = pd.to_datetime(
            data[date_column],
            errors="coerce",
            format="mixed"
        )


        # Remove invalid dates
        data = data.dropna(
            subset=[date_column]
        )


        # Group by date
        trend_data = (
            data.groupby(date_column)[number]
            .sum()
            .sort_index()
        )


        # Need at least two points
        if len(trend_data) >= 2:

            # X values
            x = np.arange(
                len(trend_data),
                dtype=float
            )


            # Y values
            y = trend_data.values.astype(
                float
            )


            # Linear regression
            slope, intercept = np.polyfit(
                x,
                y,
                1
            )


            # Calculate trend line
            trend_line = (
                slope * x
                + intercept
            )


            # Create chart
            fig, ax = plt.subplots(
                figsize=(9, 5)
            )


            # Actual values
            ax.plot(
                trend_data.index,
                trend_data.values,
                marker="o",
                label="Actual"
            )


            # Trend line
            ax.plot(
                trend_data.index,
                trend_line,
                linestyle="--",
                linewidth=2,
                label="Trend Line"
            )


            # Chart title
            ax.set_title(
                f"{number} — Actual vs Trend"
            )


            ax.set_xlabel(
                date_column
            )

            ax.set_ylabel(
                number
            )


            # Legend
            ax.legend()


            # Rotate dates
            plt.xticks(
                rotation=45
            )


            plt.tight_layout()


            # Add chart
            charts.append(
                ("trend", fig)
            )


    # =================================================
    # 4. TWO NUMERICAL COLUMNS
    # SCATTER PLOT
    # =================================================

    if len(numeric_columns) >= 2:

        x_column = numeric_columns[0]

        y_column = numeric_columns[1]


        fig, ax = plt.subplots(
            figsize=(8, 5)
        )


        ax.scatter(
            df[x_column],
            df[y_column]
        )


        ax.set_title(
            f"{y_column} vs {x_column}"
        )


        ax.set_xlabel(
            x_column
        )

        ax.set_ylabel(
            y_column
        )


        plt.tight_layout()


        charts.append(
            ("scatter", fig)
        )


    # =================================================
    # 5. NUMERICAL COLUMN
    # HISTOGRAM
    # =================================================

    if numeric_columns:

        number = numeric_columns[0]


        fig, ax = plt.subplots(
            figsize=(8, 5)
        )


        ax.hist(
            df[number].dropna(),
            bins=10
        )


        ax.set_title(
            f"Distribution of {number}"
        )


        ax.set_xlabel(
            number
        )

        ax.set_ylabel(
            "Frequency"
        )


        plt.tight_layout()


        charts.append(
            ("histogram", fig)
        )


    # =================================================
    # RETURN ALL CHARTS
    # =================================================

    return charts