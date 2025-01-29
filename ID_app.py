import streamlit as st
import pandas as pd
import supabase as supabase
from supabase import create_client, Client

# Supabase Credentials (Replace with your actual details)
SUPABASE_URL = "https://efjosfuvszkardxaelrq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVmam9zZnV2c3prYXJkeGFlbHJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgxNTcxMzgsImV4cCI6MjA1MzczMzEzOH0.2d-F717q0eeWFN5LvQlT2sv7G4Z6l9lxKr7pApR_7Wo"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to Load ID Database from Supabase
def load_id_database():
    response = supabase.table("ids").select("*").execute()
    return pd.DataFrame(response.data) if response.data else pd.DataFrame(columns=["subject_id", "xnat_id", "protocol"])

# Function to Check if an ID Exists
def id_exists(subject_id, df):
    return subject_id in df["subject_id"].values

# Function to Save New ID to Supabase
def save_id(subject_id, xnat_id, protocol):
    data = {"subject_id": subject_id, "xnat_id": xnat_id, "protocol": protocol}
    supabase.table("ids").insert(data).execute()
    st.success(f"✅ **{subject_id}** added successfully!")

# Load ID Database
df = load_id_database()

# Streamlit UI
st.title("Participant ID Manager (Supabase)")

# Search Section
search_id = st.text_input("Search for an ID", placeholder="Enter Subject ID...")
if st.button("Search"):
    if id_exists(search_id, df):
        result = df[df["subject_id"] == search_id]
        st.success(f"✅ **Subject ID:** {result['subject_id'].values[0]}")
        st.info(f"📌 **XNAT ID:** {result['xnat_id'].values[0]}")
        st.warning(f"🧩 **Protocol:** {result['protocol'].values[0]}")
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
    elif id_exists(subject_id, df):
        st.warning(f"⚠️ ID **{subject_id}** already exists.")
    else:
        save_id(subject_id, xnat_id, protocol)

# View Updated Database
st.subheader("Complete ID Database")
st.dataframe(load_id_database())  # Reload to reflect new entries
