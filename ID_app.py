# ID_app


import streamlit as st
from ID_generator import (
    generate_spins_r_ids,
    generate_spinasd_ids,
    generate_predicts_ids,
    generate_predicts_hybrid_ids,
    generate_slaight_ids,
    generate_new_healthy_control_ids,
)
# Title
st.title("Participant ID Generator")

# Step 1: Select Protocol
protocol = st.radio("Select Protocol", ["SPINS", "SPIN-ASD", "PREDICTS", "PREDICTS-HYBRID", "Slaight", "Healthy-Control"])

# Step 2: Select Scanning Location (if applicable)
if protocol in ["SPINS", "PREDICTS", "Slaight", "Healthy-Control"]:
    location = st.radio("Select Scanning Location", ["CAMH", "ToNI"])
else:
    location = None

# Dynamic Placeholder Based on Protocol
if protocol == "SPINS":
    example_id = "SPN01_CMH_0008"
elif protocol == "SPIN-ASD":
    example_id = "SPN10_CMH_0008"
elif protocol == "PREDICTS":
    example_id = "SPN30_CMH_030089"
elif protocol == "PREDICTS-HYBRID":
    example_id = "SPN32_CMH_030092"
elif protocol == "Slaight":
    example_id = "SPN30_CMH_040001"
elif protocol == "Healthy-Control":
    example_id = "SPN30_CMH_050001"
else:
    example_id = ""

# Step 3: Enter Old Subject ID
old_subject_id = st.text_input("Enter Old Subject ID", placeholder=f"e.g., {example_id}")

# Step 4: Generate ID
if st.button("Generate ID"):
    try:
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
        st.success(f"Subject ID: {subject_id}")
        st.success(f"XNAT ID: {xnat_id}")
    except ValueError as e:
        st.error(f"Error: {e}")
