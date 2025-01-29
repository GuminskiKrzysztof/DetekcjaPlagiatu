class Zespolona:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def dodaj(self,obiekt):
        rzeczywista = self.x + obiekt.x
        urojona = self.y + obiekt.y
        print("Suma wynosi " + str(rzeczywista) + " + i" + str(urojona))
l1 = Zespolona(11,1)
l2 = Zespolona(3,7)
l2.dodaj(l1)
