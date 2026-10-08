import os
import requests
import streamlit as st


# ============================================================
# GET GROQ API KEY
# ============================================================

def get_groq_api_key():

    try:
        key = st.secrets.get("GROQ_API_KEY")

        if key:
            return key

    except Exception:
        pass

    return os.getenv("GROQ_API_KEY")


# ============================================================
# OLLAMA SETTING
# ============================================================

def use_ollama():

    try:
        value = st.secrets.get("USE_OLLAMA")

        if value is not None:
            return str(value).lower() == "true"

    except Exception:
        pass

    return True


# ============================================================
# GENERATE AI INSIGHTS
# ============================================================

def generate_insights(verified_findings):

    prompt = f"""
You are a professional business data analyst.

Generate exactly 5 useful business insights from the verified
dataset findings below.

VERIFIED DATASET FINDINGS:
{verified_findings}

STRICT RULES:

1. Use ONLY facts explicitly present in the verified findings.
2. Do NOT calculate anything.
3. Do NOT perform arithmetic.
4. Do NOT calculate percentages.
5. Do NOT calculate ratios.
6. Do NOT calculate growth rates.
7. Do NOT calculate differences.
8. Do NOT invent numbers.
9. Do NOT invent categories.
10. Do NOT invent dates.
11. Do NOT invent products.
12. Do NOT combine multiple findings to create new numerical claims.
13. Do NOT change the meaning of any number.
14. Do NOT assume that the highest individual value belongs
    to the highest-performing region.
15. Do NOT assume that the lowest individual value belongs
    to the lowest-performing region.
16. Do NOT use missing values or duplicate rows if five useful
    business findings are available.
17. Do NOT repeat the same fact.
18. Return exactly 5 numbered insights.
19. Keep each insight short and professional.
20. Do not add an introduction.
21. Do not add a conclusion.

PRIORITY:

1. Overall average of the main numeric metric.
2. Highest individual value.
3. Lowest individual value.
4. Highest category/region total.
5. Lowest category/region total.

If one priority fact is unavailable, use another useful fact
that already exists in the verified findings.

The verified findings are a LOCKED DATABASE.

You may ONLY select and explain facts that already exist in
the verified findings.

Return exactly five numbered insights.
"""


    # ========================================================
    # OLLAMA
    # ========================================================

    if use_ollama():

        try:

            response = requests.post(
                "http://localhost:11434/api/generate",

                json={
                    "model": "qwen2.5:3b",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0,
                        "num_predict": 300
                    }
                },

                timeout=120
            )

            print(
                "OLLAMA STATUS:",
                response.status_code
            )

            if response.status_code == 200:

                result = response.json()

                answer = result.get(
                    "response",
                    ""
                )

                if answer and answer.strip():

                    return answer.strip()

        except Exception as error:

            print(
                "OLLAMA ERROR:",
                error
            )


    # ========================================================
    # GROQ API KEY
    # ========================================================

    groq_api_key = get_groq_api_key()

    if not groq_api_key:

        return (
            "AI service is not available.\n\n"
            "GROQ_API_KEY was not found."
        )


    # ========================================================
    # GROQ API
    # ========================================================

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
                            "You are a professional business "
                            "data analyst. "
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

                # Important for GPT-OSS reasoning models
                "reasoning_format": "hidden",

                "reasoning_effort": "low",

                "temperature": 0,

                "max_completion_tokens": 500
            },

            timeout=60
        )


        # ====================================================
        # DEBUG INFORMATION
        # ====================================================

        print(
            "GROQ STATUS:",
            response.status_code
        )

        print(
            "GROQ RESPONSE LENGTH:",
            len(response.text)
        )


        # ====================================================
        # SUCCESS
        # ====================================================

        if response.status_code == 200:

            result = response.json()

            print(
                "GROQ RESPONSE RECEIVED"
            )

            choices = result.get(
                "choices",
                []
            )

            if not choices:

                print(
                    "GROQ ERROR: No choices returned"
                )

                return (
                    "AI service returned no choices."
                )


            message = choices[0].get(
                "message",
                {}
            )


            content = message.get(
                "content"
            )


            print(
                "GROQ CONTENT TYPE:",
                type(content).__name__
            )


            if content is not None:

                content = str(
                    content
                ).strip()

            else:

                content = ""


            print(
                "GROQ CONTENT LENGTH:",
                len(content)
            )


            # =================================================
            # FINAL ANSWER
            # =================================================

            if content:

                return content


            # =================================================
            # FALLBACK: REASONING FIELD
            # =================================================

            reasoning = message.get(
                "reasoning",
                ""
            )


            if reasoning:

                reasoning = str(
                    reasoning
                ).strip()


            if reasoning:

                print(
                    "Using reasoning field as fallback."
                )

                return reasoning


            # =================================================
            # EMPTY RESPONSE
            # =================================================

            print(
                "GROQ RETURNED EMPTY CONTENT."
            )

            return (
                "AI service returned an empty response."
            )


        # ====================================================
        # API ERROR
        # ====================================================

        else:

            print(
                "GROQ ERROR:",
                response.text
            )

            return (
                f"AI service error: "
                f"{response.status_code}"
            )


    # ========================================================
    # TIMEOUT
    # ========================================================

    except requests.exceptions.Timeout:

        return (
            "AI service request timed out. "
            "Please try again."
        )


    # ========================================================
    # CONNECTION ERROR
    # ========================================================

    except requests.exceptions.RequestException as error:

        return (
            f"Unable to connect to the AI service: {error}"
        )


    # ========================================================
    # OTHER ERROR
    # ========================================================

    except Exception as error:

        return (
            f"Unexpected AI service error: {error}"
        )