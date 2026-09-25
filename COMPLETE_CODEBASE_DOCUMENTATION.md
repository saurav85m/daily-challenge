# 🎯 Gagu's Daily Challenge - Complete Codebase Documentation

**Last Updated:** September 2026  
**Purpose:** Comprehensive technical documentation for GitHub-based AI assistance and maintenance

---

## Standard ICSE Section A Category List
1. Data Types & Variables
2. Operators & Expressions
3. Library Classes (Math / Character)
4. String Handling
5. Single & Double Dimensional Arrays
6. Control Structures (Loops & Conditionals)
7. User-Defined Methods & Constructors
8. OOP Concepts & Access Modifiers

## Sub_category Mapping for Section A
#### For mcq (Questions 1 to 20):
Theory & Concepts
Operators & Precedence
Library Methods (Math/Character)
Data Types & Variables
OOP Principles & Modifiers

#### For error_finding:
Syntax Error
Logical Error
OOP/Library Error

#### For output_prediction:
String Handling
Array Tracing
Loop & Iteration Tracing
Mixed Expression Tracing

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Data Architecture](#data-architecture)
5. [Core Modules](#core-modules)
6. [Application Flow](#application-flow)
7. [Key Features](#key-features)
8. [Configuration & Secrets](#configuration--secrets)
9. [API Integration](#api-integration)
10. [Database Schema](#database-schema)
11. [Deployment Information](#deployment-information)
12. [Dependencies & Requirements](#dependencies--requirements)
13. [Known Issues & Limitations](#known-issues--limitations)
14. [Enhancement Ideas](#enhancement-ideas)

---

## 1. Project Overview

### 1.1 Purpose
**Gagu's Daily Challenge** is a mobile-first Streamlit application designed to provide daily coding assessment questions for students. The platform presents multiple-choice questions (MCQ), output prediction problems, and error-finding challenges on a daily basis.

### 1.2 Target Users
- **Primary User:** Gagu (individual student) + Guest users
- **Timeframe:** 15-minute daily coding skill-sharpening sessions
- **Platform:** Mobile-first web application with responsive UI

### 1.3 Core Value Proposition
- Daily coding challenges delivered through a clean, mobile-friendly interface
- Automatic progress tracking and performance analytics
- GitHub-based data persistence (no traditional database required)
- Submission history with timestamp and detailed performance metrics

---

## 2. Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Frontend Framework** | Streamlit | Latest | Web UI, interactive components |
| **Backend Language** | Python 3.x | - | Core application logic |
| **Data Storage** | GitHub Repository | - | Challenge JSON files & CSV logs |
| **Authentication** | GitHub Personal Access Token (PAT) | - | API access for read/write |
| **Data Processing** | Pandas | Latest | CSV manipulation, analytics |
| **API Client** | PyGithub | Latest | GitHub repository operations |
| **HTTP Requests** | requests | Latest | Raw GitHub content fetching |
| **Timezone Handling** | zoneinfo | Built-in | India Standard Time (IST) timestamps |

---

## 3. Project Structure

```
Daily_Challenge/
├── .devcontainer/
│   └── devcontainer.json         # Dev container configuration
├── .streamlit/
│   ├── secrets.toml              # GitHub credentials (DO NOT COMMIT)
│   └── secrets_copy.toml         # Backup of secrets
├── .git/                         # Git repository metadata
├── .gitignore                    # Files to exclude from version control
│
├── app.py                        # Main Streamlit application entry point
├── requirements.txt              # Python package dependencies
│
├── content/                      # Daily challenge JSON files
│   ├── challenge_2026-07-22.json
│   ├── challenge_2026-07-24.json
│   ├── challenge_2026-07-25.json
│   ├── challenge_2026-09-22.json
│   └── ... (more challenge files)
│
├── pages/
│   └── 1_Dashboard.py            # Multi-page dashboard for progress tracking
│
├── results/
│   └── progress_log.csv          # Submission records (created dynamically)
│
├── utils/
│   ├── common.py                 # Utility functions (timezone handling)
│   ├── github_db.py              # GitHub API integration & data layer
│   ├── gdrive_old.py             # Legacy Google Drive code (deprecated)
│   └── __pycache__/              # Python bytecode cache
│
├── Docs/
│   ├── Folder Structure.MD       # Repository organization guide
│   ├── Task.MD                   # Development task checklist
│   └── challenge-app-*.json      # Firebase/config backup files
│
└── venv/                         # Python virtual environment (local development)
```

---

## 4. Data Architecture

### 4.1 Challenge JSON Schema

Each daily challenge is stored as a JSON file in the `/content` folder with the naming convention: `challenge_YYYY-MM-DD.json`

**Example Structure:**
```json
{
  "date": "2026-07-22",
  "topic": "Library Classes Arrays and String Handling",
  "questions": [
    {
      "id": 1,
      "type": "mcq",
      "question": "What is the automatic conversion of a primitive data type into an object of its equivalent wrapper class called?",
      "options": ["Unboxing", "Typecasting", "Autoboxing", "Wrapping"],
      "answer": "Autoboxing",
      "explanation": "Autoboxing automatically converts primitive types (like int) into their wrapper objects (like Integer)."
    },
    {
      "id": 2,
      "type": "mcq",
      "question": "In a double dimensional array m[3][4], what does the number 3 represent?",
      "options": ["Number of columns", "Number of elements", "Number of rows", "Number of bytes"],
      "answer": "Number of rows",
      "explanation": "In a double dimensional array, the first subscript always represents the number of rows."
    }
  ]
}
```

**Question Types:**
- **`mcq`** - Multiple Choice Questions
- **`output_prediction`** - Predict the output of code (requires `code_snippet` field)
- **`error_finding`** - Identify and locate errors in code (requires `code_snippet` field)

**Field Descriptions:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `date` | String (YYYY-MM-DD) | Yes | Challenge date |
| `topic` | String | Yes | Topic/theme of the challenge |
| `questions` | Array | Yes | Array of question objects |
| `id` | Integer | Yes | Unique question identifier (1-based) |
| `type` | String | Yes | Question type (mcq, output_prediction, error_finding) |
| `question` | String | Yes | Question text |
| `code_snippet` | String | No | Python code for output_prediction/error_finding types |
| `options` | Array | Yes | Answer options |
| `answer` | String | Yes | Correct answer (must match one option exactly) |
| `explanation` | String | Yes | Explanation for the correct answer |

---

## 5. Core Modules

### 5.1 `app.py` - Main Application

**Purpose:** Streamlit entry point orchestrating the entire user experience

**Key Sections:**

#### Page Configuration
```python
st.set_page_config(
    page_title="Gagu's Daily Challenge",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)
```
- **`layout="centered"`** - Mobile-friendly centered layout
- **`initial_sidebar_state="collapsed"`** - Minimizes sidebar on mobile

#### Student Identification & Date Selection
- User selects from dropdown: ["Gagu", "Guest"]
- Date picker (defaults to today)
- Validates if student has already submitted for the selected date

#### Challenge Fetching
- Calls `fetch_daily_challenge(date_str)` from `github_db.py`
- Displays warning if challenge JSON not found for the date

#### Question Rendering
- Dynamically renders all questions from the JSON
- Creates radio button groups for MCQ options
- Displays code snippets for output_prediction/error_finding types
- Groups all questions within a single Streamlit form

#### Answer Collection & Submission
```python
user_answers = {
    question_id: {
        "question_type": str,
        "selected": str,
        "correct": str,
        "explanation": str
    }
}
```

#### Scoring & Result Persistence
1. Validates all questions are answered
2. Calculates duration (end_time - start_time)
3. Creates result rows with structure:
   ```python
   {
       "timestamp": str,
       "student_name": str,
       "date": str,
       "topic": str,
       "duration_seconds": int,
       "duration_display": str,
       "question_id": int,
       "question_type": str,
       "selected_option": str,
       "correct_answer": str,
       "is_correct": bool
   }
   ```
4. Calls `append_results_to_github()` for batch persistence

#### Display Results
- Shows celebratory animation (balloons)
- Displays score: `{correct_answers} / {total_questions}`
- Shows time taken
- Reviews each answer with explanation
- Color-coded feedback (✅ Correct/❌ Incorrect)

**Session State Variables:**
- `st.session_state.challenge_start_time` - Timer start for duration calculation

---

### 5.2 `utils/github_db.py` - Data Layer

**Purpose:** Handles all GitHub API operations and data persistence

**Core Functions:**

#### `get_github_repo()`
```python
def get_github_repo():
  """Authenticate and return the GitHub repository instance."""
  cfg = st.secrets["github"]
  g = Github(cfg["token"])
  repo = g.get_repo(f"{cfg['repo_owner']}/{cfg['repo_name']}")
  return repo
```
- Reads GitHub token from Streamlit secrets
- Returns authenticated PyGithub repository object

#### `fetch_daily_challenge(date_str)`
```python
def fetch_daily_challenge(date_str):
    """Fetches the challenge JSON for a specific date from GitHub."""
    # Constructs raw.githubusercontent.com URL
    # Returns parsed JSON or None if not found
```
- Parameters: `date_str` (format: "YYYY-MM-DD")
- Returns: Dict with challenge data or None
- Uses raw GitHub content URL for fast, lightweight fetching
- Includes authorization header with GitHub token

#### `append_result_to_github(result_dict)`
```python
def append_result_to_github(result_dict):
  """Append a submission result to progress_log.csv"""
```
- Appends single result row to `results/progress_log.csv`
- Creates CSV if it doesn't exist
- Updates with one GitHub commit

#### `append_results_to_github(results)`
```python
def append_results_to_github(results):
    """Append multiple submission results in a single commit."""
```
- **Parameters:** List of result dictionaries
- **Benefit:** Batches all question results into ONE GitHub commit (more efficient)
- Used by `app.py` for final submission

#### `has_student_submitted(student_name, date_str)`
```python
def has_student_submitted(student_name, date_str):
    """Returns True if student has submitted for this date."""
```
- Prevents duplicate submissions
- Used in `app.py` to check if user already completed challenge

#### `get_submission_details(student_name, date_str)`
```python
def get_submission_details(student_name, date_str):
    """Returns submission details or None if not found."""
    # Returns: {score, total, accuracy, submitted_at}
```
- Retrieves detailed submission metrics
- Used to display prior submission info

#### `get_progress_log()`
```python
def get_progress_log():
    """Reads progress_log.csv from GitHub and returns DataFrame."""
```
- Reads entire submission history
- Returns Pandas DataFrame for analytics
- Used by Dashboard page

**Error Handling:**
- All functions include try/except blocks
- Returns None on GitHub API errors
- Gracefully handles missing files (CSV creation)

---

### 5.3 `utils/common.py` - Utilities

**Purpose:** Timezone utilities for consistent timestamps

```python
def get_india_timestamp():
    """Returns current timestamp in Indian Standard Time."""
    return datetime.now(ZoneInfo("Asia/Kolkata"))
```
- Ensures all timestamps use IST (Asia/Kolkata timezone)
- Used for challenge start time and submission timestamps
- Consistent across different geographic locations

---

### 5.4 `pages/1_Dashboard.py` - Analytics Dashboard

**Purpose:** Multi-page dashboard displaying student progress and performance

**Streamlit Multi-Page Setup:**
- Files in `/pages/` directory automatically become separate pages in Streamlit
- Accessible via page navigation (shown as "Dashboard" button in sidebar)

**Dashboard Components:**

#### Summary Metrics (Top Cards)
```
┌─────────────────────────────────────────────────────┐
│ Challenges │ Correct/Total │ Accuracy │ Avg Time   │
│     X      │   Y / Z       │  P%      │  Q min     │
└─────────────────────────────────────────────────────┘
```

**Calculations:**
- **Total Challenges:** Unique dates in progress_log
- **Total Correct:** Sum of `is_correct` column
- **Overall Accuracy:** (total_correct / total_questions) × 100
- **Average Time:** Mean of `duration_seconds` / 60

#### Challenge History Table
- Sorted by date (descending - most recent first)
- Columns: Date, Score, Total, Accuracy (%), Time Taken, Submitted At
- Shows progression over time

#### Performance by Question Type (Currently Commented Out)
- Prepared code for analyzing accuracy by question type (mcq, output_prediction, error_finding)
- Can be enabled for detailed performance breakdown

**Data Aggregation:**
```python
challenge_summary = (
    df.groupby("date")
      .agg(
          score=("is_correct", "sum"),
          total=("is_correct", "count"),
          ...
      )
)
```

---

## 6. Application Flow

### 6.1 User Journey - First Time Challenge Attempt

```
1. User Opens App
   ↓
2. Streamlit renders page config (centered, mobile-friendly)
   ↓
3. Student Name Selection & Date Picker
   ├─ Default: "Gagu"
   └─ Default: Today's date
   ↓
4. App Fetches Challenge from GitHub
   ├─ Constructs: content/challenge_YYYY-MM-DD.json
   ├─ Uses raw.githubusercontent.com URL
   └─ Returns JSON or None
   ↓
5. Check: Is Challenge Available?
   ├─ NO → Display warning, stop execution
   └─ YES → Continue
   ↓
6. Check: Already Submitted Today?
   ├─ YES → Show submission details, stop execution
   └─ NO → Continue to questions
   ↓
7. Render Challenge Questions
   ├─ Timer Starts (stored in session_state)
   ├─ Loop through questions
   ├─ Display question text
   ├─ Show code snippet (if applicable)
   ├─ Render radio button options
   └─ Group in Form element
   ↓
8. User Selects Answers
   ├─ One answer per question required
   └─ Session state tracks selections
   ↓
9. User Clicks "Submit All Answers"
   ├─ Validate: All questions answered?
   │  ├─ NO → Show error, stay on form
   │  └─ YES → Continue
   │
   ├─ Calculate Duration
   │  ├─ End Time = current IST timestamp
   │  ├─ Duration = End - Start
   │  └─ Convert to display format
   │
   ├─ Grade Each Answer
   │  ├─ Compare selected vs correct
   │  └─ Build result rows
   │
   ├─ Save to GitHub
   │  ├─ Batch all results
   │  ├─ One commit with all rows
   │  └─ Update results/progress_log.csv
   │
   └─ Display Results Screen
      ├─ Celebration animation (balloons)
      ├─ Score: X / Y
      ├─ Time: M min S sec
      ├─ Review section with explanations
      └─ Color-coded answers (✅/❌)
```

### 6.2 Data Persistence Flow

```
Result Row
  ↓
append_results_to_github()
  ├─ Read: GitHub repo via PyGithub
  ├─ Read: Existing progress_log.csv
  ├─ Parse: Into Pandas DataFrame
  ├─ Append: New rows
  ├─ Convert: Back to CSV string
  ├─ Commit: Single update to GitHub
  └─ Return: Success boolean
  ↓
GitHub Repository
  ├─ File: results/progress_log.csv (updated)
  └─ Commit message: "Update progress log for YYYY-MM-DD"
```

### 6.3 Dashboard Access Flow

```
User Clicks "View Progress Dashboard"
  ↓
Load Dashboard Page (1_Dashboard.py)
  ↓
get_progress_log()
  ├─ Fetch: GitHub authenticated connection
  ├─ Read: results/progress_log.csv from repo
  ├─ Decode: Base64 → UTF-8 string
  ├─ Parse: String → Pandas DataFrame
  └─ Return: DataFrame with all submissions
  ↓
Render Analytics
  ├─ Group by date
  ├─ Calculate aggregations
  ├─ Display metrics & tables
  └─ Show trends
```

---

## 7. Key Features

### 7.1 Mobile-First Design
- Centered layout (`layout="centered"`)
- Full-width buttons with custom CSS
- Responsive form elements
- Collapsed sidebar to maximize screen space

### 7.2 Multiple Question Types
- **MCQ (Multiple Choice):** Traditional radio button selection
- **Output Prediction:** Users predict code output
- **Error Finding:** Users identify bugs in code

### 7.3 Automatic Progress Tracking
- Timestamps for every submission (IST)
- Duration calculation
- Accuracy percentage
- Per-question detail tracking

### 7.4 Duplicate Submission Prevention
- Checks `has_student_submitted()` before allowing attempt
- Shows existing submission details if already completed
- Encourages trying different dates

### 7.5 Batch Result Saving
- All question results saved in single GitHub commit
- Reduces API calls
- Atomic operation (all-or-nothing)

### 7.6 Progress Dashboard
- Summary metrics (challenges, correct answers, accuracy, avg time)
- Historical table with sorting
- Trend analysis capability (prepared but commented out)

---

## 8. Configuration & Secrets

### 8.1 Streamlit Secrets (`.streamlit/secrets.toml`)

**IMPORTANT:** This file contains sensitive credentials and should NEVER be committed to Git.

```toml
[github]
token = "github_pat_11AF7HCLA0..."  # GitHub Personal Access Token
repo_owner = "saurav85m"             # GitHub username
repo_name = "daily-challenge"        # Repository name
branch = "main"                      # Branch to read/write from
```

**GitHub PAT Permissions Required:**
- `repo` - Full control of private repositories
- `read:user` - Read user profile data

### 8.2 Access Control

**Read Permissions Needed:**
- `content/` directory (fetch challenge JSON files)
- `results/progress_log.csv` (read existing submissions)

**Write Permissions Needed:**
- `results/progress_log.csv` (append new submissions)

### 8.3 Environment Variables

**For Local Development:**
```bash
# Set Streamlit secrets before running
export STREAMLIT_GITHUB_TOKEN="your_pat_token"
```

**For Deployment (Streamlit Community Cloud):**
- Configure secrets in Streamlit dashboard UI
- Secrets are encrypted at rest
- Never exposed in logs or code

---

## 9. API Integration

### 9.1 GitHub REST API (via PyGithub)

**Repository Operations:**
```python
g = Github(token)
repo = g.get_repo("owner/name")

# Read file
content = repo.get_contents("path/to/file", ref="branch")
decoded = base64.b64decode(content.content).decode("utf-8")

# Update file
repo.update_file(
    path="path/to/file",
    message="Commit message",
    content=new_content,
    sha=content.sha,
    branch="branch"
)

# Create file
repo.create_file(
    path="path/to/file",
    message="Initial commit",
    content=initial_content,
    branch="branch"
)
```

### 9.2 Raw GitHub Content API

**For Fetching Challenge JSON:**
```
GET https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}
Authorization: Bearer {token}
```

**Advantages:**
- No API rate limiting issues (for authenticated requests)
- Lightweight and fast
- Direct JSON response

---

## 10. Database Schema

### 10.1 Progress Log CSV (`results/progress_log.csv`)

**Columns:**

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `timestamp` | String | "2026-07-22 14:30:45" | IST timestamp of submission |
| `student_name` | String | "Gagu" | Student identifier |
| `date` | String | "2026-07-22" | Challenge date (YYYY-MM-DD) |
| `topic` | String | "Arrays and Strings" | Challenge topic |
| `duration_seconds` | Integer | 420 | Total time in seconds |
| `duration_display` | String | "7 min 0 sec" | Human-readable duration |
| `question_id` | Integer | 1 | Question number (1-5 typically) |
| `question_type` | String | "mcq" | Type of question |
| `selected_option` | String | "Autoboxing" | User's selected answer |
| `correct_answer` | String | "Autoboxing" | Correct answer from JSON |
| `is_correct` | Boolean | 1 | 1=correct, 0=incorrect |

**Example Row:**
```csv
timestamp,student_name,date,topic,duration_seconds,duration_display,question_id,question_type,selected_option,correct_answer,is_correct
2026-07-22 14:30:45,Gagu,2026-07-22,Library Classes Arrays and String Handling,420,7 min 0 sec,1,mcq,Autoboxing,Autoboxing,1
2026-07-22 14:30:45,Gagu,2026-07-22,Library Classes Arrays and String Handling,420,7 min 0 sec,2,mcq,Number of rows,Number of rows,1
2026-07-22 14:30:45,Gagu,2026-07-22,Library Classes Arrays and String Handling,420,7 min 0 sec,3,mcq,int,int,1
```

**Index Strategy:**
- Primary: timestamp + student_name + date (for unique constraint)
- Secondary: date (for dashboard grouping)
- Secondary: student_name (for filtering by student)

---

## 11. Deployment Information

### 11.1 Local Development

**Prerequisites:**
```bash
# Python 3.8+
# pip or conda

# Install dependencies
pip install -r requirements.txt

# Set up secrets
# Create .streamlit/secrets.toml with GitHub credentials
```

**Run Locally:**
```bash
streamlit run app.py
```
- Opens browser at http://localhost:8501
- Auto-reloads on file changes

### 11.2 Streamlit Community Cloud Deployment

**Steps:**
1. Push code to public GitHub repository
2. Visit https://share.streamlit.io
3. Connect GitHub account and select repository
4. Configure secrets in Streamlit dashboard
5. Deploy - app is accessible via permanent URL

**Deployment Benefits:**
- Free hosting (Community tier)
- SSL/HTTPS by default
- Mobile-responsive automatically
- "Add to Home Screen" support for PWA-like experience

### 11.3 DevContainer Support

**`.devcontainer/devcontainer.json`** is configured for VS Code remote development:
- Standardized development environment
- All dependencies pre-installed
- Easy onboarding for team members

---

## 12. Dependencies & Requirements

### 12.1 Python Packages

```
streamlit              # Web framework for data apps
google-api-python-client  # Google Drive API (legacy, now using GitHub)
google-auth           # Google authentication (legacy)
pandas                # Data manipulation and analysis
PyGithub              # GitHub API Python wrapper
requests              # HTTP library for raw GitHub content
```

### 12.2 External Services

| Service | Purpose | Credentials | Status |
|---------|---------|-------------|--------|
| GitHub | Challenge storage & data persistence | PAT token in secrets.toml | **Active** |
| Google Drive API | Legacy data storage | Service account (deprecated) | **Inactive** |
| Streamlit | Application hosting | Free Community tier | **Active** |

---

## 13. Known Issues & Limitations

### 13.1 Current Issues

| Issue | Description | Workaround | Priority |
|-------|-------------|-----------|----------|
| Page Link Broken | `st.page_link()` commented out in app.py | Manual navigation to Dashboard URL | Medium |
| Dashboard Page Title | Multi-page setup shows "1_Dashboard" in nav | Rename to `_Dashboard.py` | Low |
| Error Handling | Generic exception catching (could be more specific) | Review and improve error messages | Low |

### 13.2 Limitations

1. **Rate Limiting:** GitHub API has rate limits (60 req/hr unauthenticated, 5000/hr authenticated)
2. **Scalability:** CSV-based storage may become slow with 1000+ submissions
3. **Concurrent Users:** Streamlit isn't ideal for high-concurrency scenarios
4. **Offline Access:** No offline mode (requires internet connection)
5. **Search:** No full-text search on past challenges

### 13.3 GitHub Limitations

- PAT token hardcoded in secrets (not ideal for multi-team scenarios)
- No role-based access control (repo access is all-or-nothing)
- Raw GitHub content URL may be inconsistent (cached by CDN)

---

## 14. Enhancement Ideas

### 14.1 Short-Term Improvements

- [ ] **Replace Page Link:** Fix the page navigation in app.py
- [ ] **Error Messages:** Add specific error messages for GitHub API failures
- [ ] **Performance Metrics:** Add speed/time-tracking per question type
- [ ] **Streak Counter:** Display consecutive day streak
- [ ] **Achievement Badges:** Reward perfect scores or consistency

### 14.2 Medium-Term Enhancements

- [ ] **Difficulty Levels:** Add Easy/Medium/Hard classification
- [ ] **Explanation Videos:** Link to YouTube explanation videos
- [ ] **Hint System:** Show hints before reveal of answer
- [ ] **Leaderboard:** Compare performance across multiple students (if multi-user)
- [ ] **Mobile App:** Convert to Flutter/React Native for offline capability
- [ ] **Database Migration:** Move from CSV to SQLite/Postgres for better scalability

### 14.3 Long-Term Architecture Changes

- [ ] **Microservices:** Separate API server from Streamlit UI
- [ ] **GraphQL API:** Replace REST with GraphQL for flexible queries
- [ ] **Real-time Sync:** WebSocket for real-time progress updates
- [ ] **Machine Learning:** Personalized challenge difficulty adjustment
- [ ] **Analytics:** Advanced analytics dashboard with Plotly/Tableau
- [ ] **Admin Dashboard:** Teacher interface to create/manage challenges

### 14.4 User Experience Improvements

- [ ] **Customizable Themes:** Light/Dark mode
- [ ] **Sound Effects:** Celebration sounds on correct answers
- [ ] **Progress Export:** Download challenge history as PDF
- [ ] **Email Reminders:** Daily reminder emails to take challenge
- [ ] **Social Sharing:** Share scores on social media
- [ ] **Accessibility:** WCAG 2.1 AA compliance (alt text, keyboard nav)

---

## 15. File Cross-Reference Guide

### For ChatGPT Assistance, Reference These Files:

| Task | Primary Files | Secondary Files |
|------|--------------|-----------------|
| **Fix UI Issues** | `app.py` (lines 1-50) | `utils/common.py` |
| **Add New Challenge** | `content/challenge_*.json` | None |
| **Debug GitHub API** | `utils/github_db.py` | `.streamlit/secrets.toml` |
| **Modify Dashboard** | `pages/1_Dashboard.py` | `utils/github_db.py` |
| **Understand Data Flow** | `app.py` → `utils/github_db.py` | `results/progress_log.csv` |
| **Optimize Performance** | `utils/github_db.py` (caching) | `pages/1_Dashboard.py` |
| **Add New Question Type** | `app.py` (question rendering) | `content/challenge_*.json` |
| **Deployment Help** | `.devcontainer/devcontainer.json` | `requirements.txt` |

---

## 16. Quick Command Reference

### Git Operations
```bash
# Clone repository
git clone https://github.com/saurav85m/daily-challenge.git

# View recent challenges
ls -la content/challenge_*.json

# Check submission history
cat results/progress_log.csv | head -20
```

### Streamlit Commands
```bash
# Run locally
streamlit run app.py

# Run specific page
streamlit run pages/1_Dashboard.py

# View logs
streamlit logs

# Clear cache
rm -rf ~/.streamlit/cache
```

### Python Testing
```bash
# Test GitHub connection
python -c "from utils.github_db import get_github_repo; print(get_github_repo())"

# Test timestamp
python -c "from utils.common import get_india_timestamp; print(get_india_timestamp())"

# Parse challenge
python -c "import json; print(json.load(open('content/challenge_2026-07-22.json')))"
```

---

## 17. Support & Troubleshooting

### Common Issues

**Q: "No challenge found for YYYY-MM-DD"**
- A: Check that `content/challenge_YYYY-MM-DD.json` exists in the GitHub repo
- Verify filename format (must be YYYY-MM-DD)

**Q: "GitHub token expired"**
- A: Generate new PAT from GitHub settings
- Update `.streamlit/secrets.toml`

**Q: "Already submitted error"**
- A: User already completed this challenge today
- Select a different date or come back tomorrow

**Q: "Streamlit app won't start"**
- A: Run `pip install -r requirements.txt`
- Check Python version (3.8+)
- Verify secrets.toml exists in `.streamlit/`

---

## 18. Document Metadata

- **Created:** September 2026
- **Last Updated:** September 2026
- **Author:** Generated from codebase analysis
- **Version:** 1.0
- **Compatibility:** Python 3.8+, Streamlit 1.x+, PyGithub 1.55+

---

**END OF DOCUMENTATION**

This document can now be uploaded to ChatGPT for comprehensive codebase understanding and assistance with requirements, features, and maintenance tasks.
