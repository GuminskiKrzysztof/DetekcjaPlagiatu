from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import pandas as pd

app = Flask(__name__)

# 1. Ścieżki do zapisanych modeli i danych
MODEL_PATH = "trained_model"
CSV_PATH = "all_codes.csv"

# 2. Wczytaj tokenizer i model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

# 3. Odtwórz LabelEncoder z pliku CSV
data = pd.read_csv(CSV_PATH)
label_encoder = LabelEncoder()
label_encoder.fit(data["category"])

MODEL_PATH2 = "c_code_classification"
CSV_PATH2 = "all_codes_c.csv"

tokenizer2 = AutoTokenizer.from_pretrained(MODEL_PATH2)
model2 = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH2)

data2 = pd.read_csv(CSV_PATH2)
label_encoder2 = LabelEncoder()
label_encoder2.fit(data2["category"])


def predict_category(code_snippet):
    """
    Funkcja przyjmuje fragment kodu i zwraca przewidywaną kategorię w formacie string.
    """
    # Tokenizacja wejściowego kodu
    inputs = tokenizer(code_snippet, truncation=True, padding="max_length", max_length=512, return_tensors="pt")
    # Przewidywanie modelu
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_label = logits.argmax(dim=1).item()  # Pobierz indeks klasy
    # Mapowanie indeksu na nazwę kategorii
    category = label_encoder.inverse_transform([predicted_label])[0]
    return category

def predict_category_c(code_snippet):
    """
    Funkcja przyjmuje fragment kodu i zwraca przewidywaną kategorię w formacie string.
    """
    # Tokenizacja wejściowego kodu
    inputs = tokenizer2(code_snippet, truncation=True, padding="max_length", max_length=512, return_tensors="pt")
    # Przewidywanie modelu
    outputs = model2(**inputs)
    logits = outputs.logits
    predicted_label = logits.argmax(dim=1).item()  # Pobierz indeks klasy
    # Mapowanie indeksu na nazwę kategorii
    category = label_encoder2.inverse_transform([predicted_label])[0]
    return category
@app.route('/predict_category', methods=['POST'])
def evaluate_text():
    data = request.get_json()
    code = data.get("code", "")
    predicted_category = predict_category(code)

    return {"Przewidywana kategoria: ": predicted_category}

@app.route('/search_codes', methods=['POST'])
def search_codes():
    data = request.get_json()
    category = data.get("category", "")
    all_codes = pd.read_csv("all_codes.csv")
    specfic_codes = all_codes[all_codes['category'] == category]
    codes_list = specfic_codes.to_dict(orient="records")
    return {"Codes: ": codes_list}

@app.route('/predict_category_c', methods=['POST'])
def evaluate_text_c():
    data = request.get_json()
    code = data.get("code", "")
    predicted_category = predict_category_c(code)

    return {"Przewidywana kategoria: ": predicted_category}

@app.route('/search_codes_c', methods=['POST'])
def search_codes_c():
    data = request.get_json()
    category = data.get("category", "")
    all_codes = pd.read_csv("all_codes_c.csv")
    specfic_codes = all_codes[all_codes['category'] == category]
    codes_list = specfic_codes.to_dict(orient="records")
    return {"Codes: ": codes_list}

if __name__ == "__main__":
    app.run(debug=True)