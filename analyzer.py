import pandas as pd
import numpy as np


def analyze_dataset(df):

    analysis = {}

    # --------------------------------------------------
    # 1. Basic information
    # --------------------------------------------------

    analysis["rows"] = df.shape[0]
    analysis["columns"] = df.shape[1]
    analysis["column_names"] = df.columns.tolist()

    # --------------------------------------------------
    # 2. Detect date columns
    # --------------------------------------------------

    datetime_columns = []

    for column in df.columns:

        # Already a datetime column
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            datetime_columns.append(column)
            continue

        # Check text/string columns
        if (
            df[column].dtype == "object"
            or pd.api.types.is_string_dtype(df[column])
        ):

            # Try converting the column to dates
            converted = pd.to_datetime(
                df[column],
                errors="coerce",
                format="mixed"
            )

            valid_ratio = converted.notna().mean()

            # If at least 80% of values look like dates
            if valid_ratio >= 0.8:
                datetime_columns.append(column)

    # --------------------------------------------------
    # 3. Detect numeric columns
    # --------------------------------------------------

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    # --------------------------------------------------
    # 4. Detect categorical columns
    # --------------------------------------------------

    categorical_columns = []

    for column in df.columns:

        # Skip date columns
        if column in datetime_columns:
            continue

        # Skip numeric columns
        if column in numeric_columns:
            continue

        # Detect categorical/text/boolean columns
        if (
            df[column].dtype == "object"
            or pd.api.types.is_string_dtype(df[column])
            or pd.api.types.is_categorical_dtype(df[column])
            or pd.api.types.is_bool_dtype(df[column])
        ):
            categorical_columns.append(column)

    analysis["numeric_columns"] = numeric_columns
    analysis["categorical_columns"] = categorical_columns
    analysis["datetime_columns"] = datetime_columns

    # --------------------------------------------------
    # 5. Missing values
    # --------------------------------------------------

    missing_values = df.isnull().sum()

    analysis["missing_values"] = {
        column: int(value)
        for column, value in missing_values.items()
        if value > 0
    }

    analysis["total_missing_values"] = int(
        df.isnull().sum().sum()
    )

    # --------------------------------------------------
    # 6. Duplicate rows
    # --------------------------------------------------

    analysis["duplicate_rows"] = int(
        df.duplicated().sum()
    )

    # --------------------------------------------------
    # 7. Unique values
    # --------------------------------------------------

    analysis["unique_values"] = {
        column: int(df[column].nunique())
        for column in df.columns
    }

    # --------------------------------------------------
    # 8. Numerical statistics
    # --------------------------------------------------

    if numeric_columns:

        statistics = df[numeric_columns].describe()

        analysis["statistics"] = statistics.to_dict()

    else:

        analysis["statistics"] = {}

    # --------------------------------------------------
    # 9. Categorical information
    # --------------------------------------------------

    categorical_summary = {}

    for column in categorical_columns:

        mode = df[column].mode()

        top_value = (
            mode.iloc[0]
            if not mode.empty
            else None
        )

        categorical_summary[column] = {
            "unique_count": int(
                df[column].nunique()
            ),
            "top_value": top_value
        }

    analysis["categorical_summary"] = (
        categorical_summary
    )

    # --------------------------------------------------
    # 10. Correlation
    # --------------------------------------------------

    if len(numeric_columns) >= 2:

        correlation = df[numeric_columns].corr()

        analysis["correlation"] = (
            correlation.to_dict()
        )

    else:

        analysis["correlation"] = {}

    return analysis