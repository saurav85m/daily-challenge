gagu-daily-challenge/
│
├── .streamlit/
│   └── secrets.toml          # Stores Google service account credentials & secrets (ignored by Git)
│
├── content/                  # (Reference) Local sample or backup daily challenge files
│   └── challenge_2026-07-21.json
│
├── utils/
│   ├── __init__.py           # Makes utils a Python package
│   └── gdrive.py             # Handles Google Drive API auth, reading challenges, & writing results
│
├── app.py                    # Main Streamlit application entry point
├── requirements.txt          # Python dependencies (streamlit, google-api-python-client, etc.)
└── README.md                 # Setup and deployment instructions