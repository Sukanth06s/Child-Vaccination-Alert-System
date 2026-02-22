import os
import numpy as np
import xgboost as xgb
import pandas as pd

# Path to model_files dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, 'model_files')

class PredictionService:
    def __init__(self):
        self.models = {}
        self.load_models()
        
    def load_models(self):
        """
        Dynamically load XGBoost JSON models from model_files directory.
        """
        if not os.path.exists(MODEL_DIR):
            return
            
        for filename in os.listdir(MODEL_DIR):
            if filename.endswith('.json') and filename != 'example.json':
                vaccine_name = filename.replace('.json', '')
                filepath = os.path.join(MODEL_DIR, filename)
                try:
                    # Load XGBoost trained models
                    model = xgb.XGBClassifier()
                    model.load_model(filepath)
                    self.models[vaccine_name] = model
                    print(f"DEBUG: Successfully loaded model: {filename}", flush=True)
                except Exception as e:
                    print(f"DEBUG: Error loading model {filename}: {e}", flush=True)
        print(f"DEBUG: Total models loaded: {len(self.models)}", flush=True)

    def extract_features(self, user_data: dict) -> pd.DataFrame:
        """
        Extract the features exactly as expected by the models.
        """
        # Helper to convert to float safely
        def safe_float(val):
            try:
                # v101 or other strings like "Tamil Nadu" will trigger ValueError and return 0.0 safely
                return float(val) if val is not None and val != '' else 0.0
            except (ValueError, TypeError):
                return 0.0

        features_dict = {
            'v012': [safe_float(user_data.get('v012'))],
            'v106': [safe_float(user_data.get('v106'))],
            'v025': [safe_float(user_data.get('v025'))],
            'v190': [safe_float(user_data.get('v190'))],
            'v101': [safe_float(user_data.get('v101'))], 
            'b19':  [safe_float(user_data.get('b19'))],
            'b4':   [safe_float(user_data.get('b4'))],
            'bord': [safe_float(user_data.get('bord'))]
        }
        df = pd.DataFrame(features_dict)
        print(f"DEBUG: Extracted features for prediction: {df.columns.tolist()} with values {df.values.tolist()}", flush=True)
        return df

    def run_predictions(self, user_data: dict) -> dict:
        """
        Runs the feature DataFrame through each loaded XGBoost model and returns probabilities.
        """
        df_input = self.extract_features(user_data)
        results = {}
        
        print(f"DEBUG: Running predictions for {len(self.models)} models", flush=True)
        for vaccine_name, model in self.models.items():
            try:
                # predict_proba returns array of probabilities for each class
                # Index 1 is the probability of the positive class (i.e. missing the vaccine)
                # We use .values to pass a pure numpy array to avoid feature_names mismatch errors
                prob_arr = model.predict_proba(df_input.values)
                prob = prob_arr[0][1]
                results[vaccine_name] = float(prob)
                print(f"DEBUG: Success for {vaccine_name}: {prob}", flush=True)
            except Exception as e:
                print(f"DEBUG: Error predicting for {vaccine_name}: {e}", flush=True)
                results[vaccine_name + "_error"] = str(e)
            
        print(f"DEBUG: Final results keys: {list(results.keys())}", flush=True)
        return results

# Singleton instance
prediction_service = PredictionService()
