def boyerMoore(tekst, wzorzec):
    wystapienia = 0
    ostatnie = {}
    for klucz,wartosc in enumerate(wzorzec):
        ostatnie[wartosc] = klucz
    i = len(wzorzec) - 1
    while i < len(tekst):
        j = len(wzorzec) - 1
        k = i
        while j >= 0 and wzorzec[j] == tekst[k]:
            j = j - 1
            k = k - 1
        if j == -1:
            print("Wzorzec występuje w tekscie na pozycji " + str(k+1))
            wystapienia = wystapienia + 1
            i = i + len(wzorzec)
        else:
            i = i + len(wzorzec) - min(j,1 + ostatnie.get(tekst[i],-1))
    if wystapienia == 0:
        print("Brak wzorca w tekscie")



tekst = input("Podaj tekst,w ktorym bedzie poszukiwany wzorzec:")
wzorzec = input("Podaj wzorzec: ")
boyerMoore(tekst, wzorzec)
