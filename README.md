# ImpersonAI - AI-Powered Domain Abuse & Impersonation Defense System

## Overview
ImpersonAI detects typosquatting and lookalike domains using XGBoost machine learning.

## Tech Stack
- **Backend**: FastAPI, Python
- **ML Model**: XGBoost
- **Frontend**: HTML, CSS, JavaScript
- **Features**: 22 lexical URL features

## How to Run
```bash
# Activate environment
venv\Scripts\activate

# Start server
python app/main.py

# Open browser
http://127.0.0.1:8000/ui

## 🚀 Features

- **AI-Powered Detection**: XGBoost classifier with 23 lexical URL features
- **Real-Time Scanning**: Sub-10ms inference latency
- **Chrome Extension**: Intercepts link clicks and blocks dangerous domains
- **Web Dashboard**: User-friendly interface for manual URL checking
- **REST API**: FastAPI with auto-generated Swagger documentation

## 📊 Model Performance

- Accuracy: 86%
- Precision: 85%
- Recall: 84%
- F1 Score: 84%

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **ML**: XGBoost, scikit-learn, pandas, numpy
- **Frontend**: HTML, CSS, JavaScript
- **Extension**: Chrome Manifest V3

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/impersonai.git
cd impersonai

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install fastapi uvicorn xgboost scikit-learn pandas numpy python-Levenshtein tldextract

# Generate training data
python data/generate_training_data.py

# Train the model
python app/train_model.py

# Start the backend
python app/main.py

--

# Testing

1. Open http://127.0.0.1:8000/ui for the web dashboard

2. Open http://127.0.0.1:8000/docs for API documentation

3. Load chrome-extension/ folder in Chrome via chrome://extensions (Developer mode → Load unpacked)

--

# Project Structure
impersonai/
├── app/                    # Backend application
│   ├── main.py             # FastAPI server
│   ├── features.py         # Feature extraction
│   ├── train_model.py      # XGBoost training
│   ├── model/              # Trained model storage
│   └── static/             # Frontend files
├── data/                   # Training data & generators
├── chrome-extension/       # Browser extension
└── README.md

--

# Authors

Vishal V P, Keerthi M G, Pooja A N
Under the guidance of: Mrs. Chaithra B M, Assistant Professor, Dept of CSE, JITD

--

