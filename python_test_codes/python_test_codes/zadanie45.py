from datetime import date
dzien = int(input("Podaj dzien: "))
miesiac = int(input("Podaj, ktory miesiac: "))
rok = int(input("Podaj rok: "))
data = date(rok, miesiac, dzien)
print(data)
