from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset, DatasetDict
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd

data = pd.read_csv("all_codes.csv")

label_encoder = LabelEncoder()
data["label"] = label_encoder.fit_transform(data["category"])

train_texts, test_texts, train_labels, test_labels = train_test_split(
    data["code"], data["label"], test_size=0.2, random_state=42
)

train_dataset = Dataset.from_dict({"text": train_texts.tolist(), "label": train_labels.tolist()})
test_dataset = Dataset.from_dict({"text": test_texts.tolist(), "label": test_labels.tolist()})
dataset = DatasetDict({"train": train_dataset, "test": test_dataset})

model_name = "microsoft/codebert-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(data["category"].unique()))

# 6. Funkcja tokenizująca
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

# Tokenizuj dane
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 7. Parametry treningu
training_args = TrainingArguments(
    output_dir="./results",  # Katalog na wyniki
    evaluation_strategy="epoch",  # Ewaluacja po każdej epoce
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',  # Logi dla TensorBoard
    save_strategy="epoch",  # Zapis modelu po każdej epoce
    logging_steps=10,
    load_best_model_at_end=True,
)

# 8. Trener
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    tokenizer=tokenizer,
)

# 9. Trenuj model
trainer.train()

# 10. Zapisz model i tokenizer
model.save_pretrained("./codebert_model")
tokenizer.save_pretrained("./codebert_model")