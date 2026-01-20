from fpdf import FPDF
import os

class AadhaarReport(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'B', 10)
            self.cell(0, 10, 'UIDAI Data Hackathon 2026 - Final Submission Report', 0, 1, 'R')
            self.line(10, 18, 200, 18)
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | UIDAI Data Hackathon 2026', 0, 0, 'C')

def clean(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

def create_report():
    pdf = AadhaarReport()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # --- 1. TITLE PAGE ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.ln(20)
    pdf.cell(0, 10, '='*60, 0, 1, 'C')
    pdf.set_font('Helvetica', 'B', 22)
    pdf.cell(0, 15, 'UIDAI DATA HACKATHON 2026', 0, 1, 'C')
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, 'FINAL SUBMISSION REPORT', 0, 1, 'C')
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, '='*60, 0, 1, 'C')
    
    pdf.ln(15)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'HIDDEN INEFFICIENCIES AND SOCIETAL SIGNALS', 0, 1, 'C')
    pdf.cell(0, 10, 'IN AADHAAR ENROLMENT AND UPDATE PATTERNS', 0, 1, 'C')
    pdf.cell(0, 10, 'ACROSS INDIA', 0, 1, 'C')
    
    pdf.ln(25)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'TEAM DETAILS', 0, 1, 'C')
    pdf.cell(0, 5, '-'*20, 0, 1, 'C')
    pdf.ln(5)
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 8, 'Team Lead: Krishna', 0, 1, 'C')
    pdf.ln(3)
    pdf.cell(0, 8, 'Members:', 0, 1, 'C')
    pdf.cell(0, 8, ' Bharat (Enrolment Data Analyst)', 0, 1, 'C')
    pdf.cell(0, 8, ' Venkat (Biometric Update Data Analyst)', 0, 1, 'C')
    pdf.cell(0, 8, ' Yashwanth (Visualization and Design)', 0, 1, 'C')
    pdf.cell(0, 8, ' Saravana (Interpretation and Policy Insights)', 0, 1, 'C')
    
    pdf.ln(20)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 10, 'Date: January 20, 2026', 0, 1, 'C')
    
    # --- 2. EXECUTIVE SUMMARY ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'SECTION 1: EXECUTIVE SUMMARY', 0, 1, 'L')
    pdf.ln(5)
    pdf.set_font('Helvetica', '', 11)
    summary_text = (
        "This report presents a comprehensive data-driven analysis of Aadhaar enrolment "
        "and update patterns across India, utilizing all three anonymized datasets "
        "provided by UIDAI: Enrolment, Biometric Update, and Demographic Update. "
        "\n\nKEY DISCOVERIES:\n"
        "- Age Group Dynamics: Enrolment is 65% children (0-5), while Demographic updates are 90% adults.\n"
        "- Geographic Patterns: UP leads nationwide; Maharashtra shows high biometric update per capita.\n"
        "- Migration Signals: UP/Bihar identified as major source states; Maharashtra/Gujarat as destinations.\n"
        "- Machine Learning: 30-day demand forecast at ~0.8L-2.8L/day; 43k+ anomalies flagged for audit."
    )
    pdf.multi_cell(0, 7, clean(summary_text))
    
    # Dashboard Visual - Home
    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Dashboard Visualization: Home Overview', 0, 1, 'L')
    if os.path.exists('pdf_screenshots/home_tab.png'):
        pdf.image('pdf_screenshots/home_tab.png', x=10, w=190)
    
    # --- 3. PROBLEM STATEMENT & APPROACH ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'SECTION 2: PROBLEM STATEMENT and APPROACH', 0, 1, 'L')
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Problem Statement:', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 7, clean("Unlocking Societal Trends in Aadhaar Enrolment and Updates. Identify meaningful patterns, trends, anomalies, or predictive indicators to support informed decision-making and system improvements."))
    
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Our Methodology:', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 7, clean("1. Exploratory Data Analysis (EDA)\n2. Pattern Identification and Demographic Segmentation\n3. Anomaly Detection (ML Isolation Forest)\n4. Predictive Modeling (Time Series Forecasting)\n5. Cross-Dataset Migration Tracking"))

    # --- 4. DATA ANALYSIS & VISUALS ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'SECTION 5: DATA ANALYSIS and VISUALIZATIONS', 0, 1, 'L')
    pdf.ln(5)
    
    # Enrolment
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '5.1 Aadhaar Enrolment Analysis', 0, 1, 'L')
    if os.path.exists('pdf_screenshots/enrolment_tab.png'):
        pdf.image('pdf_screenshots/enrolment_tab.png', x=10, w=190)
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 6, clean("Insight: New enrolments are dominated by infants (65%), indicating successful integration with birth registration systems. Top states: UP, Bihar, MP."))
    
    # Biometric
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '5.2 Aadhaar Biometric Update Analysis', 0, 1, 'L')
    if os.path.exists('pdf_screenshots/biometric_tab.png'):
        pdf.image('pdf_screenshots/biometric_tab.png', x=10, w=190)
    pdf.multi_cell(0, 6, clean("Insight: Biometric updates are nearly equal across children (49%) and adults (51%). Maharashtra shows higher per-capita update needs vs enrolment."))

    # Demographic/Migration
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '5.3 Aadhaar Demographic Update/Migration Analysis', 0, 1, 'L')
    if os.path.exists('pdf_screenshots/demographic_tab.png'):
        pdf.image('pdf_screenshots/demographic_tab.png', x=10, w=190)
    pdf.multi_cell(0, 6, clean("Insight: Demographic updates are 90% adult-driven, reflecting migration. UP/Bihar serve as source states while Maharashtra/Gujarat act as destination hubs."))

    # --- 5. MACHINE LEARNING ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'SECTION 6: MACHINE LEARNING MODELS', 0, 1, 'L')
    pdf.ln(5)
    
    # Forecasting
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '6.1 Demand Forecasting (Next 30 Days)', 0, 1, 'L')
    if os.path.exists('pdf_screenshots/forecast_tab.png'):
        pdf.image('pdf_screenshots/forecast_tab.png', x=10, w=190)
    pdf.multi_cell(0, 6, clean("Model: Weighted Moving Average with Weekly Seasonality. Predicts ~5.5L total daily transactions nationwide."))
    
    # Anomalies
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '6.2 Anomaly and Fraud Detection', 0, 1, 'L')
    if os.path.exists('pdf_screenshots/anomalies_tab.png'):
        pdf.image('pdf_screenshots/anomalies_tab.png', x=10, w=190)
    pdf.multi_cell(0, 6, clean("Model: Isolation Forest flagged 43,615 records (top 1%) for potential audit based on high-frequency transactions and geographic outliers."))

    # --- 6. STRATEGIC INSIGHTS ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'SECTION 7: STRATEGIC POLICY INSIGHTS', 0, 1, 'L')
    pdf.ln(5)
    
    insights = [
        ("Infrastructure Realignment", "Shift to 'Maintenance' phase. Decouple infant enrolments from rapid updates to reduce wait times by 40%."),
        ("Predictive Resource Allocation", "Spikes at ages 5/17 are mandatory. Deploy mobile units to schools during peak admission seasons."),
        ("High-Frequency Anomaly Prevention", "Implement real-time automated velocity checks to block suspicious transactions (>3 updates/year)."),
        ("Seasonal Load Management", "Proactive IT bandwidth scaling during Q3 (September peaks).")
    ]
    
    for title, desc in insights:
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 10, f'- {clean(title)}', 0, 1, 'L')
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 7, clean(desc))
        pdf.ln(4)

    # --- 7. RECOMMENDATIONS ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'SECTION 8: RECOMMENDATIONS FOR UIDAI', 0, 1, 'L')
    pdf.ln(5)
    if os.path.exists('pdf_screenshots/recommendations_tab.png'):
        pdf.image('pdf_screenshots/recommendations_tab.png', x=10, w=190)
    pdf.ln(5)
    if os.path.exists('pdf_screenshots/recommendations_tab_2.png'):
        pdf.image('pdf_screenshots/recommendations_tab_2.png', x=10, w=190)

    # --- 8. CONCLUSION ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'SECTION 9: CONCLUSION', 0, 1, 'L')
    pdf.ln(5)
    pdf.set_font('Helvetica', '', 11)
    conclusion_text = (
        "This submission demonstrates how anonymized Aadhaar datasets can be transformed into a powerful governance tool. "
        "By aligning infrastructure with demographic realities and leveraging predictive ML models, UIDAI can achieve "
        "unprecedented service efficiency and security.\n\n"
        "We believe this work serves as a blueprint for data-driven, proactive governance in India."
    )
    pdf.multi_cell(0, 7, clean(conclusion_text))
    
    pdf.ln(20)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'GitHub: https://github.com/KrishnaSrinivas-24/Aadhaar-Insights-Analytics', 0, 1, 'L')
    
    pdf.output("UIDAI_Hackathon_Final_Submission.pdf")
    print("PDF Report generated successfully: UIDAI_Hackathon_Final_Submission.pdf")

if __name__ == '__main__':
    create_report()
