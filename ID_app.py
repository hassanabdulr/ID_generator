import streamlit as st
import requests
import re
import pandas as pd
from ID_generator import (
    generate_spins_r_ids,
    generate_spinasd_ids,
    generate_predicts_ids,
    generate_predicts_hybrid_ids,
    generate_slaight_ids,
    generate_new_healthy_control_ids,
)

# Supabase Credentials
SUPABASE_URL = "https://efjosfuvszkardxaelrq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVmam9zZnV2c3prYXJkeGFlbHJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgxNTcxMzgsImV4cCI6MjA1MzczMzEzOH0.2d-F717q0eeWFN5LvQlT2sv7G4Z6l9lxKr7pApR_7Wo"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

# Fetch latest ID from Supabase
def get_latest_id(protocol):
    url = f"{SUPABASE_URL}/rest/v1/ids?protocol=eq.{protocol}&order=subject_id.desc&limit=1"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200 and response.json():
        return response.json()[0]["subject_id"]
    return None

# Extract numeric part of an ID
def extract_numeric_part(subject_id):
    match = re.search(r"(\d+)$", subject_id)
    return int(match.group(1)) if match else None

# Get the next ID for Healthy-Control
def get_next_healthy_control_id():
    latest_id = get_latest_id("Healthy-Control")
    
    if latest_id:
        last_number = extract_numeric_part(latest_id)
        if last_number:
            new_number = last_number + 1
            return latest_id.replace(str(last_number), str(new_number).zfill(len(str(last_number))))
    
    return "SPN30_CMH_050001"  # Default if no existing IDs

# Fetch entire database
def load_id_database():
    url = f"{SUPABASE_URL}/rest/v1/ids"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200 and response.json():
        return pd.DataFrame(response.json())
    return pd.DataFrame(columns=["subject_id", "xnat_id", "protocol"])

# Check if ID exists in Supabase
def id_exists(subject_id):
    url = f"{SUPABASE_URL}/rest/v1/ids?subject_id=eq.{subject_id}"
    response = requests.get(url, headers=HEADERS)
    return response.status_code == 200 and len(response.json()) > 0

# Streamlit UI with Tabs
st.title("TIGRLabel - ID Generator for SPIN-R")

tabs = st.tabs(["🔢 Generate IDs", "📋 View Database"])

### Tab 1: Generate IDs ###
with tabs[0]:
    st.header("🔢 Generate New IDs")

    # Step 1: Select Protocol
    protocol = st.radio(
        "Select Protocol", ["SPINS", "SPIN-ASD", "PREDICTS", "PREDICTS-HYBRID", "Slaight", "Healthy-Control"]
    )

    # Step 2: Select Scanning Location (if applicable)
    location = None
    if protocol in ["SPINS", "PREDICTS", "Slaight", "Healthy-Control"]:
        location = st.radio("Select Scanning Location", ["CAMH", "ToNI"])

    # Step 3: Auto-Suggest Old Subject ID
    if protocol == "Healthy-Control":
        old_subject_id = st.text_input("Enter Old Subject ID", value=get_next_healthy_control_id(), disabled=True)
    else:
        latest_id = get_latest_id(protocol)
        old_subject_id = st.text_input("Enter Old Subject ID", placeholder=f"Latest: {latest_id}" if latest_id else "Enter subject ID...")

    # Step 4: Generate ID
    subject_id = None
    xnat_id = None

    if st.button("Generate ID"):
        try:
            # Validation: Ensure subject ID is entered
            if not old_subject_id:
                raise ValueError("Old Subject ID is required!")
            # Validation: Ensure location is selected where applicable
            if protocol in ["SPINS", "PREDICTS", "Slaight", "Healthy-Control"] and not location:
                raise ValueError("Scanning location must be selected!")
            
            # Check for duplicate IDs
            if protocol != "Healthy-Control" and get_latest_id(old_subject_id):
                raise ValueError(f"ID **{old_subject_id}** already exists in the database.")

            # Generate ID based on selected protocol
            if protocol == "SPINS":
                subject_id, xnat_id = generate_spins_r_ids(old_subject_id, location)
            elif protocol == "SPIN-ASD":
                subject_id, xnat_id = generate_spinasd_ids(old_subject_id)
            elif protocol == "PREDICTS":
                subject_id, xnat_id = generate_predicts_ids(old_subject_id, location)
            elif protocol == "PREDICTS-HYBRID":
                subject_id, xnat_id = generate_predicts_hybrid_ids(old_subject_id)
            elif protocol == "Slaight":
                subject_id, xnat_id = generate_slaight_ids(old_subject_id, location)
            elif protocol == "Healthy-Control":
                subject_id, xnat_id = generate_new_healthy_control_ids(old_subject_id, location)
            else:
                raise ValueError("Invalid protocol selection.")
            
            # Display Results
            st.success(f"**Subject ID:** {subject_id}")
            st.success(f"**XNAT ID:** {xnat_id}")
        except ValueError as e:
            st.error(f"Error: {e}")

    # Step 5: Save ID to Database
    if subject_id and xnat_id:
        if st.button("Save ID"):
            url = f"{SUPABASE_URL}/rest/v1/ids"
            data = {"subject_id": subject_id, "xnat_id": xnat_id, "protocol": protocol}
            response = requests.post(url, json=data, headers=HEADERS)

            if response.status_code == 201:
                st.success(f"✅ ID saved successfully: {subject_id}")
            else:
                st.error(f"Error saving ID: {response.text}")

### Tab 2: View Database ###
with tabs[1]:
    st.header("📋 View Database")
    
    # Load data
    df = load_id_database()
    
    # Search for ID
    search_query = st.text_input("🔍 Search for Subject ID")
    if search_query:
        df = df[df["subject_id"].str.contains(search_query, na=False)]

    # Display database
    st.dataframe(df)

