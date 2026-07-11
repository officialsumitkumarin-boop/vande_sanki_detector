"""
🇮🇳 VANDE0.0.SANKI.2 - Advanced Multi-Branch Architecture
Purpose: Detect AI-generated images, deepfakes, and manipulated content
Features: Multi-branch, Attention, Advanced Pattern Detection
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

def attention_block(x, filters):
    """Channel + Spatial Attention for focusing on AI artifacts"""
    # Channel Attention
    avg_pool = layers.GlobalAveragePooling2D()(x)
    avg_pool = layers.Reshape((1, 1, filters))(avg_pool)
    avg_pool = layers.Conv2D(filters//8, 1, activation='relu')(avg_pool)
    avg_pool = layers.Conv2D(filters, 1, activation='sigmoid')(avg_pool)
    
    # Spatial Attention
    max_pool = layers.Lambda(lambda x: tf.reduce_max(x, axis=-1, keepdims=True))(x)
    avg_pool_spatial = layers.Lambda(lambda x: tf.reduce_mean(x, axis=-1, keepdims=True))(x)
    spatial = layers.Concatenate()([max_pool, avg_pool_spatial])
    spatial = layers.Conv2D(1, 7, padding='same', activation='sigmoid')(spatial)
    
    # Apply attention
    x = layers.Multiply()([x, avg_pool])
    x = layers.Multiply()([x, spatial])
    return x

def residual_block(x, filters):
    """Residual connection for better gradient flow"""
    shortcut = x
    x = layers.Conv2D(filters, 3, padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)
    x = layers.Conv2D(filters, 3, padding='same')(x)
    x = layers.BatchNormalization()(x)
    
    # Adjust shortcut dimensions if needed
    if shortcut.shape[-1] != filters:
        shortcut = layers.Conv2D(filters, 1, padding='same')(shortcut)
    
    x = layers.Add()([x, shortcut])
    x = layers.Activation('relu')(x)
    return x

def vande_sanki_2_0(input_shape=(224, 224, 3)):
    """
    VANDE0.0.SANKI.2 - Multi-Branch Deepfake Detector
    4 Parallel branches analyzing different aspects
    """
    
    image_input = keras.Input(shape=input_shape, name='image_input')
    
    # ============ BRANCH 1: HIGH-LEVEL FEATURES ============
    # Detects overall image structure, faces, objects
    b1 = layers.Conv2D(64, 7, strides=2, padding='same', name='b1_conv1')(image_input)
    b1 = layers.BatchNormalization()(b1)
    b1 = layers.Activation('relu')(b1)
    b1 = layers.MaxPooling2D(3, strides=2)(b1)
    
    b1 = residual_block(b1, 64)
    b1 = residual_block(b1, 128)
    b1 = attention_block(b1, 128)
    b1 = layers.GlobalAveragePooling2D()(b1)
    
    # ============ BRANCH 2: TEXTURE & PATTERN ANALYSIS ============
    # AI images have specific texture patterns
    b2 = layers.Conv2D(32, 1, name='b2_compress')(image_input)
    b2 = layers.Conv2D(64, 5, padding='same', name='b2_texture')(b2)
    b2 = layers.BatchNormalization()(b2)
    b2 = layers.Activation('relu')(b2)
    b2 = layers.MaxPooling2D()(b2)
    
    b2 = layers.Conv2D(128, 3, padding='same', dilation_rate=2)(b2)  # Dilated conv
    b2 = layers.BatchNormalization()(b2)
    b2 = layers.Activation('relu')(b2)
    b2 = layers.Conv2D(128, 3, padding='same')(b2)
    b2 = attention_block(b2, 128)
    b2 = layers.GlobalAveragePooling2D()(b2)
    
    # ============ BRANCH 3: EDGE & BOUNDARY DETECTION ============
    # AI images have unnatural edges
    b3 = layers.Conv2D(32, 3, padding='same', 
                       kernel_initializer='he_normal', name='b3_edge1')(image_input)
    b3 = layers.Conv2D(64, 3, padding='same', 
                       kernel_initializer='he_normal')(b3)
    b3 = layers.BatchNormalization()(b3)
    b3 = layers.Activation('relu')(b3)
    b3 = layers.MaxPooling2D()(b3)
    
    b3 = layers.Conv2D(128, 3, padding='same')(b3)
    b3 = layers.Conv2D(128, 3, padding='same')(b3)
    b3 = attention_block(b3, 128)
    b3 = layers.GlobalAveragePooling2D()(b3)
    
    # ============ BRANCH 4: FREQUENCY DOMAIN ============
    # Detect frequency artifacts common in AI images
    b4 = layers.Conv2D(16, 1, name='b4_freq')(image_input)
    b4 = layers.Conv2D(32, 3, padding='same')(b4)
    b4 = layers.Conv2D(64, 3, padding='same', strides=2)(b4)
    b4 = layers.BatchNormalization()(b4)
    b4 = layers.Activation('relu')(b4)
    b4 = layers.Conv2D(128, 3, padding='same')(b4)
    b4 = layers.GlobalAveragePooling2D()(b4)
    
    # ============ MERGE ALL BRANCHES ============
    combined = layers.Concatenate(name='branch_merge')([b1, b2, b3, b4])
    
    # ============ DENSE CLASSIFIER ============
    x = layers.Dense(1024, activation='relu', name='dense_1024')(combined)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(512, activation='relu', name='dense_512')(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(256, activation='relu', name='dense_256')(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation='relu', name='dense_128')(x)
    x = layers.Dense(64, activation='relu', name='dense_64')(x)
    
    # ============ OUTPUT ============
    output = layers.Dense(1, activation='sigmoid', name='output')(x)
    
    model = keras.Model(inputs=image_input, outputs=output, name='VANDE0.0.SANKI.2')
    return model

def compile_model(model, learning_rate=0.0001):
    """Compile with advanced metrics"""
    model.compile(
        optimizer=keras.optimizers.AdamW(learning_rate=learning_rate, weight_decay=1e-5),
        loss='binary_crossentropy',
        metrics=[
            'accuracy',
            keras.metrics.Precision(name='precision'),
            keras.metrics.Recall(name='recall'),
            keras.metrics.AUC(name='auc'),
            keras.metrics.F1Score(name='f1')
        ]
    )
    return model

if __name__ == "__main__":
    model = vande_sanki_2_0()
    model.summary()
    print(f"\n✅ VANDE0.0.SANKI.2 Architecture Ready!")
    print(f"   Total Parameters: {model.count_params():,}")