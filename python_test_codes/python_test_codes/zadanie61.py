class Tekst:
    def __init__(self, napis):
        self.napis = napis
    def operacja(self):
        lista = self.napis.rsplit()
        for x in range(len(lista)-1,-1,-1):
            print(lista[x], end=" ")

t1 = Tekst("Jestem studentem. Jestem studentem.")
t1.operacja()
