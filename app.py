import streamlit as st
import pandas as pd
from utils.matcher import analyze_resumes
from utils.exporter import export_excel
import time




# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="AI Powered Resume Screening Tool",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================================
# SESSION STATE
# ================================
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False






# ================================
# CSS – STABLE LIGHT THEME
# ================================
st.markdown("""
<style>
/* ===============================
   GLOBAL APP
   =============================== */
.stApp {
    background-color: #ffffff;
    color: #000000;
    font-family: Arial, Helvetica, sans-serif;
}

/* Remove outlines */
* {
    outline: none !important;
}

/* ===============================
   HERO
   =============================== */
.main-title {
    text-align: center;
    font-size: 50px;
    font-weight: 800;
    margin-top: 30px;
}

.subtitle {
    text-align: center;
    font-size: 14px;
    color: #444444;
    margin-top: 10px;
    margin-bottom: 30px;
    line-height: 1.4;
}

/* ===============================
   SECTION HEADINGS
   =============================== */
.section-title {
    font-size: 40px;
    font-weight: 800;
    margin-top: 40px;
    margin-bottom: 8px;
}

.section-subtitle {
    font-size: 15px;
    color: #555555;
    margin-bottom: 18px;
}

/* ===============================
   BUTTONS
   =============================== */
.stButton > button {
    background: #e6e6e6;
    color: #000000;
    font-weight: 700;
    border-radius: 20px;
    padding: 8px 28px;
    border: none;
    margin-top: 18px;
}

button:focus {
    box-shadow: none !important;
}

/* ===============================
   UPLOAD SECTION
   =============================== */
.upload-title {
    font-size: 40px;
    font-weight: 800;
}

.upload-subtitle {
    font-size: 15px;
    color: #555555;
    margin-bottom: 30px;
}

/* Outer uploader */
section[data-testid="stFileUploader"] {
    background: #e5e5e5 !important;
    border-radius: 18px !important;
    padding: 0 !important;
    border: none !important;
}

/* Actual drag & drop zone */
div[data-testid="stFileUploaderDropzone"] {
    min-height: 340px !important;
    padding: 90px 30px !important;
    background: #e5e5e5 !important;
    border-radius: 18px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Center uploader content */
div[data-testid="stFileUploaderDropzone"] > div {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 12px !important;
}

/* Uploader text & icon */
div[data-testid="stFileUploaderDropzone"] * {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* ===============================
   INPUTS (JOB DETAILS)
   =============================== */
input[type="text"],
textarea {
    background-color: #d9d9d9 !important;
    color: #000000 !important;
    border: 1px solid #888888 !important;
    border-radius: 10px !important;
    caret-color: #000000 !important;
}

input::placeholder,
textarea::placeholder {
    color: #555555 !important;
    opacity: 1 !important;
}

/* Labels */
label {
    color: #000000 !important;
    font-weight: 600;
}

/* ===============================
   METRIC CARDS
   =============================== */
.metric-box {
    background: #d9d9d9;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
}

.metric-value {
    font-size: 26px;
    font-weight: 800;
}

.metric-label {
    font-size: 13px;
    color: #666666;
}

/* ===============================
   IMAGES
   =============================== */
.stImage img {
    border-radius: 16px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stImage img:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}

/* ===============================
   FORCE DOWNLOAD BUTTON SAME AS ANALYZE
   =============================== */

/* Normal button (Analyze) */
.stButton > button {
    background: #e6e6e6 !important;
    color: #000000 !important;
    font-weight: 700 !important;
    border-radius: 20px !important;
    padding: 8px 28px !important;
    border: none !important;
}

/* Download button */
.stDownloadButton > button {
    background: #e6e6e6 !important;
    color: #000000 !important;
    font-weight: 700 !important;
    border-radius: 20px !important;
    padding: 8px 28px !important;
    border: none !important;
}

/* Hover effect (both) */
.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #d0d0d0 !important;
}

/* ===============================
   APP BORDER
   =============================== */
.stApp {
    border: 2px solid #000000;
    padding: 20px;
}

/* ===============================
   SECTION SEPARATOR LINE
   =============================== */
.section-divider {
    width: 100%;
    height: 1px;
    background-color: #000000;
    margin: 40px 0;
}



</style>
""", unsafe_allow_html=True)

# ================================
# HERO
# ================================
st.markdown('<div class="main-title">AI Powered Resume <br> Screening Tool</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">'
    'Your one stop for any AI powered resume screening tools,<br>'
    'select the candidate according to your Job description'
    '</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
# ================================
# HOW IT WORKS Image
# ================================
# --- HERO IMAGE (STREAMLIT SAFE) ---
st.image(
    "assets/How_it_works.png",
    use_column_width=True
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


# ================================
# STEP 1 – UPLOAD RESUME
# ================================
st.markdown('<div class="upload-title">Upload Resume</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="upload-subtitle">Upload your resume here in the box</div>',
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# Show uploaded resume names manually (fix invisible filenames)
if uploaded_files:
    st.markdown("**Uploaded Resumes:**")
    for file in uploaded_files:
        st.markdown(f"- {file.name}")


st.markdown(f"**Total uploaded:** {len(uploaded_files)} Resume")



st.markdown('</div>', unsafe_allow_html=True)


if uploaded_files:
    st.session_state.uploaded = True

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)



# ================================
# STEP 2 – JOB DETAILS
# ================================
if st.session_state.uploaded:

    st.markdown('<div class="upload-title">Job Details</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="upload-subtitle">Enter Job role and Description here in this Section</div>',
        unsafe_allow_html=True
    )

    job_role = st.text_input("Job Role (e.g. Python Developer)")
    job_desc = st.text_area("Job Description", height=200)

    if st.button("Analyze"):
        status = st.empty()

        status.info("Reading resumes...")
        time.sleep(0.5)

        status.info("Extracting skills...")
        time.sleep(0.7)

        status.info("Matching with job description...")
        time.sleep(0.7)

        st.session_state.analyzed = True
        status.success("✅ Analysis completed")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ================================
# STEP 3 – FINAL RESULTS
# ================================

if st.session_state.analyzed:

    results = analyze_resumes(uploaded_files, job_desc)

    if not results:
        st.warning("No valid results found.")
        st.stop()

    df = pd.DataFrame(results)

    st.markdown(
        '<div class="upload-title">Analysis Summary</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="upload-subtitle">'
        f'<strong>Job Role:</strong> {job_role}<br>'
        f'<strong>Total Resumes Analyzed:</strong> {len(uploaded_files)}'
        '</div>',
        unsafe_allow_html=True
    )

    # ===============================
    # METRICS
    # ===============================
    shortlisted_count = len(df[df["Matching Percentage"] >= 50])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{len(df)}</div>
            <div class="metric-label">Total Resumes</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{shortlisted_count}</div>
            <div class="metric-label">Shortlisted</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===============================
    # FINAL TABLE (ORDER FIXED)
    # ===============================
    display_df = df[
        [
            "Candidate",
            "Matching Percentage",
            "Phone",
            "Email",
            "Matched Skills",
            "Missing Skills"
        ]
    ]

    st.dataframe(display_df, use_container_width=True)



# ===============================
# DOWNLOAD RESULT (FINAL & STABLE)
# ===============================

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

if st.session_state.analyzed:

    st.markdown('<div class="upload-title">Download Result</div>', unsafe_allow_html=True)
   

    # Build filename ONLY from job role
    role_name = job_role.strip().replace(" ", "_") or "resume_screening"
    final_filename = f"{role_name}_results.xlsx"

    # Create Excel 
    excel_buffer = export_excel(df)


    # Download button
    st.download_button(
        label="Download Result",
        data=excel_buffer,
        file_name=final_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


st.markdown(
    """
    <style>
    .app-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        text-align: center;
        font-size: 13px;
        color: #e0e0e0;
        padding: 10px 0;
        z-index: 999;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    .app-footer b {
        color: #ffffff;
    }
    </style>

    <div class="app-footer">
        Developed with ❤️ by <b>NAMA Krityam</b>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    "<style>.stApp { padding-bottom: 60px; }</style>",
    unsafe_allow_html=True
)
