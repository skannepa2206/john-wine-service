from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import torch.nn as nn
import joblib
import numpy as np
import os

app = FastAPI(title="John's Wine Quality Prediction Service 🍷")

# Load the trained model (matches original Sequential structure)
model = nn.Sequential(
    nn.Linear(11, 64),
    nn.ReLU(),
    nn.Linear(64, 1)
)
model.load_state_dict(torch.load("johns_wine_model.pt"))
model.eval()

# Load the feature scaler
scaler = joblib.load("wine_feature_scaler.pkl")

# Define input schema
class WineChemicalProfile(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

@app.get("/wine-health")
def health_check():
    return {"status": "OK", "message": "Wine prediction model is ready!"}

@app.get("/wine-model-info")
def model_info():
    return {
        "model_type": "Feedforward Neural Network",
        "framework": "PyTorch",
        "features": [
            "fixed_acidity", "volatile_acidity", "citric_acid", "residual_sugar",
            "chlorides", "free_sulfur_dioxide", "total_sulfur_dioxide",
            "density", "pH", "sulphates", "alcohol"
        ],
        "output": "wine_quality_score (float)"
    }

@app.post("/predict-wine-quality")
def predict_wine_quality(wine: WineChemicalProfile):
    try:
        features = np.array([[getattr(wine, field) for field in wine.__fields__]])
        scaled = scaler.transform(features)
        with torch.no_grad():
            tensor_input = torch.from_numpy(scaled).float()
            prediction = model(tensor_input).item()
        return {"predicted_quality": round(prediction, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # Use default if not set
    uvicorn.run(app, host="0.0.0.0", port=port)
