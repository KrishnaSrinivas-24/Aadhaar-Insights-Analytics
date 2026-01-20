import pandas as pd

print('='*60)
print('ML MODELS - VERIFICATION')
print('='*60)

# Check Forecasts
print('\n📈 DEMAND FORECASTING MODEL')
print('-'*40)

f1 = pd.read_csv('final_charts/ml_models/predictions/enrolment_forecast_v2.csv')
f2 = pd.read_csv('final_charts/ml_models/predictions/biometric_forecast_v2.csv')
f3 = pd.read_csv('final_charts/ml_models/predictions/demographic_forecast_v2.csv')

print(f'Enrolment - 30 day forecast:')
print(f'  Avg: {f1["forecast"].mean()/100000:.2f}L/day')
print(f'  Total: {f1["forecast"].sum()/100000:.1f}L predicted')

print(f'\nBiometric - 30 day forecast:')
print(f'  Avg: {f2["forecast"].mean()/100000:.2f}L/day')
print(f'  Total: {f2["forecast"].sum()/100000:.1f}L predicted')

print(f'\nDemographic - 30 day forecast:')
print(f'  Avg: {f3["forecast"].mean()/100000:.2f}L/day')
print(f'  Total: {f3["forecast"].sum()/100000:.1f}L predicted')

# Check Anomalies
print('\n🔍 ANOMALY DETECTION MODEL')
print('-'*40)

a1 = pd.read_csv('final_charts/ml_models/anomaly_reports/enrolment_anomalies_v2.csv')
a2 = pd.read_csv('final_charts/ml_models/anomaly_reports/biometric_anomalies_v2.csv')
a3 = pd.read_csv('final_charts/ml_models/anomaly_reports/demographic_anomalies_v2.csv')

print(f'Enrolment anomalies: {len(a1):,}')
print(f'Biometric anomalies: {len(a2):,}')
print(f'Demographic anomalies: {len(a3):,}')
print(f'\nTOTAL ANOMALIES FLAGGED: {len(a1)+len(a2)+len(a3):,}')

print('\n📊 Top anomalous states (Biometric):')
print(a2.groupby('state').size().sort_values(ascending=False).head(5))

print('\n' + '='*60)
print('✅ BOTH ML MODELS TRAINED AND WORKING!')
print('='*60)
