import os
import re

from difflib import SequenceMatcher
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Funkcja do czyszczenia kodu (usuwanie komentarzy, białych znaków)
def clean_code(code, language='python'):
    if language == 'python':
        code = re.sub(r'#.*', '', code)  # Usuwanie komentarzy
        code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)  # Usuwanie docstringów
    code = re.sub(r'\s+', ' ', code)  # Usuwanie nadmiarowych spacji
    return code.strip()


# Funkcja do porównywania kodu za pomocą miary Levenshteina
def levenshtein_similarity(code1, code2):
    return SequenceMatcher(None, code1, code2).ratio()


# Funkcja do porównywania kodu za pomocą Jaccarda
def jaccard_similarity(code1, code2):
    tokens1 = set(code1.split())
    tokens2 = set(code2.split())
    return len(tokens1.intersection(tokens2)) / len(tokens1.union(tokens2))


# Funkcja do porównywania kodu za pomocą CountVectorizer
def vector_similarity(code1, code2):
    vectorizer = CountVectorizer().fit_transform([code1, code2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0, 1]




# Przykład porównania plików
if __name__ == '__main__':
    code1 = clean_code(open('file1.py').read())
    code2 = clean_code(open('file2.py').read())

    print("Levenshtein similarity:", levenshtein_similarity(code1, code2))
    print("Jaccard similarity:", jaccard_similarity(code1, code2))
    print("Vector similarity:", vector_similarity(code1, code2))
