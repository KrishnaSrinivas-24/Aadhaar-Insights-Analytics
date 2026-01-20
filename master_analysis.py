"""
MASTER ANALYSIS SCRIPT - Regenerate ALL Charts and ML Models
Using Cleaned V2 Data
UIDAI Data Hackathon 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

# Professional styling
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'

# Color palettes for each dataset
ENROL_COLORS = {'primary': '#2E86AB', 'secondary': '#A23B72', 'accent': '#F18F01'}
BIO_COLORS = {'primary': '#A23B72', 'secondary': '#2E86AB', 'accent': '#F18F01'}
DEMO_COLORS = {'primary': '#2D6A4F', 'secondary': '#40916C', 'accent': '#E63946'}

def format_lakhs(x, pos):
    if x >= 100000:
        return f'{x/100000:.1f}L'
    elif x >= 1000:
        return f'{x/1000:.0f}K'
    return f'{x:.0f}'

def add_value_labels(ax, bars):
    for bar in bars:
        height = bar.get_height()
        label = f'{height/100000:.1f}L' if height >= 100000 else f'{height/1000:.0f}K'
        ax.annotate(label, xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

def load_cleaned_data():
    """Load all cleaned datasets"""
    print("\n📂 Loading cleaned datasets...")
    
    enrol = pd.read_csv('cleaned_data/aadhaar_enrolment_cleaned_v2.csv')
    bio = pd.read_csv('cleaned_data/aadhaar_biometric_cleaned_v2.csv')
    demo = pd.read_csv('cleaned_data/aadhaar_demographic_cleaned_v2.csv')
    
    # Create totals
    enrol['total'] = enrol['age_0_5'] + enrol['age_5_17'] + enrol['age_18_greater']
    bio['total'] = bio['bio_age_5_17'] + bio['bio_age_17_']
    demo['total'] = demo['demo_age_5_17'] + demo['demo_age_17_']
    
    print(f"   ✅ Enrolment: {len(enrol):,} records, {enrol['state'].nunique()} states")
    print(f"   ✅ Biometric: {len(bio):,} records, {bio['state'].nunique()} states")
    print(f"   ✅ Demographic: {len(demo):,} records, {demo['state'].nunique()} states")
    
    return enrol, bio, demo

# ============================================================
# ENROLMENT CHARTS
# ============================================================

def generate_enrolment_charts(df, output_dir):
    """Generate all enrolment charts"""
    print("\n📊 Generating Enrolment Charts...")
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Age Group Chart
    age_totals = {'0-5 Years\n(Infants)': df['age_0_5'].sum(),
                  '5-17 Years\n(Children)': df['age_5_17'].sum(),
                  '18+ Years\n(Adults)': df['age_18_greater'].sum()}
    
    fig, ax = plt.subplots(figsize=(10, 7))
    colors = [ENROL_COLORS['primary'], ENROL_COLORS['secondary'], ENROL_COLORS['accent']]
    bars = ax.bar(age_totals.keys(), age_totals.values(), color=colors, edgecolor='#333', linewidth=1.2)
    add_value_labels(ax, bars)
    
    total = sum(age_totals.values())
    for bar, val in zip(bars, age_totals.values()):
        pct = (val / total) * 100
        ax.annotate(f'({pct:.1f}%)', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2),
                   ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    
    ax.set_title('Aadhaar Enrolment Distribution by Age Group\n(Based on Cleaned Dataset)', fontweight='bold', color='#1B4965')
    ax.set_ylabel('Total Enrolments')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', ha='right', fontsize=8, style='italic', color='#666')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/age_group_enrolment_v2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ age_group_enrolment_v2.png")
    
    # 2. State-wise Chart
    state_totals = df.groupby('state')['total'].sum().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    colors = plt.cm.Blues(np.linspace(0.8, 0.4, len(state_totals)))
    bars = ax.bar(range(len(state_totals)), state_totals.values, color=colors, edgecolor='#1B4965', linewidth=1.2)
    add_value_labels(ax, bars)
    ax.set_xticks(range(len(state_totals)))
    ax.set_xticklabels(state_totals.index, rotation=45, ha='right')
    ax.set_title('Top 10 States by Aadhaar Enrolment\n(Cleaned Dataset)', fontweight='bold', color='#1B4965')
    ax.set_ylabel('Total Enrolments')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', ha='right', fontsize=8, style='italic', color='#666')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/state_wise_enrolment_v2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ state_wise_enrolment_v2.png")
    
    # 3. Time Trend Chart
    df_copy = df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['date'], dayfirst=True)
    daily = df_copy.groupby('date')['total'].sum().reset_index().sort_values('date')
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.fill_between(daily['date'], daily['total'], alpha=0.3, color=ENROL_COLORS['primary'])
    ax.plot(daily['date'], daily['total'], color=ENROL_COLORS['primary'], linewidth=2, label='Daily Enrolments')
    if len(daily) > 7:
        daily['ma_7'] = daily['total'].rolling(7).mean()
        ax.plot(daily['date'], daily['ma_7'], color=ENROL_COLORS['accent'], linewidth=2.5, linestyle='--', label='7-Day MA')
    ax.set_title('Aadhaar Enrolment Trend Over Time\n(Cleaned Dataset)', fontweight='bold', color='#1B4965')
    ax.set_ylabel('Daily Enrolments')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    ax.legend(loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45, ha='right')
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', ha='right', fontsize=8, style='italic', color='#666')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/enrolment_trend_v2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ enrolment_trend_v2.png")
    
    return age_totals, state_totals

# ============================================================
# BIOMETRIC CHARTS
# ============================================================

def generate_biometric_charts(df, output_dir):
    """Generate all biometric charts"""
    print("\n📊 Generating Biometric Charts...")
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Age Group Chart
    age_totals = {'5-17 Years\n(Children & Teens)': df['bio_age_5_17'].sum(),
                  '17+ Years\n(Adults)': df['bio_age_17_'].sum()}
    
    fig, ax = plt.subplots(figsize=(10, 7))
    colors = [BIO_COLORS['secondary'], BIO_COLORS['primary']]
    bars = ax.bar(age_totals.keys(), age_totals.values(), color=colors, edgecolor='#333', linewidth=1.2, width=0.5)
    add_value_labels(ax, bars)
    
    total = sum(age_totals.values())
    for bar, val in zip(bars, age_totals.values()):
        pct = (val / total) * 100
        ax.annotate(f'({pct:.1f}%)', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2),
                   ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    
    ax.set_title('Biometric Update Distribution by Age Group\n(Cleaned Dataset)', fontweight='bold', color='#1B4965')
    ax.set_ylabel('Total Biometric Updates')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', ha='right', fontsize=8, style='italic', color='#666')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/age_group_biometric_v2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ age_group_biometric_v2.png")
    
    # 2. State-wise Chart
    state_totals = df.groupby('state')['total'].sum().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    colors = plt.cm.Purples(np.linspace(0.8, 0.4, len(state_totals)))
    bars = ax.bar(range(len(state_totals)), state_totals.values, color=colors, edgecolor='#1B4965', linewidth=1.2)
    add_value_labels(ax, bars)
    ax.set_xticks(range(len(state_totals)))
    ax.set_xticklabels(state_totals.index, rotation=45, ha='right')
    ax.set_title('Top 10 States by Biometric Updates\n(Cleaned Dataset)', fontweight='bold', color='#1B4965')
    ax.set_ylabel('Total Biometric Updates')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', ha='right', fontsize=8, style='italic', color='#666')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/state_wise_biometric_v2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ state_wise_biometric_v2.png")
    
    # 3. Time Trend Chart
    df_copy = df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['date'], dayfirst=True)
    daily = df_copy.groupby('date')['total'].sum().reset_index().sort_values('date')
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.fill_between(daily['date'], daily['total'], alpha=0.3, color=BIO_COLORS['primary'])
    ax.plot(daily['date'], daily['total'], color=BIO_COLORS['primary'], linewidth=2, label='Daily Updates')
    if len(daily) > 7:
        daily['ma_7'] = daily['total'].rolling(7).mean()
        ax.plot(daily['date'], daily['ma_7'], color=BIO_COLORS['accent'], linewidth=2.5, linestyle='--', label='7-Day MA')
    ax.set_title('Biometric Update Trend Over Time\n(Cleaned Dataset)', fontweight='bold', color='#1B4965')
    ax.set_ylabel('Daily Updates')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    ax.legend(loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45, ha='right')
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', ha='right', fontsize=8, style='italic', color='#666')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/biometric_trend_v2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ biometric_trend_v2.png")
    
    return age_totals, state_totals

# ============================================================
# DEMOGRAPHIC CHARTS
# ============================================================

def generate_demographic_charts(df, output_dir):
    """Generate all demographic charts"""
    print("\n📊 Generating Demographic Charts...")
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Age Group Chart
    age_totals = {'5-17 Years\n(Children & Teens)': df['demo_age_5_17'].sum(),
                  '17+ Years\n(Adults)': df['demo_age_17_'].sum()}
    
    fig, ax = plt.subplots(figsize=(10, 7))
    colors = [DEMO_COLORS['secondary'], DEMO_COLORS['primary']]
    bars = ax.bar(age_totals.keys(), age_totals.values(), color=colors, edgecolor='#333', linewidth=1.2, width=0.5)
    add_value_labels(ax, bars)
    
    total = sum(age_totals.values())
    for bar, val in zip(bars, age_totals.values()):
        pct = (val / total) * 100
        ax.annotate(f'({pct:.1f}%)', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2),
                   ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    
    ax.set_title('Demographic Update Distribution by Age Group\n(Address/Name/DOB Changes - Cleaned Dataset)', fontweight='bold', color='#1B4332')
    ax.set_ylabel('Total Demographic Updates')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', ha='right', fontsize=8, style='italic', color='#666')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/age_group_demographic_v2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ age_group_demographic_v2.png")
    
    # 2. State-wise Chart
    state_totals = df.groupby('state')['total'].sum().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    colors = plt.cm.Greens(np.linspace(0.8, 0.4, len(state_totals)))
    bars = ax.bar(range(len(state_totals)), state_totals.values, color=colors, edgecolor='#1B4332', linewidth=1.2)
    add_value_labels(ax, bars)
    ax.set_xticks(range(len(state_totals)))
    ax.set_xticklabels(state_totals.index, rotation=45, ha='right')
    ax.set_title('Top 10 States by Demographic Updates\n(Migration & Address Changes - Cleaned Dataset)', fontweight='bold', color='#1B4332')
    ax.set_ylabel('Total Demographic Updates')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', ha='right', fontsize=8, style='italic', color='#666')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/state_wise_demographic_v2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ state_wise_demographic_v2.png")
    
    # 3. Time Trend Chart
    df_copy = df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['date'], dayfirst=True)
    daily = df_copy.groupby('date')['total'].sum().reset_index().sort_values('date')
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.fill_between(daily['date'], daily['total'], alpha=0.3, color=DEMO_COLORS['primary'])
    ax.plot(daily['date'], daily['total'], color=DEMO_COLORS['primary'], linewidth=2, label='Daily Updates')
    if len(daily) > 7:
        daily['ma_7'] = daily['total'].rolling(7).mean()
        ax.plot(daily['date'], daily['ma_7'], color=DEMO_COLORS['accent'], linewidth=2.5, linestyle='--', label='7-Day MA')
    ax.set_title('Demographic Update Trend Over Time\n(Cleaned Dataset)', fontweight='bold', color='#1B4332')
    ax.set_ylabel('Daily Updates')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    ax.legend(loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45, ha='right')
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', ha='right', fontsize=8, style='italic', color='#666')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/demographic_trend_v2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ demographic_trend_v2.png")
    
    return age_totals, state_totals

# ============================================================
# CROSS-DATASET COMPARISON
# ============================================================

def generate_comparison_charts(enrol, bio, demo, output_dir):
    """Generate cross-dataset comparison charts"""
    print("\n📊 Generating Cross-Dataset Comparison Charts...")
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Age Group Comparison
    fig, ax = plt.subplots(figsize=(12, 7))
    
    categories = ['Enrolment\n(0-5)', 'Enrolment\n(5-17)', 'Enrolment\n(18+)', 
                  'Biometric\n(5-17)', 'Biometric\n(17+)',
                  'Demographic\n(5-17)', 'Demographic\n(17+)']
    
    values = [
        enrol['age_0_5'].sum(), enrol['age_5_17'].sum(), enrol['age_18_greater'].sum(),
        bio['bio_age_5_17'].sum(), bio['bio_age_17_'].sum(),
        demo['demo_age_5_17'].sum(), demo['demo_age_17_'].sum()
    ]
    
    colors = ['#2E86AB', '#2E86AB', '#2E86AB', '#A23B72', '#A23B72', '#2D6A4F', '#2D6A4F']
    alphas = [1.0, 0.7, 0.5, 0.8, 1.0, 0.6, 1.0]
    
    bars = ax.bar(categories, values, color=colors, edgecolor='white')
    for bar, alpha in zip(bars, alphas):
        bar.set_alpha(alpha)
    
    add_value_labels(ax, bars)
    ax.set_title('Age Group Distribution Across All Datasets\n(Cleaned Data Comparison)', fontweight='bold')
    ax.set_ylabel('Total Count')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    plt.xticks(rotation=45, ha='right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', ha='right', fontsize=8, style='italic', color='#666')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/age_comparison_all_datasets.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ age_comparison_all_datasets.png")
    
    # 2. State-wise Comparison (Top 5 states)
    enrol_states = enrol.groupby('state')['total'].sum().sort_values(ascending=False).head(5)
    bio_states = bio.groupby('state')['total'].sum()
    demo_states = demo.groupby('state')['total'].sum()
    
    states = enrol_states.index.tolist()
    
    fig, ax = plt.subplots(figsize=(14, 7))
    x = np.arange(len(states))
    width = 0.25
    
    bars1 = ax.bar(x - width, [enrol_states.get(s, 0) for s in states], width, label='Enrolment', color='#2E86AB')
    bars2 = ax.bar(x, [bio_states.get(s, 0) for s in states], width, label='Biometric', color='#A23B72')
    bars3 = ax.bar(x + width, [demo_states.get(s, 0) for s in states], width, label='Demographic', color='#2D6A4F')
    
    ax.set_xticks(x)
    ax.set_xticklabels(states, rotation=45, ha='right')
    ax.set_title('Top 5 States - Comparison Across All Updates\n(Cleaned Dataset)', fontweight='bold')
    ax.set_ylabel('Total Count')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', ha='right', fontsize=8, style='italic', color='#666')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/state_comparison_all_datasets.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ state_comparison_all_datasets.png")

# ============================================================
# ML MODELS
# ============================================================

def run_anomaly_detection(enrol, bio, demo, output_dir):
    """Run anomaly detection on all datasets"""
    print("\n🔍 Running Anomaly Detection...")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f'{output_dir}/anomaly_reports', exist_ok=True)
    
    results = {}
    
    for name, df in [('enrolment', enrol), ('biometric', bio), ('demographic', demo)]:
        df = df.copy()
        df['z_score'] = (df['total'] - df['total'].mean()) / df['total'].std()
        
        features = ['total', 'z_score']
        X = df[features].fillna(0)
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = IsolationForest(contamination=0.01, random_state=42, n_estimators=100)
        predictions = model.fit_predict(X_scaled)
        
        df['is_anomaly'] = (predictions == -1).astype(int)
        df['anomaly_score'] = -model.decision_function(X_scaled)
        
        n_anomalies = df['is_anomaly'].sum()
        results[name] = {'count': n_anomalies, 'rate': n_anomalies / len(df) * 100, 'df': df}
        
        # Save anomalies
        anomalies = df[df['is_anomaly'] == 1][['date', 'state', 'district', 'total', 'anomaly_score']]
        anomalies.to_csv(f'{output_dir}/anomaly_reports/{name}_anomalies_v2.csv', index=False)
        
        print(f"   ✅ {name}: {n_anomalies:,} anomalies ({n_anomalies/len(df)*100:.2f}%)")
    
    # Create anomaly visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    ax1 = axes[0, 0]
    counts = [results[k]['count'] for k in ['enrolment', 'biometric', 'demographic']]
    colors = ['#2E86AB', '#A23B72', '#2D6A4F']
    bars = ax1.bar(['Enrolment', 'Biometric', 'Demographic'], counts, color=colors)
    for bar in bars:
        ax1.annotate(f'{int(bar.get_height()):,}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 3), textcoords='offset points', ha='center', fontweight='bold')
    ax1.set_title('Anomalies Detected by Dataset', fontweight='bold')
    ax1.set_ylabel('Count')
    
    ax2 = axes[0, 1]
    rates = [results[k]['rate'] for k in ['enrolment', 'biometric', 'demographic']]
    bars = ax2.bar(['Enrolment', 'Biometric', 'Demographic'], rates, color=colors)
    for bar in bars:
        ax2.annotate(f'{bar.get_height():.2f}%', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 3), textcoords='offset points', ha='center', fontweight='bold')
    ax2.set_title('Anomaly Rate by Dataset (%)', fontweight='bold')
    ax2.set_ylabel('Rate (%)')
    
    ax3 = axes[1, 0]
    all_anomalies = pd.concat([results[k]['df'][results[k]['df']['is_anomaly'] == 1] for k in results])
    state_counts = all_anomalies.groupby('state').size().sort_values(ascending=True).tail(10)
    state_counts.plot(kind='barh', ax=ax3, color='#E63946')
    ax3.set_title('Top 10 States with Most Anomalies', fontweight='bold')
    ax3.set_xlabel('Count')
    
    ax4 = axes[1, 1]
    for name, color in zip(['enrolment', 'biometric', 'demographic'], colors):
        ax4.hist(results[name]['df']['anomaly_score'], bins=50, alpha=0.5, label=name.capitalize(), color=color)
    ax4.axvline(x=0, color='red', linestyle='--', linewidth=2)
    ax4.set_title('Anomaly Score Distribution', fontweight='bold')
    ax4.set_xlabel('Anomaly Score')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/anomaly_detection_v2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ anomaly_detection_v2.png")
    
    return results

def run_demand_forecasting(enrol, bio, demo, output_dir):
    """Run demand forecasting for all datasets"""
    print("\n🔮 Running Demand Forecasting...")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f'{output_dir}/predictions', exist_ok=True)
    
    forecasts = {}
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    colors = [('#2E86AB', '#F18F01'), ('#A23B72', '#F18F01'), ('#2D6A4F', '#E63946')]
    
    for idx, (name, df, ax, (color, fc_color)) in enumerate(zip(
        ['enrolment', 'biometric', 'demographic'],
        [enrol, bio, demo],
        axes,
        colors
    )):
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['date'], dayfirst=True)
        daily = df_copy.groupby('date')['total'].sum().reset_index().sort_values('date')
        daily.set_index('date', inplace=True)
        
        # Simple forecast
        recent_7 = daily['total'].tail(7).mean()
        recent_30 = daily['total'].tail(30).mean()
        base = 0.6 * recent_7 + 0.4 * recent_30
        
        forecast_dates = pd.date_range(start=daily.index.max() + pd.Timedelta(days=1), periods=30)
        forecast_values = [base * (1 + np.random.normal(0, 0.05)) for _ in range(30)]
        
        forecast_df = pd.DataFrame({'date': forecast_dates, 'forecast': forecast_values})
        forecast_df.to_csv(f'{output_dir}/predictions/{name}_forecast_v2.csv', index=False)
        forecasts[name] = forecast_df
        
        # Plot
        ax.plot(daily.index, daily['total'], color=color, linewidth=1.5, label='Historical')
        ax.plot(forecast_dates, forecast_values, color=fc_color, linewidth=2, linestyle='--', label='30-Day Forecast')
        ax.fill_between(forecast_dates, [v*0.8 for v in forecast_values], [v*1.2 for v in forecast_values], 
                       color=fc_color, alpha=0.2)
        ax.set_title(f'Aadhaar {name.capitalize()} - Demand Forecast', fontweight='bold')
        ax.set_ylabel('Daily Volume')
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
        ax.legend(loc='upper right')
        ax.text(0.02, 0.95, f'Predicted Avg: {np.mean(forecast_values)/100000:.2f}L/day', 
               transform=ax.transAxes, fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        print(f"   ✅ {name}: Forecast generated")
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/demand_forecast_v2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ demand_forecast_v2.png")
    
    return forecasts

# ============================================================
# MAIN
# ============================================================

def main():
    print("\n" + "="*70)
    print("🚀 MASTER ANALYSIS - REGENERATING ALL WITH CLEANED DATA")
    print("="*70)
    
    # Load data
    enrol, bio, demo = load_cleaned_data()
    
    # Generate charts
    generate_enrolment_charts(enrol, 'final_charts/enrolment')
    generate_biometric_charts(bio, 'final_charts/biometric')
    generate_demographic_charts(demo, 'final_charts/demographic')
    generate_comparison_charts(enrol, bio, demo, 'final_charts/comparison')
    
    # Run ML models
    run_anomaly_detection(enrol, bio, demo, 'final_charts/ml_models')
    run_demand_forecasting(enrol, bio, demo, 'final_charts/ml_models')
    
    print("\n" + "="*70)
    print("✅ ALL ANALYSIS COMPLETE!")
    print("="*70)
    print("\nOutput saved to: MY UPDATES/final_charts/")
    print("  📁 enrolment/     - 3 charts")
    print("  📁 biometric/     - 3 charts")
    print("  📁 demographic/   - 3 charts")
    print("  📁 comparison/    - 2 charts")
    print("  📁 ml_models/     - 2 charts + reports")
    print()

if __name__ == "__main__":
    main()
