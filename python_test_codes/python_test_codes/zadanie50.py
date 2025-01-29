class Zespolona:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def pomnoz(self,obiekt):
        rzeczywista = self.x*obiekt.x - self.y*obiekt.y
        urojona = self.x*obiekt.y + self.y*obiekt.x
        print("Iloczyn wynosi " + str(rzeczywista) + " + i" + str(urojona))
l1 = Zespolona(11,1)
l2 = Zespolona(3,7)
l2.pomnoz(l1)
