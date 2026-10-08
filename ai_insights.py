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

You must produce exactly 5 useful business insights.

Use ONLY the verified dataset findings below.

VERIFIED DATASET FINDINGS:
{verified_findings}

STRICT RULES:

1. Use only facts explicitly present in the verified findings.
2. Do not calculate anything yourself.
3. Do not perform arithmetic.
4. Do not calculate percentages.
5. Do not calculate ratios.
6. Do not calculate growth rates.
7. Do not calculate differences.
8. Do not invent numbers.
9. Do not invent categories.
10. Do not invent dates.
11. Do not invent products.
12. Do not combine multiple findings to create a new numerical claim.
13. Do not change the meaning of any number.
14. Do not assume that the highest individual value belongs to
    the highest-performing region.
15. Do not assume that the lowest individual value belongs to
    the lowest-performing region.
16. Do not use missing values or duplicate rows if useful
    business findings are available.
17. Do not repeat the same fact.
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

You are only allowed to select and explain facts that already
exist in the verified findings.

Return exactly five numbered insights.
"""


    # ========================================================
    # TRY OLLAMA FIRST
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

                ollama_answer = result.get(
                    "response",
                    ""
                )

                print(
                    "OLLAMA RESPONSE LENGTH:",
                    len(ollama_answer)
                )

                if ollama_answer.strip():

                    return ollama_answer.strip()

        except Exception as error:

            print(
                "OLLAMA ERROR:",
                error
            )


    # ========================================================
    # GET GROQ API KEY
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

                "temperature": 0,

                "max_tokens": 300
            },

            timeout=60
        )


        # ----------------------------------------------------
        # DEBUG STATUS
        # ----------------------------------------------------

        print(
            "GROQ STATUS:",
            response.status_code
        )

        print(
            "GROQ RESPONSE LENGTH:",
            len(response.text)
        )


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if response.status_code == 200:

            result = response.json()

            print(
                "GROQ JSON KEYS:",
                list(result.keys())
            )


            choices = result.get(
                "choices",
                []
            )


            if not choices:

                print(
                    "GROQ ERROR: choices list is empty"
                )

                return (
                    "AI service returned no choices."
                )


            message = choices[0].get(
                "message",
                {}
            )


            answer = message.get(
                "content",
                ""
            )


            print(
                "GROQ CONTENT LENGTH:",
                len(answer)
            )


            if answer and answer.strip():

                return answer.strip()


            # ------------------------------------------------
            # HANDLE EMPTY CONTENT
            # ------------------------------------------------

            print(
                "GROQ ERROR: message content is empty"
            )


            # Some API responses can provide a different
            # output field. Check it safely.

            reasoning = message.get(
                "reasoning",
                ""
            )

            if reasoning and reasoning.strip():

                return reasoning.strip()


            return (
                "AI service returned an empty response."
            )


        # ====================================================
        # API ERROR
        # ====================================================

        else:

            print(
                "GROQ ERROR RESPONSE:",
                response.text
            )

            return (
                f"AI service error: "
                f"{response.status_code}\n\n"
                "Please check the Streamlit Cloud logs."
            )


    except requests.exceptions.Timeout:

        return (
            "AI service request timed out. "
            "Please try again."
        )


    except requests.exceptions.RequestException as error:

        return (
            f"Unable to connect to the AI service: {error}"
        )


    except Exception as error:

        return (
            f"Unexpected AI service error: {error}"
        )