def kodowanieSF(alfabet, prawdobodopienstwa, ciagDoZakodowania):
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
    slowaKodowe = ["" for x in range(len(prawdobodopienstwa))]
    ciagi = []
    ciagi.append(alfabet)
    suma = 0
    sumy = []
    i = 0
    najlepszePraSum = 0
    najmniejszaRoznica = 1
    indeks = 0
    ciag1 = []
    ciag2 = []
    while len(ciagi) < len(alfabet):
        indeks = 0
        newciagi = []
        for ciag in ciagi:
            if len(ciag) != 1:
                sumy = []
                najlepszePraSum = 0
                najmniejszaRoznica = 1
                i = 0
                while i < len(ciag):
                    suma = 0
                    for x in range(indeks,i+1):
                        suma = suma + prawdobodopienstwa[x]
                    sumy.append(suma)
                    i = i + 1
                for x in range(len(sumy)):
                    if (sumy[x] - (sumy[-1]/2)) < najmniejszaRoznica:
                        najmniejszaRoznica = sumy[x] - (sumy[-1]/2)
                        najlepszePraSum = x
                if sumy[najlepszePraSum] < (sumy[-1]/2):
                    for x in range(indeks, indeks + najlepszePraSum + 1):
                        slowaKodowe[x] = slowaKodowe[x] + "1"
                    for x in range(indeks + najlepszePraSum + 1, indeks + len(ciag)):
                        slowaKodowe[x] = slowaKodowe[x] + "0"
                else:
                    for x in range(indeks, indeks + najlepszePraSum + 1):
                        slowaKodowe[x] = slowaKodowe[x] + "0"
                    for x in range(indeks + najlepszePraSum + 1, indeks + len(ciag)):
                        slowaKodowe[x] = slowaKodowe[x] + "1"
                ciag1 = []
                for x in range(indeks, indeks + najlepszePraSum + 1):
                    ciag1.append(alfabet[x])
                ciag2 = []
                for x in range(indeks + najlepszePraSum + 1, indeks + len(ciag)):
                    ciag2.append(alfabet[x])
                newciagi.append(ciag1)
                newciagi.append(ciag2)
            else:
                newciagi.append(ciag)
            indeks = indeks + len(ciag)
        ciagi = newciagi
    for x in range(len(slowaKodowe)):
        print(alfabet[x] + ": " + slowaKodowe[x])
    zakodowany = ""
    for x in ciagDoZakodowania:
        for y in range(len(alfabet)):
            if x == alfabet[y]:
                zakodowany = zakodowany + slowaKodowe[y]
    print("Zakodowany ciag: ")
    print(zakodowany)
ciagDoZakodowania = "ADBAC"
kodowanieSF(["A","B","C","D"], [0.3,0.4,0.1,0.2],ciagDoZakodowania)

