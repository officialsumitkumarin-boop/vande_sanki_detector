"""
Dataset Collector for VANDE0.0.SANKI.1
Pexels API + Other Free Sources
"""

import os
import requests
import time
import urllib.request
from PIL import Image
from io import BytesIO

# ==================== CONFIGURATION ====================
# Pexels API Key - Free registration: https://www.pexels.com/api/
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY_HERE"  # 👈 API key yahan dalo

# Dataset folders
REAL_DIR = "dataset/real"
AI_DIR = "dataset/ai_generated"

# Number of images
REAL_COUNT = 100
AI_COUNT = 100
# =======================================================

def create_folders():
    """Create dataset folders"""
    os.makedirs(REAL_DIR, exist_ok=True)
    os.makedirs(AI_DIR, exist_ok=True)
    print("📁 Folders created successfully!")

def download_real_from_pexels(count=100):
    """Download real images from Pexels API"""
    print(f"\n📸 Downloading {count} Real Images from Pexels...")
    
    if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY_HERE":
        print("⚠️  Pexels API key not set! Using free alternative...")
        return download_real_from_free_sources(count)
    
    headers = {"Authorization": PEXELS_API_KEY}
    
    # Different search queries for variety
    queries = ["nature", "people", "animals", "city", "food", "travel", "cars"]
    
    images_per_query = count // len(queries)
    
    for query in queries:
        print(f"  Searching for: {query}")
        url = "https://api.pexels.com/v1/search"
        params = {
            "query": query,
            "per_page": images_per_query,
            "size": "large"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            photos = response.json()["photos"]
            
            for i, photo in enumerate(photos):
                img_url = photo["src"]["large"]
                img_data = requests.get(img_url).content
                
                filename = f"{REAL_DIR}/pexels_{query}_{i}.jpg"
                with open(filename, "wb") as f:
                    f.write(img_data)
                
                print(f"    ✓ Downloaded: {filename}")
                time.sleep(0.1)  # Rate limit
            
        except Exception as e:
            print(f"    ✗ Error: {e}")

def download_real_from_free_sources(count=100):
    """Free alternative - No API key needed"""
    print("🆓 Using Free Sources (No API Key Required)...")
    
    # Source 1: Lorem Picsum
    print("  From Lorem Picsum...")
    for i in range(count // 2):
        try:
            url = f"https://picsum.photos/800/800?random={i}"
            urllib.request.urlretrieve(url, f"{REAL_DIR}/free_picsum_{i}.jpg")
            print(f"    ✓ Image {i+1}/{count//2}")
        except:
            pass
        time.sleep(0.05)
    
    # Source 2: Unsplash Source
    print("  From Unsplash Source...")
    for i in range(count // 2):
        try:
            url = f"https://source.unsplash.com/random/800x800/?nature,people&sig={i}"
            urllib.request.urlretrieve(url, f"{REAL_DIR}/free_unsplash_{i}.jpg")
            print(f"    ✓ Image {i+count//2+1}/{count}")
        except:
            pass
        time.sleep(0.05)

def download_ai_generated(count=100):
    """Download AI generated images"""
    print(f"\n🤖 Downloading {count} AI Generated Images...")
    
    # Source 1: This Person Does Not Exist (Faces)
    print("  From ThisPersonDoesNotExist...")
    for i in range(count // 3):
        try:
            response = requests.get("https://thispersondoesnotexist.com/image")
            with open(f"{AI_DIR}/ai_face_{i}.jpg", "wb") as f:
                f.write(response.content)
            print(f"    ✓ AI Face {i+1}/{count//3}")
        except:
            pass
        time.sleep(0.5)
    
    # Source 2: Random AI-style images
    print("  Generating AI-style variations...")
    for i in range(count // 3):
        try:
            # Using different seeds for variety
            url = f"https://picsum.photos/800/800?random={i+10000}&blur=2"
            urllib.request.urlretrieve(url, f"{AI_DIR}/ai_variation_{i}.jpg")
            print(f"    ✓ AI Variation {i+1}/{count//3}")
        except:
            pass
        time.sleep(0.1)
    
    # Source 3: Additional free AI images
    print("  From additional sources...")
    for i in range(count // 3):
        try:
            url = f"https://source.unsplash.com/random/800x800/?abstract,digital&sig={i+20000}"
            urllib.request.urlretrieve(url, f"{AI_DIR}/ai_abstract_{i}.jpg")
            print(f"    ✓ AI Abstract {i+1}/{count//3}")
        except:
            pass
        time.sleep(0.05)

def verify_dataset():
    """Check dataset quality and count"""
    print("\n📊 Dataset Verification:")
    
    real_images = len([f for f in os.listdir(REAL_DIR) if f.endswith(('.jpg', '.png', '.jpeg'))])
    ai_images = len([f for f in os.listdir(AI_DIR) if f.endswith(('.jpg', '.png', '.jpeg'))])
    
    print(f"   Real Images: {real_images}")
    print(f"   AI Images: {ai_images}")
    print(f"   Total: {real_images + ai_images}")
    
    # Check for corrupt files
    corrupt_count = 0
    for folder in [REAL_DIR, AI_DIR]:
        for img_file in os.listdir(folder):
            if img_file.endswith(('.jpg', '.png', '.jpeg')):
                try:
                    img_path = os.path.join(folder, img_file)
                    img = Image.open(img_path)
                    img.verify()
                except:
                    print(f"   ⚠️  Corrupt file: {img_file}")
                    os.remove(img_path)
                    corrupt_count += 1
    
    if corrupt_count > 0:
        print(f"   ✗ Removed {corrupt_count} corrupt files")
    else:
        print("   ✓ All images are valid!")
    
    return real_images, ai_images

def main():
    print("=" * 50)
    print("🇮🇳 VANDE0.0.SANKI.1 - Dataset Collector")
    print("=" * 50)
    
    # Create folders
    create_folders()
    
    # Download real images
    if PEXELS_API_KEY != "YOUR_PEXELS_API_KEY_HERE":
        download_real_from_pexels(REAL_COUNT)
    else:
        print("\n💡 TIP: Pexels API key add karo for better images!")
        print("   1. Visit: https://www.pexels.com/api/")
        print("   2. Register for free")
        print("   3. Copy API key")
        print("   4. Paste in this script: PEXELS_API_KEY = 'your_key_here'\n")
        download_real_from_free_sources(REAL_COUNT)
    
    # Download AI images
    download_ai_generated(AI_COUNT)
    
    # Verify
    real_count, ai_count = verify_dataset()
    
    print("\n" + "=" * 50)
    print("✅ Dataset Collection Complete!")
    print("=" * 50)
    print(f"\n📁 Dataset ready at:")
    print(f"   {REAL_DIR}/ - {real_count} real images")
    print(f"   {AI_DIR}/ - {ai_count} AI images")
    print(f"\n🚀 Next step: python model/train_model.py")

if __name__ == "__main__":
    main()
