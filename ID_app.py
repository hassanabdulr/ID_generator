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

# Step 1: Select Protocol
protocol = st.radio("Select Protocol", ["SPINS", "SPIN-ASD", "PREDICTS", "PREDICTS-HYBRID", "Slaight", "Healthy-Control"])

# Step 2: Select Scanning Location (if applicable)
location = None
if protocol in ["SPINS", "PREDICTS", "Slaight", "Healthy-Control"]:
    location = st.radio("Select Scanning Location", ["CAMH", "ToNI"])

# Step 3: Enter Old Subject ID
example_id = get_example_id(protocol)
old_subject_id = st.text_input("Enter Old Subject ID", placeholder=f"e.g., {example_id}")

# Step 4: Generate ID
if st.button("Generate ID"):
    try:
        # Validation: Ensure subject ID is entered
        if not old_subject_id:
            raise ValueError("Old Subject ID is required!")

        # Validation: Ensure location is selected where applicable
        if protocol in ["SPINS", "PREDICTS", "Slaight", "Healthy-Control"] and not location:
            raise ValueError("Scanning location must be selected!")

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