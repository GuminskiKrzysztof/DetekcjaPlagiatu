from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# 1. Ścieżki do zapisanych modeli i danych
MODEL_PATH = "C:/Users/k.guminski/PycharmProjects/plagiatDet/DetekcjaPlagiatu/trained_model"
CSV_PATH = "C:/Users/k.guminski/PycharmProjects/plagiatDet/DetekcjaPlagiatu/all_codes.csv"

# 2. Wczytaj tokenizer i model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

# 3. Odtwórz LabelEncoder z pliku CSV
data = pd.read_csv(CSV_PATH)
label_encoder = LabelEncoder()
label_encoder.fit(data["category"])

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

# 5. Testowanie przewidywania
if __name__ == "__main__":
    # Przykładowy fragment kodu do klasyfikacji
    sample_code = """def example_function():\n    print('Hello, World!')"""
    predicted_category = predict_category(sample_code)
    print(f"Przewidywana kategoria: {predicted_category}")


