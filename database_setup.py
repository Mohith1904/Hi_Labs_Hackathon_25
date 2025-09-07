import pandas as pd
import sqlite3
import re
from datetime import datetime
from fuzzywuzzy import process
from tqdm import tqdm 

PROVIDER_ROSTER_PATH = 'data/provider_roster_with_errors.csv'
NY_LICENSE_PATH = 'data/ny_medical_license_database.csv'
CA_LICENSE_PATH = 'data/ca_medical_license_database.csv'
NPI_REGISTRY_PATH = 'data/mock_npi_registry.csv'

def clean_phone_number(phone):
    """Removes all non-digit characters from a phone number string."""
    if isinstance(phone, str):
        return re.sub(r'\D', '', phone)
    return phone

def validate_provider(roster_row, ny_license_map, ca_license_map, npi_map):
    """
    Validates a single provider against license and NPI databases using fuzzy name matching.
    """
    # --- License Validation ---
    is_license_found = 0
    is_license_active = 0
    roster_name = roster_row['full_name']
    roster_state = roster_row['license_state']
    
    license_map = None
    if roster_state == 'NY':
        license_map = ny_license_map
    elif roster_state == 'CA':
        license_map = ca_license_map
        
    if license_map:
        # Use fuzzywuzzy to find the best name match in the state license data
        best_match = process.extractOne(roster_name, license_map.keys(), score_cutoff=85)
        
        if best_match:
            matched_license_data = license_map[best_match[0]]
            # If names are a close match, check if license numbers also match
            if roster_row['license_number'] == matched_license_data['license_number']:
                is_license_found = 1
                # Check if the license is expired
                if matched_license_data['expiration_date'] and pd.to_datetime(matched_license_data['expiration_date']) > datetime.now():
                    is_license_active = 1

    # --- NPI Validation ---
    is_npi_found = 0
    best_npi_match = process.extractOne(roster_name, npi_map.keys(), score_cutoff=85)
    if best_npi_match:
        matched_npi_data = npi_map[best_npi_match[0]]
        # If names are a close match, check if NPI numbers also match
        if roster_row['npi'] == matched_npi_data['npi']:
            is_npi_found = 1
            
    return is_license_found, is_license_active, is_npi_found

def setup_database():
    """
    Loads, cleans, enriches, and validates data, then populates an in-memory SQLite database.
    """
    provider_roster = pd.read_csv(PROVIDER_ROSTER_PATH)
    ny_licenses = pd.read_csv(NY_LICENSE_PATH)
    ca_licenses = pd.read_csv(CA_LICENSE_PATH)
    npi_registry = pd.read_csv(NPI_REGISTRY_PATH)

    for df in [provider_roster, ny_licenses, ca_licenses, npi_registry]:
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')

    # --- Pre-computation for Faster Matching ---
    
    #Remove duplicate provider names to ensure a unique index
    ny_licenses.drop_duplicates(subset=['provider_name'], keep='first', inplace=True)
    ca_licenses.drop_duplicates(subset=['provider_name'], keep='first', inplace=True)

    # Convert license data into dictionaries for quick lookups
    ny_licenses['expiration_date'] = pd.to_datetime(ny_licenses['expiration_date'], errors='coerce')
    ny_license_map = ny_licenses.set_index('provider_name').to_dict('index')
    
    ca_licenses['expiration_date'] = pd.to_datetime(ca_licenses['expiration_date'], errors='coerce')
    ca_license_map = ca_licenses.set_index('provider_name').to_dict('index')

    #Correctly create a 'full_name' column and remove duplicates before creating the NPI map
    npi_registry['full_name'] = npi_registry['provider_first_name'].astype(str) + ' ' + npi_registry['provider_last_name'].astype(str)
    npi_registry.drop_duplicates(subset=['full_name'], keep='first', inplace=True)
    npi_registry_map = npi_registry.set_index('full_name').to_dict('index')
    
    print("🤖 Starting provider validation with fuzzy matching... (This may take a minute)")
    
    # Use tqdm for a progress bar as this is a slow operation
    tqdm.pandas(desc="Validating Roster")
    
    # Apply the validation function to each row in the provider roster
    validation_results = provider_roster.progress_apply(
        lambda row: validate_provider(row, ny_license_map, ca_license_map, npi_registry_map),
        axis=1
    )
    
    # Add new validation columns to the DataFrame
    provider_roster[['is_license_found', 'is_license_active', 'is_npi_found']] = pd.DataFrame(validation_results.tolist(), index=provider_roster.index)
    
    print("✅ Provider validation complete.")

    # --- Final Data Loading ---
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    provider_roster.to_sql('provider_roster', conn, if_exists='replace', index=False)
    print("✅ In-memory database created with enriched provider data.")
    return conn

def get_db_schema(conn):
    """Returns the schema of all tables in the database."""
    # This function should be updated to reflect the new, enriched schema
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    schema_info = ""
    for table_name in tables:
        table_name = table_name[0]
        schema_info += f"Table '{table_name}':\n"
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for column in columns:
            schema_info += f"  - {column[1]} ({column[2]})\n"
    return schema_info