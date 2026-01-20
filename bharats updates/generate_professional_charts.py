"""
Professional Chart Generator for Aadhaar Enrolment Analysis
UIDAI Data Hackathon 2026
Author: Team - Bharat's Analysis (Enhanced by Antigravity)
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
    'light': '#BEE9E8',        # Light Cyan
    'gradient': ['#2E86AB', '#5AA9E6', '#7FC8F8', '#F9F9F9']
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
                    fontsize=9, fontweight='bold',
                    color='#333333')

def create_state_wise_chart(df):
    """Create professional state-wise enrolment chart"""
    # Calculate total enrolments per state
    state_enrolment = df.groupby('state')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
    state_enrolment['total'] = state_enrolment.sum(axis=1)
    state_enrolment = state_enrolment.sort_values('total', ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Create gradient-like effect with slightly different shades
    colors = plt.cm.Blues(np.linspace(0.8, 0.4, len(state_enrolment)))
    
    bars = ax.bar(range(len(state_enrolment)), state_enrolment['total'], 
                  color=colors, edgecolor='#1B4965', linewidth=1.2)
    
    # Add value labels
    add_value_labels(ax, bars)
    
    # Styling
    ax.set_xlabel('State', fontsize=12, fontweight='bold', color='#333333')
    ax.set_ylabel('Total Enrolments', fontsize=12, fontweight='bold', color='#333333')
    ax.set_title('Top 10 States by Aadhaar Enrolment\n(Based on Anonymised Dataset)', 
                 fontsize=14, fontweight='bold', color='#1B4965', pad=20)
    
    ax.set_xticks(range(len(state_enrolment)))
    ax.set_xticklabels(state_enrolment.index, rotation=45, ha='right', fontsize=10)
    
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
    plt.savefig('state_wise_enrolment_professional.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Generated: state_wise_enrolment_professional.png")

def create_age_group_chart(df):
    """Create professional age group enrolment chart"""
    # Calculate totals by age group
    age_totals = {
        '0-5 Years\n(Infants & Toddlers)': df['age_0_5'].sum(),
        '5-17 Years\n(Children & Teens)': df['age_5_17'].sum(),
        '18+ Years\n(Adults)': df['age_18_greater'].sum()
    }
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent']]
    
    bars = ax.bar(age_totals.keys(), age_totals.values(), color=colors, 
                  edgecolor='#333333', linewidth=1.2)
    
    # Add value labels
    add_value_labels(ax, bars)
    
    # Add percentage labels
    total = sum(age_totals.values())
    for i, (bar, val) in enumerate(zip(bars, age_totals.values())):
        percentage = (val / total) * 100
        ax.annotate(f'({percentage:.1f}%)',
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2),
                    ha='center', va='center',
                    fontsize=11, fontweight='bold',
                    color='white')
    
    # Styling
    ax.set_xlabel('Age Group', fontsize=12, fontweight='bold', color='#333333')
    ax.set_ylabel('Total Enrolments', fontsize=12, fontweight='bold', color='#333333')
    ax.set_title('Aadhaar Enrolment Distribution by Age Group\n(Dominance of Early-Age Registration)', 
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
    insight_text = "Key Insight: 0-5 age group shows\nhighest enrolments, indicating\nstrong early-age registration focus"
    props = dict(boxstyle='round,pad=0.5', facecolor='#E8F4F8', edgecolor='#2E86AB', alpha=0.9)
    ax.text(0.98, 0.98, insight_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right', bbox=props)
    
    # Add source note
    fig.text(0.99, 0.01, 'Source: UIDAI Anonymised Dataset | UIDAI Hackathon 2026', 
             ha='right', va='bottom', fontsize=8, color='#666666', style='italic')
    
    plt.tight_layout()
    plt.savefig('age_group_enrolment_professional.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Generated: age_group_enrolment_professional.png")

def create_time_trend_chart(df):
    """Create professional time trend chart"""
    # Convert date and aggregate
    df_copy = df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['date'], dayfirst=True)
    df_copy['total'] = df_copy['age_0_5'] + df_copy['age_5_17'] + df_copy['age_18_greater']
    
    daily_enrolment = df_copy.groupby('date')['total'].sum().reset_index()
    daily_enrolment = daily_enrolment.sort_values('date')
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot line with area fill
    ax.fill_between(daily_enrolment['date'], daily_enrolment['total'], 
                    alpha=0.3, color=COLORS['primary'])
    ax.plot(daily_enrolment['date'], daily_enrolment['total'], 
            color=COLORS['primary'], linewidth=2, marker='', label='Daily Enrolments')
    
    # Add moving average
    if len(daily_enrolment) > 7:
        daily_enrolment['ma_7'] = daily_enrolment['total'].rolling(window=7).mean()
        ax.plot(daily_enrolment['date'], daily_enrolment['ma_7'], 
                color=COLORS['accent'], linewidth=2.5, linestyle='--', 
                label='7-Day Moving Average')
    
    # Mark peak
    peak_idx = daily_enrolment['total'].idxmax()
    peak_date = daily_enrolment.loc[peak_idx, 'date']
    peak_value = daily_enrolment.loc[peak_idx, 'total']
    ax.annotate(f'Peak: {peak_value/100000:.1f}L',
                xy=(peak_date, peak_value),
                xytext=(10, 20), textcoords='offset points',
                fontsize=9, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['secondary']),
                color=COLORS['secondary'])
    ax.scatter([peak_date], [peak_value], color=COLORS['secondary'], s=100, zorder=5)
    
    # Styling
    ax.set_xlabel('Date', fontsize=12, fontweight='bold', color='#333333')
    ax.set_ylabel('Total Enrolments', fontsize=12, fontweight='bold', color='#333333')
    ax.set_title('Aadhaar Enrolment Trend Over Time\n(Periodic Fluctuations Indicate Enrolment Drives)', 
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
    plt.savefig('enrolment_trend_professional.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Generated: enrolment_trend_professional.png")

def main():
    print("\n" + "="*60)
    print("🎨 UIDAI Aadhaar Enrolment - Professional Chart Generator")
    print("="*60 + "\n")
    
    # Load data
    print("📂 Loading cleaned dataset...")
    df = pd.read_csv('aadhaar_enrolment_cleaned.csv')
    print(f"   ✅ Loaded {len(df):,} records\n")
    
    # Generate charts
    print("📊 Generating professional charts...\n")
    
    create_state_wise_chart(df)
    create_age_group_chart(df)
    create_time_trend_chart(df)
    
    print("\n" + "="*60)
    print("✅ All professional charts generated successfully!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
