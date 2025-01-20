from flask import Flask, render_template, request, jsonify
from backend.services import CodeCategorizationService
import pandas as pd

# Inicjalizacja usług
# python_service = CodeCategorizationService(
#     model_path="backend/models/trained_model",
#     csv_path="backend/data/all_python_codes.csv"
# )

# cpp_service = CodeCategorizationService(
#     model_path="backend/models/c_code_classification",
#     csv_path="backend/data/all_cpp_codes.csv"
# )

app = Flask(__name__)

# Obsługa frontendowych stron HTML
@app.route('/')
def home():
    return render_template('index.html', active_page='home')

@app.route('/jak-to-dziala')
def jak_to_dziala():
    return render_template('how-it-works.html', active_page='how-it-works')

@app.route('/o-nas')
def o_nas():
    return render_template('about-us.html', active_page='about-us')

@app.route('/dodaj-projekt')
def dodaj_projekt():
    return render_template('add-project.html', active_page='add-project')

@app.route('/edytor')
def edytor():
    return render_template('editor-code.html', active_page='analyze-code')

# Obsługa API dla kodów Python
@app.route('/predict_category_python', methods=['POST'])
def predict_category_python():
    data = request.get_json()
    code = data.get("code", "")
    # predicted_category = python_service.predict_category(code)
    # return jsonify({"Predicted Category": predicted_category})
    return jsonify({"Predicted Category": "test"})

@app.route('/search_codes', methods=['POST'])
def search_codes_python():
    data = request.get_json()
    category = data.get("category", "")
    # matching_codes = python_service.search_codes_by_category(category)
    # return jsonify({"Codes": matching_codes})
    return jsonify({"Codes": pd.read_csv("backend/data/all_python_codes.csv")})

# Obsługa API dla kodów C++
# @app.route('/predict_category_cpp', methods=['POST'])
# def predict_category_cpp():
#     data = request.get_json()
#     code = data.get("code", "")
#     predicted_category = cpp_service.predict_category(code)
#     return jsonify({"Predicted Category": predicted_category})

# @app.route('/search_codes_c', methods=['POST'])
# def search_codes_cpp():
#     data = request.get_json()
#     category = data.get("category", "")
#     matching_codes = cpp_service.search_codes_by_category(category)
#     return jsonify({"Codes": matching_codes})

if __name__ == '__main__':
    app.run(debug=True)
