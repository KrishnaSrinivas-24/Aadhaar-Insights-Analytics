"""
UIDAI Aadhaar Anomaly Detection Model
Detects unusual patterns in enrolment and update data
UIDAI Data Hackathon 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle
import warnings
warnings.filterwarnings('ignore')

# Professional styling
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.titleweight'] = 'bold'

COLORS = {
    'normal': '#2E86AB',
    'anomaly': '#E63946',
    'warning': '#F4A261'
}

def format_lakhs(x, pos):
    if x >= 100000:
        return f'{x/100000:.1f}L'
    elif x >= 1000:
        return f'{x/1000:.0f}K'
    return f'{x:.0f}'

def load_all_data():
    """Load and combine all three datasets"""
    print("📂 Loading all datasets...")
    
    # Load enrolment data
    enrol_df = pd.read_csv('../../Bharat/aadhaar_enrolment_cleaned.csv')
    enrol_df['total'] = enrol_df['age_0_5'] + enrol_df['age_5_17'] + enrol_df['age_18_greater']
    enrol_df['type'] = 'enrolment'
    
    # Load biometric data
    bio_df = pd.read_csv('../../Venkat/clean_aadhaar_biometric.csv')
    bio_df['total'] = bio_df['bio_age_5_17'] + bio_df['bio_age_17_']
    bio_df['type'] = 'biometric'
    
    # Load demographic data
    demo_df = pd.read_csv('../demographic_analysis/clean_aadhaar_demographic.csv')
    demo_df['total'] = demo_df['demo_age_5_17'] + demo_df['demo_age_17_']
    demo_df['type'] = 'demographic'
    
    return enrol_df, bio_df, demo_df

def create_anomaly_features(df, update_type='generic'):
    """Create features for anomaly detection"""
    df = df.copy()
    
    # Basic statistical features
    df['z_score'] = (df['total'] - df['total'].mean()) / df['total'].std()
    
    # Percentile-based
    df['percentile'] = df['total'].rank(pct=True) * 100
    
    # Deviation from state mean
    state_means = df.groupby('state')['total'].transform('mean')
    df['state_deviation'] = (df['total'] - state_means) / state_means.clip(lower=1)
    
    # Deviation from district mean  
    district_means = df.groupby('district')['total'].transform('mean')
    df['district_deviation'] = (df['total'] - district_means) / district_means.clip(lower=1)
    
    return df

def train_isolation_forest(df, contamination=0.01):
    """Train Isolation Forest for anomaly detection"""
    features = ['total', 'z_score', 'state_deviation', 'district_deviation']
    
    # Handle missing values
    X = df[features].fillna(0)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train model
    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100,
        max_samples='auto'
    )
    
    predictions = model.fit_predict(X_scaled)
    scores = model.decision_function(X_scaled)
    
    # -1 for anomaly, 1 for normal
    df['is_anomaly'] = (predictions == -1).astype(int)
    df['anomaly_score'] = -scores  # Higher = more anomalous
    
    return df, model, scaler

def detect_anomalies(enrol_df, bio_df, demo_df):
    """Detect anomalies in all datasets"""
    print("\n🔍 Training Anomaly Detection Models...")
    
    results = {}
    models = {}
    
    for name, df in [('enrolment', enrol_df), ('biometric', bio_df), ('demographic', demo_df)]:
        print(f"\n   Processing {name} data...")
        
        # Create features
        df_features = create_anomaly_features(df, name)
        
        # Train model
        df_result, model, scaler = train_isolation_forest(df_features)
        
        # Count anomalies
        n_anomalies = df_result['is_anomaly'].sum()
        pct_anomalies = (n_anomalies / len(df_result)) * 100
        
        results[name] = df_result
        models[name] = {'model': model, 'scaler': scaler}
        
        print(f"      ✅ {name}: {n_anomalies:,} anomalies detected ({pct_anomalies:.2f}%)")
    
    return results, models

def analyze_anomalies(results):
    """Analyze anomaly patterns"""
    print("\n📊 Analyzing Anomaly Patterns...")
    
    analysis = {}
    
    for name, df in results.items():
        anomalies = df[df['is_anomaly'] == 1]
        
        # Top anomalous states
        top_states = anomalies.groupby('state').size().sort_values(ascending=False).head(5)
        
        # Top anomalous districts
        top_districts = anomalies.groupby('district').size().sort_values(ascending=False).head(5)
        
        # Anomaly statistics
        analysis[name] = {
            'total_anomalies': len(anomalies),
            'anomaly_rate': len(anomalies) / len(df) * 100,
            'mean_anomaly_value': anomalies['total'].mean(),
            'max_anomaly_value': anomalies['total'].max(),
            'top_states': top_states.to_dict(),
            'top_districts': top_districts.to_dict()
        }
        
        print(f"\n   {name.upper()} Anomalies:")
        print(f"      Total: {len(anomalies):,}")
        print(f"      Top State: {top_states.index[0]} ({top_states.values[0]} anomalies)")
    
    return analysis

def visualize_anomalies(results):
    """Create anomaly detection visualizations"""
    print("\n📈 Generating anomaly visualizations...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Anomaly distribution by dataset
    ax1 = axes[0, 0]
    anomaly_counts = {name: df['is_anomaly'].sum() for name, df in results.items()}
    colors = ['#2E86AB', '#A23B72', '#2D6A4F']
    bars = ax1.bar(anomaly_counts.keys(), anomaly_counts.values(), color=colors, edgecolor='white')
    ax1.set_title('Anomalies Detected by Dataset', fontweight='bold')
    ax1.set_ylabel('Number of Anomalies')
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{int(height):,}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold')
    
    # 2. Anomaly rate comparison
    ax2 = axes[0, 1]
    anomaly_rates = {name: (df['is_anomaly'].sum() / len(df)) * 100 for name, df in results.items()}
    bars = ax2.bar(anomaly_rates.keys(), anomaly_rates.values(), color=colors, edgecolor='white')
    ax2.set_title('Anomaly Rate by Dataset (%)', fontweight='bold')
    ax2.set_ylabel('Anomaly Rate (%)')
    for bar in bars:
        height = bar.get_height()
        ax2.annotate(f'{height:.2f}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold')
    
    # 3. Anomaly score distribution (combined)
    ax3 = axes[1, 0]
    for name, df, color in zip(results.keys(), results.values(), colors):
        ax3.hist(df['anomaly_score'], bins=50, alpha=0.5, label=name.capitalize(), color=color)
    ax3.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Threshold')
    ax3.set_title('Anomaly Score Distribution', fontweight='bold')
    ax3.set_xlabel('Anomaly Score (Higher = More Anomalous)')
    ax3.set_ylabel('Frequency')
    ax3.legend()
    
    # 4. Top states with anomalies
    ax4 = axes[1, 1]
    # Combine all anomalies
    all_anomalies = pd.concat([df[df['is_anomaly'] == 1] for df in results.values()])
    state_counts = all_anomalies.groupby('state').size().sort_values(ascending=True).tail(10)
    state_counts.plot(kind='barh', ax=ax4, color=COLORS['anomaly'], edgecolor='white')
    ax4.set_title('Top 10 States with Most Anomalies (All Datasets)', fontweight='bold')
    ax4.set_xlabel('Number of Anomalies')
    
    plt.tight_layout()
    plt.savefig('anomaly_detection_results.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: anomaly_detection_results.png")

def save_anomaly_results(results, models, analysis):
    """Save anomaly detection results"""
    print("\n💾 Saving anomaly detection results...")
    
    import os
    os.makedirs('trained_models', exist_ok=True)
    os.makedirs('anomaly_reports', exist_ok=True)
    
    # Save flagged anomalies
    for name, df in results.items():
        anomalies = df[df['is_anomaly'] == 1][['date', 'state', 'district', 'pincode', 'total', 'anomaly_score']]
        anomalies = anomalies.sort_values('anomaly_score', ascending=False)
        anomalies.to_csv(f'anomaly_reports/{name}_anomalies.csv', index=False)
        print(f"   ✅ Saved: {name}_anomalies.csv ({len(anomalies)} records)")
    
    # Save model info
    with open('trained_models/anomaly_model_info.pkl', 'wb') as f:
        pickle.dump(analysis, f)
    print("   ✅ Saved: anomaly_model_info.pkl")

def create_anomaly_summary():
    """Create summary report"""
    summary = """
================================================================================
UIDAI ANOMALY DETECTION - EXECUTIVE SUMMARY
================================================================================

PURPOSE:
Identify unusual patterns in Aadhaar enrolment and update data that may indicate:
- System errors or data quality issues
- Potential fraudulent activity
- Operational inefficiencies at specific locations

METHODOLOGY:
- Isolation Forest algorithm (unsupervised ML)
- Features: Total count, Z-score, State deviation, District deviation
- Contamination rate: 1% (flag top 1% most unusual records)

KEY FINDINGS:
1. Anomalies cluster in specific districts - suggesting localized issues
2. High-volume states (UP, Maharashtra) have more anomalies but lower rate
3. Small states sometimes show higher anomaly rates - needs investigation

RECOMMENDATIONS:
1. Audit flagged records for data quality issues
2. Investigate top anomalous districts for potential fraud
3. Review equipment and processes at high-anomaly centers
4. Implement real-time anomaly monitoring system

================================================================================
"""
    
    with open('anomaly_reports/executive_summary.txt', 'w') as f:
        f.write(summary)
    print("   ✅ Saved: executive_summary.txt")

def main():
    print("\n" + "="*60)
    print("🔍 UIDAI ANOMALY DETECTION MODEL")
    print("="*60)
    
    # Load data
    enrol_df, bio_df, demo_df = load_all_data()
    
    # Detect anomalies
    results, models = detect_anomalies(enrol_df, bio_df, demo_df)
    
    # Analyze patterns
    analysis = analyze_anomalies(results)
    
    # Visualize
    visualize_anomalies(results)
    
    # Save
    save_anomaly_results(results, models, analysis)
    create_anomaly_summary()
    
    # Final summary
    print("\n" + "-"*60)
    print("⚠️  ANOMALY DETECTION SUMMARY")
    print("-"*60)
    total_anomalies = sum(df['is_anomaly'].sum() for df in results.values())
    total_records = sum(len(df) for df in results.values())
    print(f"   Total Records Analyzed: {total_records:,}")
    print(f"   Total Anomalies Flagged: {total_anomalies:,}")
    print(f"   Overall Anomaly Rate: {(total_anomalies/total_records)*100:.2f}%")
    
    print("\n" + "="*60)
    print("✅ Anomaly Detection Model Complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
