def analizuj_plagiat_kodu2(fragment_kodu):
    # Przykładowa logika analizy
    if "def" in fragment_kodu:
        print("Zawiera definicje funkcji")
    else:
        print("Brak definicji funkcji")

fragment2 = "def my_function():\n    print('Hello World')"
analizuj_plagiat_kodu2(fragment2)
