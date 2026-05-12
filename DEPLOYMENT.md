# 🚀 Deployment Guide

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] Environment variables configured
- [ ] Performance tested
- [ ] Security scan completed

---

## 🌐 Deploy to Hugging Face Spaces

### Option 1: Using Git (Recommended)

```bash
# 1. Create a Hugging Face account
# Visit: https://huggingface.co/join

# 2. Create a new Space
# Visit: https://huggingface.co/new-space
# - Space name: aadhaar-insights
# - License: MIT
# - Select Streamlit

# 3. Clone the space
git clone https://huggingface.co/spaces/YOUR-USERNAME/aadhaar-insights
cd aadhaar-insights

# 4. Copy your project files
cp -r /path/to/UIDAI_DATA_HACKATHON/MY\ UPDATES/* .

# 5. Create necessary files
touch .gitignore requirements.txt streamlit_app.py

# 6. Configure Streamlit
cat > .streamlit/config.toml <<EOF
[theme]
primaryColor = "#1E4D8C"
backgroundColor = "#F5F5F5"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#1A1A1A"

[server]
maxUploadSize = 200
enableXsrfProtection = true
port = 7860
EOF

# 7. Push to Hugging Face
git add .
git commit -m "Initial deployment"
git push
```

### Option 2: Using Hugging Face Web Interface

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Select Streamlit SDK
4. Upload files directly
5. Configure in Settings

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
# Create Dockerfile
cat > Dockerfile <<EOF
FROM python:3.10-slim

WORKDIR /app

COPY MY\ UPDATES/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY MY\ UPDATES/ .

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
EOF

# Build image
docker build -t aadhaar-insights:latest .

# Run container
docker run -p 8501:8501 aadhaar-insights:latest
```

### Push to Docker Hub

```bash
# Login
docker login

# Tag image
docker tag aadhaar-insights:latest YOUR-USERNAME/aadhaar-insights:latest

# Push
docker push YOUR-USERNAME/aadhaar-insights:latest
```

---

## ☁️ AWS Deployment

### EC2 Deployment

```bash
# SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Update system
sudo yum update -y
sudo yum install python3 git -y

# Clone repository
git clone https://github.com/YOUR-USERNAME/Aadhaar-Insights-Analytics.git
cd Aadhaar-Insights-Analytics/MY\ UPDATES

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with systemd
sudo systemctl start aadhaar-dashboard
sudo systemctl enable aadhaar-dashboard
```

### Using AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.10 aadhaar-insights

# Create environment
eb create aadhaar-production

# Deploy
eb deploy
```

---

## 🔧 Environment Variables

Create `.env` file:

```env
# API Keys
GEMINI_API_KEY=your_key_here
GEMINI_API_KEY_2=backup_key

# Database
DATABASE_URL=postgresql://user:pass@localhost/aadhaar

# Security
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Logging
LOG_LEVEL=INFO

# Feature Flags
ENABLE_ML_PREDICTIONS=true
ENABLE_ANOMALY_DETECTION=true
```

---

## 📊 Monitoring & Logging

### Application Logs

```bash
# View recent logs
tail -f logs/app.log

# Filter errors
grep ERROR logs/app.log

# Generate report
tail -100 logs/app.log > deployment_report.txt
```

### Performance Monitoring

```bash
# Check memory usage
ps aux | grep streamlit

# Monitor dashboard response time
curl -w "@curl-format.txt" https://your-app.com

# Load testing
ab -n 1000 -c 100 https://your-app.com
```

---

## 🔍 Health Checks

### API Health Endpoint

```bash
# Test API is up
curl https://your-app.com/api/health

# Expected response:
# {
#   "status": "healthy",
#   "version": "1.0.0",
#   "timestamp": "2026-05-12T10:30:00Z"
# }
```

### Database Connection

```bash
# Test data loading
python -c "import pandas as pd; df = pd.read_csv('data.csv'); print(f'Rows: {len(df)}')"
```

---

## 🚨 Troubleshooting

### Common Issues

**Dashboard won't load:**
```bash
# Check Python dependencies
pip install -r requirements.txt --force-reinstall

# Check port availability
lsof -i :8501

# Run with debug mode
streamlit run dashboard.py --logger.level=debug
```

**Memory issues:**
```bash
# Check system memory
free -h

# Use memory profiler
pip install memory_profiler
python -m memory_profiler dashboard.py
```

**API timeouts:**
```bash
# Check network connectivity
ping -c 5 api.example.com

# Test API latency
curl -w "@curl-format.txt" https://api.example.com
```

---

## ✅ Post-Deployment Checklist

- [ ] Application loads successfully
- [ ] All API endpoints working
- [ ] Database connected
- [ ] Logs flowing correctly
- [ ] Monitoring active
- [ ] Backup configured
- [ ] SSL certificate valid
- [ ] DNS pointing correctly
- [ ] Load balancer healthy
- [ ] Alerts configured

---

## 📞 Support

For deployment help:
- Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- Open a GitHub Issue
- Review logs in `logs/` directory

---

*Deployment Guide v1.0 - Last Updated: May 12, 2026*
