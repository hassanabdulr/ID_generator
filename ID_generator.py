



### Core logic that generates and produces the ID

def generate_spins_r_ids(old_subject_id, scanning_location):
    """
    Generates both the Subject ID and XNAT ID for SPIN-R participants.

    Args:
        old_subject_id (str): Old Subject ID in the format 'SPN01_CMH_0008'.
        scanning_location (str): 'CAMH' or 'ToNI'.

    Returns:
        tuple: New Subject ID and XNAT ID.
    """
    # Determine the new prefix and participant number prefix based on the scanning location
    if scanning_location == "CAMH":
        new_prefix = "SPN30"
        participant_prefix = "01"
    elif scanning_location == "ToNI":
        new_prefix = "SPN31"
        participant_prefix = "02"
    else:
        raise ValueError("Invalid scanning location. Must be 'CAMH' or 'ToNI'.")

    # Split the old Subject ID into parts
    parts = old_subject_id.split("_")
    if len(parts) < 3:
        raise ValueError("Old Subject ID format is incorrect. Expected format: 'SPN01_CMH_0008'.")

    old_prefix, location, participant_num = parts

    # Update the participant number by prepending the appropriate prefix
    new_participant_num = f"{participant_prefix}{participant_num}"

    # Generate the new Subject ID
    subject_id = f"{new_prefix}_{location}_{new_participant_num}"

    # Generate the XNAT ID by appending session and sequence
    xnat_id = f"{subject_id}_02_SE01_MR"

    return subject_id, xnat_id





def generate_spinasd_ids(old_subject_id):
    """
    Generates both the Subject ID and XNAT ID for SPIN-ASD participants.

    Args:
        old_subject_id (str): Old Subject ID in the format 'SPN10_CMH_0008'.

    Returns:
        tuple: New Subject ID and XNAT ID.
    """
    # Split the old Subject ID into parts
    parts = old_subject_id.split("_")
    if len(parts) < 3:
        raise ValueError("Old Subject ID format is incorrect. Expected format: 'SPN10_CMH_0008'.")

    old_prefix, location, participant_num = parts

    # Verify this is a SPIN-ASD ID
    if old_prefix != "SPN10":
        raise ValueError("Invalid prefix for SPIN-ASD. Expected 'SPN10'.")

    # Check if the participant number is valid (<= 4 digits)
    if len(participant_num) > 4:
        raise ValueError("Participant number exceeds 4 digits. Please check the input.")
    
    # Update the prefix and participant number
    new_prefix = "SPN31"  # SPIN-ASD maps to SPIN31 for ToNI
    new_participant_num = f"10{participant_num}"

    # Generate the new Subject ID
    subject_id = f"{new_prefix}_{location}_{new_participant_num}"

    # Generate the XNAT ID by appending session and sequence
    xnat_id = f"{subject_id}_02_SE01_MR"

    return subject_id, xnat_id


def generate_predicts_ids(old_subject_id, scanning_location):
    """
    Generates both the Subject ID and XNAT ID for PREDICTS participants.

    Args:
        old_subject_id (str): Old Subject ID in the format 'SPN30_CMH_030089'.
        scanning_location (str): 'CAMH' or 'ToNI'.

    Returns:
        tuple: New Subject ID and XNAT ID.
    """
    # Determine the prefix based on the scanning location
    if scanning_location == "CAMH":
        prefix = "SPN30"
    elif scanning_location == "ToNI":
        prefix = "SPN31"
    else:
        raise ValueError("Invalid scanning location. Must be 'CAMH' or 'ToNI'.")

    # Split the old Subject ID into parts
    parts = old_subject_id.split("_")
    if len(parts) < 3:
        raise ValueError("Old Subject ID format is incorrect. Expected format: 'SPN30_CMH_030089'.")

    old_prefix, location, participant_num = parts[:3]

    # Verify the old prefix aligns with PREDICTS
    if old_prefix not in ["SPN30", "SPN31"]:
        raise ValueError("Invalid prefix for PREDICTS. Expected 'SPN30' or 'SPN31'.")

    # Generate the new Subject ID
    subject_id = f"{prefix}_{location}_{participant_num}"

    # Generate the XNAT ID by appending session and sequence
    xnat_id = f"{subject_id}_02_SE01_MR"

    return subject_id, xnat_id



# Outputs:
# Subject ID: SPN30_CMH_030089
# XNAT ID: SPN30_CMH_030089_02_SE01_MR
#
# Subject ID: SPN31_CMH_030092
# XNAT ID: SPN31_CMH_030092_02_SE01_MR


def generate_predicts_hybrid_ids(old_subject_id):
    """
    Generates both the Subject ID and XNAT ID for PREDICTS hybrid participants.

    Args:
        old_subject_id (str): Old Subject ID in the format 'SPN32_CMH_030092'.

    Returns:
        tuple: New Subject ID and XNAT ID.
    """
    # Split the old Subject ID into parts
    parts = old_subject_id.split("_")
    if len(parts) < 3:
        raise ValueError("Old Subject ID format is incorrect. Expected format: 'SPN32_CMH_030092'.")

    old_prefix, location, participant_num = parts[:3]

    # Verify the old prefix aligns with hybrid protocol
    if old_prefix != "SPN32":
        raise ValueError("Invalid prefix for PREDICTS hybrid participants. Expected 'SPN32'.")

    # Generate the new Subject ID
    subject_id = f"{old_prefix}_{location}_{participant_num}"

    # Generate the XNAT ID by appending session and sequence
    xnat_id = f"{subject_id}_01_SE01_MR"

    return subject_id, xnat_id


# Outputs:
# Subject ID: SPN32_CMH_030092
# XNAT ID: SPN32_CMH_030092_02_SE01_MR


def generate_slaight_ids(old_subject_id, scanning_location):
    """
    Generates both the Subject ID and XNAT ID for Slaight participants.

    Args:
        old_subject_id (str): Old Subject ID in the format 'SPN30_CMH_040001'.
        scanning_location (str): 'CAMH' or 'ToNI'.

    Returns:
        tuple: New Subject ID and XNAT ID.
    """
    # Determine the prefix based on the scanning location
    if scanning_location == "CAMH":
        prefix = "SPN30"
    elif scanning_location == "ToNI":
        prefix = "SPN31"
    else:
        raise ValueError("Invalid scanning location. Must be 'CAMH' or 'ToNI'.")

    # Split the old Subject ID into parts
    parts = old_subject_id.split("_")
    if len(parts) < 3:
        raise ValueError("Old Subject ID format is incorrect. Expected format: 'SPN30_CMH_040001'.")

    old_prefix, location, participant_num = parts[:3]

    # Verify the old prefix aligns with Slaight
    if old_prefix not in ["SPN30", "SPN31"]:
        raise ValueError("Invalid prefix for Slaight. Expected 'SPN30' or 'SPN31'.")

    # Generate the new Subject ID
    subject_id = f"{prefix}_{location}_{participant_num}"

    # Generate the XNAT ID by appending session and sequence
    xnat_id = f"{subject_id}_02_SE01_MR"

    return subject_id, xnat_id


# Outputs:
# Subject ID: SPN30_CMH_040001
# XNAT ID: SPN30_CMH_040001_02_SE01_MR
#
# Subject ID: SPN31_CMH_040001
# XNAT ID: SPN31_CMH_040001_02_SE01_MR


def generate_new_healthy_control_ids(old_subject_id, scanning_location):
    """
    Generates both the Subject ID and XNAT ID for new healthy controls.

    Args:
        old_subject_id (str): Old Subject ID in the format 'SPN30_CMH_050001'.
        scanning_location (str): 'CAMH' or 'ToNI'.

    Returns:
        tuple: New Subject ID and XNAT ID.
    """
    # Determine the prefix based on the scanning location
    if scanning_location == "CAMH":
        prefix = "SPN30"
    elif scanning_location == "ToNI":
        prefix = "SPN31"
    else:
        raise ValueError("Invalid scanning location. Must be 'CAMH' or 'ToNI'.")

    # Split the old Subject ID into parts
    parts = old_subject_id.split("_")
    if len(parts) < 3:
        raise ValueError("Old Subject ID format is incorrect. Expected format: 'SPN30_CMH_050001'.")

    old_prefix, location, participant_num = parts[:3]

    # Verify the old prefix aligns with new healthy controls
    if old_prefix not in ["SPN30", "SPN31"]:
        raise ValueError("Invalid prefix for new healthy controls. Expected 'SPN30' or 'SPN31'.")

    # Generate the new Subject ID
    subject_id = f"{prefix}_{location}_{participant_num}"

    # Generate the XNAT ID by appending session and sequence
    xnat_id = f"{subject_id}_01_SE01_MR"

    return subject_id, xnat_id