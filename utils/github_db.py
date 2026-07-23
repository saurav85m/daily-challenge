import base64
import io
import json
import pandas as pd
import requests
import streamlit as st
from github import Github


def get_github_repo():
  """Authenticate and return the GitHub repository instance."""
  cfg = st.secrets["github"]
  g = Github(cfg["token"])
  repo = g.get_repo(f"{cfg['repo_owner']}/{cfg['repo_name']}")
  return repo


def fetch_daily_challenge(date_str):
  """Fetch the daily challenge JSON file directly from GitHub."""
  cfg = st.secrets["github"]
  file_path = f"content/challenge_{date_str}.json"
  branch = cfg.get("branch", "main")

  # Use raw GitHub URL for fast, lightweight fetching
  raw_url = f"https://raw.githubusercontent.com/{cfg['repo_owner']}/{cfg['repo_name']}/{branch}/{file_path}"

  try:
    response = requests.get(raw_url)
    if response.status_code == 200:
      return response.json()
    else:
      return None
  except Exception:
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