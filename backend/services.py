from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import pandas as pd


class CodeCategorizationService:
    """
    Klasa do obsługi predykcji i wyszukiwania kodów Python i C++.
    """
    def __init__(self, model_path, csv_path):
        # Inicjalizacja modelu i tokenizerów
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.data = pd.read_csv(csv_path)
        self.label_encoder = LabelEncoder().fit(self.data["category"])

    def predict_category(self, code_snippet):
        """
        Przewiduje kategorię dla fragmentu kodu.
        """
        inputs = self.tokenizer(code_snippet, truncation=True, padding="max_length", max_length=512, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_label = logits.argmax(dim=1).item()
        category = self.label_encoder.inverse_transform([predicted_label])[0]
        return category

    def search_codes_by_category(self, category):
        """
        Wyszukuje kody w pliku CSV na podstawie kategorii.
        """
        matching_codes = self.data[self.data["category"] == category]
        return matching_codes.to_dict(orient="records")
