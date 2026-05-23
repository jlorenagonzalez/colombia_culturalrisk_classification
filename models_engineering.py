import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Prevents crash errors on web servers like Render
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Three Selected Classification Models
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Global variables 
_models_cache = {}
_scaler_cache = None
_classes_cache = []

def train_all_models():
    """
    Performs data loading, dataset split, hyperparameter configuration,
    model training, evaluation metrics calculation, and confusion matrix plotting.
    All logic is encapsulated here away from app.py.
    """
    global _models_cache, _scaler_cache, _classes_cache
    
    csv_path = "colombian.xlsx"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing dataset: {csv_path}")
        
    df = pd.read_excel(csv_path)
    df = df.dropna()
    
    # Feature columns select (Independent variables)
    feature_cols = [
        'net_youth_migration', 
        'median_age', 
        'indigenous_pop_ratio', 
        'primary_poverty_index', 
        'annual_festivals_count', 
        'active_cultural_groups', 
        'subsidized_cultural_budget'
    ]
    
    X = df[feature_cols].copy()
    y = df['cultural_erosion_risk'].copy()
    
    # Target variable
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    _classes_cache = list(label_encoder.classes_)
    
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    
    _scaler_cache = StandardScaler()
    X_train_scaled = _scaler_cache.fit_transform(X_train)
    X_test_scaled = _scaler_cache.transform(X_test)
    
    
    _models_cache["Logistic Regression"] = LogisticRegression(max_iter=1000, C=1.0, random_state=42)
    _models_cache["Decision Tree"] = DecisionTreeClassifier(max_depth=5, min_samples_split=4, random_state=42)
    _models_cache["Random Forest"] = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    
    metrics_results = {}
    os.makedirs('static', exist_ok=True)
    
    print("\n=== STARTING MACHINE LEARNING TRAINING PROCESS ===")
    
    for name, model in _models_cache.items():
        
        # Choose appropriate features based on model type
        X_tr = X_train_scaled if name == "Logistic Regression" else X_train
        X_te = X_test_scaled if name == "Logistic Regression" else X_test
        
        # Training process execution
        model.fit(X_tr, y_train)
        
        # Validation process
        y_pred = model.predict(X_te)
        
        # Performance Evaluation 
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        metrics_results[name] = {
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1-Score": round(f1, 4)
        }
        
        print(f"Model: {name} | Parameters: {model.get_params()}")
        print(f" -> Accuracy: {acc:.4f} | F1-Score: {f1:.4f}")
        
        # Graphical Visualizations (Confusion Matrix)
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(6, 4.5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=_classes_cache, yticklabels=_classes_cache)
        plt.title(f'Confusion Matrix: {name}')
        plt.ylabel('Actual Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        
        filename = f"static/cm_{name.lower().replace(' ', '_')}.png"
        plt.savefig(filename)
        plt.close()
        
    print("=== TRAINING PROCESS COMPLETED SUCCESSFULLY ===\n")
    return metrics_results

def predict_cultural_risk(model_name, features_list):
    """
    Functional prediction testing helper. 
    Applies scaling if necessary and returns the text classification label.
    """
    global _models_cache, _scaler_cache, _classes_cache
    
    if model_name not in _models_cache:
        raise ValueError(f"Model {model_name} is not trained or available.")
        
    raw_features = np.array([features_list])
  

    if model_name == "Logistic Regression" and _scaler_cache is not None:
        processed_features = _scaler_cache.transform(raw_features)
    else:
        processed_features = raw_features
        
    model_instance = _models_cache[model_name]
    numeric_prediction = model_instance.predict(processed_features)[0]
    
   
    return _classes_cache[numeric_prediction]

if __name__ == "__main__":
    # Test script locally via console
    train_all_models()