from datetime import datetime
import streamlit as st
#from utils.github_db import fetch_daily_challenge, append_result_to_drive
# To this:
from utils.github_db import (
    append_result_to_github,
    fetch_daily_challenge,
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
    challenge_data = fetch_daily_challenge(date_str)

if not challenge_data:
    st.warning(
        f"⏳ No challenge found for **{date_str}** yet! Please add the challenge JSON file to your Google Drive content folder."
    )
    st.stop()

st.success(f"Loaded challenge for **{challenge_data.get('date')}**!")

# 4. Render Questions & Collect Answers
questions = challenge_data.get("questions", [])

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
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
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
                    "question_id": qid,
                    "question_type": val["question_type"],
                    "selected_option": val["selected"],
                    "correct_answer": val["correct"],
                    "is_correct": is_correct
                }
                
                # Append each question result back to Google Drive
                #append_result_to_drive(result_row)
                append_result_to_github(result_row)
        
        # Display Results Dashboard
        st.balloons()
        st.success(f"🎉 Great job! You scored **{score} / {len(questions)}**!")
        
        st.markdown("### 📝 Review Explanations:")
        for qid, val in user_answers.items():
            status = "✅ Correct!" if val["selected"] == val["correct"] else "❌ Incorrect."
            st.write(f"**Q{qid}:** {status}")
            if val["selected"] != val["correct"]:
                st.write(f"- **Your Answer:** {val['selected']}")
                st.write(f"- **Correct Answer:** {val['correct']}")
            st.info(f"💡 **Explanation:** {val['explanation']}")
            st.markdown("---")