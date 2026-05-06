"""
app.py - FastAPI Backend for MNIST Digit Recognition
Serves the scikit-learn model via a POST endpoint.
"""

import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Import training logic if model doesn't exist
try:
    from model_train import train_model
except ImportError:
    # If used as a standalone file, we'd need to define training here
    pass

app = FastAPI(title="MNIST Digit Recognizer API")

# Enable CORS for all origins (useful for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model = None

class ImageData(BaseModel):
    # Expecting a list of 784 pixel values (0-255 or scaled)
    pixels: List[float]

@app.on_event("startup")
def load_model():
    """Load model on startup, train it if missing."""
    global model
    model_path = "model.pkl"
    
    if not os.path.exists(model_path):
        print(f"{model_path} not found. Starting automatic training...")
        # Since I can't easily call train_model() here without a full environment,
        # in a real FastAPI app you would ensure the model is trained first.
        # For this exercise, we'll try to import and run it.
        try:
            train_model()
        except NameError:
            print("Training function not available. Please run model_train.py first.")
            return

    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print("Model loaded successfully.")

@app.post("/predict")
async def predict(data: ImageData):
    """Predict the digit from pixel data."""
    global model
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Try again later.")
    
    try:
        # Reshape and check pixels
        pixels = np.array(data.pixels).reshape(1, -1)
        
        # Ensure pixels are scaled if the model was trained on scaled data
        # (Assuming model_train.py scaled to [0, 1])
        if pixels.max() > 1.1:
            pixels = pixels / 255.0
            
        prediction = model.predict(pixels)[0]
        probabilities = model.predict_proba(pixels)[0]
        confidence = float(np.max(probabilities))
        
        return {
            "prediction": str(prediction),
            "confidence": confidence
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}

if __name__ == "__main__":
    import uvicorn
    # Use environment port or default to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
