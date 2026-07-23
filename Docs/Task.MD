Implementation Plan & Task List
Phase 1: Google Drive & API Setup
[X] Task 1.1: Create a Dedicated Project Folder

Set up a root folder in Google Drive (e.g., Gagu_Daily_Challenge) with subfolders for /content (daily questions) and /results (student submissions).

[X] Task 1.2: Google Cloud Console & Service Account

Create a Google Cloud project, enable the Google Drive API, and generate a Service Account JSON key.

[X] Task 1.3: Folder Permissions

Share both the /content and /results Drive folders with the Service Account's email address (giving it Editor access).

Phase 2: Data Structure Design
[X] Task 2.1: Design Content Schema (challenge_YYYY-MM-DD.json)

Structure daily challenges to support MCQs, error-finding, and output predictions:

JSON
{
  "date": "2026-07-21",
  "questions": [
    {
      "id": 1,
      "type": "mcq",
      "question": "What is the output of print(type([]))?",
      "options": ["<class 'list'>", "<class 'dict'>", "<class 'tuple'>"],
      "answer": "<class 'list'>"
    }
  ]
}
[ ] Task 2.2: Design Progress Log Schema (progress_log.csv)

Define columns for tracking submissions: timestamp, student_name, date, question_id, selected_option, is_correct.

Phase 3: Core Streamlit Application Development (app.py)
[X] Task 3.1: Drive Connection Module (utils/gdrive.py)

Implement authentication using gspread or google-api-python-client via Streamlit secrets (st.secrets).

Write helper functions: fetch_daily_challenge(date) and append_result_to_drive(result_dict).

[X] Task 3.2: Mobile-First UI Layout

Configure st.set_page_config(layout="centered").

Build a clean authentication/name entry screen or direct identifier for Gagu.

Design card layouts for rendering questions cleanly on mobile screens.

[X] Task 3.3: Interactive Assessment Flow

Render the daily questions dynamically based on the fetched JSON.

Add a "Submit Answer" button with immediate feedback (correct/incorrect indicators).

[X] Task 3.4: Progress Writing & Feedback

Trigger the write-back function to append the attempt directly to the progress_log.csv file residing in Google Drive upon completion.

Show a summary screen with her daily score and streak.

Phase 4: Testing & Deployment
[ ] Task 4.1: Local Testing

Test file reads and writes locally using Streamlit secrets for credentials.

[ ] Task 4.2: Streamlit Community Cloud Deployment

Push the code to a private or public GitHub repository.

Configure st.secrets securely on the Streamlit dashboard.

[ ] Task 4.3: Home Screen Pinned Access

Open the deployment URL on her phone and guide her to "Add to Home Screen" for the app-like experience.