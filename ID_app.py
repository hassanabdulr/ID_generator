import streamlit as st
import requests
from ID_generator import (
    generate_spins_r_ids,
    generate_spinasd_ids,
    generate_predicts_ids,
    generate_predicts_hybrid_ids,
    generate_slaight_ids,
    generate_new_healthy_control_ids,
)

# Supabase Credentials (Replace with your actual details)
SUPABASE_URL = "https://efjosfuvszkardxaelrq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVmam9zZnV2c3prYXJkeGFlbHJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgxNTcxMzgsImV4cCI6MjA1MzczMzEzOH0.2d-F717q0eeWFN5LvQlT2sv7G4Z6l9lxKr7pApR_7Wo"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

# Helper Function to Get Example ID Format
def get_example_id(protocol):
    example_ids = {
        "SPINS": "SPN01_CMH_0008",
        "SPIN-ASD": "SPN10_CMH_0008",
        "PREDICTS": "SPN30_CMH_030089",
        "PREDICTS-HYBRID": "SPN32_CMH_030092",
        "Slaight": "SPN30_CMH_040001",
        "Healthy-Control": "SPN30_CMH_050001",
    }
    return example_ids.get(protocol, "")

# Check if ID exists in Supabase
def id_exists(subject_id):
    url = f"{SUPABASE_URL}/rest/v1/ids?subject_id=eq.{subject_id}"
    response = requests.get(url, headers=HEADERS)
    return response.status_code == 200 and len(response.json()) > 0

# Save new ID to Supabase
def save_id(subject_id, xnat_id, protocol):
    url = f"{SUPABASE_URL}/rest/v1/ids"
    data = {"subject_id": subject_id, "xnat_id": xnat_id, "protocol": protocol}
    response = requests.post(url, json=data, headers=HEADERS)
    if response.status_code == 201:
        st.success(f"✅ ID saved successfully: {subject_id}")
    else:
        st.error(f"Error saving ID: {response.text}")

# Streamlit UI
st.title("Participant ID Generator with Save Option")

# Step 1: Select Protocol
protocol = st.radio(
    "Select Protocol", ["SPINS", "SPIN-ASD", "PREDICTS", "PREDICTS-HYBRID", "Slaight", "Healthy-Control"]
)

# Step 2: Select Scanning Location (if applicable)
location = None
if protocol in ["SPINS", "PREDICTS", "Slaight", "Healthy-Control"]:
    location = st.radio("Select Scanning Location", ["CAMH", "ToNI"])

# Step 3: Enter Old Subject ID
example_id = get_example_id(protocol)
old_subject_id = st.text_input("Enter Old Subject ID", placeholder=f"e.g., {example_id}")

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
        if id_exists(old_subject_id):
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
        save_id(subject_id, xnat_id, protocol)
