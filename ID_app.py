import streamlit as st
import pandas as pd
import requests

# Supabase Credentials (Replace with your actual details)
SUPABASE_URL = "https://efjosfuvszkardxaelrq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVmam9zZnV2c3prYXJkeGFlbHJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgxNTcxMzgsImV4cCI6MjA1MzczMzEzOH0.2d-F717q0eeWFN5LvQlT2sv7G4Z6l9lxKr7pApR_7Wo"

# Headers for Supabase requests
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

# Function to Load ID Database from Supabase
def load_id_database():
    url = f"{SUPABASE_URL}/rest/v1/ids"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error(f"Error loading data: {response.text}")
        return pd.DataFrame(columns=["subject_id", "xnat_id", "protocol"])

# Function to Check if an ID Exists
def id_exists(subject_id):
    url = f"{SUPABASE_URL}/rest/v1/ids?subject_id=eq.{subject_id}"
    response = requests.get(url, headers=HEADERS)
    return response.status_code == 200 and len(response.json()) > 0

# Function to Save New ID to Supabase
def save_id(subject_id, xnat_id, protocol):
    url = f"{SUPABASE_URL}/rest/v1/ids"
    data = {"subject_id": subject_id, "xnat_id": xnat_id, "protocol": protocol}
    response = requests.post(url, json=data, headers=HEADERS)
    if response.status_code == 201:
        st.success(f"✅ **{subject_id}** added successfully!")
    else:
        st.error(f"Error saving ID: {response.text}")

# Load ID Database
df = load_id_database()

# Streamlit UI
st.title("Participant ID Manager (Supabase - REST API)")

# Search Section
search_id = st.text_input("Search for an ID", placeholder="Enter Subject ID...")
if st.button("Search"):
    if id_exists(search_id):
        url = f"{SUPABASE_URL}/rest/v1/ids?subject_id=eq.{search_id}"
        response = requests.get(url, headers=HEADERS)
        result = response.json()[0]  # Get the first matching record
        st.success(f"✅ **Subject ID:** {result['subject_id']}")
        st.info(f"📌 **XNAT ID:** {result['xnat_id']}")
        st.warning(f"🧩 **Protocol:** {result['protocol']}")
    else:
        st.error("❌ ID not found.")

# Add New ID Section
st.subheader("Generate & Save a New ID")

subject_id = st.text_input("Enter New Subject ID")
xnat_id = st.text_input("Enter XNAT ID")
protocol = st.selectbox("Select Protocol", ["SPINS", "SPIN-ASD", "PREDICTS", "PREDICTS-HYBRID", "Slaight", "Healthy-Control"])

if st.button("Save New ID"):
    if not subject_id or not xnat_id or not protocol:
        st.error("⚠️ All fields are required!")
    elif id_exists(subject_id):
        st.warning(f"⚠️ ID **{subject_id}** already exists.")
    else:
        save_id(subject_id, xnat_id, protocol)

# View Updated Database
st.subheader("Complete ID Database")
st.dataframe(load_id_database())  # Reload to reflect new entries
