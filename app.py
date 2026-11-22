
import streamlit as st
import ollama

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Code Review Assistant",
    page_icon="💻",
    layout="wide"
)

# --------------------------------
# HEADER
# --------------------------------

st.title("💻 Code Review Assistant")
st.subheader("Your Beginner-Friendly AI Programming Tutor")

st.write(
    "Find bugs, understand errors, and improve your "
    "programming skills with AI-powered feedback."
)

st.divider()

# --------------------------------
# LANGUAGE SELECTION
# --------------------------------

language = st.selectbox(
    "Select Programming Language",
    ["Python", "C", "C++", "Java", "JavaScript"]
)

# --------------------------------
# CODE INPUT
# --------------------------------

code = st.text_area(
    "Paste Your Code",
    height=300,
    placeholder="Write or paste your code here..."
)

# --------------------------------
# AI CODE REVIEW FUNCTION
# --------------------------------

def generate_review(language, code):

    prompt = f"""
You are an expert Code Review Assistant for beginner programmers.

IMPORTANT:
Review ONLY the student code provided below.
Do not review, discuss, or refer to any examples or instructions
as if they were submitted code.
Do not invent additional programs.

PROGRAMMING LANGUAGE:
{language}

BEGIN STUDENT CODE
{code}
END STUDENT CODE

TASK:
Analyse only the code between BEGIN STUDENT CODE and END STUDENT CODE.

REVIEW RULES:
1. Identify syntax, logical and runtime errors.
2. Separate confirmed bugs, potential risks and style improvements.
3. Mention accurate line numbers wherever possible.
4. Explain issues in simple beginner-friendly language.
5. Give actionable hints instead of corrected code.
6. Never invent errors.
7. If the code is correct, clearly confirm it.
8. Never provide the complete corrected program.
9. Do not ask the student to submit revised code.
10. Do not discuss hypothetical example programs.
11. If no code is provided, request valid code.
12. Never report an error that cannot occur in the submitted code.
13. Do not invent hypothetical risks unrelated to the actual operations.
14. Addition, subtraction and multiplication do not cause division-by-zero errors.
15. Do not call ordinary variable or function names reserved keywords.
16. Only report a potential risk when it is relevant to the submitted code.
17. Verify every reported error against the actual code before including it.

REQUIRED OUTPUT FORMAT:

1. Overall Code Status
2. Confirmed Bugs
   - Issue
   - Line Number
   - Error Category
   - Explanation
   - Hint to Fix
3. Potential Risks
4. Optional Style Improvements
5. Correctness Check
6. Learning Concepts
7. Final Feedback

Be accurate, supportive, educational and beginner-friendly.
Review the actual student code independently.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful programming instructor. "
                    "Review only the student's submitted code. "
                    "Never provide a complete corrected program."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.2
        }
    )

    return response["message"]["content"]


# --------------------------------
# REVIEW BUTTON
# --------------------------------

if st.button("🔍 Review My Code", type="primary"):

    if not code.strip():

        st.warning("Please enter some code first.")

    else:

        try:

            with st.spinner("AI is analysing your code..."):

                result = generate_review(language, code)

            st.success("Code review completed!")

            st.divider()

            st.markdown("## 📋 Code Review Report")

            st.markdown(result)

        except Exception as e:

            st.error(
                "Unable to connect to the local AI model. "
                "Make sure Ollama is running."
            )

            st.code(str(e))


# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "AI Code Review Assistant | "
    "Built for Beginner Programmers"
)
