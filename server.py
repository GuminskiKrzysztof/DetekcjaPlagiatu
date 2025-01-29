from flask import Flask, render_template, request, jsonify
from pydantic import BaseModel, ValidationError

app = Flask(__name__,template_folder='view/templates')


from model.services import CodeCategorizationService
import sys
import os
import pandas as pd

# Dodaj ścieżkę do folderu 'code_s'
sys.path.append(os.path.abspath('../code_similarities'))

# Teraz możesz zaimportować funkcje z code_similarities.py
from model.code_similarities.similarity import *

import warnings
warnings.filterwarnings('ignore')


#Inicjalizacja usług
python_service = CodeCategorizationService(
    model_path="model/models_ai/trained_model",
    csv_path="model/data/all_python_codes.csv"
)

cpp_service = CodeCategorizationService(
    model_path="model/models_ai/c_code_classification",
    csv_path="model/data/all_cpp_codes.csv"
)

class TextInput(BaseModel):
    text: str


# Obsługa frontendowych stron HTML
@app.route('/')
def home():
    return render_template('index.html', active_page='home')


@app.route('/jak-to-dziala')
def jak_to_dziala():
    return render_template('how-it-works.html', active_page='how-it-works')


#@app.route('/analizuj-kod')
#def analizuj_kod():
#    return render_template('analyze-code.html', active_page='analyze-code')


@app.route('/o-nas')
def o_nas():
    return render_template('about-us.html', active_page='about-us')


@app.route('/dodaj-projekt')
def dodaj_projekt():
    return render_template('add-project.html', active_page='add-project')


@app.route('/edytor')
def edytor():
    return render_template('editor-code.html', active_page='analyze-code')


@app.route('/python_information', methods=['POST'])
def python_information():
    code = request.json['code']
    plagiarism = False
    predicted_category = python_service.predict_category(code)
    matching_codes = python_service.search_codes_by_category(predicted_category)
    plagiarism_probalities = []
    max_probality = 0
    max_index = -1
    i = 0
    for single_code in matching_codes:
        check_code = single_code['code']
        plagiarism_probality = similarity(code, check_code)
        plagiarism_probalities.append(plagiarism_probality)
        if plagiarism_probality > max_probality:
            max_probality = plagiarism_probality
            max_index = i
        i = i + 1
    if max_probality > 0.5:
        plagiarism = True
    return {"Information: ": [plagiarism, max_probality, matching_codes[max_index]]}


@app.route('/cpp_information', methods=['POST'])
def cpp_information():
    code = request.json['code']
    plagiarism = False
    predicted_category = cpp_service.predict_category(code)
    matching_codes = cpp_service.search_codes_by_category(predicted_category)
    plagiarism_probalities = []
    max_probality = 0
    max_index = -1
    i = 0
    for single_code in matching_codes:
        check_code = single_code['code']
        plagiarism_probality = similarity(code, check_code)
        plagiarism_probalities.append(plagiarism_probality)
        if plagiarism_probality > max_probality:
            max_probality = plagiarism_probality
            max_index = i
        i = i + 1
    if max_probality > 0.5:
        plagiarism = True
    return {"Information: ": [plagiarism, max_probality, matching_codes[max_index]]}

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
