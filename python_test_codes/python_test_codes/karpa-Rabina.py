def h(x):
    wartosc = 0
    modulo = 107
    z = 271
    for litera in x:
       wartosc = (wartosc * z + ord(litera)) % modulo
    return wartosc

def karpaRabina(tekst, wzorzec):
    wystepowanie = 0
    hWzor = h(wzorzec)
    for i in range(len(tekst) - len(wzorzec) + 1):
        przedzial = tekst[i:i+len(wzorzec)]
        hPrzedzial = h(przedzial)
        if hWzor == hPrzedzial:
            print("Wzorzec występuje w tekscie na pozycji " + str(i))
            wystepowanie = wystepowanie + 1
    if wystepowanie==0:
        print("Brak wzorca w tekscie")

tekst = input("Podaj tekst,w ktorym bedzie poszukiwany wzorzec:")
wzorzec = input("Podaj wzorzec: ")
karpaRabina(tekst, wzorzec)
