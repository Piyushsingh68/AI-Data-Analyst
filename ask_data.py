import pandas as pd
import numpy as np
import requests


# ============================================================
# COLUMN DETECTION
# ============================================================

def find_column(df, question):

    question_lower = question.lower()

    # Exact column name match
    for column in df.columns:

        if str(column).lower() in question_lower:
            return column

    # Partial column name match
    for column in df.columns:

        column_words = (
            str(column)
            .lower()
            .replace("_", " ")
            .split()
        )

        if any(
            word in question_lower
            for word in column_words
            if len(word) > 2
        ):
            return column

    return None


def find_numeric_column(df, question=""):

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if not numeric_columns:
        return None

    if question:

        detected = find_column(
            df,
            question
        )

        if detected in numeric_columns:
            return detected

    priority_words = [
        "sales",
        "revenue",
        "profit",
        "income",
        "salary",
        "amount",
        "price",
        "cost",
        "quantity",
        "score",
        "marks",
        "age"
    ]

    for word in priority_words:

        for column in numeric_columns:

            if word in str(column).lower():
                return column

    return numeric_columns[0]


def find_categorical_column(df, question=""):

    categorical_columns = df.select_dtypes(
        include=[
            "object",
            "category",
            "bool"
        ]
    ).columns.tolist()

    if not categorical_columns:
        return None

    if question:

        detected = find_column(
            df,
            question
        )

        if detected in categorical_columns:
            return detected

    return categorical_columns[0]


def find_date_column(df):

    for column in df.columns:

        if pd.api.types.is_datetime64_any_dtype(
            df[column]
        ):
            return column

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


# ============================================================
# FIND CATEGORY VALUES MENTIONED IN QUESTION
# ============================================================

def find_mentioned_categories(df, question):

    categorical_columns = df.select_dtypes(
        include=[
            "object",
            "category",
            "bool"
        ]
    ).columns.tolist()

    question_lower = question.lower()

    matches = []

    for column in categorical_columns:

        for value in df[column].dropna().unique():

            value_text = str(value)

            if value_text.lower() in question_lower:

                matches.append(
                    (
                        column,
                        value
                    )
                )

    return matches


# ============================================================
# COMPARISON
# ============================================================

def calculate_comparison(
    df,
    question
):

    numeric_column = find_numeric_column(
        df,
        question
    )

    if numeric_column is None:
        return None

    mentioned = find_mentioned_categories(
        df,
        question
    )

    if len(mentioned) < 2:
        return None

    # Use the first categorical column containing
    # at least two mentioned values.

    selected_column = None
    selected_values = []

    for column, value in mentioned:

        if selected_column is None:

            selected_column = column
            selected_values = [value]

        elif column == selected_column:

            if value not in selected_values:
                selected_values.append(value)

    if (
        selected_column is None
        or len(selected_values) < 2
    ):
        return None

    grouped = (
        df.groupby(
            selected_column
        )[numeric_column]
        .sum()
    )

    first = selected_values[0]
    second = selected_values[1]

    if (
        first not in grouped.index
        or second not in grouped.index
    ):
        return None

    first_value = float(
        grouped.loc[first]
    )

    second_value = float(
        grouped.loc[second]
    )

    difference = abs(
        first_value - second_value
    )

    if first_value > second_value:

        higher = first
        lower = second

    elif second_value > first_value:

        higher = second
        lower = first

    else:

        return (
            f"**{first}** and **{second}** "
            f"have the same "
            f"{numeric_column}: "
            f"**{first_value:,.2f}**."
        )

    return (
        f"**{higher}** has higher "
        f"{numeric_column} than "
        f"**{lower}**.\n\n"

        f"- {first}: "
        f"**{first_value:,.2f}**\n"

        f"- {second}: "
        f"**{second_value:,.2f}**\n"

        f"- Difference: "
        f"**{difference:,.2f}**"
    )


# ============================================================
# TOP N
# ============================================================

def calculate_top_n(
    df,
    question
):

    numeric_column = find_numeric_column(
        df,
        question
    )

    category_column = find_categorical_column(
        df,
        question
    )

    if (
        numeric_column is None
        or category_column is None
    ):
        return None

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
        return None

    question_lower = question.lower()

    n = 5

    for number in range(1, 11):

        if f"top {number}" in question_lower:

            n = number
            break

    result = grouped.head(n)

    text = (
        f"### Top {n} "
        f"{category_column} by "
        f"{numeric_column}\n\n"
    )

    for index, value in result.items():

        text += (
            f"- **{index}**: "
            f"{value:,.2f}\n"
        )

    return text


# ============================================================
# BOTTOM N
# ============================================================

def calculate_bottom_n(
    df,
    question
):

    numeric_column = find_numeric_column(
        df,
        question
    )

    category_column = find_categorical_column(
        df,
        question
    )

    if (
        numeric_column is None
        or category_column is None
    ):
        return None

    grouped = (
        df.groupby(
            category_column
        )[numeric_column]
        .sum()
        .sort_values(
            ascending=True
        )
    )

    if grouped.empty:
        return None

    question_lower = question.lower()

    n = 5

    for number in range(1, 11):

        if f"bottom {number}" in question_lower:

            n = number
            break

    result = grouped.head(n)

    text = (
        f"### Bottom {n} "
        f"{category_column} by "
        f"{numeric_column}\n\n"
    )

    for index, value in result.items():

        text += (
            f"- **{index}**: "
            f"{value:,.2f}\n"
        )

    return text


# ============================================================
# GROUP ANALYSIS
# ============================================================

def calculate_group_analysis(
    df,
    question
):

    numeric_column = find_numeric_column(
        df,
        question
    )

    category_column = find_categorical_column(
        df,
        question
    )

    if (
        numeric_column is None
        or category_column is None
    ):
        return None

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
        return None

    question_lower = question.lower()

    # Highest
    if any(
        word in question_lower
        for word in [
            "highest",
            "best",
            "maximum",
            "max"
        ]
    ):

        index = grouped.idxmax()
        value = grouped.max()

        return (
            f"The highest "
            f"{numeric_column} is for "
            f"**{index}** with "
            f"**{value:,.2f}**."
        )

    # Lowest
    if any(
        word in question_lower
        for word in [
            "lowest",
            "worst",
            "minimum",
            "min"
        ]
    ):

        index = grouped.idxmin()
        value = grouped.min()

        return (
            f"The lowest "
            f"{numeric_column} is for "
            f"**{index}** with "
            f"**{value:,.2f}**."
        )

    # Average by
    if (
        "average by" in question_lower
        or "mean by" in question_lower
    ):

        grouped_average = (
            df.groupby(
                category_column
            )[numeric_column]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        text = (
            f"### Average "
            f"{numeric_column} by "
            f"{category_column}\n\n"
        )

        for index, value in grouped_average.items():

            text += (
                f"- **{index}**: "
                f"{value:,.2f}\n"
            )

        return text

    # Total / sum / each / by
    if (
        "total by" in question_lower
        or "sum by" in question_lower
        or "each" in question_lower
        or "by" in question_lower
    ):

        text = (
            f"### {numeric_column} by "
            f"{category_column}\n\n"
        )

        for index, value in grouped.items():

            text += (
                f"- **{index}**: "
                f"{value:,.2f}\n"
            )

        return text

    return None


# ============================================================
# BASIC NUMERICAL ANALYSIS
# ============================================================

def calculate_basic_analysis(
    df,
    question
):

    numeric_column = find_numeric_column(
        df,
        question
    )

    if numeric_column is None:
        return None

    values = pd.to_numeric(
        df[numeric_column],
        errors="coerce"
    ).dropna()

    if values.empty:
        return None

    question_lower = question.lower()

    # Average
    if (
        "average" in question_lower
        or "mean" in question_lower
    ):

        return (
            f"The average "
            f"{numeric_column} is "
            f"**{values.mean():,.2f}**."
        )

    # Total
    if (
        "total" in question_lower
        or "sum" in question_lower
    ):

        return (
            f"The total "
            f"{numeric_column} is "
            f"**{values.sum():,.2f}**."
        )

    # Maximum
    if (
        "maximum" in question_lower
        or "highest" in question_lower
        or "max" in question_lower
    ):

        return (
            f"The maximum "
            f"{numeric_column} is "
            f"**{values.max():,.2f}**."
        )

    # Minimum
    if (
        "minimum" in question_lower
        or "lowest" in question_lower
        or "min" in question_lower
    ):

        return (
            f"The minimum "
            f"{numeric_column} is "
            f"**{values.min():,.2f}**."
        )

    return None


# ============================================================
# DATE ANALYSIS
# ============================================================

def calculate_date_analysis(
    df,
    question
):

    date_column = find_date_column(df)

    if date_column is None:
        return None

    numeric_column = find_numeric_column(
        df,
        question
    )

    if numeric_column is None:
        return None

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
        return None

    question_lower = question.lower()

    # Yearly
    if "year" in question_lower:

        yearly = (
            data.groupby(
                data[date_column].dt.year
            )[numeric_column]
            .sum()
            .sort_index()
        )

        text = (
            f"### Yearly "
            f"{numeric_column}\n\n"
        )

        for year, value in yearly.items():

            text += (
                f"- **{year}**: "
                f"{value:,.2f}\n"
            )

        return text

    # Monthly
    if "month" in question_lower:

        monthly = (
            data.groupby(
                data[date_column].dt.to_period("M")
            )[numeric_column]
            .sum()
            .sort_index()
        )

        text = (
            f"### Monthly "
            f"{numeric_column}\n\n"
        )

        for month, value in monthly.items():

            text += (
                f"- **{month}**: "
                f"{value:,.2f}\n"
            )

        return text

    # Highest by date
    if (
        (
            "highest" in question_lower
            or "maximum" in question_lower
        )
        and "date" in question_lower
    ):

        grouped = (
            data.groupby(
                date_column
            )[numeric_column]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        if grouped.empty:
            return None

        date = grouped.index[0]
        value = grouped.iloc[0]

        return (
            f"The date with the highest "
            f"{numeric_column} was "
            f"**{date.strftime('%Y-%m-%d')}** "
            f"with **{value:,.2f}**."
        )

    # Lowest by date
    if (
        (
            "lowest" in question_lower
            or "minimum" in question_lower
        )
        and "date" in question_lower
    ):

        grouped = (
            data.groupby(
                date_column
            )[numeric_column]
            .sum()
            .sort_values(
                ascending=True
            )
        )

        if grouped.empty:
            return None

        date = grouped.index[0]
        value = grouped.iloc[0]

        return (
            f"The date with the lowest "
            f"{numeric_column} was "
            f"**{date.strftime('%Y-%m-%d')}** "
            f"with **{value:,.2f}**."
        )

    # By date
    if "date" in question_lower:

        grouped = (
            data.groupby(
                date_column
            )[numeric_column]
            .sum()
            .sort_index()
        )

        text = (
            f"### {numeric_column} by Date\n\n"
        )

        for date, value in grouped.items():

            text += (
                f"- **{date.strftime('%Y-%m-%d')}**: "
                f"{value:,.2f}\n"
            )

        return text

    return None


# ============================================================
# TREND ANALYSIS
# ============================================================

def calculate_trend_answer(
    df,
    question
):

    date_column = find_date_column(df)

    if date_column is None:

        return (
            "I could not identify a date column "
            "for trend analysis."
        )

    number_column = find_numeric_column(
        df,
        question
    )

    if number_column is None:

        return (
            "I could not identify the numerical "
            "column for trend analysis."
        )

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

        return (
            "No valid dates were found "
            "for trend analysis."
        )

    trend_data = (
        data.groupby(
            date_column
        )[number_column]
        .sum()
        .sort_index()
    )

    if len(trend_data) < 2:

        return (
            "There is not enough date data "
            "to determine a trend."
        )

    x = np.arange(
        len(trend_data),
        dtype=float
    )

    y = trend_data.values.astype(float)

    slope, intercept = np.polyfit(
        x,
        y,
        1
    )

    predicted = (
        slope * x
        + intercept
    )

    ss_total = np.sum(
        (y - np.mean(y)) ** 2
    )

    ss_residual = np.sum(
        (y - predicted) ** 2
    )

    if ss_total != 0:

        r_squared = (
            1
            - ss_residual / ss_total
        )

    else:

        r_squared = 0

    if slope > 0:

        direction = "Increasing"

    elif slope < 0:

        direction = "Decreasing"

    else:

        direction = "Stable"

    first_value = float(
        trend_data.iloc[0]
    )

    last_value = float(
        trend_data.iloc[-1]
    )

    change = (
        last_value - first_value
    )

    percentage_change = (
        change / first_value * 100
        if first_value != 0
        else 0
    )

    differences = (
        trend_data.diff().dropna()
    )

    increases = int(
        (differences > 0).sum()
    )

    decreases = int(
        (differences < 0).sum()
    )

    unchanged = int(
        (differences == 0).sum()
    )

    highest_date = trend_data.idxmax()

    highest_value = float(
        trend_data.max()
    )

    lowest_date = trend_data.idxmin()

    lowest_value = float(
        trend_data.min()
    )

    if r_squared >= 0.70:

        strength = "Strong"

    elif r_squared >= 0.40:

        strength = "Moderate"

    else:

        strength = "Weak"

    return (
        f"### {number_column} Trend\n\n"

        f"**Overall trend:** "
        f"{direction}\n\n"

        f"**Trend strength:** "
        f"{strength}\n\n"

        f"- Trend slope: "
        f"**{slope:,.2f} per period**\n"

        f"- R²: "
        f"**{r_squared:.2f}**\n"

        f"- First value "
        f"({trend_data.index[0].strftime('%Y-%m-%d')}): "
        f"**{first_value:,.2f}**\n"

        f"- Last value "
        f"({trend_data.index[-1].strftime('%Y-%m-%d')}): "
        f"**{last_value:,.2f}**\n"

        f"- Change: "
        f"**{change:,.2f} "
        f"({percentage_change:+.2f}%)**\n"

        f"- Increasing periods: "
        f"**{increases}**\n"

        f"- Decreasing periods: "
        f"**{decreases}**\n"

        f"- Unchanged periods: "
        f"**{unchanged}**\n"

        f"- Highest value: "
        f"**{highest_value:,.2f}** on "
        f"**{highest_date.strftime('%Y-%m-%d')}**\n"

        f"- Lowest value: "
        f"**{lowest_value:,.2f}** on "
        f"**{lowest_date.strftime('%Y-%m-%d')}**"
    )


# ============================================================
# DATASET SUMMARY
# ============================================================

def create_dataset_summary(df):

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),

        "numeric_columns": df.select_dtypes(
            include=np.number
        ).columns.tolist(),

        "categorical_columns": df.select_dtypes(
            include=[
                "object",
                "category",
                "bool"
            ]
        ).columns.tolist(),

        "missing_values": int(
            df.isnull().sum().sum()
        )
    }


# ============================================================
# OPERATION DETECTION
# ============================================================

def detect_operation(question):

    question_lower = question.lower()

    # IMPORTANT:
    # Comparison must be checked BEFORE TOP/BOTTOM
    # and before other numerical operations.

    if any(
        word in question_lower
        for word in [
            "compare",
            "comparison",
            "versus",
            " vs ",
            "higher than",
            "lower than",
            "greater than",
            "less than",
            "better than"
        ]
    ):

        return "COMPARISON"

    # Trend
    if any(
        word in question_lower
        for word in [
            "trend",
            "increasing",
            "decreasing",
            "growth",
            "declining",
            "over time"
        ]
    ):

        return "TREND_ANALYSIS"

    # Top
    if "top" in question_lower:

        return "TOP_N"

    # Bottom
    if "bottom" in question_lower:

        return "BOTTOM_N"

    # Date
    if any(
        word in question_lower
        for word in [
            "date",
            "monthly",
            "month",
            "yearly",
            "year"
        ]
    ):

        return "DATE_ANALYSIS"

    # Group analysis
    if any(
        word in question_lower
        for word in [
            "highest",
            "lowest",
            "best",
            "worst",
            "average by",
            "total by",
            "sum by",
            "each",
            "by"
        ]
    ):

        return "GROUP_ANALYSIS"

    # Basic numerical analysis
    if any(
        word in question_lower
        for word in [
            "average",
            "mean",
            "total",
            "sum",
            "maximum",
            "minimum"
        ]
    ):

        return "BASIC_ANALYSIS"

    return "AI"


# ============================================================
# LOCAL AI FALLBACK
# ============================================================

def ask_local_ai(
    df,
    question
):

    summary = create_dataset_summary(df)

    prompt = f"""
You are a professional data analyst.

Answer the user's question using the dataset information.

Dataset summary:
{summary}

User question:
{question}

Rules:

- Answer only using information available in the dataset.
- Do not invent numbers.
- If the question cannot be answered from the dataset, clearly say so.
- Use actual column names.
- Keep the answer concise.
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",

            json={
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False,

                "options": {
                    "temperature": 0.1,
                    "num_predict": 300
                }
            },

            timeout=180
        )

        response.raise_for_status()

        return (
            response.json()
            ["response"]
            .strip()
        )

    except Exception as e:

        return (
            "⚠️ I could not answer "
            "the question automatically.\n\n"
            f"Error: {str(e)}"
        )


# ============================================================
# MAIN QUESTION ANSWER
# ============================================================

def answer_question(
    df,
    question
):

    operation = detect_operation(
        question
    )

    # COMPARISON
    if operation == "COMPARISON":

        answer = calculate_comparison(
            df,
            question
        )

        if answer:
            return answer

    # TREND
    if operation == "TREND_ANALYSIS":

        answer = calculate_trend_answer(
            df,
            question
        )

        if answer:
            return answer

    # TOP N
    if operation == "TOP_N":

        answer = calculate_top_n(
            df,
            question
        )

        if answer:
            return answer

    # BOTTOM N
    if operation == "BOTTOM_N":

        answer = calculate_bottom_n(
            df,
            question
        )

        if answer:
            return answer

    # DATE
    if operation == "DATE_ANALYSIS":

        answer = calculate_date_analysis(
            df,
            question
        )

        if answer:
            return answer

    # GROUP
    if operation == "GROUP_ANALYSIS":

        answer = calculate_group_analysis(
            df,
            question
        )

        if answer:
            return answer

    # BASIC
    if operation == "BASIC_ANALYSIS":

        answer = calculate_basic_analysis(
            df,
            question
        )

        if answer:
            return answer

    # AI FALLBACK
    return ask_local_ai(
        df,
        question
    )