import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import os
import cv2
from sklearn.model_selection import train_test_split

class VandeSankiModel:
    def __init__(self):
        self.model = None
        self.img_size = (224, 224)
        
    def create_model(self):
        """VANDE0.0.SANKI.1 - Custom Architecture"""
        model = keras.Sequential([
            # Input Layer
            layers.Input(shape=(224, 224, 3)),
            
            # Block 1 - Feature Detection
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(),
            layers.Dropout(0.25),
            
            # Block 2 - Pattern Recognition
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(),
            layers.Dropout(0.25),
            
            # Block 3 - Texture Analysis
            layers.Conv2D(128, 3, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.Conv2D(128, 3, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(),
            layers.Dropout(0.25),
            
            # Block 4 - Deep Feature Extraction
            layers.Conv2D(256, 3, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.GlobalAveragePooling2D(),
            
            # Dense Layers - Indian Flag Colors Theme
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(128, activation='relu'),
            layers.Dense(1, activation='sigmoid')  # 0=Real, 1=AI Generated
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
        )
        
        return model
    
    def load_dataset(self, data_dir):
        """Load images from dataset folder"""
        images = []
        labels = []
        
        # Load Real Images (Label: 0)
        real_path = os.path.join(data_dir, 'real')
        for img_name in os.listdir(real_path):
            img_path = os.path.join(real_path, img_name)
            img = cv2.imread(img_path)
            if img is not None:
                img = cv2.resize(img, self.img_size)
                img = img / 255.0
                images.append(img)
                labels.append(0)  # Real = 0
        
        # Load AI Generated Images (Label: 1)
        ai_path = os.path.join(data_dir, 'ai_generated')
        for img_name in os.listdir(ai_path):
            img_path = os.path.join(ai_path, img_name)
            img = cv2.imread(img_path)
            if img is not None:
                img = cv2.resize(img, self.img_size)
                img = img / 255.0
                images.append(img)
                labels.append(1)  # AI Generated = 1
        
        return np.array(images), np.array(labels)
    
    def train_model(self, data_dir='dataset', epochs=50):
        """Train VANDE0.0.SANKI.1 Model"""
        print("🚀 VANDE0.0.SANKI.1 - Training Started")
        print("=" * 50)
        
        # Load data
        X, y = self.load_dataset(data_dir)
        print(f"📊 Total Images: {len(X)}")
        print(f"   Real: {sum(y == 0)}")
        print(f"   AI Generated: {sum(y == 1)}")
        
        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Create model
        self.model = self.create_model()
        print("\n🏗️ Model Architecture:")
        self.model.summary()
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
            keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5),
            keras.callbacks.ModelCheckpoint(
                'vande0.0.sanki.1.h5',
                save_best_only=True,
                monitor='val_accuracy'
            )
        ]
        
        # Train
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=epochs,
            batch_size=32,
            callbacks=callbacks
        )
        
        # Evaluate
        test_loss, test_acc, test_precision, test_recall = self.model.evaluate(X_test, y_test)
        print(f"\n📈 Test Results:")
        print(f"   Accuracy: {test_acc:.2%}")
        print(f"   Precision: {test_precision:.2%}")
        print(f"   Recall: {test_recall:.2%}")
        
        # Save model
        self.model.save('vande0.0.sanki.1.h5')
        print("\n✅ Model Saved: vande0.0.sanki.1.h5")
        print("🎉 VANDE0.0.SANKI.1 Training Complete!")
        
        return history

if __name__ == "__main__":
    # Create detector
    detector = VandeSankiModel()
    
    # Train model (dataset folder mein images rakho)
    # Structure: dataset/real/ and dataset/ai_generated/
    history = detector.train_model()
