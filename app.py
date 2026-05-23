from flask import Flask, render_template, request
import models_engineering as ml_core

app = Flask(__name__)


try:
    models_metrics = ml_core.train_all_models()
    print("[INIT SUCCESS] Machine learning models trained and decoupled from app routes.")
except Exception as e:
    print(f"[INIT ERROR] Failed to load data or train models: {e}")
    models_metrics = {}

@app.route('/')
def prinpage():
    return render_template('index.html')

@app.route('/information')
def information():
    return render_template('info.html')

@app.route('/conceps')
def conceps():
    return render_template('conceps.html')

@app.route('/classification', methods=['GET', 'POST'])
def classification():
    return render_template('classification.html')

@app.route('/data_engineering')
def data_engineering():
    return render_template('data_engineering.html')

@app.route('/data_understanding')
def data_understanding():
    return render_template('data_understanding.html')


@app.route('/model_development', methods=['GET', 'POST'])
def model_development():
    prediction_result = None
    selected_model = None
    user_inputs = None
    
    if request.method == 'POST':
        try:
            # 1. Capture inputs from form elements
            net_youth_migration = float(request.form['net_youth_migration'])
            median_age = float(request.form['median_age'])
            indigenous_pop_ratio = float(request.form['indigenous_pop_ratio'])
            primary_poverty_index = float(request.form['primary_poverty_index'])
            annual_festivals_count = float(request.form['annual_festivals_count'])
            active_cultural_groups = float(request.form['active_cultural_groups'])
            subsidized_cultural_budget = float(request.form['subsidized_cultural_budget'])
            
            selected_model = request.form['model_choice']
            
            features_list = [
                net_youth_migration, 
                median_age, 
                indigenous_pop_ratio, 
                primary_poverty_index, 
                annual_festivals_count, 
                active_cultural_groups, 
                subsidized_cultural_budget
            ]
            
         
            prediction_result = ml_core.predict_cultural_risk(selected_model, features_list)
            
            user_inputs = {
                "Net Youth Migration": net_youth_migration,
                "Median Age": median_age,
                "Indigenous Pop Ratio": indigenous_pop_ratio,
                "Primary Poverty Index": primary_poverty_index,
                "Annual Festivals Count": annual_festivals_count,
                "Active Cultural Groups": active_cultural_groups,
                "Subsidized Cultural Budget": subsidized_cultural_budget
            }
            
           
            print("\n=== CONSOLE PREDICTION EXAMPLE ===")
            print(f"Selected Algorithm: {selected_model}")
            print(f"Features Array Matrix: {features_list}")
            print(f"Output Categorical Prediction: {prediction_result}")
            print("==================================\n")
            
        except Exception as error:
            prediction_result = f"Inference Error: {error}"
            print(f"[ERROR ENGINE] {error}")

   
    return render_template(
        'model_development.html',
        metrics=models_metrics,
        prediction=prediction_result,
        chosen_model=selected_model,
        inputs_sent=user_inputs
    )

if __name__ == '__main__':
    app.run(debug=True)