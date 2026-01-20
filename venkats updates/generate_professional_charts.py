"""
Professional Chart Generator for Aadhaar Biometric Update Analysis
UIDAI Data Hackathon 2026
Author: Team - Venkat's Analysis (Enhanced by Antigravity)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Set professional styling
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'

# Professional color palette
COLORS = {
    'primary': '#2E86AB',      # Blue
    'secondary': '#A23B72',    # Purple
    'accent': '#F18F01',       # Orange
    'success': '#28A745',      # Green
    'dark': '#1B4965',         # Dark Blue
    'warning': '#DC3545',      # Red
    'light': '#BEE9E8',        # Light Cyan
}

def format_lakhs(x, pos):
    """Format numbers in Lakhs for Indian context"""
    if x >= 100000:
        return f'{x/100000:.1f}L'
    elif x >= 1000:
        return f'{x/1000:.0f}K'
    return f'{x:.0f}'

def add_value_labels(ax, bars, format_func=None):
    """Add value labels on top of bars"""
    for bar in bars:
        height = bar.get_height()
        if format_func:
            label = format_func(height)
        else:
            label = f'{height/100000:.1f}L' if height >= 100000 else f'{height/1000:.0f}K'
        ax.annotate(label,
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold',
                    color='#333333')

def create_age_group_chart(df):
    """Create professional age group vs biometric updates chart"""
    # Calculate totals by age group
    age_totals = {
        '5-17 Years\n(Children & Teens)': df['bio_age_5_17'].sum(),
        '17+ Years\n(Adults & Elderly)': df['bio_age_17_'].sum()
    }
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    colors = [COLORS['secondary'], COLORS['primary']]
    
    bars = ax.bar(age_totals.keys(), age_totals.values(), color=colors, 
                  edgecolor='#333333', linewidth=1.2, width=0.5)
    
    # Add value labels
    add_value_labels(ax, bars)
    
    # Add percentage labels
    total = sum(age_totals.values())
    for i, (bar, val) in enumerate(zip(bars, age_totals.values())):
        percentage = (val / total) * 100
        ax.annotate(f'({percentage:.1f}%)',
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2),
                    ha='center', va='center',
                    fontsize=12, fontweight='bold',
                    color='white')
    
    # Styling
    ax.set_xlabel('Age Group', fontsize=12, fontweight='bold', color='#333333')
    ax.set_ylabel('Total Biometric Updates', fontsize=12, fontweight='bold', color='#333333')
    ax.set_title('Biometric Update Distribution by Age Group\n(Higher Updates in Adult Population)', 
                 fontsize=14, fontweight='bold', color='#1B4965', pad=20)
    
    # Format Y-axis
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    
    # Add subtle grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add insight box
    insight_text = "Key Insight: 17+ age group dominates\nbiometric updates, suggesting age-related\nbiometric changes in adult population"
    props = dict(boxstyle='round,pad=0.5', facecolor='#E8F4F8', edgecolor='#2E86AB', alpha=0.9)
    ax.text(0.98, 0.98, insight_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right', bbox=props)
    
    # Add source note
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', 
             ha='right', va='bottom', fontsize=8, color='#666666', style='italic')
    
    plt.tight_layout()
    plt.savefig('age_group_biometric_professional.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Generated: age_group_biometric_professional.png")

def create_state_wise_chart(df):
    """Create professional state-wise biometric update chart"""
    # Calculate total updates per state
    df['total_updates'] = df['bio_age_5_17'] + df['bio_age_17_']
    state_updates = df.groupby('state')['total_updates'].sum().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Create gradient-like effect with slightly different shades
    colors = plt.cm.Purples(np.linspace(0.8, 0.4, len(state_updates)))
    
    bars = ax.bar(range(len(state_updates)), state_updates.values, 
                  color=colors, edgecolor='#1B4965', linewidth=1.2)
    
    # Add value labels
    add_value_labels(ax, bars)
    
    # Styling
    ax.set_xlabel('State', fontsize=12, fontweight='bold', color='#333333')
    ax.set_ylabel('Total Biometric Updates', fontsize=12, fontweight='bold', color='#333333')
    ax.set_title('Top 10 States by Biometric Update Frequency\n(Regional Disparities in Update Patterns)', 
                 fontsize=14, fontweight='bold', color='#1B4965', pad=20)
    
    ax.set_xticks(range(len(state_updates)))
    ax.set_xticklabels(state_updates.index, rotation=45, ha='right', fontsize=10)
    
    # Format Y-axis
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    
    # Add subtle grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add source note
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', 
             ha='right', va='bottom', fontsize=8, color='#666666', style='italic')
    
    plt.tight_layout()
    plt.savefig('state_wise_biometric_professional.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Generated: state_wise_biometric_professional.png")
    
    return state_updates

def create_anomaly_chart(df):
    """Create professional anomaly detection chart"""
    df['total_updates'] = df['bio_age_5_17'] + df['bio_age_17_']
    
    mean = df['total_updates'].mean()
    std = df['total_updates'].std()
    threshold = mean + 3*std
    
    # Count anomalies
    anomaly_count = len(df[df['total_updates'] > threshold])
    normal_count = len(df[df['total_updates'] <= threshold])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create histogram with custom colors
    n, bins, patches = ax.hist(df['total_updates'], bins=50, color=COLORS['primary'], 
                                edgecolor='white', alpha=0.7, label='Normal Updates')
    
    # Color the anomaly bins differently
    for i, (patch, right_edge) in enumerate(zip(patches, bins[1:])):
        if right_edge > threshold:
            patch.set_facecolor(COLORS['warning'])
            patch.set_alpha(0.8)
    
    # Add threshold line
    ax.axvline(threshold, color=COLORS['warning'], linewidth=2.5, linestyle='--', 
               label=f'Anomaly Threshold (μ + 3σ = {threshold:.0f})')
    
    # Add mean line
    ax.axvline(mean, color=COLORS['success'], linewidth=2, linestyle='-', 
               label=f'Mean = {mean:.1f}')
    
    # Styling
    ax.set_xlabel('Total Updates per Record', fontsize=12, fontweight='bold', color='#333333')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold', color='#333333')
    ax.set_title('Anomaly Detection in Biometric Update Patterns\n(Identifying Unusual Spikes and Inefficiencies)', 
                 fontsize=14, fontweight='bold', color='#1B4965', pad=20)
    
    # Format axes
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x/1000:.0f}K' if x >= 1000 else f'{x:.0f}'))
    
    # Add legend
    ax.legend(loc='upper right', framealpha=0.9, fontsize=9)
    
    # Add subtle grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add stats box
    stats_text = f"Anomalies Detected: {anomaly_count:,}\nNormal Records: {normal_count:,}\nAnomaly Rate: {(anomaly_count/len(df))*100:.2f}%"
    props = dict(boxstyle='round,pad=0.5', facecolor='#FFE5E5', edgecolor=COLORS['warning'], alpha=0.9)
    ax.text(0.98, 0.75, stats_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right', bbox=props)
    
    # Add source note
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', 
             ha='right', va='bottom', fontsize=8, color='#666666', style='italic')
    
    plt.tight_layout()
    plt.savefig('anomaly_detection_professional.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Generated: anomaly_detection_professional.png")
    
    return anomaly_count, normal_count, mean, std, threshold

def create_time_trend_chart(df):
    """Create time-based biometric update trend chart"""
    df_copy = df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['date'], dayfirst=True)
    df_copy['total_updates'] = df_copy['bio_age_5_17'] + df_copy['bio_age_17_']
    
    daily_updates = df_copy.groupby('date')['total_updates'].sum().reset_index()
    daily_updates = daily_updates.sort_values('date')
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot line with area fill
    ax.fill_between(daily_updates['date'], daily_updates['total_updates'], 
                    alpha=0.3, color=COLORS['secondary'])
    ax.plot(daily_updates['date'], daily_updates['total_updates'], 
            color=COLORS['secondary'], linewidth=2, marker='', label='Daily Updates')
    
    # Add moving average
    if len(daily_updates) > 7:
        daily_updates['ma_7'] = daily_updates['total_updates'].rolling(window=7).mean()
        ax.plot(daily_updates['date'], daily_updates['ma_7'], 
                color=COLORS['accent'], linewidth=2.5, linestyle='--', 
                label='7-Day Moving Average')
    
    # Mark peak
    peak_idx = daily_updates['total_updates'].idxmax()
    peak_date = daily_updates.loc[peak_idx, 'date']
    peak_value = daily_updates.loc[peak_idx, 'total_updates']
    ax.annotate(f'Peak: {peak_value/100000:.1f}L',
                xy=(peak_date, peak_value),
                xytext=(10, 20), textcoords='offset points',
                fontsize=9, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['dark']),
                color=COLORS['dark'])
    ax.scatter([peak_date], [peak_value], color=COLORS['dark'], s=100, zorder=5)
    
    # Styling
    ax.set_xlabel('Date', fontsize=12, fontweight='bold', color='#333333')
    ax.set_ylabel('Total Biometric Updates', fontsize=12, fontweight='bold', color='#333333')
    ax.set_title('Biometric Update Trend Over Time\n(Identifying Spike Patterns and Infrastructure Load)', 
                 fontsize=14, fontweight='bold', color='#1B4965', pad=20)
    
    # Format Y-axis
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
    
    # Format X-axis
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    plt.xticks(rotation=45, ha='right')
    
    # Add legend
    ax.legend(loc='upper right', framealpha=0.9)
    
    # Add subtle grid
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add source note
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', 
             ha='right', va='bottom', fontsize=8, color='#666666', style='italic')
    
    plt.tight_layout()
    plt.savefig('biometric_trend_professional.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Generated: biometric_trend_professional.png")

def main():
    print("\n" + "="*60)
    print("🎨 UIDAI Biometric Update - Professional Chart Generator")
    print("="*60 + "\n")
    
    # Load data
    print("📂 Loading cleaned dataset...")
    df = pd.read_csv('../../Venkat/clean_aadhaar_biometric.csv')
    print(f"   ✅ Loaded {len(df):,} records\n")
    
    # Generate charts
    print("📊 Generating professional charts...\n")
    
    create_age_group_chart(df)
    state_updates = create_state_wise_chart(df)
    anomaly_count, normal_count, mean, std, threshold = create_anomaly_chart(df)
    create_time_trend_chart(df)
    
    # Print summary stats
    print("\n" + "-"*60)
    print("📈 ANALYSIS SUMMARY")
    print("-"*60)
    print(f"   Total Records: {len(df):,}")
    print(f"   Top State: {state_updates.index[0]} ({state_updates.values[0]/100000:.1f}L updates)")
    print(f"   Mean Updates/Record: {mean:.2f}")
    print(f"   Anomaly Threshold: {threshold:.0f}")
    print(f"   Anomalies Detected: {anomaly_count:,} ({(anomaly_count/len(df))*100:.2f}%)")
    
    print("\n" + "="*60)
    print("✅ All professional charts generated successfully!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
