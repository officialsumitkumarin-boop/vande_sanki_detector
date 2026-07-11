"""
🇮🇳 VANDE0.0.SANKI.2 - Training Script
Advanced AI Deepfake Detector
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
import os
from sklearn.model_selection import train_test_split
from model_architecture_v2 import vande_sanki_2_0, compile_model
import matplotlib.pyplot as plt
from datetime import datetime

class VandeSankiTrainerV2:
    def __init__(self, data_dir='../dataset'):
        self.data_dir = data_dir
        self.model = None
        self.history = None
        self.img_size = (224, 224)
    
    def load_data(self):
        print("\n📂 Loading dataset...")
        images, labels = [], []
        
        categories = [
            ('real', 0),
            ('ai_generated', 1),
            ('fake_faces', 1)
        ]
        
        for folder, label in categories:
            path = os.path.join(self.data_dir, folder)
            if not os.path.exists(path):
                continue
                
            for f in os.listdir(path):
                if f.lower().endswith(('.jpg', '.png', '.jpeg')):
                    img_path = os.path.join(path, f)
                    img = cv2.imread(img_path)
                    if img is not None:
                        img = cv2.resize(img, self.img_size)
                        img = img / 255.0
                        images.append(img)
                        labels.append(label)
        
        X = np.array(images)
        y = np.array(labels)
        print(f"✅ Loaded: {len(X)} images ({sum(y==0)} Real, {sum(y==1)} AI)")
        return X, y
    
    def augment_data(self, X, y):
        datagen = keras.preprocessing.image.ImageDataGenerator(
            rotation_range=30,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.15,
            zoom_range=0.2,
            horizontal_flip=True,
            brightness_range=[0.8, 1.2],
            fill_mode='reflect'
        )
        return datagen
    
    def train(self, epochs=50, batch_size=32):
        print("\n" + "="*60)
        print("🚀 VANDE0.0.SANKI.2 - Training Started")
        print("="*60)
        
        X, y = self.load_data()
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # ============ SHAPE FIX FOR F1 METRIC ============
        y_train = y_train.reshape(-1, 1)
        y_val = y_val.reshape(-1, 1)
        # ================================================
        
        print(f"\n📊 Split: Train={len(X_train)}, Val={len(X_val)}")
        
        # Create model
        self.model = vande_sanki_2_0()
        self.model = compile_model(self.model)
        self.model.summary()
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
            keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-7),
            keras.callbacks.ModelCheckpoint('vande0.0.sanki.2.h5', monitor='val_accuracy', save_best_only=True),
            keras.callbacks.CSVLogger('training_log_v2.csv')
        ]
        
        # Data augmentation
        datagen = self.augment_data(X_train, y_train)
        
        # Train
        self.history = self.model.fit(
            datagen.flow(X_train, y_train, batch_size=batch_size),
            validation_data=(X_val, y_val),
            epochs=epochs,
            callbacks=callbacks
        )
        
        # Save
        self.model.save('vande0.0.sanki.2.h5')
        self.model.save('vande0.0.sanki.2.keras')
        
        # Evaluate
        results = self.model.evaluate(X_val, y_val, verbose=0)
        print(f"\n📈 Validation Results:")
        metrics = ['Loss', 'Accuracy', 'Precision', 'Recall', 'AUC', 'F1']
        for name, val in zip(metrics, results):
            print(f"   {name}: {val:.4f}")
        
        print(f"\n✅ Model Saved: vande0.0.sanki.2.h5")
        print("🎉 VANDE0.0.SANKI.2 Training Complete!")
        return self.history

if __name__ == "__main__":
    trainer = VandeSankiTrainerV2()
    trainer.train(epochs=50, batch_size=32)