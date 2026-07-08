"""
VANDE0.0.SANKI.1 - Model Architecture
India's First Custom AI vs Real Image Detection Model
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os

def create_vande_sanki_model(input_shape=(224, 224, 3)):
    """
    VANDE0.0.SANKI.1 Architecture
    
    Features:
    - 4 CNN Blocks for deep feature extraction
    - Batch Normalization for stable training
    - Dropout for preventing overfitting
    - Global Average Pooling instead of Flatten
    - Custom dense layers with Indian flag inspired neurons (512, 256, 128)
    """
    
    # Input Layer
    inputs = keras.Input(shape=input_shape, name='image_input')
    
    # ============ BLOCK 1: Basic Feature Detection ============
    # Saffron Layer - Initial feature extraction
    x = layers.Conv2D(32, (3, 3), padding='same', activation='relu', name='saffron_conv1')(inputs)
    x = layers.BatchNormalization(name='saffron_bn1')(x)
    x = layers.Conv2D(32, (3, 3), padding='same', activation='relu', name='saffron_conv2')(x)
    x = layers.BatchNormalization(name='saffron_bn2')(x)
    x = layers.MaxPooling2D((2, 2), name='saffron_pool')(x)
    x = layers.Dropout(0.25, name='saffron_dropout')(x)
    
    # ============ BLOCK 2: Pattern Recognition ============
    # White Layer - Peace and truth detection
    x = layers.Conv2D(64, (3, 3), padding='same', activation='relu', name='white_conv1')(x)
    x = layers.BatchNormalization(name='white_bn1')(x)
    x = layers.Conv2D(64, (3, 3), padding='same', activation='relu', name='white_conv2')(x)
    x = layers.BatchNormalization(name='white_bn2')(x)
    x = layers.MaxPooling2D((2, 2), name='white_pool')(x)
    x = layers.Dropout(0.25, name='white_dropout')(x)
    
    # ============ BLOCK 3: Texture Analysis ============
    # Green Layer - Growth and prosperity in detection
    x = layers.Conv2D(128, (3, 3), padding='same', activation='relu', name='green_conv1')(x)
    x = layers.BatchNormalization(name='green_bn1')(x)
    x = layers.Conv2D(128, (3, 3), padding='same', activation='relu', name='green_conv2')(x)
    x = layers.BatchNormalization(name='green_bn2')(x)
    x = layers.MaxPooling2D((2, 2), name='green_pool')(x)
    x = layers.Dropout(0.25, name='green_dropout')(x)
    
    # ============ BLOCK 4: Deep Feature Extraction ============
    # Ashoka Chakra - 24 spokes of deep learning
    x = layers.Conv2D(256, (3, 3), padding='same', activation='relu', name='chakra_conv1')(x)
    x = layers.BatchNormalization(name='chakra_bn')(x)
    x = layers.GlobalAveragePooling2D(name='chakra_gap')(x)
    
    # ============ DENSE LAYERS: Indian Flag Colors Theme ============
    # 512 - Saffron (Courage)
    x = layers.Dense(512, activation='relu', name='saffron_dense')(x)
    x = layers.Dropout(0.5, name='saffron_dense_dropout')(x)
    
    # 256 - White (Peace)
    x = layers.Dense(256, activation='relu', name='white_dense')(x)
    x = layers.Dropout(0.5, name='white_dense_dropout')(x)
    
    # 128 - Green (Growth)
    x = layers.Dense(128, activation='relu', name='green_dense')(x)
    
    # ============ OUTPUT LAYER ============
    # 1 neuron: 0 = Real Image, 1 = AI Generated
    outputs = layers.Dense(1, activation='sigmoid', name='output')(x)
    
    # Create model
    model = keras.Model(inputs=inputs, outputs=outputs, name='VANDE0.0.SANKI.1')
    
    return model


def compile_model(model, learning_rate=0.001):
    """Compile model with custom metrics"""
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss='binary_crossentropy',
        metrics=[
            'accuracy',
            keras.metrics.Precision(name='precision'),
            keras.metrics.Recall(name='recall'),
            keras.metrics.AUC(name='auc')
        ]
    )
    return model


def get_model_summary():
    """Get model architecture summary as string"""
    model = create_vande_sanki_model()
    
    # Count parameters
    total_params = model.count_params()
    trainable_params = sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
    
    summary = f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║           VANDE0.0.SANKI.1 - Model Architecture              ║
    ╚══════════════════════════════════════════════════════════════╝
    
    📊 Model Statistics:
    ├── Input Shape: 224 × 224 × 3 (RGB)
    ├── Total Parameters: {total_params:,}
    ├── Trainable Parameters: {trainable_params:,}
    ├── Total Layers: {len(model.layers)}
    
    🏗️ Architecture Blocks:
    ├── Block 1 (Saffron): 32→32 filters (Basic Features)
    ├── Block 2 (White):   64→64 filters (Pattern Recognition)
    ├── Block 3 (Green):   128→128 filters (Texture Analysis)
    ├── Block 4 (Chakra):  256 filters (Deep Features)
    ├── Dense Layer 1:     512 neurons (Courage)
    ├── Dense Layer 2:     256 neurons (Peace)
    ├── Dense Layer 3:     128 neurons (Growth)
    └── Output Layer:      1 neuron (Real/AI)
    
    🎯 Special Features:
    ├── Batch Normalization after every Conv layer
    ├── Dropout (25%) after each block
    ├── Global Average Pooling (reduces overfitting)
    └── 50% Dropout in Dense layers
    
    🇮🇳 Made with Indian Flag Colors Theme
    """
    return summary


if __name__ == "__main__":
    # Test model creation
    print(get_model_summary())
    
    # Create and show model
    model = create_vande_sanki_model()
    model.summary()
    
    # Save model architecture visualization
    tf.keras.utils.plot_model(
        model,
        to_file='vande_sanki_architecture.png',
        show_shapes=True,
        show_layer_names=True,
        rankdir='TB',
        dpi=96
    )
    print("\n✅ Architecture diagram saved as 'vande_sanki_architecture.png'")
