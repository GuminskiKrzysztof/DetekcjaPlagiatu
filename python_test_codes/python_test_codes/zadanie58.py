def naRzymski(liczba):
    rzymskieSymbole = {"M":1000, "CM":900, "D":500, "CD":400, "C":100,"XC":90,"L":50,"XL":40, "X":10,"IX":9,"V":5,
                        "IV":4,"I":1}
    liczbaRzymska = ""
    for symbol, wartosc in rzymskieSymbole.items():
        while liczba >= wartosc:
            liczbaRzymska += symbol
            liczba -= wartosc
    print(liczbaRzymska)
naRzymski(719)

