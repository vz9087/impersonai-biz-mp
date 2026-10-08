from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import numpy as np
import sys
import os
sys.path.append('.')
from app.features import extract_features
import time

artifact = joblib.load('app/model/phishing_model.joblib')
model = artifact['model']
feature_cols = artifact['feature_cols']

app = FastAPI(title="ImpersonAI Demo", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BRANDS = ['google.com', 'paypal.com', 'amazon.com', 'microsoft.com', 
          'apple.com', 'facebook.com', 'netflix.com', 'instagram.com',
          'linkedin.com', 'github.com', 'dropbox.com']

class ScanRequest(BaseModel):
    url: str

class ScanResponse(BaseModel):
    url: str
    risk_level: str
    probability: float
    is_suspicious: bool
    closest_brand: str | None
    levenshtein_distance: int | None
    features: dict
    processing_time_ms: float

@app.get("/")
def root():
    return {"message": "ImpersonAI Demo API", "status": "running"}

@app.post("/scan", response_model=ScanResponse)
def scan_url(request: ScanRequest):
    start_time = time.time()
    
    url = request.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")
    
    domain = url.replace('http://', '').replace('https://', '').split('/')[0]
    
    closest_brand = None
    min_distance = 999
    for brand in BRANDS:
        from Levenshtein import distance
        d = distance(domain, brand)
        if d < min_distance:
            min_distance = d
            closest_brand = brand

    exact_match = min_distance == 0
    
    features = extract_features(url, closest_brand)
    
    features['has_https'] = 0
    feature_vector = np.array([[features.get(col, 0) for col in feature_cols]])    

    if exact_match:
        prob = 0.0  # Force legitimate score
    else:
        prob = model.predict_proba(feature_vector)[0][1]
    
    is_suspicious = prob > 0.5
    
    if prob > 0.8:
        risk_level = "HIGH"
    elif prob > 0.5:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    processing_time = (time.time() - start_time) * 1000
    
    return ScanResponse(
        url = url,      risk_level = risk_level,
        probability =   round (float(prob), 4),
        is_suspicious = is_suspicious,
        closest_brand = closest_brand       if min_distance <= 3 else None,
        levenshtein_distance = min_distance if min_distance <= 3 else None,
        
	features = {k: round(v, 4) if isinstance(v, float) else v for k, v in features.items()},
        processing_time_ms = round(processing_time, 2)
    )

@app.get ("/brands")
def get_brands () :
    return {"brands": BRANDS}

@app.get("/ui")
def serve_ui():
    return FileResponse('app/static/index.html')

if __name__ == "__main__" :
    import uvicorn
    uvicorn.run (app, host = "127.0.0.1", port = 8000)