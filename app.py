import os
import json
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
    page_title="Medha Talent Optimizer",
    page_icon="📊",
    layout="wide"
)

st.title("Medha Talent Optimizer" )
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

14. JOB SUMMARY
Write a very short 1–2 sentence summary of the job.
Include the job title, main purpose, and 2–4 key responsibilities.
Maximum 40 words.
Do not add opinions or unnecessary details.

IMPORTANT PRINCIPLES:
- Analyze the job, not the person.
- Do not make a hiring decision.
- Do not rank candidates at this stage.
- Do not invent requirements.
- Distinguish explicit requirements from reasonable interpretations.
- Keep the analysis job-related and evidence-based.
- Make the output easy for a recruiter to review.

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
        "Screen candidates against the requirements extracted from the Job Description. "
        "The JD determines what is assessed; the candidate data provides the evidence."
    )

    if st.button("🚀 Screen Candidates"):
        if not job_description.strip():
            st.warning("Please analyze or paste a Job Description before screening candidates.")
        else:
            # Basic identity columns are required. Other candidate fields are allowed.
            required_columns = ["Candidate ID", "Name"]
            missing_columns = [
                col for col in required_columns
                if col not in candidates_df.columns
            ]

            if missing_columns:
                st.error("Missing columns: " + ", ".join(missing_columns))
            else:
                with st.spinner("Building JD-driven screening criteria and evaluating candidates with Gemini..."):
                    try:
                        candidate_records = (
                            candidates_df.fillna("").to_dict(orient="records")
                        )

                        screening_prompt = f"""
You are the Candidate Screening Engine of Medhā-Cayanam AI, an explainable AI recruitment decision-support system.

The Job Description is the SOURCE OF TRUTH for what should be assessed.
Do not use a fixed or generic screening checklist.
First derive the screening criteria from this specific Job Description, then evaluate every candidate against those same criteria.

JOB DESCRIPTION:
{job_description}

CANDIDATE DATABASE:
{json.dumps(candidate_records, ensure_ascii=False, default=str)}

TASK:
1. Extract the job-relevant requirements from the JD.
2. Classify each important requirement as Must-Have, Nice-to-Have, or Not Clearly Specified.
3. Convert the requirements into a practical screening scorecard. Suggested weights must total exactly 100.
4. Evaluate EVERY candidate against the JD-derived criteria.
5. For every criterion, use only evidence present in the candidate data.
6. If evidence is missing, say "Not Demonstrated" rather than assuming the candidate lacks the capability.
7. If the candidate data explicitly conflicts with a mandatory requirement, mark that requirement as "Does Not Meet" and explain the evidence.
8. Distinguish "Not Demonstrated" from "Does Not Meet".
9. Do not invent candidate experience, skills, education, certifications, or achievements.
10. Do not use or infer protected characteristics such as race, ethnicity, religion, gender, age, disability, health, marital status, or similar attributes.
11. Do not infer personality, intelligence, culture fit, or other non-job-related traits.
12. Do not make the final hiring decision. The output is decision support for recruiter review.
13. Keep the assessment traceable: explain the evidence behind important scores and gaps.

SCORING:
- Each criterion receives a score from 0 to 100.
- Overall Match % is the weighted average using the JD-derived weights.
- A missing resume field must not automatically mean the candidate fails a requirement.
- For Must-Have requirements, separately report whether the evidence Meets, Partially Meets, Not Demonstrated, or Does Not Meet the requirement.
- Use the overall score only as a summary of job-requirement alignment, not as an automatic hiring decision.

Return ONLY valid JSON in this exact structure:
{{
  "screening_criteria": [
    {{
      "criterion": "string",
      "category": "Knowledge | Skill | Ability | Experience | Education | Competency | Other",
      "requirement_type": "Must-Have | Nice-to-Have | Not Clearly Specified",
      "weight": 0,
      "evidence_expected": "string"
    }}
  ],
  "candidates": [
    {{
      "candidate_id": "string",
      "name": "string",
      "overall_match_percent": 0,
      "overall_status": "Meets Requirements | Potential Match | Review Required | Requirement Gap",
      "must_have_status": "All demonstrated | Some not demonstrated | Explicit gap identified | No must-haves specified",
      "criteria_assessment": [
        {{
          "criterion": "string",
          "score": 0,
          "status": "Meets | Partially Meets | Not Demonstrated | Does Not Meet",
          "evidence": "string"
        }}
      ],
      "strengths": ["string"],
      "gaps": ["string"],
      "why": "string"
    }}
  ]
}}

IMPORTANT:
- Include every candidate exactly once.
- Use the same screening criteria for every candidate.
- Screening criteria and weights must come from the JD, not from the candidate data.
- Weights must total exactly 100.
"""

                        response = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=screening_prompt
                        )

                        raw = response.text.strip()
                        if raw.startswith("```"):
                            raw = raw.replace("```json", "", 1).replace("```", "", 1).strip()

                        screening_data = json.loads(raw)
                        criteria = screening_data.get("screening_criteria", [])
                        candidate_results = screening_data.get("candidates", [])

                        if not criteria or not candidate_results:
                            raise ValueError("Gemini returned incomplete screening data.")

                        weight_total = sum(float(c.get("weight", 0)) for c in criteria)
                        if abs(weight_total - 100) > 0.01:
                            raise ValueError(
                                f"JD-derived screening weights total {weight_total:.1f}, not 100."
                            )

                        # Show the actual criteria generated from this JD.
                        st.subheader("🎯 JD-Derived Screening Criteria")
                        criteria_df = pd.DataFrame(criteria)
                        st.dataframe(criteria_df, use_container_width=True, hide_index=True)

                        # Convert candidate assessments into a ranking table.
                        screening_results = []
                        for item in candidate_results:
                            screening_results.append({
                                "Candidate ID": item.get("candidate_id", ""),
                                "Name": item.get("name", ""),
                                "Match %": float(item.get("overall_match_percent", 0)),
                                "Status": item.get("overall_status", "Review Required"),
                                "Must-Have Status": item.get("must_have_status", ""),
                                "Strengths": "; ".join(item.get("strengths", [])[:4]),
                                "Gaps": "; ".join(item.get("gaps", [])[:4]),
                                "WHY": item.get("why", ""),
                                "Criteria Assessment": json.dumps(
                                    item.get("criteria_assessment", []),
                                    ensure_ascii=False
                                )
                            })

                        results_df = pd.DataFrame(screening_results)
                        results_df = results_df.sort_values(
                            by="Match %", ascending=False
                        ).reset_index(drop=True)
                        results_df.insert(0, "Rank", range(1, len(results_df) + 1))

                        st.session_state["results_df"] = results_df
                        st.session_state["screening_criteria"] = criteria
                        st.session_state["screening_raw"] = screening_data

                        st.success(
                            f"JD-driven screening completed for {len(results_df)} candidates."
                        )

                    except json.JSONDecodeError:
                        st.error(
                            "Gemini returned an invalid screening format. Please try screening again."
                        )
                    except Exception as e:
                        st.error(f"Error during JD-driven candidate screening: {e}")

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
        f"Showing Top {top_n} candidates out of {total_candidates} screened candidates."
    )

    st.dataframe(
        top_candidates[
            [
                "Rank",
                "Candidate ID",
                "Name",
                "Match %",
                "Status",
                "Must-Have Status",
                "Strengths",
                "Gaps",
                "WHY"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🔍 Requirement-Level Evidence")
    selected_name = st.selectbox(
        "Select a candidate to inspect",
        top_candidates["Name"].tolist(),
        key="screening_candidate_detail"
    )

    selected = results_df[results_df["Name"] == selected_name].iloc[0]
    st.write(f"**Overall Match:** {selected['Match %']:.1f}%")
    st.write(f"**Status:** {selected['Status']}")
    st.write(f"**Must-Have Status:** {selected['Must-Have Status']}")

    try:
        detail = json.loads(selected["Criteria Assessment"])
        detail_df = pd.DataFrame(detail)
        st.dataframe(detail_df, use_container_width=True, hide_index=True)
    except Exception:
        st.write(selected["Criteria Assessment"])

    st.write(f"**Strengths:** {selected['Strengths'] or 'None explicitly demonstrated'}")
    st.write(f"**Gaps:** {selected['Gaps'] or 'None explicitly identified'}")
    st.write(f"**WHY:** {selected['WHY']}")

