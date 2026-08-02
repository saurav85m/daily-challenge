import streamlit as st
import pandas as pd

from utils.github_db import get_progress_log

st.set_page_config(
    page_title="Student Progress Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Progress Dashboard")

# ----------------------------------------------------
# Load Progress Data
# ----------------------------------------------------

df = get_progress_log()

if df.empty:
    st.warning("No student progress found.")
    st.stop()

# ----------------------------------------------------
# Challenge Summary
# ----------------------------------------------------

challenge_summary = (
    df.groupby("date")
      .agg(
          score=("is_correct", "sum"),
          total=("is_correct", "count"),
          submitted_at=("timestamp", "first"),
          duration=("duration_display", "first"),
          duration_seconds=("duration_seconds", "first"),
      )
      .reset_index()
)

challenge_summary["accuracy"] = (
    challenge_summary["score"]
    / challenge_summary["total"]
    * 100
).round(2)

# ----------------------------------------------------
# Overall Statistics
# ----------------------------------------------------

total_challenges = len(challenge_summary)

total_questions = len(df)

total_correct = int(df["is_correct"].sum())

overall_accuracy = round(
    total_correct / total_questions * 100,
    2
)

avg_time_minutes = round(
    challenge_summary["duration_seconds"].mean() / 60,
    2
)

# ----------------------------------------------------
# Summary Cards
# ----------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Challenges",
        total_challenges
    )

with col2:
    st.metric(
        "Questions Correct",
        f"{total_correct}/{total_questions}"
    )

with col3:
    st.metric(
        "Accuracy",
        f"{overall_accuracy}%"
    )

with col4:
    st.metric(
        "Average Time",
        f"{avg_time_minutes} min"
    )

st.divider()

# ----------------------------------------------------
# Challenge History
# ----------------------------------------------------

st.subheader("📅 Challenge History")

history = challenge_summary[
    [
        "date",
        "score",
        "total",
        "accuracy",
        "duration",
        "submitted_at"
    ]
].copy()

history.rename(
    columns={
        "score": "Score",
        "total": "Total",
        "accuracy": "Accuracy (%)",
        "duration": "Time Taken",
        "submitted_at": "Submitted At",
        "date": "Date",
    },
    inplace=True,
)

history = history.sort_values(
    by="Date",
    ascending=False
)

st.dataframe(
    history,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ----------------------------------------------------
# Question Type Performance
# ----------------------------------------------------

# st.subheader("📚 Performance by Question Type")

# type_summary = (
#     df.groupby("question_type")
#       .agg(
#           Correct=("is_correct", "sum"),
#           Total=("is_correct", "count")
#       )
#       .reset_index()
# )

# type_summary["Accuracy (%)"] = (
#     type_summary["Correct"]
#     / type_summary["Total"]
#     * 100
# ).round(2)

# st.dataframe(
#     type_summary,
#     use_container_width=True,
#     hide_index=True,
# )
# st.subheader("📚 Performance by Question Type (Date Wise)")

# type_summary = (
#     df.groupby(["date", "question_type"])
#       .agg(
#           Correct=("is_correct", "sum"),
#           Total=("is_correct", "count")
#       )
#       .reset_index()
# )

# type_summary["Accuracy"] = (
#     type_summary["Correct"]
#     / type_summary["Total"]
#     * 100
# ).round(2)

# performance = type_summary.pivot(
#     index="date",
#     columns="question_type",
#     values="Accuracy"
# )

# performance = performance.rename(
#     columns={
#         "mcq": "MCQ (%)",
#         "output_prediction": "Output Prediction (%)",
#         "error_finding": "Error Finding (%)"
#     }
# )

# st.dataframe(
#     performance,
#     use_container_width=True
# )

st.subheader("📚 Performance by Question Type (Date Wise)")

# ----------------------------------------------------
# Build Question Type Summary
# ----------------------------------------------------

# type_summary = (
#     df.groupby(["date", "question_type"])
#       .agg(
#           Correct=("is_correct", "sum"),
#           Total=("is_correct", "count")
#       )
#       .reset_index()
# )

type_summary = (
    df.groupby(
        [
            "date",
            "topic",
            "question_type"
        ]
    )
    .agg(
        Correct=("is_correct", "sum"),
        Total=("is_correct", "count")
    )
    .reset_index()
)

# Calculate accuracy
type_summary["Accuracy"] = (
    type_summary["Correct"]
    / type_summary["Total"]
    * 100
).round(0).astype(int)

# Create display text like 4/5 (80%)
type_summary["Display"] = (
    type_summary["Correct"].astype(str)
    + "/"
    + type_summary["Total"].astype(str)
    + " ("
    + type_summary["Accuracy"].astype(str)
    + "%)"
)

# ----------------------------------------------------
# Create Pivot Table
# ----------------------------------------------------

# performance_table = (
#     type_summary
#     .pivot(
#         index="date",
#         columns="question_type",
#         values="Display"
#     )
#     .reset_index()
# )

performance_table = (
    type_summary.pivot(
        index=["date", "topic"],
        columns="question_type",
        values="Display"
    )
    .reset_index()
)

# Remove the extra column header
performance_table.columns.name = None

# Rename columns nicely
performance_table.rename(
    columns={
        "date": "Date",
        "topic": "Topic",
        "mcq": "MCQ",
        "predict_output": "Predict Output",
        "error_finding": "Error Finding",
    },
    inplace=True,
)

performance_table = performance_table.sort_values(
    by="Date",
    ascending=False
)

# st.dataframe(
#     performance_table,
#     use_container_width=True,
#     hide_index=True,
# )

st.dataframe(
    performance_table,
    hide_index=True,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# Accuracy Trend
# ----------------------------------------------------

st.subheader("📈 Accuracy Trend")

trend = challenge_summary[
    ["date", "accuracy"]
].copy()

trend.columns = [
    "Date",
    "Accuracy"
]

trend = trend.sort_values("Date")

st.line_chart(
    trend.set_index("Date")
)


# st.subheader("📈 Question Type Trend")

# st.line_chart(
#     performance
# )

st.subheader("📈 Question Type Trend")

graph_table = (
    type_summary
    .pivot(
        index="date",
        columns="question_type",
        values="Accuracy"
    )
)

graph_table.columns.name = None

graph_table.rename(
    columns={
        "mcq": "MCQ",
        "predict_output": "Predict Output",
        "error_finding": "Error Finding",
    },
    inplace=True,
)

st.line_chart(graph_table)