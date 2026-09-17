import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()

# Connect to Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Page settings
st.set_page_config(
    page_title="Medhā-Cayanam AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Medhā-Cayanam AI")
st.subheader("AI Recruitment Decision-Support Copilot")

st.write(
    "Transform a Job Description into structured hiring requirements "
    "using KSAO, competencies, and job-relevant criteria."
)

st.divider()

# Job Description
st.header("1. Job Description")

job_description = st.text_area(
    "Paste the Job Description",
    height=300,
    placeholder="Paste the complete Job Description here..."
)

# Analyze button
if st.button("🔍 Analyze Job Description"):

    if not job_description.strip():
        st.warning("Please paste a Job Description first.")

    else:
        with st.spinner("Analyzing Job Description with Gemini..."):

            prompt = f"""
You are the Job Analysis Engine of Medhā-Cayanam AI,
an explainable AI recruitment decision-support system.

Analyze the following Job Description using structured
HR and competency-based frameworks.

1. JOB ANALYSIS
Identify:
- Job Title
- Department/function
- Industry
- Primary purpose of the role
- Major responsibilities

2. KSAO ANALYSIS
Classify requirements into:
- Knowledge
- Skills
- Abilities
- Other job-relevant characteristics

Do not use protected characteristics such as gender, religion,
race, ethnicity, age, disability, or similar attributes.

3. REQUIREMENT CLASSIFICATION
Classify important requirements as:
- Must-Have
- Nice-to-Have
- Not Clearly Specified

4. COMPETENCY FRAMEWORK
Identify relevant competencies such as:
- Analytical Thinking
- Problem Solving
- Communication
- Teamwork
- Attention to Detail
- Learning Agility
- Job-specific competencies

Only include competencies supported by the JD.

5. EXPERIENCE ANALYSIS
Identify:
- Minimum experience
- Preferred experience
- Whether freshers are acceptable
- Relevant types of previous experience

6. EDUCATION ANALYSIS
Identify:
- Required degree
- Preferred educational background
- Whether the degree is mandatory or flexible

7. JOB REQUIREMENT → COMPETENCY MAPPING
Map each major requirement to the competency or capability
it represents.

8. EVIDENCE EXPECTATIONS
For each major requirement, explain what evidence we should
look for in a candidate's resume or application.

9. REQUIREMENT GAP ANALYSIS
Identify:
- Ambiguous requirements
- Missing information
- Requirements needing clarification
- Requirements difficult to assess from a resume alone

10. WEIGHTED SCORECARD
Create a suggested scorecard with weights totaling exactly 100%.

For each criterion provide:
- Criterion
- Weight
- Reason for the weight

These are AI-suggested starting points, not universal HR standards.

11. INTERVIEW ASSESSMENT AREAS
Identify areas that should later be tested through
a structured interview.

12. BARS DIMENSIONS
Suggest competencies that could later be evaluated using
Behaviorally Anchored Rating Scales.

13. ANALYSIS CONFIDENCE
Provide:
- High
- Medium
- Low

Explain briefly why.

IMPORTANT PRINCIPLES:
- Analyze the job, not the person.
- Do not make a hiring decision.
- Do not rank candidates at this stage.
- Do not invent requirements.
- Distinguish explicit requirements from reasonable interpretations.
- Keep the analysis job-related and evidence-based.
- Make the output easy for a recruiter to review.

14. JOB SUMMARY
Write a very short 1–2 sentence summary of the job.
Include the job title, main purpose, and 2–4 key responsibilities.
Maximum 40 words.
Do not add opinions or unnecessary details.

JOB DESCRIPTION:

{job_description}
"""

            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                job_analysis = response.text

                st.success("Job Description analyzed successfully!")

                st.markdown("### 📋 AI Job Analysis")
                st.write(job_analysis)

            except Exception as e:
                st.error(f"Error connecting to Gemini: {e}")
                # ============================================================
# CANDIDATE DATABASE
# ============================================================

st.divider()

st.header("👥 Candidate Database")

st.write(
    "Upload a candidate database in Excel format to begin "
    "AI-assisted candidate screening."
)

candidate_file = st.file_uploader(
    "Upload Candidate Excel File",
    type=["xlsx"],
    key="candidate_upload"
)

if candidate_file is not None:

    try:
        candidates_df = pd.read_excel(candidate_file)

        st.success(
            f"Successfully loaded {len(candidates_df)} candidates."
        )

        st.subheader("📊 Candidate Database")

        st.dataframe(
            candidates_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("📋 Database Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Candidates",
                len(candidates_df)
            )

        with col2:
            st.metric(
                "Columns",
                len(candidates_df.columns)
            )

        with col3:
            st.metric(
                "File",
                candidate_file.name
            )

    except Exception as e:

        st.error(
            f"Could not read the candidate file: {e}"
        )
       # ============================================================
# CANDIDATE SCREENING ENGINE
# ============================================================

if candidate_file is not None:

    st.divider()

    st.header("🔎 Candidate Screening")

    st.write(
        "Screen candidates against the job requirements using "
        "a transparent, evidence-based scoring system."
    )

    if st.button("🚀 Screen Candidates"):

        # Required columns
        required_columns = [
            "Candidate ID",
            "Name",
            "Email",
            "Degree",
            "Skills",
            "Experience (Years)",
            "Knowledge",
            "Competencies",
            "City"
        ]

        missing_columns = [
            col for col in required_columns
            if col not in candidates_df.columns
        ]

        if missing_columns:

            st.error(
                "Missing columns: "
                + ", ".join(missing_columns)
            )

        else:

            # ------------------------------------------------
            # Scoring criteria
            # ------------------------------------------------

            weights = {
                "Skills": 30,
                "Experience": 20,
                "Knowledge": 15,
                "Education": 10,
                "Problem Solving": 10,
                "Communication": 5,
                "Competencies": 10
            }

            screening_results = []

            # ------------------------------------------------
            # Screen each candidate
            # ------------------------------------------------

            for _, candidate in candidates_df.iterrows():

                skills = str(candidate["Skills"]).lower()
                knowledge = str(candidate["Knowledge"]).lower()
                competencies = str(
                    candidate["Competencies"]
                ).lower()

                degree = str(candidate["Degree"]).lower()

                experience = float(
                    candidate["Experience (Years)"]
                )

                # --------------------------------------------
                # Skills score
                # --------------------------------------------

                skill_points = 0

                important_skills = [
                    "google ads",
                    "excel",
                    "ga4",
                    "digital marketing",
                    "analytics"
                ]

                for skill in important_skills:

                    if skill in skills:
                        skill_points += 6

                skill_score = min(skill_points, 30)

                # --------------------------------------------
                # Experience score
                # --------------------------------------------

                if experience >= 2:
                    experience_score = 20

                elif experience >= 1:
                    experience_score = 17

                elif experience >= 0.5:
                    experience_score = 14

                elif experience > 0:
                    experience_score = 10

                else:
                    experience_score = 7

                # --------------------------------------------
                # Knowledge score
                # --------------------------------------------

                knowledge_terms = [
                    "google ads",
                    "campaign",
                    "cpc",
                    "ctr",
                    "roas",
                    "ga4",
                    "conversion",
                    "reporting",
                    "optimization"
                ]

                knowledge_matches = sum(
                    term in knowledge
                    for term in knowledge_terms
                )

                knowledge_score = min(
                    knowledge_matches * 2,
                    15
                )

                # --------------------------------------------
                # Education score
                # --------------------------------------------

                relevant_degrees = [
                    "bba",
                    "b.com",
                    "commerce",
                    "economics",
                    "marketing",
                    "business"
                ]

                education_score = 10 if any(
                    degree_name in degree
                    for degree_name in relevant_degrees
                ) else 5

                # --------------------------------------------
                # Problem-solving score
                # --------------------------------------------

                problem_terms = [
                    "problem solving",
                    "analytical thinking",
                    "analytical",
                    "data analysis"
                ]

                problem_score = 10 if any(
                    term in competencies or
                    term in knowledge
                    for term in problem_terms
                ) else 5

                # --------------------------------------------
                # Communication score
                # --------------------------------------------

                communication_score = (
                    5
                    if "communication" in competencies
                    else 3
                )

                # --------------------------------------------
                # Competency score
                # --------------------------------------------

                competency_terms = [
                    "teamwork",
                    "attention to detail",
                    "learning agility",
                    "problem solving",
                    "analytical thinking"
                ]

                competency_matches = sum(
                    term in competencies
                    for term in competency_terms
                )

                competency_score = min(
                    competency_matches * 2,
                    10
                )

                # --------------------------------------------
                # Total score
                # --------------------------------------------

                total_score = (
                    skill_score
                    + experience_score
                    + knowledge_score
                    + education_score
                    + problem_score
                    + communication_score
                    + competency_score
                )

                # --------------------------------------------
                # Fit category
                # --------------------------------------------

                if total_score >= 85:
                    fit = "Strong Match"

                elif total_score >= 70:
                    fit = "Potential Match"

                elif total_score >= 50:
                    fit = "Review"

                else:
                    fit = "Requirement Gap"

                # --------------------------------------------
                # WHY?
                # --------------------------------------------

                strengths = []

                if "google ads" in skills:
                    strengths.append("Google Ads")

                if "excel" in skills:
                    strengths.append("Excel")

                if "ga4" in skills:
                    strengths.append("GA4")

                if "analytical thinking" in competencies:
                    strengths.append("Analytical Thinking")

                if "problem solving" in competencies:
                    strengths.append("Problem Solving")

                gaps = []

                if "google ads" not in skills:
                    gaps.append("Google Ads")

                if "excel" not in skills:
                    gaps.append("Excel")

                if "ga4" not in skills:
                    gaps.append("GA4")

                if experience < 0.5:
                    gaps.append("Limited experience")

                if strengths:
                    strength_text = ", ".join(strengths[:3])

                else:
                    strength_text = "Limited evidence"

                if gaps:
                    gap_text = ", ".join(gaps[:3])

                else:
                    gap_text = "No major gap identified"

                why_text = (
                    f"Strengths: {strength_text}. "
                    f"Main gaps: {gap_text}."
                )

                screening_results.append({
                    "Candidate ID": candidate["Candidate ID"],
                    "Name": candidate["Name"],
                    "Match %": total_score,
                    "Fit": fit,
                    "Skills": skill_score,
                    "Experience": experience_score,
                    "Knowledge": knowledge_score,
                    "Education": education_score,
                    "Problem Solving": problem_score,
                    "Communication": communication_score,
                    "Competencies": competency_score,
                    "WHY": why_text
                })

            # ------------------------------------------------
            # Create results DataFrame
            # ------------------------------------------------

            results_df = pd.DataFrame(
                screening_results
            )

         # Sort highest score first
            results_df = results_df.sort_values(
                by="Match %",
                ascending=False
            ).reset_index(drop=True)

            # Add rank number
            results_df.insert(
                0,
                "Rank",
                range(1, len(results_df) + 1)
            )

            # Save results so they remain available
            st.session_state["results_df"] = results_df

            # ------------------------------------------------
            # Display screening results
            # ------------------------------------------------

            st.success("Candidates screened successfully!")

# ============================================================
# TOP CANDIDATES / RANKING
# ============================================================

if (
    candidate_file is not None
    and "results_df" in st.session_state
):

    results_df = st.session_state["results_df"]

    st.divider()
    st.subheader("🏆 Candidate Ranking")

    total_candidates = len(results_df)

    top_n = st.number_input(
        "How many top candidates do you want to view?",
        min_value=1,
        max_value=total_candidates,
        value=min(5, total_candidates),
        step=1,
        key="top_candidates_count"
    )

    top_n = int(top_n)

    top_candidates = results_df.head(top_n)

    st.write(
        f"Showing Top {top_n} candidates out of "
        f"{total_candidates} screened candidates."
    )

    st.dataframe(
        top_candidates[
            [
                "Rank",
                "Candidate ID",
                "Name",
                "Match %",
                "Fit",
                "WHY"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
