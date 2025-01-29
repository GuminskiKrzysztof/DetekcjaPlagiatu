import random

def wymieszajListe(lista):
    random.shuffle(lista)
    return(lista[0])

file = open("dane.txt", "r")
lista1 = file.read().split("\n")
lista1.pop()
print(lista1)
wymieszajListe(lista1)
