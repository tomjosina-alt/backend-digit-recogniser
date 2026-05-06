"""
model_train.py - MNIST Digit Recognition Model Training
This script trains a scikit-learn MLPClassifier on the MNIST dataset.
"""

import joblib
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

def train_model():
    print("Loading MNIST dataset... (This might take a moment)")
    # Load data from https://www.openml.org/d/554
    X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False, parser='auto')
    
    # Scale pixels to [0, 1]
    X = X / 255.0
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training MLPClassifier...")
    # Using a simple Multi-layer Perceptron (MLP)
    # Hidden layers: (128, 64)
    model = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=20, alpha=1e-4,
                        solver='adam', verbose=True, random_state=42,
                        learning_rate_init=.001)
    
    model.fit(X_train, y_train)
    
    # Calculate accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Training complete! Test Accuracy: {accuracy * 100:.2f}%")
    
    # Save the model
    joblib.dump(model, 'model.pkl')
    print("Model saved as model.pkl")

if __name__ == "__main__":
    train_model()
