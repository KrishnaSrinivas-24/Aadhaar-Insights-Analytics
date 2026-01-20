"""
COMPREHENSIVE DATA CLEANING SCRIPT
Standardizes state names and fixes data quality issues across all datasets
UIDAI Data Hackathon 2026
"""

import pandas as pd
import glob
import os
import re

# Official Indian States and Union Territories (Standardized Names)
STATE_MAPPING = {
    # Andaman & Nicobar
    'andaman & nicobar islands': 'Andaman & Nicobar Islands',
    'andaman and nicobar islands': 'Andaman & Nicobar Islands',
    'andaman and nicobar': 'Andaman & Nicobar Islands',
    'a&n islands': 'Andaman & Nicobar Islands',
    
    # Andhra Pradesh
    'andhra pradesh': 'Andhra Pradesh',
    'andrapradesh': 'Andhra Pradesh',
    'ap': 'Andhra Pradesh',
    
    # Arunachal Pradesh
    'arunachal pradesh': 'Arunachal Pradesh',
    'arunachalpradesh': 'Arunachal Pradesh',
    
    # Assam
    'assam': 'Assam',
    
    # Bihar
    'bihar': 'Bihar',
    'biharisgarh': 'Bihar',  # Corrupted name
    
    # Chandigarh
    'chandigarh': 'Chandigarh',
    'chandigarhrh': 'Chandigarh',  # Corrupted name
    
    # Chhattisgarh
    'chhattisgarh': 'Chhattisgarh',
    'chattisgarh': 'Chhattisgarh',
    'chhatisgarh': 'Chhattisgarh',
    'chhatisgarhar haveli': 'Chhattisgarh',  # Corrupted name
    'chhattisgarhgar haveli': 'Chhattisgarh',  # Corrupted name
    
    # Dadra & Nagar Haveli and Daman & Diu (merged UT)
    'dadra & nagar haveli': 'Dadra & Nagar Haveli and Daman & Diu',
    'dadra and nagar haveli': 'Dadra & Nagar Haveli and Daman & Diu',
    'dadra and nagar haveli and daman and diu': 'Dadra & Nagar Haveli and Daman & Diu',
    'the dadra and nagar haveli and daman and diu': 'Dadra & Nagar Haveli and Daman & Diu',
    'daman & diu': 'Dadra & Nagar Haveli and Daman & Diu',
    'daman and diu': 'Dadra & Nagar Haveli and Daman & Diu',
    'dadra & nagar havelili and daman and diu': 'Dadra & Nagar Haveli and Daman & Diu',  # Corrupted
    
    # Delhi
    'delhi': 'Delhi',
    'new delhi': 'Delhi',
    'delhina': 'Delhi',  # Corrupted
    
    # Goa
    'goa': 'Goa',
    'goaachal pradesh': 'Goa',  # Corrupted
    
    # Gujarat
    'gujarat': 'Gujarat',
    'gujarat kashmir': 'Gujarat',  # Corrupted
    
    # Haryana
    'haryana': 'Haryana',
    'haryanand kashmir': 'Haryana',  # Corrupted
    
    # Himachal Pradesh
    'himachal pradesh': 'Himachal Pradesh',
    'himachalpradesh': 'Himachal Pradesh',
    'hp': 'Himachal Pradesh',
    
    # Jammu & Kashmir
    'jammu & kashmir': 'Jammu & Kashmir',
    'jammu and kashmir': 'Jammu & Kashmir',
    'jammu and kashmir': 'Jammu & Kashmir',
    'j&k': 'Jammu & Kashmir',
    
    # Jharkhand
    'jharkhand': 'Jharkhand',
    'jharkhandep': 'Jharkhand',  # Corrupted
    
    # Karnataka
    'karnataka': 'Karnataka',
    'karnatakaadesh': 'Karnataka',  # Corrupted
    
    # Kerala
    'kerala': 'Kerala',
    'keralashtra': 'Kerala',  # Corrupted
    
    # Ladakh
    'ladakh': 'Ladakh',
    'ladakhr': 'Ladakh',  # Corrupted
    
    # Lakshadweep
    'lakshadweep': 'Lakshadweep',
    
    # Madhya Pradesh
    'madhya pradesh': 'Madhya Pradesh',
    'madhyapradesh': 'Madhya Pradesh',
    'mp': 'Madhya Pradesh',
    
    # Maharashtra
    'maharashtra': 'Maharashtra',
    
    # Manipur
    'manipur': 'Manipur',
    
    # Meghalaya
    'meghalaya': 'Meghalaya',
    
    # Mizoram
    'mizoram': 'Mizoram',
    'mizoramerry': 'Mizoram',  # Corrupted
    
    # Nagaland
    'nagaland': 'Nagaland',
    'nagalandry': 'Nagaland',  # Corrupted
    
    # Odisha
    'odisha': 'Odisha',
    'orissa': 'Odisha',
    'orissanadu': 'Odisha',  # Corrupted
    'odishahan': 'Odisha',  # Corrupted
    
    # Puducherry
    'puducherry': 'Puducherry',
    'pondicherry': 'Puducherry',
    
    # Punjab
    'punjab': 'Punjab',
    'punjaba': 'Punjab',  # Corrupted
    
    # Rajasthan
    'rajasthan': 'Rajasthan',
    'rajasthnal': 'Rajasthan',  # Corrupted
    
    # Sikkim
    'sikkim': 'Sikkim',
    'sikkimengal': 'Sikkim',  # Corrupted
    
    # Tamil Nadu
    'tamil nadu': 'Tamil Nadu',
    'tamilnadu': 'Tamil Nadu',
    'tn': 'Tamil Nadu',
    
    # Telangana
    'telangana': 'Telangana',
    'telanganagal': 'Telangana',  # Corrupted
    
    # Tripura
    'tripura': 'Tripura',
    'tripurangal': 'Tripura',  # Corrupted
    
    # Uttar Pradesh
    'uttar pradesh': 'Uttar Pradesh',
    'uttarpradesh': 'Uttar Pradesh',
    'up': 'Uttar Pradesh',
    
    # Uttarakhand
    'uttarakhand': 'Uttarakhand',
    'uttaranchal': 'Uttarakhand',
    
    # West Bengal
    'west bengal': 'West Bengal',
    'westbengal': 'West Bengal',
    'west  bengal': 'West Bengal',
    'west bangal': 'West Bengal',
    'west bengli': 'West Bengal',
    'west bengalesh': 'West Bengal',  # Corrupted
}

# Cities that appeared as states (need to be mapped to correct state)
CITY_TO_STATE = {
    'balanagar': 'Telangana',
    'balanagarhali': 'Telangana',
    'darbhanga': 'Bihar',
    'jaipur': 'Rajasthan',
    'jaipuraka': 'Rajasthan',
    'madanapalle': 'Andhra Pradesh',
    'nagpur': 'Maharashtra',
    'puttenahalli': 'Karnataka',
    'puttenahallih': 'Karnataka',
    'raja annamalai puram': 'Tamil Nadu',
}

def clean_state_name(state):
    """Standardize a state name"""
    if pd.isna(state) or state is None:
        return 'Unknown'
    
    # Convert to lowercase and strip
    state_lower = str(state).lower().strip()
    
    # Remove extra spaces
    state_lower = re.sub(r'\s+', ' ', state_lower)
    
    # Check in state mapping
    if state_lower in STATE_MAPPING:
        return STATE_MAPPING[state_lower]
    
    # Check in city to state mapping
    if state_lower in CITY_TO_STATE:
        return CITY_TO_STATE[state_lower]
    
    # If numeric, return Unknown
    if state_lower.isdigit():
        return 'Unknown'
    
    # Try partial matching for corrupted names
    for key, value in STATE_MAPPING.items():
        if key in state_lower or state_lower in key:
            return value
    
    # If still not found, capitalize and return
    return state.strip().title()

def clean_dataframe(df, dataset_name):
    """Clean a dataframe"""
    print(f"\n   Processing {dataset_name}...")
    original_rows = len(df)
    
    # Clean state names
    print(f"      Original unique states: {df['state'].nunique()}")
    df['state'] = df['state'].apply(clean_state_name)
    print(f"      Cleaned unique states: {df['state'].nunique()}")
    
    # Remove 'Unknown' states
    unknown_count = (df['state'] == 'Unknown').sum()
    if unknown_count > 0:
        print(f"      Removed {unknown_count} records with unknown state")
        df = df[df['state'] != 'Unknown']
    
    # Remove duplicates
    before_dedup = len(df)
    df = df.drop_duplicates()
    print(f"      Removed {before_dedup - len(df)} duplicates")
    
    # Fill NA values
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        if col != 'pincode':
            df[col] = df[col].fillna(0)
    
    print(f"      Final records: {len(df):,} (from {original_rows:,})")
    
    return df

def load_and_clean_enrolment():
    """Load and clean enrolment data"""
    print("\n" + "="*60)
    print("📂 ENROLMENT DATA")
    print("="*60)
    
    files = glob.glob('datasets/api_data_aadhar_enrolment/*.csv')
    df_list = [pd.read_csv(f) for f in files]
    df = pd.concat(df_list, ignore_index=True)
    print(f"   Loaded {len(df):,} records from {len(files)} files")
    
    df = clean_dataframe(df, "Enrolment")
    
    # Save cleaned file
    output_path = 'MY UPDATES/cleaned_data/aadhaar_enrolment_cleaned_v2.csv'
    os.makedirs('MY UPDATES/cleaned_data', exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"   ✅ Saved: {output_path}")
    
    return df

def load_and_clean_biometric():
    """Load and clean biometric data"""
    print("\n" + "="*60)
    print("📂 BIOMETRIC DATA")
    print("="*60)
    
    files = glob.glob('datasets/api_data_aadhar_biometric/*.csv')
    df_list = [pd.read_csv(f) for f in files]
    df = pd.concat(df_list, ignore_index=True)
    print(f"   Loaded {len(df):,} records from {len(files)} files")
    
    df = clean_dataframe(df, "Biometric")
    
    # Save cleaned file
    output_path = 'MY UPDATES/cleaned_data/aadhaar_biometric_cleaned_v2.csv'
    df.to_csv(output_path, index=False)
    print(f"   ✅ Saved: {output_path}")
    
    return df

def load_and_clean_demographic():
    """Load and clean demographic data"""
    print("\n" + "="*60)
    print("📂 DEMOGRAPHIC DATA")
    print("="*60)
    
    files = glob.glob('datasets/api_data_aadhar_demographic/*.csv')
    df_list = [pd.read_csv(f) for f in files]
    df = pd.concat(df_list, ignore_index=True)
    print(f"   Loaded {len(df):,} records from {len(files)} files")
    
    df = clean_dataframe(df, "Demographic")
    
    # Save cleaned file
    output_path = 'MY UPDATES/cleaned_data/aadhaar_demographic_cleaned_v2.csv'
    df.to_csv(output_path, index=False)
    print(f"   ✅ Saved: {output_path}")
    
    return df

def print_state_summary(enrol_df, bio_df, demo_df):
    """Print summary of states after cleaning"""
    print("\n" + "="*60)
    print("📊 STATE SUMMARY AFTER CLEANING")
    print("="*60)
    
    all_states = set(enrol_df['state'].unique()) | set(bio_df['state'].unique()) | set(demo_df['state'].unique())
    
    print(f"\n   Total unique states/UTs: {len(all_states)}")
    print("\n   State list:")
    for state in sorted(all_states):
        e_count = len(enrol_df[enrol_df['state'] == state])
        b_count = len(bio_df[bio_df['state'] == state])
        d_count = len(demo_df[demo_df['state'] == state])
        print(f"      {state}: E={e_count:,} | B={b_count:,} | D={d_count:,}")

def main():
    print("\n" + "="*60)
    print("🧹 COMPREHENSIVE DATA CLEANING")
    print("="*60)
    
    # Clean all datasets
    enrol_df = load_and_clean_enrolment()
    bio_df = load_and_clean_biometric()
    demo_df = load_and_clean_demographic()
    
    # Print summary
    print_state_summary(enrol_df, bio_df, demo_df)
    
    print("\n" + "="*60)
    print("✅ DATA CLEANING COMPLETE!")
    print("="*60)
    print("\nCleaned files saved to: MY UPDATES/cleaned_data/")
    print("  - aadhaar_enrolment_cleaned_v2.csv")
    print("  - aadhaar_biometric_cleaned_v2.csv")
    print("  - aadhaar_demographic_cleaned_v2.csv")
    print()

if __name__ == "__main__":
    main()
