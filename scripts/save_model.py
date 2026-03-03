"""
Script to save trained model for use in API and prediction script.
Run this after training the model in the notebook.
"""
import joblib
import os
import sys
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_sample_model():
    """
    Create a sample trained model for demonstration purposes.
    In production, you would load the model trained in the notebook.
    """
    # Create a simple Random Forest model with default parameters
    # This serves as a placeholder - in production, load from notebook
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )
    
    # Create dummy training data
    np.random.seed(42)
    n_samples = 1000
    X_train = np.random.randn(n_samples, 9)
    y_train = np.random.randn(n_samples)
    
    # Fit the model
    model.fit(X_train, y_train)
    
    return model


def save_model(model_path='models/trained_model.pkl'):
    """
    Save the trained model to a file.
    
    Args:
        model_path: Path to save the model
    """
    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # Create and save the model
    model = create_sample_model()
    
    # Get absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    full_path = os.path.join(project_root, model_path)
    
    joblib.dump(model, full_path)
    print(f"✓ Model saved to {full_path}")
    
    return model


if __name__ == '__main__':
    # Save the model
    model = save_model()
    print("\nModel ready for use in API and prediction script!")

