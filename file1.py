def analizuj_plagiat_kodu1(fragment_kodu):
    # Przykładowa logika analizy
    if "import" in fragment_kodu:
        print("Zawiera importy")
    else:
        print("Brak importów")

fragment1 = "import numpy as np\nprint(np.array([1, 2, 3]))"
analizuj_plagiat_kodu1(fragment1)
