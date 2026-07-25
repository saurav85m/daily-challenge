import base64
import io
import json
import pandas as pd
import requests
import streamlit as st
from github import Github
import requests


def get_github_repo():
  """Authenticate and return the GitHub repository instance."""
  cfg = st.secrets["github"]
  g = Github(cfg["token"])
  repo = g.get_repo(f"{cfg['repo_owner']}/{cfg['repo_name']}")
  return repo


# def fetch_daily_challenge(date_str):
#   """Fetch the daily challenge JSON file directly from GitHub."""
#   cfg = st.secrets["github"]
#   file_path = f"content/challenge_{date_str}.json"
#   branch = cfg.get("branch", "main")

#   # Use raw GitHub URL for fast, lightweight fetching
#   raw_url = f"https://raw.githubusercontent.com/{cfg['repo_owner']}/{cfg['repo_name']}/{branch}/{file_path}"

#   try:
#     response = requests.get(raw_url)
#     if response.status_code == 200:
#       return response.json()
#     else:
#       return None
#   except Exception:
#     return None

#@st.cache_data(ttl=0) # ttl=0 ensures Streamlit doesn't cache old versions
def fetch_daily_challenge(date_str):
    """
    Fetches the challenge JSON for a specific date from the GitHub repository.
    """
    cfg = st.secrets["github"]
    token = cfg["token"]
    repo_owner = cfg["repo_owner"]
    repo_name = cfg["repo_name"]
    branch = cfg.get("branch", "main")
    
    # Dynamically targets the file matching the selected date
    file_path = f"content/challenge_{date_str}.json"
    
    url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{file_path}"
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(url, headers=headers)
    #Saurav
    #st.write("URL:", url)
    #st.write("Status:", response.status_code)
    #st.write("Response:", response.text)
    
    if response.status_code == 200:
        return response.json()
    #Saurav
    return None


def append_result_to_github(result_dict):
  """Append a submission result to progress_log.csv and commit it back to GitHub."""
  repo = get_github_repo()
  file_path = "results/progress_log.csv"
  branch = st.secrets["github"].get("branch", "main")

  df_new_row = pd.DataFrame([result_dict])

  try:
    # Try fetching the existing progress log from the repo
    file_content = repo.get_contents(file_path, ref=branch)
    decoded_content = base64.b64decode(file_content.content).decode("utf-8")
    df_existing = pd.read_csv(io.StringIO(decoded_content))

    # Append new row
    df_updated = pd.concat([df_existing, df_new_row], ignore_index=True)
    csv_content = df_updated.to_csv(index=False)

    # Update file on GitHub
    repo.update_file(
        path=file_path,
        message=f"Update progress log for {result_dict['date']}",
        content=csv_content,
        sha=file_content.sha,
        branch=branch,
    )
  except Exception:
    # If progress_log.csv doesn't exist yet, create it
    csv_content = df_new_row.to_csv(index=False)
    repo.create_file(
        path=file_path,
        message="Initialize progress log",
        content=csv_content,
        branch=branch,
    )

def append_results_to_github(results):
    """
    Append multiple submission results to progress_log.csv
    using a single GitHub commit.
    """

    repo = get_github_repo()

    file_path = "results/progress_log.csv"

    branch = st.secrets["github"].get("branch", "main")

    # Create DataFrame from all result rows
    df_new_rows = pd.DataFrame(results)

    try:
        # Read existing CSV
        file_content = repo.get_contents(file_path, ref=branch)

        decoded_content = base64.b64decode(
            file_content.content
        ).decode("utf-8")

        df_existing = pd.read_csv(
            io.StringIO(decoded_content)
        )

        # Append ALL rows
        df_updated = pd.concat(
            [df_existing, df_new_rows],
            ignore_index=True
        )

        csv_content = df_updated.to_csv(index=False)

        # ONE GitHub commit
        repo.update_file(
            path=file_path,
            message=f"Update progress log for {results[0]['date']}",
            content=csv_content,
            sha=file_content.sha,
            branch=branch,
        )

    except Exception:

        # CSV doesn't exist yet
        csv_content = df_new_rows.to_csv(index=False)

        repo.create_file(
            path=file_path,
            message="Initialize progress log",
            content=csv_content,
            branch=branch,
        )

    return True

def has_student_submitted(student_name, date_str):
    """
    Returns True if the student has already submitted
    the selected challenge date.
    """

    repo = get_github_repo()

    file_path = "results/progress_log.csv"

    branch = st.secrets["github"].get("branch", "main")

    try:

        file_content = repo.get_contents(
            file_path,
            ref=branch
        )

        decoded = base64.b64decode(
            file_content.content
        ).decode("utf-8")

        df = pd.read_csv(io.StringIO(decoded))

        # Empty CSV
        if df.empty:
            return False

        submitted = (
            (df["student_name"] == student_name)
            &
            (df["date"] == date_str)
        ).any()

        return submitted

    except Exception:
        # CSV doesn't exist yet
        return False

def get_submission_details(student_name, date_str):
    """
    Returns submission details if the student has already
    completed the challenge, otherwise returns None.
    """

    repo = get_github_repo()

    file_path = "results/progress_log.csv"

    branch = st.secrets["github"].get("branch", "main")

    try:

        file_content = repo.get_contents(file_path, ref=branch)

        decoded = base64.b64decode(
            file_content.content
        ).decode("utf-8")

        df = pd.read_csv(io.StringIO(decoded))

        # Filter for this student and date
        df_filtered = df[
            (df["student_name"] == student_name)
            &
            (df["date"] == date_str)
        ]

        if df_filtered.empty:
            return None

        score = df_filtered["is_correct"].sum()
        total = len(df_filtered)
        accuracy = round(score / total * 100, 2)

        submitted_at = df_filtered.iloc[0]["timestamp"]

        return {
            "score": score,
            "total": total,
            "accuracy": accuracy,
            "submitted_at": submitted_at
        }

    except Exception:
        return None