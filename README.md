# Child Vaccination Prediction System

A research-oriented, full-stack application for predicting missing child vaccinations based on demographic data. Built with Clean Architecture principles, ensuring scalability and modularity.

## Architecture

The system follows a strict modular structure separating concerns across different layers:

- **Routes (`routes/`)**: Handles HTTP requests, payload parsing, and returning JSON responses.
- **Services (`services/`)**: Contains the core business logic.
  - `prediction_service.py`: Dynamically loads ML models from `model_files/`, extracts demographic features, and runs predictions.
  - `risk_service.py`: Evaluates probabilities to assign risk tiers (LOW/MEDIUM/HIGH).
- **Models (`models/`)**: SQLAlchemy ORM models defining the database schema.
- **Model Files (`model_files/`)**: Directory containing serialized machine learning models (currently supports JSON format) loaded dynamically at runtime.
- **Frontend (`templates/`, `static/`)**: Clean HTML UI and modular vanilla JavaScript to communicate with the REST API.

## Requirements

Ensure you have Python 3.8+ and MySQL installed. 

Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Database Setup

1. Open your MySQL client or command line.
2. Run the provided schema file to initialize the database and tables:
```bash
mysql -u root -p < schema.sql
```
*(Enter your MySQL password when prompted)*

## Configuration

The application uses environment variables for configuration. If not set, it defaults to a local MySQL instance: `mysql+pymysql://root:MyNewPass@localhost/vacc_pred`.

To override this default, set the `DATABASE_URL` environment variable:

**Windows (PowerShell):**
```powershell
$env:DATABASE_URL="mysql+pymysql://<user>:<password>@<host>/vacc_pred"
```

**Linux/Mac:**
```bash
export DATABASE_URL="mysql+pymysql://<user>:<password>@<host>/vacc_pred"
```

## Running the Application

Start the Flask development server:
```bash
python app.py
```

The application will be available at `http://localhost:5000/`.

## Future Extensibility

This system is built with future requirements in mind:
1. **Model Upgrades**: The `PredictionService` is designed modularly. If you need to replace the JSON models with XGBoost `.json` or PyTorch `.pt` files, simply update the `load_models` and `run_predictions` methods in `prediction_service.py` without touching the route layer.
2. **Authentication**: Can be easily added by protecting the `vaccination_bp` blueprint in `routes`.
3. **Mobile API Integrations**: The `/api/vaccination` endpoint strictly consumes and produces JSON, acting decoupled from the web UI.
