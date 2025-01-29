import math
iloscBokow = int(input("Podaj ilosc bokow: "))
dlugoscBoku = int(input("Podaj dlugosc pojedynczego boku: "))
pole = (iloscBokow*dlugoscBoku*dlugoscBoku)/(4*math.tan(math.pi/iloscBokow))
print("Pole wynosi " + str(pole))
