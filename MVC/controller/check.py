import sys
import os
from backend.services import CodeCategorizationService
import pandas as pd

# Dodaj ścieżkę do folderu 'code_s'
sys.path.append(os.path.abspath('../code_similarities'))

# Teraz możesz zaimportować funkcje z code_similarities.py
from code_similarities.similarity import *

python_service = CodeCategorizationService(
    model_path="backend/models/trained_model",
    csv_path="backend/data/all_python_codes.csv"
)

cpp_service = CodeCategorizationService(
    model_path="backend/models/c_code_classification",
    csv_path="backend/data/all_cpp_codes.csv"
)


#def predict_category_python():
#    code = data.get("code", "")
#    # predicted_category = python_service.predict_category(code)
#    # return jsonify({"Predicted Category": predicted_category})
#    return

#def search_codes_python():
#    category = data.get("category", "")
#    # matching_codes = python_service.search_codes_by_category(category)
#    return jsonify({"Codes": pd.read_csv("backend/data/all_python_codes.csv")})

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

code1 = """#include <bits/stdc++.h> 
using namespace std; 
  
// Driver Code 
int main() 
{ 
  
    // Variables 
    auto an_int = 26; 
    auto a_bool = false; 
    auto a_float = 26.24; 
    auto ptr = &a_float; 
  
    // Print typeid 
    cout << typeid(a_bool).name() << "\n"; 
    cout << typeid(an_int).name() << "\n"; 
    return 0; 
}
"""

cpp_information(code1)