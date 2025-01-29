import math
x = float(input("Podaj czesc rzeczywista: "))
y = float(input("Podaj czesc urojona: "))

luk = abs(math.atan(y/x))
print("Dlugosc luku wynosi " + str(luk))
