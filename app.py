
import streamlit as st
import fitz
from matcher import calculate_similarity


# -------------------- PAGE CONFIGURATION --------------------

st.set_page_config(
    page_title="Matchly | Resume Matcher",
    page_icon="✦",
    layout="centered"
)


# -------------------- BLUE THEME --------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #0B1224, #101D38, #13294B);
    color: #EAF2FF;
}

.block-container {
    max-width: 900px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

.hero {
    text-align: center;
    padding: 1.5rem 0 2rem;
}

.eyebrow {
    color: #79B8FF;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 1.5px;
}

.hero h1 {
    font-size: 2.8rem;
    color: #F4F8FF;
    margin: 0.5rem 0;
}

.hero p {
    color: #B5C7E3;
    font-size: 1.08rem;
    line-height: 1.7;
}

h2, h3, label {
    color: #EAF2FF;
}

.stMarkdown, [data-testid="stCaptionContainer"] {
    color: #D3E2F7;
}

.stButton > button {
    width: 100%;
    min-height: 3.2rem;
    background: linear-gradient(90deg, #3984F7, #58B7FF);
    color: white;
    border: 1px solid #6CBFFF;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1rem;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #2468D9, #329CEB);
    border-color: #9DD8FF;
    color: white;
}

div[data-testid="stFileUploader"] {
    background: #172844;
    border-radius: 16px;
    padding: 1rem;
    border: 1px solid #2C456B;
}

div[data-testid="stFileUploader"] section {
    background: #172844;
    border-color: #35547D;
}

div[data-testid="stTextArea"] textarea {
    background: #14233D;
    border-radius: 12px;
    border: 1px solid #35547D;
    color: #F1F6FF;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #58B7FF;
    box-shadow: 0 0 0 1px #58B7FF;
}

div[data-testid="stTextArea"] textarea::placeholder {
    color: #8DA5C7;
}

.result-card {
    background: linear-gradient(145deg, #172C4C, #1B365A);
    border: 1px solid #355985;
    border-radius: 20px;
    padding: 1.8rem;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.18);
}

.result-score {
    color: #72C4FF;
    font-size: 3.7rem;
    font-weight: 800;
}

.helper {
    color: #B5C7E3;
    font-size: 0.9rem;
    line-height: 1.7;
}

div[data-testid="stAlert"] {
    background: #172B49;
    border: 1px solid #355985;
    border-radius: 12px;
    color: #EAF2FF;
}

hr {
    border-color: #2C456B;
}

</style>
""", unsafe_allow_html=True)


# -------------------- HEADER --------------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">✦ YOUR CAREER COMPANION</div>
    <h1>Meet Matchly.</h1>
    <p>
        A little clarity for your job search.<br>
        Compare your resume with a job description
        and see how closely their wording aligns.
    </p>
</div>
""", unsafe_allow_html=True)


# -------------------- RESUME UPLOAD --------------------

st.markdown("### 01 · Bring your resume")

st.write(
    "Start with your latest resume. "
    "We'll take care of reading the PDF."
)

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"],
    help="Choose a text-based PDF resume."
)


# -------------------- JOB DESCRIPTION --------------------

st.markdown("### 02 · Choose a role")

job_description = st.text_area(
    "Paste the job description",
    placeholder=(
        "Paste the job responsibilities, required skills "
        "and qualifications here..."
    ),
    height=220,
    max_chars=20000
)

st.caption(
    "Tip: A complete job description gives the matcher more context."
)

st.write("")


# -------------------- MATCHING LOGIC --------------------

if st.button("✦  Check my match", use_container_width=True):

    if uploaded_file is None:
        st.warning(
            "Let's start with your resume. Please upload a PDF."
        )

    elif not job_description.strip():
        st.warning(
            "Please paste the job description so we can compare both texts."
        )

    else:
        try:
            with st.spinner(
                "Reading your resume and comparing the text..."
            ):
                pdf_bytes = uploaded_file.getvalue()

                with fitz.open(
                    stream=pdf_bytes,
                    filetype="pdf"
                ) as pdf:
                    resume_text = "\n".join(
                        page.get_text() for page in pdf
                    )

                if len(resume_text.strip()) < 30:
                    st.error(
                        "We couldn't find enough readable text in this PDF. "
                        "Try a text-based PDF instead of a scanned image."
                    )

                elif not resume_text.strip():
                    st.error(
                        "No readable text was found in your resume."
                    )

                else:
                    score = calculate_similarity(
                        resume_text,
                        job_description
                    )

                    st.markdown("---")

                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="eyebrow">YOUR RESULTS</div>
                            <div class="result-score">{score:.2f}%</div>
                            <h3>Resume–job text similarity</h3>
                            <p class="helper">
                                This score estimates how similar the wording
                                of your resume and the job description is.
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.progress(score / 100)

                    st.info(
                        "A higher score does not guarantee a better "
                        "application or a job offer. This version measures "
                        "text similarity, not your overall qualifications."
                    )

        except Exception as error:
            st.error(
                "We couldn't process this file. Please try another "
                "text-based PDF and try again."
            )
            st.caption(f"Technical details: {error}")


# -------------------- FOOTER --------------------

st.markdown("---")

st.markdown(
    """
    <p class="helper" style="text-align:center;">
        Made to make job searching a little clearer. ✦<br>
        Your resume is processed by this app's code and is not
        intentionally saved by this version.
    </p>
    """,
    unsafe_allow_html=True
)
