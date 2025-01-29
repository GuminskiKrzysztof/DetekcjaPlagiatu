from fractions import Fraction

liczba = float(input("Podaj liczbe w postaci dziesietnej: "))
ulamek = Fraction(liczba).limit_denominator()
print(ulamek)
