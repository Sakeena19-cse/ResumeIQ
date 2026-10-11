import pandas as pd
import streamlit as st

from analyzer import analyze_resume, extract_pdf_text


st.set_page_config(
    page_title="ResumeIQ | Resume Intelligence",
    page_icon="📄",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #ede9fe, #f5f3ff);
        margin-bottom: 22px;
    }

    .hero h1 {
        color: #4c1d95;
        font-size: 2.5rem;
        margin-bottom: 8px;
    }

    .hero p {
        color: #4b5563;
        font-size: 1.05rem;
    }

   div[data-testid="stMetric"] {
    background: #faf9ff;
    border: 1px solid #e9e3ff;
    padding: 16px;
    border-radius: 12px;
}

div[data-testid="stMetric"] [data-testid="stMetricLabel"],
div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #1f2937 !important;
}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>ResumeIQ</h1>
        <p>
            Turn your resume into an actionable career insights report.
            Compare your skills with a target job using NLP.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("ResumeIQ")
    st.caption("Your resume analysis workspace")
    st.divider()
    st.subheader("How it works")
    st.write("1. Upload a text-based PDF.")
    st.write("2. Paste a job description.")
    st.write("3. Review matching skills and text similarity.")
    st.divider()
    st.caption(
        "Scores are experimental text-overlap estimates, "
        "not hiring probabilities or measures of ability."
    )

st.subheader("Analyze your resume")

left, right = st.columns(2)

with left:
    uploaded_file = st.file_uploader(
        "Upload resume (PDF)",
        type=["pdf"],
        help="Use a text-based PDF. Scanned PDFs may not work.",
    )

with right:
    job_description = st.text_area(
        "Paste job description",
        height=200,
        placeholder=(
            "Example: Python developer with Flask, SQL, "
            "REST API, Git, and Docker experience..."
        ),
    )

analyze_clicked = st.button(
    "Analyze Resume",
    type="primary",
    use_container_width=True,
)

if analyze_clicked:
    st.session_state.pop("analysis", None)

    if uploaded_file is None:
        st.error("Please upload a PDF resume.")

    elif not job_description.strip():
        st.error("Please paste a job description.")

    else:
        try:
            with st.spinner("Extracting text and analyzing skills..."):
                resume_text = extract_pdf_text(uploaded_file)
                result = analyze_resume(
                    resume_text,
                    job_description,
                )

            st.session_state["analysis"] = result
            st.session_state["job_description"] = job_description

        except Exception as error:
            st.error(f"Analysis failed: {error}")

result = st.session_state.get("analysis")

if result:
    st.divider()
    st.subheader("Your analysis overview")

    score = result["overall_score"]
    coverage = result["skill_coverage"]
    similarity = result["text_similarity"]
    st.write("DEBUG - analysis results:",result)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Overall Match Estimate",
        f"{score:.1f}%" if score is not None else "N/A",
    )
    col2.metric(
        "Skill Coverage",
        f"{coverage:.1f}%" if coverage is not None else "N/A",
    )
    col3.metric(
        "Text Similarity",
        f"{similarity:.1f}%",
    )

    st.caption(
        "Overall estimate = 80% recognized skill coverage + "
        "20% TF-IDF text similarity. It does not predict hiring."
    )

    if coverage is not None:
        st.write("Recognized skill coverage")
        st.progress(coverage / 100)

    if not result["job_skills"]:
        st.warning(
            "No recognized skills were found in the job description. "
            "Try a more detailed description or expand the skill dictionary."
        )

    st.divider()
    st.subheader("Skill gap analysis")

    matched = result["matched_skills"]
    missing = result["missing_skills"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Matched skills")
        st.metric("Skills found in both", len(matched))

        if matched:
            for skill in matched:
                st.markdown(f"- ✅ {skill}")
        else:
            st.info("No recognized matching skills were found.")

    with col2:
        st.markdown("#### Skills to review")
        st.metric("Required skills not detected", len(missing))

        if missing:
            for skill in missing:
                st.markdown(f"- 🔎 {skill}")
        else:
            st.success("No recognized skill gaps detected.")

    # Visual comparison of recognized job skills.
    if result["job_skills"]:
        st.divider()
        st.subheader("Skills comparison chart")

        chart_rows = [
            {
                "Skill": skill,
                "Status": (
                    "Matched" if skill in matched else "Not detected"
                ),
                "Count": 1,
            }
            for skill in result["job_skills"]
        ]

        chart_df = pd.DataFrame(chart_rows)

        chart_data = chart_df.pivot_table(
            index="Skill",
            columns="Status",
            values="Count",
            aggfunc="sum",
            fill_value=0,
        )

        for column in ["Matched", "Not detected"]:
            if column not in chart_data.columns:
                chart_data[column] = 0

        chart_data = chart_data[["Matched", "Not detected"]]
        st.bar_chart(chart_data)

    st.divider()
    st.subheader("Action plan")

    if missing:
        st.write(
            "Review these job requirements and honestly assess "
            "whether you have the relevant experience."
        )

        for skill in missing:
            st.markdown(f"- Learn or practice **{skill}** if relevant.")

        st.info(
            "Update your resume only with skills you genuinely possess "
            "and can explain in an interview."
        )
    else:
        st.write(
            "No recognized skill gaps were detected. Review the job's "
            "responsibilities and ensure your resume includes relevant "
            "project examples."
        )

    with st.expander("View detected skills"):
        st.write("**Resume skills**")
        st.write(", ".join(result["resume_skills"]) or "None detected")

        st.write("**Job description skills**")
        st.write(", ".join(result["job_skills"]) or "None detected")

    # Detailed downloadable report.
    report_rows = [
        {
            "Section": "Score",
            "Item": "Overall match estimate",
            "Value": score if score is not None else "N/A",
        },
        {
            "Section": "Score",
            "Item": "Skill coverage",
            "Value": coverage if coverage is not None else "N/A",
        },
        {
            "Section": "Score",
            "Item": "Text similarity",
            "Value": similarity,
        },
    ]

    for skill in result["job_skills"]:
        report_rows.append({
            "Section": "Skill analysis",
            "Item": skill,
            "Value": "Matched" if skill in matched else "Not detected",
        })

    report_df = pd.DataFrame(report_rows)

    st.divider()
    st.subheader("Export report")

    st.download_button(
        label="Download detailed CSV report",
        data=report_df.to_csv(index=False),
        file_name="resumeiq_analysis.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.caption(
        "Privacy reminder: use sample resumes for public demos. "
        "The analysis is an estimate and may miss skills due to "
        "wording or limitations in the skill dictionary."
    )
else:
    st.info(
        "Upload a resume and paste a job description to see "
        "your analysis dashboard."
    )