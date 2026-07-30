from datetime import datetime
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.common import get_india_timestamp
#from utils.github_db import fetch_daily_challenge, append_result_to_drive
# To this:
from utils.github_db import (
    append_result_to_github,
    append_results_to_github,
    fetch_daily_challenge,
    get_submission_details,
)

# 1. Page Configuration for Mobile-First experience
st.set_page_config(
    page_title="Gagu's Daily Challenge",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom styling for mobile friendliness
st.markdown(
    """
    <style>
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎯 Gagu's Daily Challenge")

st.page_link(
    "pages/1_Dashboard.py",
    label="View Progress Dashboard",
    icon=""
)

st.write("Sharpen your coding skills 15 minutes a day!")

# 2. Student Identification & Date selection
col1, col2 = st.columns([1, 1])
with col1:
    student_name = st.selectbox(
        "Student", ["Gagu", "Guest"], index=0
    )
with col2:
    challenge_date = st.date_input(
        "Challenge Date", value=datetime.now().date()
    )

st.divider()

# 3. Fetch Challenge from Google Drive
with st.spinner("Fetching today's challenge..."):
    date_str = challenge_date.strftime("%Y-%m-%d")
    submission = get_submission_details(
        student_name,
        date_str
    )
    #st.write(date_str) #Saurav
    challenge_data = fetch_daily_challenge(date_str)
    topic = challenge_data.get("topic", "")

if not challenge_data:
    st.warning(
        f"⏳ No challenge found for **{date_str}** yet! Please add the challenge JSON file to your Google Drive content folder."
    )
    st.stop()

st.success(f"Loaded challenge for **{challenge_data.get('date')}**!")

# score = df_filtered["is_correct"].sum()

# total = len(df_filtered)

# accuracy = score / total * 100

if submission:

    st.success("✅ You have already completed today's challenge. Please choose another date or come back tomorrow.")

    st.write(f"**Student :** {student_name}")
    st.write(f"**Date :** {date_str}")
    st.write(f"**Score :** {submission['score']} / {submission['total']}")
    st.write(f"**Accuracy :** {submission['accuracy']}%")
    st.write(f"**Submitted At :** {submission['submitted_at']}")

    # st.info(
    #     "Please choose another date or come back tomorrow."
    # )

    st.stop()

# 4. Render Questions & Collect Answers
questions = challenge_data.get("questions", [])
# Start timer when quiz is first loaded
if "challenge_start_time" not in st.session_state:
    st.session_state.challenge_start_time = get_india_timestamp()

with st.form("challenge_form"):
    user_answers = {}
    
    for idx, q in enumerate(questions):
        st.subheader(f"Question {q.get('id')}: ({q.get('type').replace('_', ' ').title()})")
        st.write(q.get("question"))
        
        # Render code snippet if available (for output_prediction or error_finding)
        if "code_snippet" in q:
            st.code(q.get("code_snippet"), language="python")
            
        # Radio buttons for options
        options = q.get("options", [])
        user_choice = st.radio(
            "Select your answer:",
            options,
            key=f"q_{q.get('id')}",
            index=None # Forces her to intentionally pick an option
        )
        user_answers[q.get('id')] = {
            "question_type": q.get("type"),
            "selected": user_choice,
            "correct": q.get("answer"),
            "explanation": q.get("explanation")
        }
        st.divider()

    # Submit button inside the form
    submitted = st.form_submit_button("🚀 Submit All Answers")

# 5. Evaluate and Save Results to Google Drive
if submitted:
    # Check if all questions were answered
    unanswered = [qid for qid, val in user_answers.items() if val["selected"] is None]
    
    if unanswered:
        st.error("⚠️ Please answer all questions before submitting!")
    else:
        score = 0
        rows_to_save = []
        #timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #timestamp = get_india_timestamp().strftime("%Y-%m-%d %H:%M:%S")
        end_time = get_india_timestamp()
        start_time = st.session_state.challenge_start_time

        duration = end_time - start_time
        duration_seconds = int(duration.total_seconds())

        minutes = duration_seconds // 60
        seconds = duration_seconds % 60

        duration_display = f"{minutes} min {seconds} sec"

        timestamp = end_time.strftime("%Y-%m-%d %H:%M:%S")

        with st.spinner("Saving your progress to Google Drive..."):
            for qid, val in user_answers.items():
                is_correct = (val["selected"] == val["correct"])
                if is_correct:
                    score += 1
                
                # Prepare result row dictionary for Google Drive CSV logging
                result_row = {
                    "timestamp": timestamp,
                    "student_name": student_name,
                    "date": date_str,
                    "topic": topic,
                    "duration_seconds": duration_seconds,
                    "duration_display": duration_display,
                    "question_id": qid,
                    "question_type": val["question_type"],
                    "selected_option": val["selected"],
                    "correct_answer": val["correct"],
                    "is_correct": is_correct
                }
                
                # Append each question result back to Google Drive
                #append_result_to_drive(result_row)
                #append_result_to_github(result_row)
                
                # Store in memory instead of saving immediately
                rows_to_save.append(result_row)

        # Save all rows in ONE GitHub commit
        success = append_results_to_github(rows_to_save)
        if success and "challenge_start_time" in st.session_state:
            del st.session_state.challenge_start_time

        if success:
            st.success("✅ Results saved successfully.")
        else:
            st.error("❌ Failed to save results.")
        
        # Display Results Dashboard
        st.balloons()
        st.success(f"🎉 Great job! You scored **{score} / {len(questions)}**!")
        st.info(f"⏱ Time Taken: {duration_display}")
        
        st.markdown("### 📝 Review Explanations:")
        for qid, val in user_answers.items():
            status = "✅ Correct!" if val["selected"] == val["correct"] else "❌ Incorrect."
            st.write(f"**Q{qid}:** {status}")
            if val["selected"] != val["correct"]:
                st.write(f"- **Your Answer:** {val['selected']}")
                st.write(f"- **Correct Answer:** {val['correct']}")
            st.info(f"💡 **Explanation:** {val['explanation']}")
            st.markdown("---")