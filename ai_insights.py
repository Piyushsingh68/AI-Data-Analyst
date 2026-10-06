import requests


def generate_insights(verified_findings):

    dataset = verified_findings.get(
        "dataset",
        {}
    )

    column_detection = verified_findings.get(
        "column_detection",
        {}
    )

    main_columns = verified_findings.get(
        "main_columns",
        {}
    )

    numeric_analysis = verified_findings.get(
        "main_numeric_analysis",
        {}
    )

    category_analysis = verified_findings.get(
        "category_analysis",
        {}
    )

    data_quality = verified_findings.get(
        "data_quality",
        {}
    )


    prompt = f"""
You are a professional data analyst.

Analyze the verified dataset findings below.

IMPORTANT RULES:

- Use ONLY the information provided.
- Do NOT invent facts.
- Do NOT assume the dataset is about sales.
- Do NOT assume column names such as Sales, Product, or Region.
- Use the actual column names provided.
- Use actual numbers from the verified findings.
- Do not add a currency symbol unless the dataset explicitly provides one.
- Do not add unnecessary introductory text.
- Do not use placeholder text.
- Do not write template instructions in the answer.
- Return exactly 5 numbered insights.
- Each insight should be one clear sentence.
- Make the insights professional and useful.

VERIFIED DATASET FINDINGS

Dataset:
{dataset}

Detected Columns:
{column_detection}

Main Columns:
{main_columns}

Main Numerical Analysis:
{numeric_analysis}

Category Analysis:
{category_analysis}

Data Quality:
{data_quality}


OUTPUT FORMAT:

1. Write the first actual finding.
2. Write the second actual finding.
3. Write an actual category or comparison finding.
4. Write an actual data quality or statistical finding.
5. Write another useful actual analytical finding.

IMPORTANT:
The output must contain ONLY the five numbered insights.

Do NOT write phrases such as:
- "[Important finding using an actual number]"
- "[Category or comparison finding]"
- "[Data quality or statistical finding]"
- "[Another useful analytical finding]"
- "Here are the insights:"
- "Based on the data:"

Return only the final five insights.
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


        result = response.json()["response"]


        return result.strip()


    except Exception as e:

        return (
            "⚠️ Unable to generate AI insights.\n\n"
            f"Error: {str(e)}"
        )