from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
import cv2
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
try:
    model = tf.keras.models.load_model('model/vande0.0.sanki.1.h5')
    print("✅ VANDE0.0.SANKI.1 Model Loaded Successfully")
except:
    model = None
    print("⚠️ Model file not found")

def preprocess_image(image):
    """Preprocess image for model"""
    img = cv2.resize(image, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def analyze_image(image):
    """Deep analysis of image"""
    # Check for AI artifacts
    prediction = model.predict(image, verbose=0)[0][0]
    
    # Confidence calculation
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
    try:
        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return JSONResponse(
                content={"error": "Invalid image"},
                status_code=400
            )
        
        # Preprocess
        processed_img = preprocess_image(img)
        
        # Predict
        result, confidence = analyze_image(processed_img)
        
        # Additional analysis
        analysis_details = {
            "filename": file.filename,
            "result": result,
            "confidence": f"{confidence:.2f}%",
            "model_version": "VANDE0.0.SANKI.1",
            "country": "India",
            "made_with": "❤️",
            "details": {
                "if_ai_detected": {
                    "possible_sources": ["Midjourney", "DALL-E", "Stable Diffusion"],
                    "artifacts": "AI generation patterns detected"
                } if result == "AI Generated" else {
                    "source": "Natural/Camera captured",
                    "quality": "Original photograph"
                }
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
