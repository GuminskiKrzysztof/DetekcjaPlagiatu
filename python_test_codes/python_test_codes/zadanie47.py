import datetime
def znajdzPoniedzialek(rok, numerTygodnia):
    pierszyDzienRoku = datetime.date(rok,1,1)
    roznicaDni = (7 - pierszyDzienRoku.weekday() + 1)%7
    pierwszyPoniedzialek = pierszyDzienRoku + datetime.timedelta(days=roznicaDni)
    szukanyPoniedzialek = pierwszyPoniedzialek + datetime.timedelta(weeks=(numerTygodnia-1))
    return szukanyPoniedzialek

rok = int(input("Podaj rok: "))
nrTyg = int(input("Podaj numer tygodnia: "))
data = znajdzPoniedzialek(rok,nrTyg)
print(data)
