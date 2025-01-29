from flask import Blueprint, request, jsonify
from model.services import CodeCategorizationService
from model.code_similarities.similarity import similarity

api_bp = Blueprint('api', __name__)

python_service = CodeCategorizationService(
    model_path="model/models_ai/trained_model",
    csv_path="model/data/all_python_codes.csv"
)

cpp_service = CodeCategorizationService(
    model_path="model/models_ai/c_code_classification",
    csv_path="model/data/all_cpp_codes.csv"
)

@api_bp.route('/python_information', methods=['POST'])
def python_information():
    try:
        if not request.json or 'code' not in request.json:
            return jsonify({"error": "Brak kodu do analizy"}), 400

        code = request.json['code']
        if not code.strip():
            return jsonify({"error": "Kod nie może być pusty"}), 400

        plagiarism = False
        predicted_category = python_service.predict_category(code)
        matching_codes = python_service.search_codes_by_category(predicted_category)
        
        if not matching_codes:
            return jsonify({
                "Information: ": [False, 0, {"code": ""}]
            })

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
        return jsonify({
            "Information: ": [plagiarism, max_probality, matching_codes[max_index]]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/cpp_information', methods=['POST'])
def cpp_information():
    try:
        if not request.json or 'code' not in request.json:
            return jsonify({"error": "Brak kodu do analizy"}), 400

        code = request.json['code']
        if not code.strip():
            return jsonify({"error": "Kod nie może być pusty"}), 400

        plagiarism = False
        predicted_category = cpp_service.predict_category(code)
        matching_codes = cpp_service.search_codes_by_category(predicted_category)
        
        if not matching_codes:
            return jsonify({
                "Information: ": [False, 0, {"code": ""}]
            })

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
        return jsonify({
            "Information: ": [plagiarism, max_probality, matching_codes[max_index]]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
