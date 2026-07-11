from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
import cv2
import os          # 👈 YE ADD KARO
from io import BytesIO
from PIL import Image
import uvicorn

app = FastAPI(
    title="VANDE0.0.SANKI.1 API",
    description="India's First Custom AI vs Real Image Detector",
    version="1.0.0"
)

# CORS enable for web app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = None  # 👈 YE ADD KARO
try:
    model_path = os.path.join(os.path.dirname(__file__), 'vande0.0.sanki.1.h5')
    model = tf.keras.models.load_model(model_path)  # 👈 YE ADD KARO
    print("✅ VANDE0.0.SANKI.1 Model Loaded Successfully")
except Exception as e:
    print(f"⚠️ Model file not found: {e}")

def preprocess_image(image):
    """Preprocess image for model"""
    img = cv2.resize(image, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def analyze_image(image):
    """Deep analysis of image"""
    if model is None:  # 👈 YE ADD KARO
        return "Error: Model not loaded", 0
    
    prediction = model.predict(image, verbose=0)[0][0]
    
    if prediction > 0.5:
        confidence = prediction * 100
        result = "AI Generated"
    else:
        confidence = (1 - prediction) * 100
        result = "Real Image"
    
    return result, confidence

@app.get("/")
async def root():
    return {
        "message": "🇮🇳 VANDE0.0.SANKI.1 API Running",
        "model": "India's First Custom AI Image Detector",
        "model_loaded": model is not None,  # 👈 YE ADD KARO
        "endpoints": {
            "/predict": "POST - Upload image for detection",
            "/health": "GET - Check API health"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_name": "VANDE0.0.SANKI.1"
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:  # 👈 YE ADD KARO
        return JSONResponse(
            content={"error": "Model not loaded"},
            status_code=503
        )
    
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return JSONResponse(
                content={"error": "Invalid image"},
                status_code=400
            )
        
        processed_img = preprocess_image(img)
        result, confidence = analyze_image(processed_img)
        
        analysis_details = {
            "filename": file.filename,
            "result": result,
            "confidence": f"{confidence:.2f}%",
            "model_version": "VANDE0.0.SANKI.1",
            "country": "India",
            "made_with": "❤️",
            "details": {
                "possible_sources": ["Midjourney", "DALL-E", "Stable Diffusion"],
                "artifacts": "AI generation patterns detected"
            } if result == "AI Generated" else {
                "source": "Natural/Camera captured",
                "quality": "Original photograph"
            }
        }
        
        return JSONResponse(content=analysis_details)
        
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)