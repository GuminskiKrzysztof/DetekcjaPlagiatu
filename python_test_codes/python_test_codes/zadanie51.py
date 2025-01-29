class Zespolona:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def podziel(self,obiekt):
        rzeczywista = (self.x*obiekt.x - self.y*obiekt.y)/(obiekt.x*obiekt.x + obiekt.y*obiekt.y)
        urojona = (self.y*obiekt.x + self.x*obiekt.y)/(obiekt.x*obiekt.x + obiekt.y*obiekt.y)
        print("Iloczyn wynosi " + str(rzeczywista) + " + i" + str(urojona))
l1 = Zespolona(1,1)
l2 = Zespolona(3,2)
l2.podziel(l1)
