import os
import numpy as np
import xgboost as xgb
import pandas as pd

# Path to model_files dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, 'datasetfinal')

class PredictionService:
    def __init__(self):
        self.models = {}
        # Define strict feature mappings for each vaccine model
        self.generic_features = ["v012", "v106", "v190", "v025", "v101", "b4", "bord", "m14", "m15", "m17", "m18", "h1", "v113", "v116"]
        
        self.feature_map = {
            "bcg": self.generic_features,
            "polio0": self.generic_features,
            "hepbbirth": self.generic_features,
            "dpt1": self.generic_features + ["h2", "h0", "h50"],
            "polio1": self.generic_features + ["h2", "h0", "h50"],
            "penta1": self.generic_features + ["h2", "h0", "h50"],
            "hepb1": self.generic_features + ["h2", "h0", "h50"],
            "rota1": self.generic_features + ["h2", "h0", "h50"],
            "dpt2": self.generic_features + ["v157", "v158", "v159", "h3"],
            "polio2": self.generic_features + ["v157", "v158", "v159", "h4"],
            "penta2": self.generic_features + ["v157", "v158", "v159", "h51"],
            "hepb2": self.generic_features + ["v157", "v158", "v159", "h61"],
            "rota2": self.generic_features + ["v157", "v158", "v159", "h57"],
            "dpt3": self.generic_features + ["h3", "h5", "v467d"],
            "polio3": self.generic_features + ["h0", "h4", "h6", "v467d"],
            "penta3": self.generic_features + ["h51", "h52", "v467d"],
            "hepb3": self.generic_features + ["h50", "h61", "h62", "v467d"],
            "rota3": self.generic_features + ["h57", "h58", "v467d"],
            "measles1": self.generic_features + ["v481", "h7", "h8", "h53", "h63", "h59"],
            "measles2": self.generic_features + ["v155", "v481", "h7", "h8", "h53", "h63", "h59", "h9"]
        }
        self.load_models()
        
    def load_models(self):
        if not os.path.exists(MODEL_DIR):
            print(f"DEBUG: MODEL_DIR {MODEL_DIR} does not exist", flush=True)
            return
            
        failed_models = []
        target_vaccines = list(self.feature_map.keys())

        for vaccine in target_vaccines:
            filename = f"{vaccine}.json"
            filepath = os.path.join(MODEL_DIR, filename)
            if os.path.exists(filepath):
                try:
                    model = xgb.XGBClassifier()
                    model.load_model(filepath)
                    self.models[vaccine] = model
                except Exception as e:
                    failed_models.append(vaccine)
            else:
                failed_models.append(vaccine)

        loaded_count = len(self.models)
        total_expected = len(target_vaccines)

        if not failed_models:
            print(f"DEBUG: All models loaded successfully. Total models loaded: {loaded_count}", flush=True)
        else:
            print(f"DEBUG: Some models loaded successfully ({loaded_count}/{total_expected}), some failed to load: {', '.join(failed_models)}", flush=True)

    def get_confidence(self, prob):
        if prob < 0.4: return "Low"
        if prob < 0.7: return "Medium"
        return "High"

    def run_predictions(self, user_data: dict) -> list:
        results = []
        
        # Helper to convert to float safely
        def safe_float(val):
            try:
                if val is None or val == '': return 0.0
                return float(val)
            except (ValueError, TypeError):
                return 0.0

        for vaccine, features in self.feature_map.items():
            if vaccine not in self.models:
                continue
                
            try:
                # Prepare feature array in strict order
                vals = [safe_float(user_data.get(f)) for f in features]
                df_input = pd.DataFrame([vals], columns=features)
                
                print(f"DEBUG: Prediction Input for {vaccine}: {vals}", flush=True)
                
                model = self.models[vaccine]
                prob_arr = model.predict_proba(df_input.values)
                prob = float(prob_arr[0][1])
                
                results.append({
                    "vaccine_name": vaccine,
                    "prediction": 1 if prob >= 0.35 else 0, # Match training threshold
                    "probability": round(prob * 100, 2),
                    "confidence_level": self.get_confidence(prob)
                })
            except Exception as e:
                print(f"DEBUG: Error predicting for {vaccine}: {e}", flush=True)
            
        return results

# Singleton instance
prediction_service = PredictionService()
