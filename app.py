
import streamlit as st
import ollama

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="LogicLens | AI Code Reviewer",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

.stApp {
    background: #080B16;
    color: #E8EAF6;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.hero {
    text-align: center;
    padding: 35px 15px 25px;
}

.logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 48px;
    font-weight: 800;
    letter-spacing: 5px;
    background: linear-gradient(90deg, #A78BFA, #60A5FA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.logo-icon {
    font-size: 38px;
    margin-right: 10px;
}

.tagline {
    color: #A5B4FC;
    font-size: 17px;
    letter-spacing: 1px;
    margin-top: 5px;
}

.hero-desc {
    color: #929BB5;
    font-size: 14px;
    margin-top: 14px;
}

.section-heading {
    color: #E2E8F0;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 8px;
}

.info-card {
    background: linear-gradient(135deg, #151B31, #101426);
    border: 1px solid #293253;
    border-radius: 15px;
    padding: 17px;
    text-align: center;
    min-height: 105px;
}

.info-title {
    color: #A5B4FC;
    font-size: 13px;
    font-weight: 600;
}

.info-value {
    color: #F1F5F9;
    font-size: 18px;
    font-weight: 700;
    margin-top: 7px;
}

.stTextArea textarea {
    background: #0D1222 !important;
    color: #E2E8F0 !important;
    border: 1px solid #303A5C !important;
    border-radius: 12px !important;
    font-family: Consolas, monospace !important;
    font-size: 14px !important;
}

.stTextArea textarea:focus {
    border: 1px solid #8B5CF6 !important;
    box-shadow: 0 0 0 1px #8B5CF6 !important;
}

.stSelectbox > div > div {
    background: #11182B !important;
    border: 1px solid #303A5C !important;
    border-radius: 10px !important;
    color: white !important;
}

.stButton > button {
    width: 100%;
    height: 53px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(90deg, #7C3AED, #4F46E5);
    color: white;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button:hover {
    border: 1px solid #A78BFA;
    background: linear-gradient(90deg, #8B5CF6, #6366F1);
    box-shadow: 0 0 22px #7C3AED55;
    transform: translateY(-2px);
}

.report-box {
    background: #101629;
    border: 1px solid #303A5C;
    border-radius: 15px;
    padding: 22px;
    margin-top: 15px;
}

.footer {
    text-align: center;
    color: #69738F;
    font-size: 12px;
    padding-top: 35px;
    border-top: 1px solid #202943;
    margin-top: 45px;
}

.stAlert {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------
# HEADER
# --------------------------------

st.markdown("""
<div class="hero">
    <div>
        <span class="logo-icon">🔮</span>
        <span class="logo">LOGICLENS</span>
    </div>
    <div class="tagline">
        See the bug. Understand the logic.
    </div>
    <div class="hero-desc">
        Your personal AI programming mentor.
        Find errors, understand concepts and become a better programmer.
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------
# FEATURE CARDS
# --------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="info-card">
        <div class="info-title">01 · DETECT</div>
        <div class="info-value">Find Bugs</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="info-card">
        <div class="info-title">02 · UNDERSTAND</div>
        <div class="info-value">Learn Concepts</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="info-card">
        <div class="info-title">03 · IMPROVE</div>
        <div class="info-value">Get Hints</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# --------------------------------
# LANGUAGE SELECTION
# --------------------------------

st.markdown(
    '<div class="section-heading">01 / Choose Your Language</div>',
    unsafe_allow_html=True
)

language = st.selectbox(
    "Programming Language",
    ["Python", "C", "C++", "Java", "JavaScript"],
    label_visibility="collapsed"
)

st.write("")

# --------------------------------
# CODE INPUT
# --------------------------------

st.markdown(
    '<div class="section-heading">02 / Your Code</div>',
    unsafe_allow_html=True
)

st.caption("Paste your code below and let LogicLens analyse it.")

code = st.text_area(
    "Code Editor",
    height=310,
    placeholder="""# Write or paste your code here...

def example():
    print("Hello, LogicLens!")
""",
    label_visibility="collapsed"
)

st.write("")

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
11. If the code is empty, request valid code.
12. Never report an error that cannot occur in the submitted code.
13. Do not invent hypothetical risks unrelated to actual operations.
14. Addition, subtraction and multiplication do not cause division-by-zero errors.
15. Do not call ordinary variable or function names reserved keywords.
16. Only report relevant potential risks.
17. Verify every reported error against the actual code.

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

st.markdown(
    '<div class="section-heading">03 / Analyse Your Code</div>',
    unsafe_allow_html=True
)

if st.button("✦  REVIEW MY CODE", type="primary"):

    if not code.strip():

        st.warning("Please enter some code first.")

    else:

        try:

            with st.spinner("LogicLens is analysing your code..."):

                result = generate_review(language, code)

            st.success("Your code review is ready!")

            st.markdown("""
            <div class="section-heading">
                ✦ AI Code Review Report
            </div>
            """, unsafe_allow_html=True)

            with st.container(border=True):
                st.markdown(result)

        except Exception as e:

            st.error(
                "Unable to connect to the local AI model. "
                "Make sure Ollama is running and Llama 3.2:3b is installed."
            )

            st.code(str(e))


# --------------------------------
# FOOTER
# --------------------------------

st.markdown("""
<div class="footer">
    <b>LOGICLENS</b> · AI-POWERED CODE REVIEW ASSISTANT
    <br><br>
    Built with Python · Streamlit · Ollama · Llama 3.2:3b
    <br>
    Made for curious minds and beginner programmers.
</div>
""", unsafe_allow_html=True)
