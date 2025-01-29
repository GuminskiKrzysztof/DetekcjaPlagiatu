class Operacja:
    def pow(self,x,n):
        wynik = 1
        for y in range(n):
            wynik = wynik * x
        return wynik
op = Operacja()
pow = op.pow(10,3)
print(pow)
