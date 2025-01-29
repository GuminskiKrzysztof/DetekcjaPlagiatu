def algorytmAWCG(m,j,k,tablica,ile):
    indeks = 0
    c=0
    oldtablica = []
    for x in range(ile):
        oldtablica = tablica.copy()
        indeks=x%k
        tablica[indeks] = (tablica[((k+indeks-j)%k)] + tablica[indeks] + c)%m
        if oldtablica[((k+indeks-j)%k)] + oldtablica[indeks] + c >= m:
            c=1
        else:
            c=0
    print(tablica)
algorytmAWCG(17,1,4,[0,1,2,3],12)
