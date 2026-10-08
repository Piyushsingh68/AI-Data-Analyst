import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from analyzer import analyze_dataset
from charts import generate_charts
from outlier_detector import detect_outliers
from kpi_generator import generate_kpis
from time_analysis import analyze_time_data

from insight_engine import (
    generate_verified_findings,
    find_main_numeric_column,
    find_main_category
)

from ai_insights import generate_insights
from ask_data import answer_question


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("📊 AI Excel / CSV Data Analyst")

st.write(
    "Upload your CSV or Excel dataset and get automatic "
    "analysis, charts, KPIs, business insights and AI-powered answers."
)


# ============================================================
# FILE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📂 Upload your CSV or Excel file",
    type=["csv", "xlsx"]
)


# ============================================================
# LOAD DATASET
# ============================================================

if uploaded_file is not None:

    try:

        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif uploaded_file.name.lower().endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        else:
            st.error("Unsupported file format.")
            st.stop()

    except Exception as error:

        st.error(f"Unable to read the file: {error}")
        st.stop()


    # ========================================================
    # SUCCESS MESSAGE
    # ========================================================

    st.success("✅ Dataset loaded successfully!")


    # ========================================================
    # DATASET PREVIEW
    # ========================================================

    st.header("👀 Dataset Preview")

    st.dataframe(
        df.head(10),
        width="stretch"
    )


    # ========================================================
    # BASIC OVERVIEW
    # ========================================================

    st.header("📋 Dataset Overview")

    analysis = analyze_dataset(df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Rows",
            analysis["rows"]
        )

    with col2:
        st.metric(
            "Columns",
            analysis["columns"]
        )

    with col3:
        st.metric(
            "Missing Values",
            analysis["total_missing_values"]
        )

    with col4:
        st.metric(
            "Duplicate Rows",
            analysis["duplicate_rows"]
        )


    # ========================================================
    # COLUMN INFORMATION
    # ========================================================

    st.header("🧩 Dataset Profile")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("🔢 Numeric Columns")

        if analysis["numeric_columns"]:

            for column in analysis["numeric_columns"]:
                st.write(f"- {column}")

        else:
            st.write("No numeric columns found.")


    with col2:

        st.subheader("🔤 Categorical Columns")

        if analysis["categorical_columns"]:

            for column in analysis["categorical_columns"]:
                st.write(f"- {column}")

        else:
            st.write("No categorical columns found.")


    with col3:

        st.subheader("📅 Date Columns")

        if analysis["datetime_columns"]:

            for column in analysis["datetime_columns"]:
                st.write(f"- {column}")

        else:
            st.write("No date columns found.")


    # ========================================================
    # DATA QUALITY
    # ========================================================

    st.header("🧹 Data Quality")

    quality_col1, quality_col2 = st.columns(2)

    with quality_col1:

        st.subheader("Missing Values")

        if analysis["missing_values"]:

            missing_df = pd.DataFrame(
                list(analysis["missing_values"].items()),
                columns=[
                    "Column",
                    "Missing Values"
                ]
            )

            st.dataframe(
                missing_df,
                width="stretch"
            )

        else:

            st.success(
                "✅ No missing values found."
            )


    with quality_col2:

        st.subheader("Duplicate Rows")

        if analysis["duplicate_rows"] > 0:

            st.warning(
                f"{analysis['duplicate_rows']} duplicate rows found."
            )

        else:

            st.success(
                "✅ No duplicate rows found."
            )


    # ========================================================
    # AUTOMATIC CHARTS
    # ========================================================

    st.header("📈 Automatic Data Visualization")

    try:

        charts = generate_charts(df)

        if charts:

            for chart_name, figure in charts:

                st.subheader(
                    chart_name.replace(
                        "_",
                        " "
                    ).title()
                )

                st.pyplot(
                    figure,
                    width="stretch"
                )

                plt.close(figure)

        else:

            st.info(
                "Not enough suitable columns to generate charts."
            )

    except Exception as error:

        st.warning(
            f"Some charts could not be generated: {error}"
        )


    # ========================================================
    # TIME ANALYSIS
    # ========================================================

    st.header("📅 Time Analysis")

    try:

        time_result = analyze_time_data(df)

        if time_result:

            if time_result.get("date_column"):

                st.write(
                    f"**Date column:** "
                    f"{time_result['date_column']}"
                )

            if time_result.get("monthly_data"):

                st.subheader(
                    "Monthly Analysis"
                )

                for metric, data in time_result[
                    "monthly_data"
                ].items():

                    st.write(
                        f"### {metric}"
                    )

                    st.dataframe(
                        data,
                        width="stretch"
                    )

            if time_result.get("yearly_data"):

                st.subheader(
                    "Yearly Analysis"
                )

                for metric, data in time_result[
                    "yearly_data"
                ].items():

                    st.write(
                        f"### {metric}"
                    )

                    st.dataframe(
                        data,
                        width="stretch"
                    )

            if time_result.get("best_period"):

                st.subheader(
                    "🏆 Best Period"
                )

                for metric, result in time_result[
                    "best_period"
                ].items():

                    st.write(
                        f"**{metric}:** {result}"
                    )

            if time_result.get("worst_period"):

                st.subheader(
                    "📉 Worst Period"
                )

                for metric, result in time_result[
                    "worst_period"
                ].items():

                    st.write(
                        f"**{metric}:** {result}"
                    )

        else:

            st.info(
                "No suitable date column was found "
                "for time analysis."
            )

    except Exception as error:

        st.warning(
            f"Time analysis could not be completed: {error}"
        )


    # ========================================================
    # OUTLIER DETECTION
    # ========================================================

    st.header("🚨 Outlier Detection")

    try:

        outliers = detect_outliers(df)

        if outliers:

            for column, result in outliers.items():

                st.subheader(
                    f"📌 {column}"
                )

                st.write(
                    f"**Outlier Count:** "
                    f"{result['count']}"
                )

                st.write(
                    f"**Lower Bound:** "
                    f"{result['lower_bound']:.2f}"
                )

                st.write(
                    f"**Upper Bound:** "
                    f"{result['upper_bound']:.2f}"
                )

                st.write(
                    "**Outlier Values:**"
                )

                st.write(
                    result["values"]
                )

        else:

            st.success(
                "✅ No significant outliers detected."
            )

    except Exception as error:

        st.warning(
            f"Outlier detection failed: {error}"
        )


    # ========================================================
    # STATISTICAL SUMMARY
    # ========================================================

    st.header("📊 Statistical Summary")

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if numeric_columns:

        st.dataframe(
            df[numeric_columns].describe().T,
            width="stretch"
        )

    else:

        st.info(
            "No numeric columns available for statistics."
        )


    # ========================================================
    # KPI GENERATOR
    # ========================================================

    st.header("🎯 Key Performance Indicators")

    try:

        kpis = generate_kpis(df)

        if kpis:

            for column, values in kpis.items():

                st.subheader(
                    f"📌 {column}"
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Total",
                        f"{values['sum']:,.2f}"
                    )

                with col2:
                    st.metric(
                        "Average",
                        f"{values['average']:,.2f}"
                    )

                with col3:
                    st.metric(
                        "Minimum",
                        f"{values['minimum']:,.2f}"
                    )

                with col4:
                    st.metric(
                        "Maximum",
                        f"{values['maximum']:,.2f}"
                    )

        else:

            st.info(
                "No numeric columns available for KPI generation."
            )

    except Exception as error:

        st.warning(
            f"KPI generation failed: {error}"
        )


    # ========================================================
    # AUTOMATIC BUSINESS ANALYSIS
    # ========================================================

    st.header("💼 Automatic Business Analysis")

    try:

        main_numeric = find_main_numeric_column(df)

        main_category = find_main_category(df)

        if main_numeric:

            series = pd.to_numeric(
                df[main_numeric],
                errors="coerce"
            ).dropna()

            if not series.empty:

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        f"Total {main_numeric}",
                        f"{series.sum():,.2f}"
                    )

                with col2:
                    st.metric(
                        f"Average {main_numeric}",
                        f"{series.mean():,.2f}"
                    )

                with col3:
                    st.metric(
                        f"Highest {main_numeric}",
                        f"{series.max():,.2f}"
                    )

                with col4:
                    st.metric(
                        f"Lowest {main_numeric}",
                        f"{series.min():,.2f}"
                    )

        if main_category and main_numeric:

            grouped = (
                df.groupby(main_category)[main_numeric]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            if not grouped.empty:

                st.subheader(
                    f"{main_numeric} by {main_category}"
                )

                business_df = grouped.reset_index()

                business_df.columns = [
                    main_category,
                    f"Total {main_numeric}"
                ]

                st.dataframe(
                    business_df,
                    width="stretch"
                )

                st.write(
                    f"🏆 **Highest {main_category}:** "
                    f"{grouped.index[0]} "
                    f"({grouped.iloc[0]:,.2f})"
                )

                st.write(
                    f"📉 **Lowest {main_category}:** "
                    f"{grouped.index[-1]} "
                    f"({grouped.iloc[-1]:,.2f})"
                )

        else:

            st.info(
                "Automatic business analysis requires "
                "suitable numeric and categorical columns."
            )

    except Exception as error:

        st.warning(
            f"Business analysis failed: {error}"
        )


    # ========================================================
    # CORRELATION ANALYSIS
    # ========================================================

    st.header("🔗 Correlation Analysis")

    if len(numeric_columns) >= 2:

        try:

            correlation = df[numeric_columns].corr()

            fig, ax = plt.subplots(
                figsize=(9, 6)
            )

            image = ax.imshow(
                correlation.values,
                aspect="auto"
            )

            ax.set_xticks(
                range(len(correlation.columns))
            )

            ax.set_yticks(
                range(len(correlation.columns))
            )

            ax.set_xticklabels(
                correlation.columns,
                rotation=45,
                ha="right"
            )

            ax.set_yticklabels(
                correlation.columns
            )

            ax.set_title(
                "Correlation Heatmap"
            )

            fig.colorbar(
                image,
                ax=ax
            )

            plt.tight_layout()

            st.pyplot(
                fig,
                width="stretch"
            )

            plt.close(fig)

        except Exception as error:

            st.warning(
                f"Correlation analysis failed: {error}"
            )

    else:

        st.info(
            "At least two numeric columns are required "
            "for correlation analysis."
        )


    # ========================================================
    # VERIFIED DATASET FINDINGS
    # ========================================================

    st.header("🔎 Verified Dataset Findings")

    try:

        verified_findings = generate_verified_findings(df)

        st.code(
            verified_findings,
            language="text"
        )

    except Exception as error:

        verified_findings = ""

        st.error(
            f"Unable to generate verified findings: {error}"
        )


    # ========================================================
    # AI INSIGHTS
    # ========================================================

    st.header("🤖 AI Insights")

    st.write(
        "Generate five business insights using only "
        "verified facts from your dataset."
    )

    if not verified_findings:

        st.warning(
            "Verified dataset findings are unavailable. "
            "AI insights cannot be generated."
        )

    else:

        if st.button(
            "🚀 Generate AI Insights",
            key="generate_ai_insights"
        ):

            with st.spinner(
                "🤖 AI is analyzing your verified dataset findings..."
            ):

                try:

                    insights = generate_insights(
                        verified_findings
                    )

                    # ----------------------------------------
                    # RESPONSE CHECK
                    # ----------------------------------------

                    if insights is None:

                        st.error(
                            "❌ AI returned no response."
                        )

                    elif isinstance(
                        insights,
                        str
                    ) and insights.strip():

                        st.success(
                            "✅ AI insights generated successfully!"
                        )

                        st.subheader(
                            "📊 AI-Generated Business Insights"
                        )

                        st.markdown(
                            insights
                        )

                    else:

                        st.error(
                            "❌ AI returned an empty response."
                        )

                        st.write(
                            "Raw AI response:"
                        )

                        st.code(
                            repr(insights)
                        )

                except Exception as error:

                    st.error(
                        "❌ AI insight generation failed."
                    )

                    st.exception(
                        error
                    )


    # ========================================================
    # ASK YOUR DATA
    # ========================================================

    st.header("💬 Ask Your Data")

    st.write(
        "Ask a question about the uploaded dataset."
    )

    question = st.text_input(
        "Example: What is the highest sales value?"
    )

    if st.button(
        "🔍 Ask Question",
        key="ask_data_button"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "🔎 Analyzing your question..."
            ):

                try:

                    answer = answer_question(
                        df,
                        question
                    )

                    if answer:

                        st.subheader(
                            "💡 Answer"
                        )

                        st.write(
                            answer
                        )

                    else:

                        st.warning(
                            "No answer could be generated."
                        )

                except Exception as error:

                    st.error(
                        f"Unable to answer the question: {error}"
                    )


# ============================================================
# NO FILE UPLOADED
# ============================================================

else:

    st.info(
        "👆 Upload a CSV or Excel file to start your analysis."
    )

    st.markdown(
        """
### 🚀 Features

- 📋 Dataset preview
- 📊 Dataset overview
- 🧩 Automatic column detection
- 🧹 Data quality analysis
- 📈 Automatic charts
- 📅 Time-series analysis
- 🚨 Outlier detection
- 📊 Statistical analysis
- 🎯 KPI generation
- 💼 Automatic business analysis
- 🔗 Correlation analysis
- 🤖 AI-generated business insights
- 💬 Ask Your Data
        """
    )