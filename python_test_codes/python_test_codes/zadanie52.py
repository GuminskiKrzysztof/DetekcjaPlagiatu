import math
class Zespolona:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def modul(self):
        modul = math.sqrt(self.x*self.x + self.y*self.y)
        print("Modul wynosi " + str(modul))
l = Zespolona(3,4)
l.modul()
