import json
import io
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

# Define the scopes required by the Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    """Authenticate and return the Google Drive API service instance."""
    # Load credentials securely from Streamlit secrets
    creds_dict = st.secrets["gcp_service_account"]
    creds = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)
    return service

def fetch_daily_challenge(date_str):
    """Fetch and parse the JSON challenge file for a specific date."""
    service = get_drive_service()
    filename = f"challenge_{date_str}.json"
    
    # Search for the specific JSON file globally in the shared Drive
    query = f"name='{filename}' and trashed=false and mimeType='application/json'"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    
    if not items:
        return None  # No challenge found for this date
        
    file_id = items[0]['id']
    
    # Download the file contents into memory
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        
    fh.seek(0)
    return json.loads(fh.read().decode('utf-8'))

def append_result_to_drive(result_dict):
    """Append a submission result to progress_log.csv."""
    service = get_drive_service()
    filename = "progress_log.csv"
    
    # Search for the existing progress log CSV
    query = f"name='{filename}' and trashed=false and mimeType='text/csv'"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    
    # Convert the incoming dictionary into a Pandas DataFrame row
    df_new_row = pd.DataFrame([result_dict])
    
    if not items:
        # If progress_log.csv doesn't exist yet, create it with headers
        csv_content = df_new_row.to_csv(index=False)
        file_metadata = {'name': filename, 'mimeType': 'text/csv'}
        media = MediaIoBaseUpload(io.BytesIO(csv_content.encode('utf-8')), mimetype='text/csv', resumable=True)
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    else:
        # If it exists, download it, append the new row, and upload the updated version
        file_id = items[0]['id']
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            
        fh.seek(0)
        df_existing = pd.read_csv(fh)
        
        # Append new data
        df_updated = pd.concat([df_existing, df_new_row], ignore_index=True)
        csv_content = df_updated.to_csv(index=False)
        
        # Overwrite the file on Drive
        media = MediaIoBaseUpload(io.BytesIO(csv_content.encode('utf-8')), mimetype='text/csv', resumable=True)
        service.files().update(fileId=file_id, media_body=media).execute()