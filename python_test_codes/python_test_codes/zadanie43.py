def sortowanie(alfabet, prawdobodopienstwa):
    liczba = 0
    litera = ""
    zamiana = True
    while zamiana:
        zamiana = False
        for x in range(len(prawdobodopienstwa) - 1):
            if prawdobodopienstwa[x] < prawdobodopienstwa[x+1]:
                liczba = prawdobodopienstwa[x+1]
                prawdobodopienstwa[x+1] = prawdobodopienstwa[x]
                prawdobodopienstwa[x] = liczba
                litera = alfabet[x+1]
                alfabet[x + 1] = alfabet[x]
                alfabet[x] = litera
                zamiana = True

def kodowanieHuffmana(alfabet, prawdobodopienstwa, ciagDoZdekodowania):
    sortowanie(alfabet, prawdobodopienstwa)
    slownik = {}
    for x in alfabet:
        slownik[x] = ""
    p1 = 0
    p2 = 0
    ciag1 = []
    ciag2 = []
    alfabet2 = []
    for x in alfabet:
        alfabet2.append([x])
    while prawdobodopienstwa[0] != 1.0:
        sortowanie(alfabet2, prawdobodopienstwa)
        p1 = prawdobodopienstwa.pop()
        p2 = prawdobodopienstwa.pop()
        prawdobodopienstwa.append(p1+p2)
        ciag1 = alfabet2.pop()
        ciag2 = alfabet2.pop()
        for y in ciag1:
            for klucz in slownik:
                if y == klucz:
                    slownik[klucz] = slownik[klucz] + "1"
        for y in ciag2:
            for klucz in slownik:
                if y == klucz:
                    slownik[klucz] = slownik[klucz] + "0"
        alfabet2.append(ciag1 + ciag2)
    ostateczneKodowania = {}
    for klucz, wartosc in slownik.items():
        ostateczneKodowania[klucz] = ""
        for x in range(len(wartosc)-1,-1,-1):
            ostateczneKodowania[klucz] = ostateczneKodowania[klucz] + wartosc[x]
    for klucz, wartosc in ostateczneKodowania.items():
        print(klucz + ": " + wartosc)
    aktualnyCiag = ""
    zdekodowany = ""
    for x in ciagDoZdekodowania:
        aktualnyCiag = aktualnyCiag + x
        for klucz, wartosc in ostateczneKodowania.items():
            if aktualnyCiag == wartosc:
                zdekodowany = zdekodowany + klucz
                aktualnyCiag = ""
    print("Zdekodowany ciag: ")
    print(zdekodowany)
doZdekodowania = "10100000101"
kodowanieHuffmana(["A","B","C","D"], [0.3,0.4,0.1,0.2],doZdekodowania)

