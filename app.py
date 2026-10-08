import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ai_insights import generate_insights
from analyzer import analyze_dataset
from charts import generate_charts
from outlier_detector import detect_outliers
from kpi_generator import generate_kpis
from ask_data import answer_question
from time_analysis import analyze_time_data
from insight_engine import (
    generate_verified_findings,
    find_main_numeric_column,
    find_main_category
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🤖 AI Excel/CSV Data Analyst")

st.write(
    "Upload an Excel or CSV file and automatically "
    "analyze your data."
)


# ============================================================
# FILE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "Upload your Excel or CSV file",
    type=["csv", "xlsx"]
)


if uploaded_file is not None:

    # ========================================================
    # READ DATASET
    # ========================================================

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

    st.success(
        "File uploaded successfully!"
    )


    # ========================================================
    # SQLITE DATABASE
    # ========================================================
    # Database saving has been removed from the main upload
    # flow because Streamlit Cloud can create SQLite state/race
    # issues. The uploaded dataframe is already available as df.

    st.success(
        "Dataset loaded successfully!"
    )


    # ========================================================
    # DATASET PREVIEW
    # ========================================================

    st.subheader(
        "📋 Dataset Preview"
    )

    st.dataframe(
        df.head(10),
        use_container_width=True
    )


    # ========================================================
    # DATASET OVERVIEW
    # ========================================================

    st.subheader(
        "📊 Dataset Overview"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Rows",
        df.shape[0]
    )

    col2.metric(
        "Columns",
        df.shape[1]
    )

    col3.metric(
        "Missing Values",
        int(
            df.isnull()
            .sum()
            .sum()
        )
    )


    # ========================================================
    # AUTOMATIC DATASET PROFILE
    # ========================================================

    st.subheader(
        "🧠 Automatic Dataset Profile"
    )

    analysis = analyze_dataset(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Numerical Columns",
        len(
            analysis[
                "numeric_columns"
            ]
        )
    )

    col2.metric(
        "Categorical Columns",
        len(
            analysis[
                "categorical_columns"
            ]
        )
    )

    col3.metric(
        "Date Columns",
        len(
            analysis[
                "datetime_columns"
            ]
        )
    )

    col4.metric(
        "Duplicate Rows",
        analysis[
            "duplicate_rows"
        ]
    )


    # ========================================================
    # NUMERICAL COLUMNS
    # ========================================================

    st.write(
        "### 🔢 Numerical Columns"
    )

    if analysis[
        "numeric_columns"
    ]:

        st.write(
            ", ".join(
                analysis[
                    "numeric_columns"
                ]
            )
        )

    else:

        st.info(
            "No numerical columns detected."
        )


    # ========================================================
    # CATEGORICAL COLUMNS
    # ========================================================

    st.write(
        "### 📝 Categorical Columns"
    )

    if analysis[
        "categorical_columns"
    ]:

        st.write(
            ", ".join(
                analysis[
                    "categorical_columns"
                ]
            )
        )

    else:

        st.info(
            "No categorical columns detected."
        )


    # ========================================================
    # DATE COLUMNS
    # ========================================================

    st.write(
        "### 📅 Date Columns"
    )

    if analysis[
        "datetime_columns"
    ]:

        st.write(
            ", ".join(
                analysis[
                    "datetime_columns"
                ]
            )
        )

    else:

        st.info(
            "No date columns detected."
        )


    # ========================================================
    # DATA QUALITY
    # ========================================================

    st.subheader(
        "🧹 Data Quality"
    )

    quality_df = pd.DataFrame({

        "Column":
            df.columns,

        "Data Type":
            df.dtypes
            .astype(str)
            .values,

        "Missing Values":
            df.isnull()
            .sum()
            .values,

        "Unique Values":
            df.nunique()
            .values

    })

    st.dataframe(
        quality_df,
        use_container_width=True
    )


    # ========================================================
    # AUTOMATIC DATA VISUALIZATION
    # ========================================================

    st.subheader(
        "📊 Automatic Data Visualization"
    )

    charts = generate_charts(df)

    if charts:

        for chart_type, figure in charts:

            if chart_type == "bar":

                st.write(
                    "### 📊 Category Comparison"
                )

            elif chart_type == "line":

                st.write(
                    "### 📈 Trend Over Time"
                )

            elif chart_type == "trend":

                st.write(
                    "### 📈 Actual vs Trend"
                )

            elif chart_type == "scatter":

                st.write(
                    "### 🔗 Relationship Between Variables"
                )

            elif chart_type == "histogram":

                st.write(
                    "### 📉 Data Distribution"
                )

            st.pyplot(
                figure
            )

    else:

        st.info(
            "No suitable charts could be generated "
            "for this dataset."
        )


    # ========================================================
    # TIME-BASED ANALYSIS
    # ========================================================

    st.subheader(
        "📅 Time-Based Analysis"
    )

    time_analysis = analyze_time_data(df)

    if "error" in time_analysis:

        st.info(
            time_analysis[
                "error"
            ]
        )

    else:

        date_column = (
            time_analysis[
                "date_column"
            ]
        )

        st.write(
            f"**Date column detected:** "
            f"`{date_column}`"
        )


        # ----------------------------------------------------
        # MONTHLY ANALYSIS
        # ----------------------------------------------------

        st.write(
            "### 📅 Monthly Analysis"
        )

        monthly_data = (
            time_analysis[
                "monthly"
            ]
        )

        for column, values in monthly_data.items():

            st.write(
                f"#### {column}"
            )

            monthly_df = pd.DataFrame(
                list(
                    values.items()
                ),
                columns=[
                    "Month",
                    column
                ]
            )

            st.dataframe(
                monthly_df,
                use_container_width=True
            )

            st.bar_chart(
                monthly_df.set_index(
                    "Month"
                )[column]
            )


        # ----------------------------------------------------
        # YEARLY ANALYSIS
        # ----------------------------------------------------

        st.write(
            "### 📆 Yearly Analysis"
        )

        yearly_data = (
            time_analysis[
                "yearly"
            ]
        )

        for column, values in yearly_data.items():

            st.write(
                f"#### {column}"
            )

            yearly_df = pd.DataFrame(
                list(
                    values.items()
                ),
                columns=[
                    "Year",
                    column
                ]
            )

            st.dataframe(
                yearly_df,
                use_container_width=True
            )


        # ----------------------------------------------------
        # BEST AND WORST MONTH
        # ----------------------------------------------------

        st.write(
            "### 🏆 Best & Worst Month"
        )

        best_worst = (
            time_analysis[
                "best_worst"
            ]
        )

        for column, values in best_worst.items():

            st.write(
                f"#### {column}"
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Best Month",
                values[
                    "best_month"
                ],
                f"{values['best_value']:,.2f}"
            )

            col2.metric(
                "Worst Month",
                values[
                    "worst_month"
                ],
                f"{values['worst_value']:,.2f}"
            )


    # ========================================================
    # OUTLIER DETECTION
    # ========================================================

    st.subheader(
        "🔍 Outlier Detection"
    )

    outliers = detect_outliers(df)

    if outliers:

        for column, details in outliers.items():

            st.write(
                f"### 📌 {column}"
            )

            st.write(
                f"**Number of outliers:** "
                f"{details['count']}"
            )

            st.write(
                f"**Lower boundary:** "
                f"{details['lower_bound']:.2f}"
            )

            st.write(
                f"**Upper boundary:** "
                f"{details['upper_bound']:.2f}"
            )

            st.write(
                "**Outlier values:**"
            )

            st.dataframe(
                pd.DataFrame({
                    column:
                        details[
                            "values"
                        ]
                }),
                use_container_width=True
            )

    else:

        st.success(
            "✅ No outliers detected in the "
            "numerical columns."
        )


    # ========================================================
    # STATISTICAL SUMMARY
    # ========================================================

    st.subheader(
        "📈 Statistical Summary"
    )

    numeric_columns = (
        df.select_dtypes(
            include="number"
        )
        .columns
        .tolist()
    )

    if numeric_columns:

        st.dataframe(
            df[
                numeric_columns
            ].describe(),
            use_container_width=True
        )

    else:

        st.info(
            "No numerical columns found."
        )


    # ========================================================
    # DYNAMIC KPIs
    # ========================================================

    st.subheader(
        "📌 Dynamic Key Performance Indicators"
    )

    kpis = generate_kpis(df)

    if kpis:

        for column, values in kpis.items():

            st.write(
                f"### {column}"
            )

            col1, col2, col3, col4, col5 = (
                st.columns(5)
            )

            col1.metric(
                "Total",
                f"{values['sum']:,.2f}"
            )

            col2.metric(
                "Average",
                f"{values['average']:,.2f}"
            )

            col3.metric(
                "Minimum",
                f"{values['minimum']:,.2f}"
            )

            col4.metric(
                "Maximum",
                f"{values['maximum']:,.2f}"
            )

            col5.metric(
                "Count",
                f"{values['count']:,}"
            )

    else:

        st.info(
            "No numerical columns available "
            "for KPI generation."
        )


    # ========================================================
    # AUTOMATIC BUSINESS ANALYSIS
    # ========================================================

    st.subheader(
        "🧠 Automatic Business Analysis"
    )

    verified_findings = (
        generate_verified_findings(df)
    )

    main_numeric = find_main_numeric_column(df)
    main_category = find_main_category(df)


    # --------------------------------------------------------
    # MAIN NUMERICAL METRIC
    # --------------------------------------------------------

    if main_numeric:

        numeric_series = pd.to_numeric(
            df[main_numeric],
            errors="coerce"
        ).dropna()

        if not numeric_series.empty:

            total = numeric_series.sum()
            average = numeric_series.mean()
            maximum = numeric_series.max()

            st.write(
                f"**Main numerical metric detected:** "
                f"`{main_numeric}`"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total",
                f"{total:,.2f}"
            )

            col2.metric(
                "Average",
                f"{average:,.2f}"
            )

            col3.metric(
                "Maximum",
                f"{maximum:,.2f}"
            )


    # --------------------------------------------------------
    # CATEGORY PERFORMANCE
    # --------------------------------------------------------

    if main_category and main_numeric:

        st.write(
            f"**Category analysis:** "
            f"`{main_category}` vs "
            f"`{main_numeric}`"
        )

        category_totals = (
            df.groupby(
                main_category
            )[main_numeric]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        if not category_totals.empty:

            highest_category = (
                category_totals.index[0]
            )

            highest_value = (
                category_totals.iloc[0]
            )

            lowest_category = (
                category_totals.index[-1]
            )

            lowest_value = (
                category_totals.iloc[-1]
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Highest Category",
                highest_category,
                f"{highest_value:,.2f}"
            )

            col2.metric(
                "Lowest Category",
                lowest_category,
                f"{lowest_value:,.2f}"
            )

            st.write(
                f"### 📊 {main_numeric} by "
                f"{main_category}"
            )

            st.bar_chart(
                category_totals
            )

    else:

        st.info(
            "No suitable categorical column was "
            "found for automatic category analysis."
        )


    # ========================================================
    # CORRELATION ANALYSIS
    # ========================================================

    if len(numeric_columns) >= 2:

        st.subheader(
            "🔗 Correlation Analysis"
        )

        correlation = (
            df[
                numeric_columns
            ]
            .corr()
        )

        st.dataframe(
            correlation,
            use_container_width=True
        )

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        sns.heatmap(
            correlation,
            annot=True,
            fmt=".2f",
            ax=ax
        )

        ax.set_title(
            "Correlation Heatmap"
        )

        st.pyplot(
            fig
        )


    # ========================================================
    # AI DATA ANALYST
    # ========================================================

    st.subheader(
        "🤖 AI Data Analyst"
    )

    st.write(
        "Generate automatic business insights "
        "from your verified dataset analysis."
    )

    if st.button(
        "Generate AI Insights"
    ):

        with st.spinner(
            "🤖 AI is analyzing your verified "
            "dataset findings..."
        ):

            insights = generate_insights(
                verified_findings
            )

        st.markdown(
            insights
        )


    # ========================================================
    # ASK YOUR DATA
    # ========================================================

    st.subheader(
        "💬 Ask Your Data"
    )

    st.write(
        "Ask questions about your uploaded dataset."
    )

    question = st.text_input(
        "Enter your question"
    )

    if st.button(
        "Ask"
    ):

        if question.strip():

            with st.spinner(
                "🔎 Analyzing your question..."
            ):

                answer = answer_question(
                    df,
                    question
                )

            st.success(
                answer
            )

        else:

            st.warning(
                "Please enter a question first."
            )