# 🤝 Contributing to Aadhaar Insights Analytics

Thank you for your interest in contributing to this project! This guide will help you get started.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Questions?](#questions)

---

## 🤝 Code of Conduct

We're committed to providing a welcoming and inclusive environment. Please:
- Be respectful and professional
- Provide constructive feedback
- Focus on the code, not the person
- Follow Python's Zen philosophy

---

## 🚀 Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/KrishnaSrinivas-24/Aadhaar-Insights-Analytics.git
cd Aadhaar-Insights-Analytics/MY\ UPDATES
```

### 2. Set Up Development Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pytest black flake8  # Development tools
```

### 3. Verify Installation
```bash
streamlit run dashboard.py
```

---

## 🔄 Development Workflow

### Branch Naming Convention
```
feature/description        → New features
bugfix/description         → Bug fixes
docs/description          → Documentation updates
refactor/description      → Code refactoring
```

### Example:
```bash
git checkout -b feature/add-export-csv
```

### Commit Messages
Follow the conventional commit format:
```
type(scope): short description

Longer description if needed. Explain the "why" not the "what".

- Point 1
- Point 2
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Example:**
```
feat(ml_models): add time-series validation method

Implement cross-validation for demand forecasting model
to improve reliability of 30-day predictions.

- Add fold validation logic
- Update test suite
- Document in README
```

---

## 📐 Code Standards

### Python Style Guide
- Follow **PEP 8** using `black` formatter
- Maximum line length: **100 characters**
- Use descriptive variable names
- Add docstrings to all functions

### Format Code
```bash
black *.py
flake8 --max-line-length=100 *.py
```

### Example Function:
```python
def forecast_demand(historical_data: pd.DataFrame, 
                   days_ahead: int = 30) -> pd.DataFrame:
    """
    Forecast future demand using weighted moving average.
    
    Args:
        historical_data: DataFrame with historical patterns
        days_ahead: Number of days to forecast (default: 30)
    
    Returns:
        DataFrame with forecast and confidence intervals
    
    Raises:
        ValueError: If days_ahead is negative
    """
    if days_ahead < 0:
        raise ValueError("days_ahead must be positive")
    
    # Implementation...
    return forecast_df
```

### File Organization
```python
# 1. Imports (stdlib, third-party, local)
import os
import pandas as pd
from sklearn.ensemble import IsolationForest

# 2. Constants
MIN_RECORDS = 100
DEFAULT_THRESHOLD = 0.95

# 3. Functions/Classes
def process_data(df):
    pass

# 4. Main execution
if __name__ == "__main__":
    pass
```

---

## 🧪 Testing

### Run Tests
```bash
pytest tests/
pytest --cov=.  # With coverage
```

### Add Tests
Create tests in `tests/` directory:
```python
import pytest
from ml_models.demand_forecaster import forecast_demand

def test_forecast_returns_dataframe():
    historical = pd.DataFrame({...})
    result = forecast_demand(historical)
    assert isinstance(result, pd.DataFrame)

def test_forecast_length():
    historical = pd.DataFrame({...})
    result = forecast_demand(historical, days_ahead=30)
    assert len(result) == 30
```

---

## 📤 Submitting Changes

### 1. Create Pull Request
```bash
git push origin feature/your-feature
```

### 2. PR Description Template
```markdown
## Description
Brief explanation of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] Added/updated tests
- [ ] Dashboard still loads

## Checklist
- [ ] Code follows PEP 8
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Performance verified
```

### 3. Code Review Process
- Maintainers will review your code
- Request changes if needed
- Merge after approval

---

## 📝 Documentation Guidelines

### For Code
- Use clear, descriptive variable names
- Add docstrings to all public functions
- Explain complex logic with comments

### For Files
- Update README.md if changing features
- Document new parameters in DETAILED_SUBMISSION_GUIDE.md
- Add usage examples

### Example:
```python
def detect_anomalies(df: pd.DataFrame, threshold: float = 0.95) -> pd.DataFrame:
    """
    Detect anomalous records using Isolation Forest.
    
    This function identifies records that significantly deviate
    from normal patterns using the Isolation Forest algorithm.
    
    Parameters:
        df: Input dataset with numeric features
        threshold: Contamination factor (0-1)
    
    Returns:
        DataFrame with anomaly flags (-1 = anomaly, 1 = normal)
    
    Example:
        >>> df = pd.read_csv('data.csv')
        >>> anomalies = detect_anomalies(df, threshold=0.99)
        >>> print(f"Found {(anomalies == -1).sum()} anomalies")
    """
```

---

## 🔍 Areas for Contribution

### High Priority
- [ ] Unit tests for ML models
- [ ] Performance optimization for large datasets
- [ ] Data validation improvements
- [ ] Error handling enhancements

### Medium Priority
- [ ] Additional visualization types
- [ ] Documentation translations
- [ ] API endpoint development
- [ ] Docker containerization

### Low Priority
- [ ] UI/UX improvements
- [ ] Configuration optimization
- [ ] Code refactoring
- [ ] Example notebooks

---

## 💡 Tips for Success

1. **Start Small**: Pick a bug fix or documentation update
2. **Ask Questions**: Open an issue before starting major work
3. **Test Thoroughly**: Run the dashboard and verify changes
4. **Update Docs**: Every code change needs documentation
5. **Be Patient**: Reviews take time, respond to feedback quickly

---

## 🐛 Reporting Bugs

### Create an Issue with:
```markdown
## Description
Clear, concise explanation

## Steps to Reproduce
1. Run dashboard.py
2. Filter by Maharashtra
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happened

## Environment
- OS: Windows/macOS/Linux
- Python: 3.10/3.11/etc
- Browser: Chrome/Firefox/etc
```

---

## ❓ Questions?

- Check existing [issues](https://github.com/KrishnaSrinivas-24/Aadhaar-Insights-Analytics/issues)
- Review [FINAL_REPORT.txt](./FINAL_REPORT.txt)
- Start a [discussion](https://github.com/KrishnaSrinivas-24/Aadhaar-Insights-Analytics/discussions)

---

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas API Reference](https://pandas.pydata.org/docs/)
- [Scikit-learn ML Guides](https://scikit-learn.org/stable/documentation.html)
- [Python PEP 8 Style Guide](https://pep8.org/)

---

## 🎓 Learning Resources

This project is great for learning:
- Building production dashboards with Streamlit
- Implementing ML models (forecasting, anomaly detection)
- Data cleaning and preprocessing at scale
- Government compliance (GIGW 3.0)
- Professional documentation practices

---

Thank you for contributing! 🙌
