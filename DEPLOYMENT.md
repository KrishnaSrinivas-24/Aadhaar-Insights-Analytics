# 🚀 How to Run This Project

## Local Setup

### Prerequisites
- Python 3.10+
- pip
- ~2GB disk space

### Installation Steps

```bash
# 1. Clone the repo
git clone https://github.com/KrishnaSrinivas-24/Aadhaar-Insights-Analytics.git
cd Aadhaar-Insights-Analytics/MY\ UPDATES

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
streamlit run dashboard.py
```

The app will open at `http://localhost:8501`

---

## Deploy to Hugging Face Spaces (Easy!)

1. Go to https://huggingface.co/spaces
2. Create new Space (select Streamlit)
3. Clone it: `git clone https://huggingface.co/spaces/YOUR-USERNAME/your-space-name`
4. Copy files from `MY UPDATES/` folder
5. Push: `git add . && git commit -m "Initial" && git push`

Done! Your app is live 🎉

---

## Generate Reports

```bash
python generate_report.py
# Creates PDF reports with all charts
```

---

*For more details, see README.md*
