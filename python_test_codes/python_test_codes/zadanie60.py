import math
class Kolo:
    def __init__(self,promien):
        self.promien = promien
    def pole(self):
        print("Pole:" + str(math.pi*self.promien*self.promien))
    def obwod(self):
        print("Pole:" + str(2*math.pi*self.promien))
    def dlugoscOkregu(self):
        print("Dlugosc okregu :" + str(2*math.pi*self.promien))
k1 = Kolo(3)
k1.pole()
k1.obwod()
k1.dlugoscOkregu()
