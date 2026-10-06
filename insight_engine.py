import pandas as pd
import numpy as np


# =====================================================
# FIND NUMERICAL COLUMNS
# =====================================================

def find_numeric_columns(df):

    return df.select_dtypes(
        include=np.number
    ).columns.tolist()


# =====================================================
# FIND DATE COLUMN
# =====================================================

def find_date_column(df):

    for column in df.columns:

        # Already datetime
        if pd.api.types.is_datetime64_any_dtype(
            df[column]
        ):
            return column

        # Try converting text to dates
        if (
            df[column].dtype == "object"
            or pd.api.types.is_string_dtype(
                df[column]
            )
        ):

            converted = pd.to_datetime(
                df[column],
                errors="coerce",
                format="mixed"
            )

            valid_ratio = (
                converted.notna().mean()
            )

            if valid_ratio >= 0.8:

                return column

    return None


# =====================================================
# FIND CATEGORICAL COLUMNS
# =====================================================

def find_categorical_columns(df):

    columns = []

    for column in df.columns:

        if pd.api.types.is_numeric_dtype(
            df[column]
        ):
            continue

        if column == find_date_column(df):
            continue

        if (
            df[column].dtype == "object"
            or pd.api.types.is_string_dtype(
                df[column]
            )
            or pd.api.types.is_categorical_dtype(
                df[column]
            )
            or pd.api.types.is_bool_dtype(
                df[column]
            )
        ):

            columns.append(column)

    return columns


# =====================================================
# FIND MAIN NUMERICAL COLUMN
# =====================================================

def find_main_numeric_column(df):

    numeric_columns = find_numeric_columns(df)

    if not numeric_columns:

        return None

    # Select the numerical column with
    # the largest total magnitude.
    column_scores = {}

    for column in numeric_columns:

        values = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()

        if values.empty:

            column_scores[column] = 0

        else:

            column_scores[column] = abs(
                values.sum()
            )

    return max(
        column_scores,
        key=column_scores.get
    )


# =====================================================
# FIND MAIN CATEGORY
# =====================================================

def find_main_category(df):

    categorical_columns = (
        find_categorical_columns(df)
    )

    if not categorical_columns:

        return None

    # Prefer columns with a reasonable
    # number of categories.
    candidates = []

    for column in categorical_columns:

        unique_count = (
            df[column]
            .nunique(dropna=True)
        )

        if 2 <= unique_count <= 20:

            candidates.append(
                (column, unique_count)
            )

    if candidates:

        # Prefer the column with the
        # highest number of useful categories.
        candidates.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return candidates[0][0]

    return categorical_columns[0]


# =====================================================
# CATEGORY PERFORMANCE ANALYSIS
# =====================================================

def analyze_category_performance(
    df,
    category_column,
    numeric_column
):

    if (
        category_column is None
        or numeric_column is None
    ):

        return {}

    grouped = (
        df.groupby(
            category_column
        )[numeric_column]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    if grouped.empty:

        return {}

    return {

        "category_column":
            category_column,

        "numeric_column":
            numeric_column,

        "highest_category":
            str(grouped.index[0]),

        "highest_value":
            float(grouped.iloc[0]),

        "lowest_category":
            str(grouped.index[-1]),

        "lowest_value":
            float(grouped.iloc[-1]),

        "category_totals":
            {
                str(index): float(value)
                for index, value
                in grouped.items()
            }

    }


# =====================================================
# NUMERICAL SUMMARY
# =====================================================

def analyze_numeric_column(
    df,
    numeric_column
):

    if numeric_column is None:

        return {}

    values = pd.to_numeric(
        df[numeric_column],
        errors="coerce"
    ).dropna()

    if values.empty:

        return {}

    return {

        "column":
            numeric_column,

        "total":
            float(values.sum()),

        "average":
            float(values.mean()),

        "minimum":
            float(values.min()),

        "maximum":
            float(values.max()),

        "count":
            int(values.count())

    }


# =====================================================
# MAIN INSIGHT ENGINE
# =====================================================

def generate_verified_findings(df):

    findings = {}

    # -------------------------------------------------
    # Basic dataset information
    # -------------------------------------------------

    findings["dataset"] = {

        "rows":
            int(df.shape[0]),

        "columns":
            int(df.shape[1]),

        "column_names":
            df.columns.tolist()

    }


    # -------------------------------------------------
    # Detect column types
    # -------------------------------------------------

    numeric_columns = (
        find_numeric_columns(df)
    )

    categorical_columns = (
        find_categorical_columns(df)
    )

    date_column = find_date_column(df)


    findings["column_detection"] = {

        "numeric_columns":
            numeric_columns,

        "categorical_columns":
            categorical_columns,

        "date_column":
            date_column

    }


    # -------------------------------------------------
    # Identify main columns
    # -------------------------------------------------

    main_numeric = (
        find_main_numeric_column(df)
    )

    main_category = (
        find_main_category(df)
    )


    findings["main_columns"] = {

        "main_numeric_column":
            main_numeric,

        "main_category_column":
            main_category

    }


    # -------------------------------------------------
    # Numerical analysis
    # -------------------------------------------------

    findings["main_numeric_analysis"] = (
        analyze_numeric_column(
            df,
            main_numeric
        )
    )


    # -------------------------------------------------
    # Category analysis
    # -------------------------------------------------

    findings["category_analysis"] = (
        analyze_category_performance(
            df,
            main_category,
            main_numeric
        )
    )


    # -------------------------------------------------
    # Data quality
    # -------------------------------------------------

    findings["data_quality"] = {

        "missing_values":
            int(
                df.isnull()
                .sum()
                .sum()
            ),

        "duplicate_rows":
            int(
                df.duplicated()
                .sum()
            )

    }


    return findings