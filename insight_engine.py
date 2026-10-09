import pandas as pd
import numpy as np


# =========================================================
# COLUMN DETECTION
# =========================================================

def find_numeric_columns(df):
    """
    Find all numeric columns in the dataset.
    """
    return df.select_dtypes(include=np.number).columns.tolist()


def find_categorical_columns(df):
    """
    Find categorical/text columns.

    Numeric columns are excluded.
    Date and date-like text columns are excluded.
    Text, category, and boolean columns are treated
    as categorical.
    """

    categorical_columns = []

    for column in df.columns:

        # -------------------------------------------------
        # Skip numeric columns
        # -------------------------------------------------
        if pd.api.types.is_numeric_dtype(df[column]):
            continue

        # -------------------------------------------------
        # Skip actual datetime columns
        # -------------------------------------------------
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            continue

        # -------------------------------------------------
        # Check whether text column is actually a date
        # -------------------------------------------------
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

            # If 80% or more values look like dates,
            # treat the column as a date column, not categorical.
            if valid_ratio >= 0.8:
                continue

        # -------------------------------------------------
        # Keep genuine categorical columns
        # -------------------------------------------------
        if (
            df[column].dtype == "object"
            or pd.api.types.is_string_dtype(df[column])
            or pd.api.types.is_categorical_dtype(df[column])
            or pd.api.types.is_bool_dtype(df[column])
        ):
            categorical_columns.append(column)

    return categorical_columns


def find_date_column(df):
    """
    Detect the first date-like column.
    """

    for column in df.columns:

        # -------------------------------------------------
        # Already a datetime column
        # -------------------------------------------------
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            return column

        # -------------------------------------------------
        # Try to detect dates stored as text
        # -------------------------------------------------
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


# =========================================================
# MAIN NUMERIC COLUMN
# =========================================================

def find_main_numeric_column(df):
    """
    Select the main numeric column.

    Preference:
    1. Sales
    2. Revenue
    3. Amount
    4. Profit
    5. Income
    6. Price
    7. Value
    8. First numeric column
    """

    numeric_columns = find_numeric_columns(df)

    if not numeric_columns:
        return None

    preferred_names = [
        "sales",
        "revenue",
        "amount",
        "profit",
        "income",
        "price",
        "value"
    ]

    for preferred in preferred_names:

        for column in numeric_columns:

            if column.lower().strip() == preferred:
                return column

    return numeric_columns[0]


# =========================================================
# MAIN CATEGORY COLUMN
# =========================================================

def find_main_category(df):
    """
    Select the main categorical column.

    Preference:
    1. Region
    2. Category
    3. Product
    4. Department
    5. Segment
    6. Type
    7. First categorical column
    """

    categorical_columns = find_categorical_columns(df)

    if not categorical_columns:
        return None

    preferred_names = [
        "region",
        "category",
        "product",
        "department",
        "segment",
        "type"
    ]

    for preferred in preferred_names:

        for column in categorical_columns:

            if column.lower().strip() == preferred:
                return column

    return categorical_columns[0]


# =========================================================
# NUMERIC ANALYSIS
# =========================================================

def analyze_numeric_column(df, column):
    """
    Calculate verified statistics for a numeric column.
    """

    if column is None:
        return {}

    if column not in df.columns:
        return {}

    series = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if series.empty:
        return {}

    return {
        "column": column,
        "total": float(series.sum()),
        "average": float(series.mean()),
        "minimum": float(series.min()),
        "maximum": float(series.max()),
        "count": int(series.count())
    }


# =========================================================
# CATEGORY PERFORMANCE
# =========================================================

def analyze_category_performance(
    df,
    category_column,
    numeric_column
):
    """
    Calculate verified totals by category.
    """

    if category_column is None:
        return {}

    if numeric_column is None:
        return {}

    if category_column not in df.columns:
        return {}

    if numeric_column not in df.columns:
        return {}

    grouped = (
        df.groupby(category_column)[numeric_column]
        .sum()
        .sort_values(ascending=False)
    )

    if grouped.empty:
        return {}

    highest_category = grouped.index[0]
    highest_value = float(grouped.iloc[0])

    lowest_category = grouped.index[-1]
    lowest_value = float(grouped.iloc[-1])

    return {
        "category_column": category_column,
        "numeric_column": numeric_column,
        "highest_category": highest_category,
        "highest_value": highest_value,
        "lowest_category": lowest_category,
        "lowest_value": lowest_value,
        "category_totals": {
            str(category): float(value)
            for category, value in grouped.items()
        }
    }


# =========================================================
# VERIFIED FINDINGS FOR AI
# =========================================================

def generate_verified_findings(df):
    """
    Create clearly labelled verified findings.

    These findings are passed to the AI as a locked
    collection of facts.

    The AI should not calculate or infer anything
    beyond these facts.
    """

    findings = []

    # =====================================================
    # DATASET INFORMATION
    # =====================================================

    findings.append(
        f"Dataset rows = {int(df.shape[0])}."
    )

    findings.append(
        f"Dataset columns = {int(df.shape[1])}."
    )

    # =====================================================
    # DETECT COLUMNS
    # =====================================================

    numeric_columns = find_numeric_columns(df)

    categorical_columns = find_categorical_columns(df)

    date_column = find_date_column(df)

    # =====================================================
    # MAIN COLUMNS
    # =====================================================

    main_numeric = find_main_numeric_column(df)

    main_category = find_main_category(df)

    # =====================================================
    # MAIN NUMERIC FINDINGS
    # =====================================================

    if main_numeric:

        series = pd.to_numeric(
            df[main_numeric],
            errors="coerce"
        ).dropna()

        if not series.empty:

            total = float(series.sum())

            average = float(series.mean())

            minimum = float(series.min())

            maximum = float(series.max())

            findings.append(
                f"Total {main_numeric} = {total:.2f}."
            )

            findings.append(
                f"Overall average {main_numeric} = {average:.2f}."
            )

            findings.append(
                f"Highest individual {main_numeric} value = "
                f"{maximum:.2f}."
            )

            findings.append(
                f"Lowest individual {main_numeric} value = "
                f"{minimum:.2f}."
            )

    # =====================================================
    # CATEGORY / REGION FINDINGS
    # =====================================================

    if main_category and main_numeric:

        grouped = (
            df.groupby(main_category)[main_numeric]
            .sum()
            .sort_values(ascending=False)
        )

        if not grouped.empty:

            highest_category = grouped.index[0]

            highest_value = float(
                grouped.iloc[0]
            )

            lowest_category = grouped.index[-1]

            lowest_value = float(
                grouped.iloc[-1]
            )

            findings.append(
                f"Highest {main_category} "
                f"{main_numeric} total = "
                f"{highest_category} with "
                f"{highest_value:.2f}."
            )

            findings.append(
                f"Lowest {main_category} "
                f"{main_numeric} total = "
                f"{lowest_category} with "
                f"{lowest_value:.2f}."
            )

    # =====================================================
    # DATA QUALITY
    # =====================================================

    missing_values = int(
        df.isnull()
        .sum()
        .sum()
    )

    duplicate_rows = int(
        df.duplicated()
        .sum()
    )

    findings.append(
        f"Total missing values = "
        f"{missing_values}."
    )

    findings.append(
        f"Total duplicate rows = "
        f"{duplicate_rows}."
    )

    # =====================================================
    # RETURN FINDINGS
    # =====================================================

    return "\n".join(
        f"- {finding}"
        for finding in findings
    )