from transformers import pipeline
import matplotlib.pyplot as plt
from googletrans import Translator

backupModel = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
model = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier", top_k=None)

def translate(string, lang=None):
    translator = Translator()
    return translator.translate(string, src=lang, dest='en').text

def textToEmotions(string):
    results = model(string)
    return {result['label']: result['score'] for result in results[0]}

def backupTextToEmotions(string):
    results = backupModel(string)
    return {result['label']: result['score'] for result in results[0]}

def dualModelPrediction(string):
    r1 = textToEmotions(string)
    r2 = backupTextToEmotions(string)
    return {label: (r1[label] + r2[label]) / 2 for label in r2}

input = input(">> ")
lang = "en" #w domyśle dajemy użytkownikowi opcje angielski, polski i inne(lang=None)
if lang != "en":
    input = translate(input, lang)
emotions = dualModelPrediction(input)
#print(emotions)
plt.figure(figsize=(10, 6))
plt.bar(emotions.keys(), emotions.values())
#plt.yscale('log')
plt.xlabel('Emotions')
plt.ylabel('Scores')
plt.title(f'"{input}"')
plt.show()
