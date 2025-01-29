import sys
import os
from backend.services import CodeCategorizationService
import pandas as pd

# Dodaj ścieżkę do folderu 'code_s'
sys.path.append(os.path.abspath('../code_similarities'))

# Teraz możesz zaimportować funkcje z code_similarities.py
from model.code_similarities.similarity import *

python_service = CodeCategorizationService(
    model_path="model/models_ai/trained_model",
    csv_path="model/data/all_python_codes.csv"
)

cpp_service = CodeCategorizationService(
    model_path="model/models_ai/c_code_classification",
    csv_path="model/data/all_cpp_codes.csv"
)


#def predict_category_python():
#    code = data.get("code", "")
#    # predicted_category = python_service.predict_category(code)
#    # return jsonify({"Predicted Category": predicted_category})
#    return

#def search_codes_python():
#    category = data.get("category", "")
#    # matching_codes = python_service.search_codes_by_category(category)
#    return jsonify({"Codes": pd.read_csv("model/data/all_python_codes.csv")})

def python_information(code):
    plagiarism = False
    predicted_category = python_service.predict_category(code)
    print(predicted_category)
    matching_codes = python_service.search_codes_by_category(predicted_category)
    plagiarism_probalities = []
    max_probality = 0
    max_index = -1
    i = 0
    for single_code in matching_codes:
        check_code = single_code['code']
        print(check_code)
        plagiarism_probality = similarity(code, check_code)
        plagiarism_probalities.append(plagiarism_probality)
        if plagiarism_probality > max_probality:
            max_probality = plagiarism_probality
            max_index = i
        i = i + 1
    if max_probality > 0.5:
        plagiarism = True
    print({"Information: ": [plagiarism, max_probality, matching_codes[max_index]]})

def cpp_information(code):
    plagiarism = False
    predicted_category = cpp_service.predict_category(code)
    print(predicted_category)
    matching_codes = cpp_service.search_codes_by_category(predicted_category)
    plagiarism_probalities = []
    max_probality = 0
    max_index = -1
    i = 0
    for single_code in matching_codes:
        check_code = single_code['code']
        print(check_code)
        plagiarism_probality = similarity(code, check_code)
        plagiarism_probalities.append(plagiarism_probality)
        if plagiarism_probality > max_probality:
            max_probality = plagiarism_probality
            max_index = i
        i = i + 1
    if max_probality > 0.5:
        plagiarism = True
    print({"Information: ": [plagiarism, max_probality, matching_codes[max_index]]})

code1 = """
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import pandas as pd


class CodeCategorizationService:

    def __init__(self, model_path, csv_path):
        # Inicjalizacja modelu i tokenizerów
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        
"""

cpp_information(code1)