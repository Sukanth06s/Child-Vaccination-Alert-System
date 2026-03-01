from flask import Blueprint, request, jsonify
from datetime import datetime
import pandas as pd
from sqlalchemy import text
from models.db_models import db, UserInput, Prediction
from services.prediction_service import prediction_service
from services.risk_service import RiskService

vaccination_bp = Blueprint('vaccination_api', __name__)

@vaccination_bp.route('/health', methods=['GET'])
def health_check():
    try:
        models_loaded = list(prediction_service.models.keys())
        # Check DB connection
        db.session.execute(text('SELECT 1'))
        return jsonify({
            "status": "online",
            "models_count": len(models_loaded),
            "models": models_loaded,
            "db_connection": "healthy"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@vaccination_bp.route('/vaccination', methods=['POST'])
def process_vaccination():
    try:
        print("DEBUG: Received request at /api/vaccination", flush=True)
        data = request.json
        if not data:
            print("DEBUG: No payload provided", flush=True)
            return jsonify({"error": "No payload provided."}), 400

            
        # Parse DOB
        dob_str = data.get('dob')
        try:
            if dob_str and str(dob_str).strip() != '':
                dob_date = datetime.strptime(str(dob_str).strip(), '%Y-%m-%d').date()
            else:
                dob_date = datetime.utcnow().date()
        except Exception:
            dob_date = datetime.utcnow().date()
            
        # Helper to handle empty strings for integer db columns
        def safe_int(val):
            return None if val == '' or pd.isna(val) else val

        # 1. Create UserInput record
        user_input = UserInput(
            child_name=data.get('childName', 'Unknown'),
            dob=dob_date,
            father_name=data.get('fatherName'),
            mother_name=data.get('motherName'),
            v012=safe_int(data.get('v012')),
            v106=safe_int(data.get('v106')),
            v190=safe_int(data.get('v190')),
            v025=safe_int(data.get('v025')),
            v101=data.get('v101'),
            v155=safe_int(data.get('v155')),
            v157=safe_int(data.get('v157')),
            v158=safe_int(data.get('v158')),
            v159=safe_int(data.get('v159')),
            v467d=safe_int(data.get('v467d')),
            v481=safe_int(data.get('v481')),
            b19=safe_int(data.get('b19')),
            b4=safe_int(data.get('b4')),
            b5=safe_int(data.get('b5')),
            bord=safe_int(data.get('bord')),
            h1=safe_int(data.get('h1')),
            v113=data.get('v113'),
            v116=data.get('v116'),
            m14=safe_int(data.get('m14')),
            m15=safe_int(data.get('m15')),
            m17=safe_int(data.get('m17')),
            m18=safe_int(data.get('m18')),
            h2=safe_int(data.get('h2', 0)),
            h0=safe_int(data.get('h0', 0)),
            h50=safe_int(data.get('h50', 0)),
            h3=safe_int(data.get('h3', 0)),
            h4=safe_int(data.get('h4', 0)),
            h5=safe_int(data.get('h5', 0)),
            h6=safe_int(data.get('h6', 0)),
            h7=safe_int(data.get('h7', 0)),
            h8=safe_int(data.get('h8', 0)),
            h9=safe_int(data.get('h9', 0)),
            h9a=safe_int(data.get('h9a', 0)),
            h51=safe_int(data.get('h51', 0)),
            h52=safe_int(data.get('h52', 0)),
            h53=safe_int(data.get('h53', 0)),
            h57=safe_int(data.get('h57', 0)),
            h58=safe_int(data.get('h58', 0)),
            h59=safe_int(data.get('h59', 0)),
            h61=safe_int(data.get('h61', 0)),
            h62=safe_int(data.get('h62', 0)),
            h63=safe_int(data.get('h63', 0))
        )
        db.session.add(user_input)
        db.session.commit()
        
        # 2. Extract features and run predictions
        print("DEBUG: Running PredictionService.run_predictions...", flush=True)
        raw_results = prediction_service.run_predictions(data)
        
        # 3. Filter and save results
        vax_status_map = {
            'bcg': 'h2', 'polio0': 'h0', 'hepbbirth': 'h50',
            'dpt1': 'h3', 'dpt2': 'h5', 'dpt3': 'h7',
            'polio1': 'h4', 'polio2': 'h6', 'polio3': 'h8',
            'measles1': 'h9', 'measles2': 'h9a',
            'penta1': 'h51', 'penta2': 'h52', 'penta3': 'h53',
            'rota1': 'h57', 'rota2': 'h58', 'rota3': 'h59',
            'hepb1': 'h61', 'hepb2': 'h62', 'hepb3': 'h63'
        }

        final_predictions = []
        for res in raw_results:
            vaccine = res['vaccine_name']
            h_field = vax_status_map.get(vaccine)
            
            # Skip if already taken
            if h_field and safe_int(data.get(h_field)) == 1:
                continue

            # Save prediction to DB
            prediction = Prediction(
                user_id=user_input.id,
                vaccine_name=vaccine,
                miss_probability=res['probability'],
                risk_level=res['confidence_level'].upper()
            )
            db.session.add(prediction)
            final_predictions.append(res)
            
        db.session.commit()
        
        return jsonify({
            "message": "Data processed successfully",
            "predictions": final_predictions
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
