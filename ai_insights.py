import os
import requests
import streamlit as st


def get_groq_api_key():
    """
    Get Groq API key safely.

    Priority:
    1. Streamlit Cloud Secrets
    2. Windows environment variable
    """

    try:
        key = st.secrets.get("GROQ_API_KEY")

        if key:
            return key

    except Exception:
        pass

    return os.getenv("GROQ_API_KEY")


def use_ollama():
    """
    Decide whether local Ollama should be used.

    Default:
    - Local computer: Ollama enabled
    - Streamlit Cloud: can be disabled using USE_OLLAMA=false
    """

    try:
        value = st.secrets.get("USE_OLLAMA")

        if value is not None:
            return str(value).lower() == "true"

    except Exception:
        pass

    return True


def generate_insights(verified_findings):

    prompt = f"""
You are a professional business data analyst.

Your job is to present exactly 5 useful business insights from the
VERIFIED DATASET FINDINGS below.

VERIFIED DATASET FINDINGS:
{verified_findings}

STRICT RULES:

1. Use ONLY facts explicitly written in the verified findings.
2. Do NOT calculate anything yourself.
3. Do NOT perform arithmetic.
4. Do NOT calculate percentages, ratios, differences, growth rates,
   or contributions.
5. Do NOT invent any number, date, category, product, region, or value.
6. Do NOT combine multiple findings to create a new claim.
7. Do NOT change the meaning of any number.
8. Keep labels accurate.
9. Do NOT assume that the highest individual value belongs to the
   highest-performing region.
10. Do NOT assume that the lowest individual value belongs to the
    lowest-performing region.
11. Do NOT use missing values or duplicate rows as an insight if
    five useful business findings are available.
12. Do NOT repeat the same fact.
13. Number the insights from 1 to 5.
14. Keep each insight short and professional.
15. Do not add an introduction or conclusion.

IMPORTANT PRIORITY:

When the following facts are available, prioritize them in this order:

1. Overall average of the main numeric metric.
2. Highest individual value of the main numeric metric.
3. Lowest individual value of the main numeric metric.
4. Highest category/region total of the main numeric metric.
5. Lowest category/region total of the main numeric metric.

If one of these priority facts is unavailable, use another useful
business fact from the verified findings.

The total of the main numeric metric may be used only when necessary
to fill a missing insight.

Think of the verified findings as a locked database.
You may ONLY select and explain facts that already exist there.
You are NOT allowed to calculate or modify the database.

Return exactly 5 numbered insights.
"""

    # ---------------------------------------------------------
    # 1. TRY LOCAL OLLAMA
    # ---------------------------------------------------------

    if use_ollama():

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:3b",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.0,
                        "num_predict": 300
                    }
                },
                timeout=120
            )

            print("OLLAMA STATUS:", response.status_code)

            if response.status_code == 200:

                result = response.json()

                if result.get("response"):

                    print("OLLAMA RESPONSE RECEIVED")

                    return result["response"]

        except requests.exceptions.RequestException as error:

            print("OLLAMA ERROR:", error)

    # ---------------------------------------------------------
    # 2. FALLBACK TO GROQ
    # ---------------------------------------------------------

    groq_api_key = get_groq_api_key()

    if groq_api_key:

        try:

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-oss-20b",
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a professional business data analyst. "
                                "Use ONLY the verified findings. "
                                "Never calculate, infer, combine, "
                                "or invent facts."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.0,
                    "max_tokens": 300
                },
                timeout=30
            )

            print("GROQ STATUS:", response.status_code)

            if response.status_code == 200:

                result = response.json()

                return result["choices"][0]["message"]["content"]

            return (
                f"AI service error: {response.status_code}. "
                "Please check the API configuration."
            )

        except requests.exceptions.RequestException as error:

            return (
                f"Unable to connect to the AI service: {error}"
            )

    # ---------------------------------------------------------
    # 3. NO AI SERVICE AVAILABLE
    # ---------------------------------------------------------

    return (
        "AI service is not available.\n\n"
        "For local use, start Ollama and run the Qwen model.\n"
        "For Streamlit Cloud, configure the GROQ_API_KEY secret."
    )