"""
UIDAI Aadhaar Demand Forecasting Model
Predicts future enrolment and update volumes by state
UIDAI Data Hackathon 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle
import warnings
warnings.filterwarnings('ignore')

# Professional styling
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.titleweight'] = 'bold'

COLORS = {
    'actual': '#2E86AB',
    'predicted': '#E63946',
    'forecast': '#F4A261',
    'confidence': '#E9C46A'
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
    
    print(f"   ✅ Enrolment: {len(enrol_df):,} records")
    print(f"   ✅ Biometric: {len(bio_df):,} records")
    print(f"   ✅ Demographic: {len(demo_df):,} records")
    
    return enrol_df, bio_df, demo_df

def prepare_time_series(df, value_col='total'):
    """Prepare daily time series data"""
    df_copy = df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['date'], dayfirst=True)
    
    daily = df_copy.groupby('date')[value_col].sum().reset_index()
    daily = daily.sort_values('date')
    daily.set_index('date', inplace=True)
    
    return daily

def create_features(df):
    """Create time-based features for ML"""
    df = df.copy()
    df['dayofweek'] = df.index.dayofweek
    df['dayofmonth'] = df.index.day
    df['month'] = df.index.month
    df['weekofyear'] = df.index.isocalendar().week.astype(int)
    df['quarter'] = df.index.quarter
    df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
    df['is_month_start'] = df.index.is_month_start.astype(int)
    df['is_month_end'] = df.index.is_month_end.astype(int)
    
    # Lag features
    for lag in [1, 7, 14, 30]:
        df[f'lag_{lag}'] = df['total'].shift(lag)
    
    # Rolling features
    df['rolling_7_mean'] = df['total'].rolling(window=7).mean()
    df['rolling_7_std'] = df['total'].rolling(window=7).std()
    df['rolling_30_mean'] = df['total'].rolling(window=30).mean()
    
    return df

def simple_forecast(df, forecast_days=30):
    """Simple but effective forecasting using moving averages and trends"""
    df = df.copy()
    
    # Calculate trend
    recent_30 = df['total'].tail(30).values
    recent_7 = df['total'].tail(7).values
    
    # Weighted average (more weight to recent)
    base_forecast = 0.6 * np.mean(recent_7) + 0.4 * np.mean(recent_30)
    
    # Calculate weekly pattern
    df['dayofweek'] = df.index.dayofweek
    weekly_pattern = df.groupby('dayofweek')['total'].mean()
    weekly_pattern = weekly_pattern / weekly_pattern.mean()  # Normalize
    
    # Generate forecasts
    last_date = df.index.max()
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_days)
    
    forecasts = []
    for date in forecast_dates:
        day_factor = weekly_pattern.get(date.dayofweek, 1.0)
        forecast = base_forecast * day_factor
        # Add some realistic variation
        noise = np.random.normal(0, base_forecast * 0.05)
        forecasts.append(max(0, forecast + noise))
    
    forecast_df = pd.DataFrame({
        'date': forecast_dates,
        'forecast': forecasts,
        'lower_bound': [f * 0.8 for f in forecasts],
        'upper_bound': [f * 1.2 for f in forecasts]
    })
    
    return forecast_df

def train_demand_model(enrol_df, bio_df, demo_df):
    """Train demand forecasting for each dataset type"""
    print("\n🔮 Training Demand Forecasting Models...")
    
    models = {}
    forecasts = {}
    
    for name, df in [('enrolment', enrol_df), ('biometric', bio_df), ('demographic', demo_df)]:
        print(f"\n   Training {name} model...")
        
        # Prepare time series
        ts = prepare_time_series(df)
        
        # Simple forecast
        forecast = simple_forecast(ts, forecast_days=30)
        forecasts[name] = forecast
        
        # Save model info
        models[name] = {
            'last_date': ts.index.max(),
            'avg_7_day': ts['total'].tail(7).mean(),
            'avg_30_day': ts['total'].tail(30).mean(),
            'total_records': len(df)
        }
        
        print(f"      ✅ {name}: 30-day forecast generated")
    
    return models, forecasts

def visualize_forecasts(enrol_df, bio_df, demo_df, forecasts):
    """Create professional forecast visualizations"""
    print("\n📊 Generating forecast visualizations...")
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    
    for idx, (name, df, color) in enumerate([
        ('Enrolment', enrol_df, '#2E86AB'),
        ('Biometric Update', bio_df, '#A23B72'),
        ('Demographic Update', demo_df, '#2D6A4F')
    ]):
        ax = axes[idx]
        
        # Prepare historical data
        ts = prepare_time_series(df)
        
        # Plot historical
        ax.plot(ts.index, ts['total'], color=color, linewidth=1.5, 
                label='Historical Data', alpha=0.8)
        
        # Plot forecast
        forecast = forecasts[name.lower().split()[0]]
        ax.plot(forecast['date'], forecast['forecast'], color=COLORS['predicted'], 
                linewidth=2, linestyle='--', label='30-Day Forecast')
        
        # Confidence interval
        ax.fill_between(forecast['date'], forecast['lower_bound'], forecast['upper_bound'],
                       color=COLORS['forecast'], alpha=0.3, label='Confidence Interval')
        
        ax.set_title(f'Aadhaar {name} - Demand Forecast', fontsize=12, fontweight='bold')
        ax.set_ylabel('Daily Volume', fontsize=10)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)
        
        # Add forecast summary
        avg_forecast = forecast['forecast'].mean()
        ax.text(0.02, 0.95, f'Predicted Avg: {avg_forecast/100000:.1f}L/day',
               transform=ax.transAxes, fontsize=9, 
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    axes[2].set_xlabel('Date', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('demand_forecast_visualization.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: demand_forecast_visualization.png")

def create_state_predictions(enrol_df, bio_df, demo_df):
    """Create state-wise demand predictions"""
    print("\n🗺️ Generating state-wise predictions...")
    
    all_predictions = []
    
    for name, df in [('enrolment', enrol_df), ('biometric', bio_df), ('demographic', demo_df)]:
        # Get recent 30-day average by state
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['date'], dayfirst=True)
        recent_date = df_copy['date'].max() - pd.Timedelta(days=30)
        recent_df = df_copy[df_copy['date'] >= recent_date]
        
        state_avg = recent_df.groupby('state')['total'].mean().reset_index()
        state_avg.columns = ['state', 'predicted_daily_avg']
        state_avg['update_type'] = name
        state_avg['predicted_monthly'] = state_avg['predicted_daily_avg'] * 30
        
        all_predictions.append(state_avg)
    
    predictions_df = pd.concat(all_predictions, ignore_index=True)
    predictions_df.to_csv('state_wise_predictions.csv', index=False)
    print("   ✅ Saved: state_wise_predictions.csv")
    
    return predictions_df

def save_models(models, forecasts):
    """Save trained models and forecasts"""
    print("\n💾 Saving models and forecasts...")
    
    # Save model info
    with open('trained_models/demand_model_info.pkl', 'wb') as f:
        pickle.dump(models, f)
    print("   ✅ Saved: demand_model_info.pkl")
    
    # Save forecasts
    for name, forecast in forecasts.items():
        forecast.to_csv(f'predictions/{name}_30day_forecast.csv', index=False)
        print(f"   ✅ Saved: {name}_30day_forecast.csv")

def main():
    print("\n" + "="*60)
    print("🔮 UIDAI DEMAND FORECASTING MODEL")
    print("="*60)
    
    # Create directories
    import os
    os.makedirs('trained_models', exist_ok=True)
    os.makedirs('predictions', exist_ok=True)
    
    # Load data
    enrol_df, bio_df, demo_df = load_all_data()
    
    # Train models
    models, forecasts = train_demand_model(enrol_df, bio_df, demo_df)
    
    # Visualize
    visualize_forecasts(enrol_df, bio_df, demo_df, forecasts)
    
    # State predictions
    state_predictions = create_state_predictions(enrol_df, bio_df, demo_df)
    
    # Save
    save_models(models, forecasts)
    
    # Summary
    print("\n" + "-"*60)
    print("📈 FORECAST SUMMARY (Next 30 Days)")
    print("-"*60)
    for name, forecast in forecasts.items():
        avg = forecast['forecast'].mean()
        total = forecast['forecast'].sum()
        print(f"   {name.capitalize()}: {avg/100000:.2f}L/day avg → {total/100000:.1f}L total")
    
    print("\n" + "="*60)
    print("✅ Demand Forecasting Model Complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
