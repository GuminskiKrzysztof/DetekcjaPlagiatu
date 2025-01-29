import numpy as np
import pandas as pd
import math
import re
from scipy.stats import norm


# Pobranie ramki danych z kodami wykorzystywanymi do doboru wartosci wag
# data2 = pd.read_csv("C:\\Users\\Admin\\Desktop\\codes_to_weights_choose.csv")

# Funkcje obliczajace wartosci podobienstwa miedzy tekstami

# Względna odległość Hamminga
def relative_hamming_distance(str1, str2):
    # Sprawdzenie, czy oba ciągi znaków są takie same
    if str1 == str2:
        print("Oba ciągi znaków są takie same.")
        return 1

    # Dostosowanie długości znaków, jeżeli ciągi znaków mają różną długość

    # Przypadek I: Drugi ciąg znaków jest dłuższy od pierwszego ciągu znaków
    if len(str1) < len(str2):
        for i in range(len(str2) - len(str1)):
            str1 += "|"
    # Przypadek II: Pierwszy ciąg znaków jest dłuższy od drugiego ciągu znaków
    elif len(str1) > len(str2):
        for i in range(len(str1) - len(str2)):
            str2 += "|"

    # Licznik zliczający wystąpienia różnych znaków na tych samych pozycjach
    hamming_counter = 0

    # Sprawdzenie, na ilu pozycjach znaki w obu ciągach różnią się od siebie
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            hamming_counter += 1

    # Obliczenie względnej odległości Hamminga i zaokrąglenie jej do 4 miejsc po przecinku
    hamming_value = round(1 - hamming_counter / len(str1), 4)

    return hamming_value


# Odległość Jaro
def jaro_distance(str1, str2):
    # Sprawdzenie, czy oba ciągi znaków są takie same
    if str1 == str2:
        print("Oba ciągi znaków są takie same.")
        return 1
    else:
        # Ustalenie rozmiaru zakresu dopasowania wewnątrz którego porównywane będą ciągi znaków
        zakres_dopasowan = math.floor(max(len(str1), len(str2)) * 0.5) - 1

        # Licznik "pasujących" znaków
        licznik_p = 0

        # Listy przechowujące "dopasowania"
        dopasowania_1 = [0] * len(str1)
        dopasowania_2 = [0] * len(str2)

        # Porównywanie kolejnych znaków pierwszego ciągu znaków z drugim ciągiem
        for i in range(len(str1)):
            for j in range(max(0, i - zakres_dopasowan), min(len(str2), i + zakres_dopasowan + 1)):
                # Zwiększenie licznika o 1, jeżeli zostały znalezione takie same znaki oraz nie został wcześniej wykorzystany
                if (str1[i] == str2[j] and dopasowania_2[j] == 0):
                    dopasowania_1[i] = 1
                    dopasowania_2[j] = 1
                    licznik_p += 1
                    break

        # Zwrócenie wartości 0, gdy żaden znak z pierwszego ciągu nie został znaleziony w zakresie dopasowania w drugim ciągu
        if licznik_p == 0:
            return 0

        # Licznik transpozycji
        licznik_t = 0
        l = 0

        # Sprawdzenie liczby transpozycji
        for k in range(len(str1)):
            if dopasowania_1[k] == 1:
                while dopasowania_2[l] == 0:
                    l += 1
                if str1[k] != str2[l]:
                    licznik_t += 1
                l += 1

        # Obliczenie odległości Jaro
        jaro_value = round(
            ((licznik_p / len(str1)) + (licznik_p / len(str2)) + ((licznik_p - licznik_t / 2) / licznik_p)) / 3, 4)

        return jaro_value


# Odległość Jaro - Winklera
def jaro_winkler_distance(str1, str2):
    # Sprawdzenie, czy oba ciągi znaków są takie same
    if str1 == str2:
        print("Oba ciągi znaków są takie same.")
        return 1
    else:
        # Ustalenie rozmiaru zakresu dopasowania wewnątrz którego porównywane będą ciągi znaków
        zakres_dopasowan = math.floor(max(len(str1), len(str2)) * 0.5) - 1

        # Licznik "pasujących" znaków
        licznik_p = 0

        # Listy przechowujące "dopasowania"
        dopasowania_1 = [0] * len(str1)
        dopasowania_2 = [0] * len(str2)

        # Porównywanie kolejnych znaków pierwszego ciągu znaków z drugim ciągiem
        for i in range(len(str1)):
            for j in range(max(0, i - zakres_dopasowan), min(len(str2), i + zakres_dopasowan + 1)):
                # Zwiększenie licznika o 1, jeżeli zostały znalezione takie same znaki oraz nie został wcześniej wykorzystany
                if (str1[i] == str2[j] and dopasowania_2[j] == 0):
                    dopasowania_1[i] = 1
                    dopasowania_2[j] = 1
                    licznik_p += 1
                    break

        # Zwrócenie wartości 0, gdy żaden znak z pierwszego ciągu nie został znaleziony w zakresie dopasowania w drugim ciągu
        if licznik_p == 0:
            return 0

        # Licznik transpozycji
        licznik_t = 0
        l = 0

        # Sprawdzenie liczby transpozycji
        for k in range(len(str1)):
            if dopasowania_1[k] == 1:
                while dopasowania_2[l] == 0:
                    l += 1
                if str1[k] != str2[l]:
                    licznik_t += 1
                l += 1

        # Obliczenie odległości Jaro ze wzoru
        jaro_value = ((licznik_p / len(str1)) + (licznik_p / len(str2)) + ((licznik_p - licznik_t / 2) / licznik_p)) / 3

        # Poprawka Winklera

        # Parametr skalujący
        skala = 0.1

        # Ilość zgodnych znaków na początku obu tekstów
        rozmiar_prefiksu = 0

        # Sprawdzenie długości wspólnego prefiksu (maksymalnie do 4 znaków)
        for m in range(4):
            if str1[m] == str2[m]:
                rozmiar_prefiksu += 1
            else:
                break

        # Obliczenie odległości Jaro - Winklera
        jaro_winkler_value = round(jaro_value + skala * rozmiar_prefiksu * (1 - jaro_value), 4)

        return jaro_winkler_value


# Odległość Levenshteina
def levenshtein_distance(str1, str2, maks):
    # Sprawdzenie, czy dowolny z ciągów znaków nie jest pusty
    if len(str1) == 0 and len(str2) != 0:
        return len(str2)
    elif len(str1) != 0 and len(str2) == 0:
        return len(str1)

    # Sprawdzenie, czy ciągi są takie same
    if str1 == str2:
        return 1

    # Sprawdzenie, czy pierwsze znaki obu tekstów są takie same
    if str1[0] == str2[0]:
        str1 = str1[1:]
        str2 = str2[1:]
        return levenshtein_distance(str1, str2, maks)

    # Utworzenie macierzy Levenshteina
    macierz = (np.zeros((len(str1) + 1, len(str2) + 1))).astype(int)

    # Wypełnienie pierwszej kolumny macierzy kolejnymi liczbami naturalnymi
    for j in range(len(str1) + 1):
        macierz[j][0] = j

    # Wypełnienie pierwszego wiersza macierzy kolejnymi liczbami naturalnymi
    for i in range(len(str2) + 1):
        macierz[0][i] = i

    # Obliczenie pozostałych wyrazów macierzy Levenshteina
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            # Sprawdzenie, czy znaki są takie same (Wartość jest taka sama jak dla indeksu (i-1,j-1))
            if str1[i - 1] == str2[j - 1]:
                macierz[i][j] = min(macierz[i - 1][j] + 1, macierz[i][j - 1] + 1, macierz[i - 1][j - 1])
            else:
                macierz[i][j] = min(macierz[i - 1][j] + 1, macierz[i][j - 1] + 1, macierz[i - 1][j - 1] + 1)

    # Obliczenie odległości Levenshteina
    levenshtein_value = round(1 - macierz[len(str1), len(str2)] / maks, 4)

    return levenshtein_value


# Odległość Damerau - Levenshteina
def damerau_levenshtein_distance(str1, str2, maks):
    # Sprawdzenie, czy dowolny z ciągów znaków nie jest pusty
    if len(str1) == 0 and len(str2) != 0:
        return len(str2)
    elif len(str1) != 0 and len(str2) == 0:
        return len(str1)

    # Sprawdzenie, czy ciągi nie są takie same
    if str1 == str2:
        return 1

    # Utworzenie macierzy Damerau - Levenshteina
    macierz = (np.zeros((len(str1) + 1, len(str2) + 1))).astype(int)

    # Wypełnienie pierwszej kolumny macierzy kolejnymi liczbami naturalnymi
    for j in range(len(str1) + 1):
        macierz[j][0] = j

    # Wypełnienie pierwszego wiersza macierzy kolejnymi liczbami naturalnymi
    for i in range(len(str2) + 1):
        macierz[0][i] = i

    # Obliczenie pozostałych wyrazów macierzy Damerau - Levenshteina
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            # Sprawdzenie, czy znaki są takie same (Wartość jest taka sama jak dla indeksu (i-1,j-1))
            if str1[i - 1] == str2[j - 1]:
                macierz[i][j] = macierz[i - 1][j - 1]
            else:
                # W przeciwnym wypadku sprawdzamy trzy możliwe opcje (usunięcie, wstawienie lub zamianę miejscami)
                macierz[i][j] = min(macierz[i][j - 1] + 1, macierz[i - 1][j] + 1, macierz[i - 1][j - 1] + 1)

                # Jeżeli odpowiednie znaki w obu ciągach są takie same to sprawdzamy, czy wartość dla indeksu (i-2,j-2) nie jest mniejsza od wcześniej obliczonej wartości
                if (i > 1 and j > 1 and str1[i - 1] == str2[j - 2] and str1[i - 2] == str2[j - 1]):
                    macierz[i][j] = min(macierz[i][j], macierz[i - 2][j - 2] + 1)

    # Obliczenie wartości podobieństwa Damerau - Levenshteina
    damerau_levenshtein_value = round(1 - macierz[len(str1), len(str2)] / maks, 4)

    return damerau_levenshtein_value


# Odległość Tversky'ego oparta na unigramach
def tversky_unigrams_distance(alpha, beta, str1, str2):
    # Utworzenie list przechowujących wszystkie znaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie znaków z pierwszego ciągu znaków do listy
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 1])

    # Utworzenie listy z ilościa wystąpień poszczególnych znaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    # Dodanie dwuznaków z drugiego ciągu znaków do listy
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 1])

    # Utworzenie listy z ilością wystąpień poszczególnych znaków w pierwszym ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    # Sprawdzenie, ile poszczególnych znaków występuje w obu ciągach znaków
    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    # Sprawdzenie, ile poszczególnych znaków występuje w ciągu 1 i nie występuje w ciągu 2
    licznik_xy = 0
    for j in str1_dict:
        if j in str2_dict:
            if str1_dict[j] - str2_dict[j] > 0:
                licznik_xy += str1_dict[j] - str2_dict[j]
        else:
            licznik_xy += str1_dict[j]

    # Sprawdzenie, ile poszczególnych znaków występuje w ciągu 2 i nie występuje w ciągu 1
    licznik_yx = 0
    for k in str2_dict:
        if k in str1_dict:
            if str2_dict[k] - str1_dict[k] > 0:
                licznik_yx += str2_dict[k] - str1_dict[k]
        else:
            licznik_yx += str2_dict[k]

    # Obliczenie odległości Tversky'ego ze wzoru
    tversky_unigrams_value = round(licznik_wspolny / (licznik_wspolny + alpha * licznik_xy + beta * licznik_yx), 4)

    return tversky_unigrams_value


# Odległość Tversky'ego oparta na bigramach
def tversky_bigrams_distance(alpha, beta, str1, str2):
    # Utworzenie list przechowujących wszystkie dwuznaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie dwuznaków z pierwszego ciągu znaków do listy
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 2])

    # Utworzenie listy wystąpień poszczególnych dwuznaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    # Dodanie dwuznaków z drugiego ciągu znaków do listy
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 2])

    # Utworzenie listy wystąpień poszczególnych dwuznaków w pierwszym ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    # Sprawdzenie, ile poszczególnych dwuznaków występuje w obu ciągach znaków
    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    # Sprawdzenie, ile poszczególnych dwuznaków występuje w ciągu 1 i nie występuje w ciągu 2
    licznik_xy = 0
    for j in str1_dict:
        if j in str2_dict:
            if str1_dict[j] - str2_dict[j] > 0:
                licznik_xy += str1_dict[j] - str2_dict[j]
        else:
            licznik_xy += str1_dict[j]

    # Sprawdzenie, ile poszczególnych dwuznaków występuje w ciągu 2 i nie występuje w ciągu 1
    licznik_yx = 0
    for k in str2_dict:
        if k in str1_dict:
            if str2_dict[k] - str1_dict[k] > 0:
                licznik_yx += str2_dict[k] - str1_dict[k]
        else:
            licznik_yx += str2_dict[k]

    # Obliczenie odległości Tversky'ego ze wzoru
    tversky_bigrams_value = round(licznik_wspolny / (licznik_wspolny + alpha * licznik_xy + beta * licznik_yx), 4)

    return tversky_bigrams_value


# Odległość Tversky'ego oparta na trigramach
def tversky_trigrams_distance(alpha, beta, str1, str2):
    # Utworzenie list przechowujących wszystkie dwuznaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie dwuznaków z pierwszego ciągu znaków do listy
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 3])

    # Utworzenie listy wystąpień poszczególnych dwuznaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    # Dodanie dwuznaków z drugiego ciągu znaków do listy
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 3])

    # Utworzenie listy wystąpień poszczególnych dwuznaków w pierwszym ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    # Sprawdzenie, ile poszczególnych dwuznaków występuje w obu ciągach znaków
    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    # Sprawdzenie, ile poszczególnych dwuznaków występuje w ciągu 1 i nie występuje w ciągu 2
    licznik_xy = 0
    for j in str1_dict:
        if j in str2_dict:
            if str1_dict[j] - str2_dict[j] > 0:
                licznik_xy += str1_dict[j] - str2_dict[j]
        else:
            licznik_xy += str1_dict[j]

    # Sprawdzenie, ile poszczególnych dwuznaków występuje w ciągu 2 i nie występuje w ciągu 1
    licznik_yx = 0
    for k in str2_dict:
        if k in str1_dict:
            if str2_dict[k] - str1_dict[k] > 0:
                licznik_yx += str2_dict[k] - str1_dict[k]
        else:
            licznik_yx += str2_dict[k]

    # Obliczenie odległości Tversky'ego ze wzoru
    tversky_trigrams_value = round(licznik_wspolny / (licznik_wspolny + alpha * licznik_xy + beta * licznik_yx), 4)

    return tversky_trigrams_value


# Odległość Jaccarda oparta na unigramach
def jaccard_unigrams_distance(str1, str2):
    # Utworzenie list przechowujących wszystkie znaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie znaków z pierwszego ciągu znaków do listy
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 1])

    # Utworzenie listy wystąpień poszczególnych znaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    # Dodanie znaków z drugiego ciągu znaków do listy
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 1])

    # Utworzenie listy wystąpień poszczególnych znaków w pierwszym ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    # Sprawdzenie, ile poszczególnych znaków występuje w obu ciągach znaków
    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    # Sprawdzenie, ile poszczególnych znaków występuje w ciągu 1 i nie występuje w ciągu 2
    licznik_xy = 0
    for j in str1_dict:
        if j in str2_dict:
            if str1_dict[j] - str2_dict[j] > 0:
                licznik_xy += str1_dict[j] - str2_dict[j]
        else:
            licznik_xy += str1_dict[j]

    # Sprawdzenie, ile poszczególnych znaków występuje w ciągu 2 i nie występuje w ciągu 1
    licznik_yx = 0
    for k in str2_dict:
        if k in str1_dict:
            if str2_dict[k] - str1_dict[k] > 0:
                licznik_yx += str2_dict[k] - str1_dict[k]
        else:
            licznik_yx += str2_dict[k]

    # Obliczenie wartości podobieństwa Jaccarda opartej na unigramach
    jaccard_unigrams_value = round(licznik_wspolny / (licznik_wspolny + (licznik_xy + licznik_yx) * 0.5), 4)

    return jaccard_unigrams_value


# Odległość Jaccarda oparta na bigramach
def jaccard_bigrams_distance(str1, str2):
    # Utworzenie list przechowujących wszystkie dwuznaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie dwuznaków z pierwszego ciągu znaków do listy
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 2])

    # Utworzenie listy wystąpień poszczególnych dwuznaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    # Dodanie dwuznaków z drugiego ciągu znaków do listy
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 2])

    # Utworzenie listy wystąpień poszczególnych dwuznaków w pierwszym ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    # Sprawdzenie, ile poszczególnych dwuznaków występuje w obu ciągach znaków
    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    # Sprawdzenie, ile poszczególnych dwuznaków występuje w ciągu 1 i nie występuje w ciągu 2
    licznik_xy = 0
    for j in str1_dict:
        if j in str2_dict:
            if str1_dict[j] - str2_dict[j] > 0:
                licznik_xy += str1_dict[j] - str2_dict[j]
        else:
            licznik_xy += str1_dict[j]

    # Sprawdzenie, ile poszczególnych dwuznaków występuje w ciągu 2 i nie występuje w ciągu 1
    licznik_yx = 0
    for k in str2_dict:
        if k in str1_dict:
            if str2_dict[k] - str1_dict[k] > 0:
                licznik_yx += str2_dict[k] - str1_dict[k]
        else:
            licznik_yx += str2_dict[k]

    # Obliczenie wartości podobieństwa Jaccarda opartej na bigramach
    jaccard_bigrams_value = licznik_wspolny / (licznik_wspolny + (licznik_xy + licznik_yx) * 0.5)

    return round(jaccard_bigrams_value, 4)


# Odległość Jaccarda oparta na trigramach
def jaccard_trigrams_distance(str1, str2):
    # Utworzenie list przechowujących wszystkie trójznaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie trójznaków z pierwszego ciągu znaków do listy
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 3])

    # Utworzenie listy wystąpień poszczególnych trójznaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    # Dodanie trójznaków z drugiego ciągu znaków do listy
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 3])

    # Utworzenie listy wystąpień poszczególnych trójznaków w pierwszym ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    # Sprawdzenie, ile poszczególnych trójznaków występuje w obu ciągach znaków
    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    # Sprawdzenie, ile poszczególnych trójznaków występuje w ciągu 1 i nie występuje w ciągu 2
    licznik_xy = 0
    for j in str1_dict:
        if j in str2_dict:
            if str1_dict[j] - str2_dict[j] > 0:
                licznik_xy += str1_dict[j] - str2_dict[j]
        else:
            licznik_xy += str1_dict[j]

    # Sprawdzenie, ile poszczególnych trójznaków występuje w ciągu 2 i nie występuje w ciągu 1
    licznik_yx = 0
    for k in str2_dict:
        if k in str1_dict:
            if str2_dict[k] - str1_dict[k] > 0:
                licznik_yx += str2_dict[k] - str1_dict[k]
        else:
            licznik_yx += str2_dict[k]

    # Obliczenie wartości podobieństwa Jaccarda opartej na trigramach
    jaccard_bigrams_value = licznik_wspolny / (licznik_wspolny + (licznik_xy + licznik_yx) * 0.5)

    return round(jaccard_bigrams_value, 4)


# Odległość Hellingera oparta na unigramach
def hellinger_unigrams_distance(str1, str2):
    # Utworzenie list przechowujących wszystkie znaki ciągów znaków
    str1_list = []
    str2_list = []

    # Histogram pierwszego ciągu znaków
    for i in range(len(str1)):
        str1_list.append(str1[i])

    str1_dict = dict.fromkeys(str1_list, 0)

    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1 / len(str1)

    # Histogram drugiego ciągu znaków
    for j in range(len(str2)):
        str2_list.append(str2[j])

    str2_dict = dict.fromkeys(str2_list, 0)

    for j in range(len(str2_list)):
        str2_dict[str2_list[j]] += 1 / len(str2)

    # Konkatenacja dwóch ciągów znaków
    str12 = str1 + str2

    # Utworzenie listy ze znakami występującymi w co najmniej jednym ciągu znaków
    str12_list = []

    # Dodanie do listy wszystkich znaków
    for k in range(len(str12)):
        str12_list.append(str12[k])

    # Utworzenie słownika z wszystkimi znakami występującymi w co najmniej jednym ciągu znaków
    str12_dict = dict.fromkeys(str12_list, 0)

    # Suma Hellingera
    hellinger_unigrams_sum = 0

    # Obliczenie sumy Hellingera
    for item in str12_dict:
        if item in str1_dict and item not in str2_dict:
            hellinger_unigrams_sum += str1_dict[item]
        elif item not in str1_dict and item in str2_dict:
            hellinger_unigrams_sum += str2_dict[item]
        elif item in str1_dict and item in str2_dict:
            hellinger_unigrams_sum += pow(np.sqrt(str1_dict[item]) - np.sqrt(str2_dict[item]), 2)

    # Obliczenie odległosci Hellingera ze wzoru:
    hellinger_unigrams_value = round(1 - np.sqrt(hellinger_unigrams_sum / 2), 4)

    return hellinger_unigrams_value


# Odległość Hellingera oparta na bigramach
def hellinger_bigrams_distance(str1, str2):
    # Utworzenie list przechowujących wszystkie dwuznaki ciągów znaków
    str1_list = []
    str2_list = []

    # Histogram pierwszego ciągu znaków
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 2])

    str1_dict = dict.fromkeys(str1_list, 0)

    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1 / (len(str1) - 1)

    # Histogram drugiego ciągu znaków
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 2])

    str2_dict = dict.fromkeys(str2_list, 0)

    for j in range(len(str2_list)):
        str2_dict[str2_list[j]] += 1 / (len(str2) - 1)

    # Konkatenacja dwóch ciągów znaków
    str12 = str1 + str2

    # Utworzenie listy ze dwuznakami występującymi w co najmniej jednym ciągu znaków
    str12_list = []

    # Dodanie do listy wszystkich dwuznaków
    for k in range(len(str12) - 1):
        if k != len(str1) - 1:
            str12_list.append(str12[k:k + 2])

    # Utworzenie słownika z wszystkimi dwuznakami występującymi w co najmniej jednym ciągu znaków
    str12_dict = dict.fromkeys(str12_list, 0)

    # Suma Hellingera
    hellinger_bigrams_sum = 0

    # Obliczenie sumy Hellingera
    for item in str12_dict:
        if item in str1_dict and item not in str2_dict:
            hellinger_bigrams_sum += str1_dict[item]
        elif item not in str1_dict and item in str2_dict:
            hellinger_bigrams_sum += str2_dict[item]
        elif item in str1_dict and item in str2_dict:
            hellinger_bigrams_sum += pow(np.sqrt(str1_dict[item]) - np.sqrt(str2_dict[item]), 2)

    # Obliczanie odległości Hellingera ze wzoru
    hellinger_bigrams_value = round(1 - np.sqrt(hellinger_bigrams_sum / 2), 4)

    return hellinger_bigrams_value


# Odległość Hellingera oparta na trigramach
def hellinger_trigrams_distance(str1, str2):
    # Utworzenie list przechowujących wszystkie trójznaki ciągów znaków
    str1_list = []
    str2_list = []

    # Histogram pierwszego ciągu znaków
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 3])

    str1_dict = dict.fromkeys(str1_list, 0)

    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1 / (len(str1) - 1)

    # Histogram drugiego ciągu znaków
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 3])

    str2_dict = dict.fromkeys(str2_list, 0)

    for j in range(len(str2_list)):
        str2_dict[str2_list[j]] += 1 / (len(str2) - 1)

    # Konkatenacja dwóch ciągów znaków
    str12 = str1 + str2

    # Utworzenie listy ze trójznakami występującymi w co najmniej jednym ciągu znaków
    str12_list = []

    # Dodanie do listy wszystkich trójznaków
    for k in range(len(str12) - 1):
        if k != len(str1) - 1 or k != len(str1) - 2:
            str12_list.append(str12[k:k + 3])

    # Utworzenie słownika z wszystkimi trójznakami występującymi w co najmniej jednym ciągu znaków
    str12_dict = dict.fromkeys(str12_list, 0)

    # Suma Hellingera
    hellinger_trigrams_sum = 0

    # Obliczenie sumy Hellingera
    for item in str12_dict:
        if item in str1_dict and item not in str2_dict:
            hellinger_trigrams_sum += str1_dict[item]
        elif item not in str1_dict and item in str2_dict:
            hellinger_trigrams_sum += str2_dict[item]
        elif item in str1_dict and item in str2_dict:
            hellinger_trigrams_sum += pow(np.sqrt(str1_dict[item]) - np.sqrt(str2_dict[item]), 2)

    # Obliczanie odległości Hellingera ze wzoru
    hellinger_trigrams_value = round(1 - np.sqrt(hellinger_trigrams_sum / 2), 4)

    return hellinger_trigrams_value


# Odległość Bhattacharyyi oparta na unigramach
def bhattacharyya_unigrams_distance(str1, str2):
    # Utworzenie list przechowujących wszystkie znaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie znaków z pierwszego ciągu znaków do listy
    for i in range(len(str1)):
        str1_list.append(str1[i])

    # Utworzenie listy wystąpień poszczególnych znaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1 / len(str1)

    # Dodanie znaków z drugiego ciągu znaków do listy
    for j in range(len(str2)):
        str2_list.append(str2[j])

    # Utworzenie listy wystąpień poszczególnych znaków w drugim ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for j in range(len(str2_list)):
        str2_dict[str2_list[j]] += 1 / len(str2)

    # Konkatenacja obu ciągów znaków
    str12 = str1 + str2

    # Lista przechowująca wszystkie znaki obu ciągów znaków
    str12_list = []

    # Dodanie do listy wszystkich znaków
    for k in range(len(str12)):
        str12_list.append(str12[k])

    # Utworzenie listy wystąpień poszczególnych znaków w połączonym ciągu znaków
    str12_dict = dict.fromkeys(str12_list, 0)

    # Suma Bhattacharyyi dla unigramów
    bhattacharyya_unigrams_sum = 0

    # Obliczenie odległości Bhattacharyyi ze wzoru:
    for item in str12_dict:
        if item in str1_dict and item in str2_dict:
            bhattacharyya_unigrams_sum += np.sqrt(str1_dict[item] * str2_dict[item])

    # Zaokrąglenie wartości do 4 miejsc po przecinku
    bhattacharyya_unigrams_value = round(bhattacharyya_unigrams_sum, 4)

    return bhattacharyya_unigrams_value


# Odległość Bhattacharyyi oparta na bigramach
def bhattacharyya_bigrams_distance(str1, str2):
    # Utworzenie list przechowujących wszystkie dwuznaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie dwuznaków z pierwszego ciągu znaków do listy
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 2])

    # Utworzenie listy wystąpień poszczególnych dwuznaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1 / (len(str1) - 1)

    # Dodanie dwuznaków z drugiego ciągu znaków do listy
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 2])

    # Utworzenie listy wystąpień poszczególnych dwuznaków w drugim ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for j in range(len(str2_list)):
        str2_dict[str2_list[j]] += 1 / (len(str2) - 1)

    # Konkatenacja ciągów znaków
    str12 = str1 + str2

    # Lista przechowująca wszystkie dwuznaki obu ciągów znaków
    str12_list = []

    # Dodanie do listy wszystkich dwuznaków
    for k in range(len(str12) - 1):
        if k != len(str1) - 1:
            str12_list.append(str12[k:k + 2])

    # Utworzenie listy wystąpień poszczególnych dwuznaków w połączonym ciągu znaków
    str12_dict = dict.fromkeys(str12_list, 0)

    # Suma Bhattacharyyi dla dwuznaków
    bhattacharyya_bigrams_sum = 0

    # Obliczenie odległości Bhattacharyyi ze wzoru:
    for item in str12_dict:
        if item in str1_dict and item in str2_dict:
            bhattacharyya_bigrams_sum += np.sqrt(str1_dict[item] * str2_dict[item])

    # Zaokrąglenie wartości do 4 miejsc po przecinku
    bhattacharyya_bigrams_value = round(bhattacharyya_bigrams_sum, 4)

    return bhattacharyya_bigrams_value


# Odległość Bhattacharyyi oparta na trigramach
def bhattacharyya_trigrams_distance(str1, str2):
    # Utworzenie list przechowujących wszystkie trójznaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie trójznaków z pierwszego ciągu znaków do listy
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 3])

    # Utworzenie listy wystąpień poszczególnych trójznaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1 / (len(str1) - 1)

    # Dodanie trójznaków z drugiego ciągu znaków do listy
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 3])

    # Utworzenie listy wystąpień poszczególnych trigramów w pierwszym ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for j in range(len(str2_list)):
        str2_dict[str2_list[j]] += 1 / (len(str2) - 1)

    # Konkatenacja ciągów znaków
    str12 = str1 + str2

    # Lista przechowująca wszystkie trigramy obu ciągów znaków
    str12_list = []

    # Dodanie do listy wszystkich trójznaków
    for k in range(len(str12) - 1):
        if k != len(str1) - 1 and k != len(str1) - 2:
            str12_list.append(str12[k:k + 3])

    # Utworzenie listy wystąpień poszczególnych trigramów w połączonym ciągu znaków
    str12_dict = dict.fromkeys(str12_list, 0)

    # Suma Bhattacharyyi dla trigramów
    bhattacharyya_trigrams_sum = 0

    # Obliczenie odległości Bhattacharyyi ze wzoru:
    for item in str12_dict:
        if item in str1_dict and item in str2_dict:
            bhattacharyya_trigrams_sum += np.sqrt(str1_dict[item] * str2_dict[item])

    # Zaokrąglenie wartości do 4 miejsc po przecinku
    bhattacharyya_trigrams_value = round(bhattacharyya_trigrams_sum, 4)

    return bhattacharyya_trigrams_value


# Względny najdłuższy wspólny podciąg
def relative_lcs(str1, str2):
    # Zmienna przechowująca najdłuższy wspólny podciąg
    lcs = 0

    # Pętla przechodząca po wszystkich znakach obu ciągów znaków
    for i in range(len(str1)):
        for j in range(len(str2)):

            # Zmienna tymczasowo przechowująca długość wspólnego podciągu
            przesuniecie = 0
            while i + przesuniecie < len(str1) and j + przesuniecie < len(str2) and str1[i + przesuniecie] == str2[
                j + przesuniecie]:
                # Zwiększenie przesunięcia w przypadku gdy znaki na odpowiednich pozycjach są takie same
                przesuniecie += 1

            # Sprawdzenie, czy odnaleziony wspólny podciąg jest dłuższy od najdłuższego dotychczasowego wspólnego podciągu
            lcs = max(lcs, przesuniecie)

    # Obliczenie względnego najdłuższego wspólnego podciągus
    rlcs_value = round(lcs / max(len(str1), len(str2)), 4)

    return rlcs_value


# Odległość Szymkiewicza - Simpsona oparta na unigramach
def Szymkiewicz_Simpson_unigrams(str1, str2):
    # Utworzenie list przechowujących wszystkie znaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie znaków z pierwszego ciągu znaków do listy
    for i in range(len(str1)):
        str1_list.append(str1[i:i + 1])

    # Utworzenie listy wystąpień poszczególnych znaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    # Dodanie znaków z drugiego ciągu znaków do listy
    for j in range(len(str2)):
        str2_list.append(str2[j:j + 1])

    # Utworzenie listy wystąpień poszczególnych znaków w pierwszym ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    # Sprawdzenie, ile poszczególnych znaków występuje w obu ciągach znaków
    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    # Obliczenie wartości podobieństwa Szymkiewicza - Simpsona opartej na unigramach
    ss_unigrams_value = round(licznik_wspolny / min(len(str1), len(str2)), 4)

    return ss_unigrams_value


# Odległość Szymkiewicza - Simpsona oparta na bigramach
def Szymkiewicz_Simpson_bigrams(str1, str2):
    # Utworzenie list przechowujących wszystkie dwuznaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie znaków z pierwszego ciągu dwuznaków do listy
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 2])

    # Utworzenie listy wystąpień poszczególnych dwuznaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    # Dodanie dwuznaków z drugiego ciągu znaków do listy
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 2])

    # Utworzenie listy wystąpień poszczególnych dwuznaków w pierwszym ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    # Sprawdzenie, ile poszczególnych dwuznaków występuje w obu ciągach znaków
    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    # Obliczenie wartości podobieństwa Szymkiewicza - Simpsona opartej na bigramach
    ss_bigrams_value = round(licznik_wspolny / min(len(str1) - 1, len(str2) - 1), 4)

    return ss_bigrams_value


# Odległość Szymkiewicza - Simpsona oparta na trigramach
def Szymkiewicz_Simpson_trigrams(str1, str2):
    # Utworzenie list przechowujących wszystkie trigramy ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie znaków z pierwszego ciągu trigramów do listy
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 3])

    # Utworzenie listy wystąpień poszczególnych trigramów w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    # Dodanie dwuznaków z drugiego ciągu znaków do listy
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 3])

    # Utworzenie listy wystąpień poszczególnych trigramów w pierwszym ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    # Sprawdzenie, ile poszczególnych trigramów występuje w obu ciągach znaków
    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    # Obliczenie wartości podobieństwa Szymkiewicza - Simpsona opartej na trigramach
    ss_trigrams_value = licznik_wspolny / min(len(str1) - 2, len(str2) - 2)

    return round(ss_trigrams_value, 4)


# Odległość Dice - Sorensena oparta na unigramach
def Dice_Sorensen_unigrams(str1, str2):
    # Utworzenie list przechowujących wszystkie znaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie znaków z pierwszego ciągu znaków do listy
    for i in range(len(str1)):
        str1_list.append(str1[i:i + 1])

    # Utworzenie listy wystąpień poszczególnych znaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    # Dodanie znaków z drugiego ciągu znaków do listy
    for j in range(len(str2)):
        str2_list.append(str2[j:j + 1])

    # Utworzenie listy wystąpień poszczególnych znaków w pierwszym ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    # Sprawdzenie, ile poszczególnych znaków występuje w obu ciągach znaków
    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    # Obliczenie wartości podobieństwa Dice - Sorensena opartej na unigramach
    ds_unigrams_value = round(2 * licznik_wspolny / (len(str1) + len(str2)), 4)

    return ds_unigrams_value


# Odległość Dice - Sorensena oparta na bigramach
def Dice_Sorensen_bigrams(str1, str2):
    # Utworzenie list przechowujących wszystkie dwuznaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie znaków z pierwszego ciągu dwuznaków do listy
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 2])

    # Utworzenie listy wystąpień poszczególnych dwuznaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    # Dodanie dwuznaków z drugiego ciągu znaków do listy
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 2])

    # Utworzenie listy wystąpień poszczególnych dwuznaków w pierwszym ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    # Sprawdzenie, ile poszczególnych dwuznaków występuje w obu ciągach znaków
    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    # Obliczenie wartości podobieństwa Dice - Sorensena opartej na bigramach
    ds_bigrams_value = round(2 * licznik_wspolny / (len(str1) + len(str2) - 2), 4)

    return ds_bigrams_value


# Odległość Dice - Sorensena oparta na trigramach
def Dice_Sorensen_trigrams(str1, str2):
    # Utworzenie list przechowujących wszystkie trójznaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie znaków z pierwszego ciągu trójznaków do listy
    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 3])

    # Utworzenie listy wystąpień poszczególnych trójznaków w pierwszym ciągu znaków
    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    # Dodanie trójznaków z drugiego ciągu znaków do listy
    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 3])

    # Utworzenie listy wystąpień poszczególnych trójznaków w pierwszym ciągu znaków
    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    # Sprawdzenie, ile poszczególnych trójznaków występuje w obu ciągach znaków
    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    # Obliczenie wartości podobieństwa Dice - Sorensena opartej na trigramach
    ds_trigrams_value = 2 * licznik_wspolny / (len(str1) + len(str2) - 4)

    return round(ds_trigrams_value, 4)


# Funkcja "oczyszczająca" kod
def cleancode(code):
    code = re.sub(r'#.*', '', code)  # Usuwanie komentarzy
    code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)  # Usuwanie docstringów
    code = re.sub(r'\s+', ' ', code)  # Usuwanie nadmiarowych spacji
    return code.strip()


# Obliczenie wartosci funkcji podobienstwa, a nastepnie prawdopodobienstwa plagiatu dla wszystkich par tekstów
def similarity(str1, str2):
    # Oczyszczenie kodu z komentarzy, spacji
    str11 = cleancode(str1)
    str12 = cleancode(str2)

    # Zmiana dużych znaków na małe
    str11 = str11.lower()
    str12 = str12.lower()

    # Ustalenie maksymalnej długosci tekstów po oczyszczeniu
    maks = max(len(str11), len(str12))

    data = pd.DataFrame(columns=('Kod 1', 'Kod 2'))

    data.loc[0] = [str11, str12]

    # Wartosci srednie dla kodow bedacych plagiatem
    u1 = [0.08938,0.76564,0.78654,0.74966,0.74980,0.87616,0.76794,0.71744,0.86784,0.76079,0.71088,0.80924,0.58786,0.50544,0.96118,0.82360,0.74619,0.17781,0.91207,0.79874,0.74860,0.86801,0.76079,0.71363]
    
    # Odchylenia standardowe dla kodow bedacych plagiatem
    s1 = [0.05681,0.03532,0.03438,0.09145,0.09151,0.04688,0.07923,0.10364,0.04996,0.08126,0.10532,0.05018,0.08222,0.09695,0.01948,0.06494,0.09466,0.11678,0.03895,0.07232,0.09790,0.04996,0.08126,0.10598]

    # Wagi obliczone na podstawie wartosci funkcji dla kodow bedacych i niebedacych plagiatem
    wagi = [0.0143, 0.035, 0.0356, 0.0514, 0.0514, 0.0352, 0.0534, 0.0524, 0.0351, 0.0533, 0.0524, 0.0265, 0.0444, 0.048, 0.0249, 0.048, 0.051, 0.0209, 0.0241, 0.051, 0.0512, 0.0352, 0.0533, 0.0523]

    # Dodanie kolumn przechowujących wartosci funkcji podobienstwa
    data.insert(2, "Wzgledna odleglosc Hamminga", 0)
    data.insert(3, "Odleglosc Jaro", 0)
    data.insert(4, "Odleglosc Jaro - Winklera", 0)
    data.insert(5, "Odleglosc Levenshteina", 0)
    data.insert(6, "Odleglosc Damerau - Levenshteina", 0)
    data.insert(7, "Odleglosc Tversky'ego (unigramy)", 0)
    data.insert(8, "Odleglosc Tversky'ego (bigramy)", 0)
    data.insert(9, "Odleglosc Tversky'ego (trigramy)", 0)
    data.insert(10, "Odleglosc Jaccarda (unigramy)", 0)
    data.insert(11, "Odleglosc Jaccarda (bigramy)", 0)
    data.insert(12, "Odleglosc Jaccarda (trigramy)", 0)
    data.insert(13, "Odleglosc Hellingera (unigramy)", 0)
    data.insert(14, "Odleglosc Hellingera (bigramy)", 0)
    data.insert(15, "Odleglosc Hellingera (trigramy)", 0)
    data.insert(16, "Odleglosc Bhattacharyyi (unigramy)", 0)
    data.insert(17, "Odleglosc Bhattacharyyi (bigramy)", 0)
    data.insert(18, "Odleglosc Bhattacharyyi (trigramy)", 0)
    data.insert(19, "Wzgledny najdluzszy wspolny podciag", 0)
    data.insert(20, "Odleglosc Szymkiewicza - Simpsona (unigramy)", 0)
    data.insert(21, "Odleglosc Szymkiewicza - Simpsona (bigramy)", 0)
    data.insert(22, "Odleglosc Szymkiewicza - Simpsona (trigramy)", 0)
    data.insert(23, "Odleglosc Dice - Sorensena (unigramy)", 0)
    data.insert(24, "Odleglosc Dice - Sorensena (bigramy)", 0)
    data.insert(25, "Odleglosc Dice - Sorensena (trigramy)", 0)

    # Dodanie kolumn przechowujących prawdopodobienstwa plagiatu
    data.insert(26, "Wzgledna odleglosc Hamminga - prawdopodobieństwo", 0)
    data.insert(27, "Odleglosc Jaro - prawdopodobieństwo", 0)
    data.insert(28, "Odleglosc Jaro - Winklera - prawdopodobieństwo", 0)
    data.insert(29, "Odleglosc Levenshteina - prawdopodobieństwo", 0)
    data.insert(30, "Odleglosc Damerau - Levenshteina - prawdopodobieństwo", 0)
    data.insert(31, "Odleglosc Tversky'ego (unigramy) - prawdopodobieństwo", 0)
    data.insert(32, "Odleglosc Tversky'ego (bigramy) - prawdopodobieństwo", 0)
    data.insert(33, "Odleglosc Tversky'ego (trigramy) - prawdopodobieństwo", 0)
    data.insert(34, "Odleglosc Jaccarda (unigramy) - prawdopodobieństwo", 0)
    data.insert(35, "Odleglosc Jaccarda (bigramy) - prawdopodobieństwo", 0)
    data.insert(36, "Odleglosc Jaccarda (trigramy) - prawdopodobieństwo", 0)
    data.insert(37, "Odleglosc Hellingera (unigramy) - prawdopodobieństwo", 0)
    data.insert(38, "Odleglosc Hellingera (bigramy) - prawdopodobieństwo", 0)
    data.insert(39, "Odleglosc Hellingera (trigramy) - prawdopodobieństwo", 0)
    data.insert(40, "Odleglosc Bhattacharyyi (unigramy) - prawdopodobieństwo", 0)
    data.insert(41, "Odleglosc Bhattacharyyi (bigramy) - prawdopodobieństwo", 0)
    data.insert(42, "Odleglosc Bhattacharyyi (trigramy) - prawdopodobieństwo", 0)
    data.insert(43, "Wzgledny najdluzszy wspolny podciag - prawdopodobieństwo", 0)
    data.insert(44, "Odleglosc Szymkiewicza - Simpsona (unigramy) - prawdopodobieństwo", 0)
    data.insert(45, "Odleglosc Szymkiewicza - Simpsona (bigramy) - prawdopodobieństwo", 0)
    data.insert(46, "Odleglosc Szymkiewicza - Simpsona (trigramy) - prawdopodobieństwo", 0)
    data.insert(47, "Odleglosc Dice - Sorensena (unigramy) - prawdopodobieństwo", 0)
    data.insert(48, "Odleglosc Dice - Sorensena (bigramy) - prawdopodobieństwo", 0)
    data.insert(49, "Odleglosc Dice - Sorensena (trigramy) - prawdopodobieństwo", 0)
    data.insert(50, "Prawdopodobienstwo plagiatu", 0)

    # Obliczanie wartosci funkcji podobieństwa i wpisanie ich do ramki danych
    data.loc[0, "Wzgledna odleglosc Hamminga"] = relative_hamming_distance(str11, str12)
    data.loc[0, "Odleglosc Jaro"] = jaro_distance(str11, str12)
    data.loc[0, "Odleglosc Jaro - Winklera"] = jaro_winkler_distance(str11, str12)
    data.loc[0, "Odleglosc Levenshteina"] = levenshtein_distance(str11, str12, maks)
    data.loc[0, "Odleglosc Damerau - Levenshteina"] = damerau_levenshtein_distance(str11, str12, maks)
    data.loc[0, "Odleglosc Tversky'ego (unigramy)"] = tversky_unigrams_distance(0.6, 0.4, str11, str12)
    data.loc[0, "Odleglosc Tversky'ego (bigramy)"] = tversky_bigrams_distance(0.6, 0.4, str11, str12)
    data.loc[0, "Odleglosc Tversky'ego (trigramy)"] = tversky_trigrams_distance(0.6, 0.4, str11, str12)
    data.loc[0, "Odleglosc Jaccarda (unigramy)"] = jaccard_unigrams_distance(str11, str12)
    data.loc[0, "Odleglosc Jaccarda (bigramy)"] = jaccard_bigrams_distance(str11, str12)
    data.loc[0, "Odleglosc Jaccarda (trigramy)"] = jaccard_trigrams_distance(str11, str12)
    data.loc[0, "Odleglosc Hellingera (unigramy)"] = hellinger_unigrams_distance(str11, str12)
    data.loc[0, "Odleglosc Hellingera (bigramy)"] = hellinger_bigrams_distance(str11, str12)
    data.loc[0, "Odleglosc Hellingera (trigramy)"] = hellinger_trigrams_distance(str11, str12)
    data.loc[0, "Odleglosc Bhattacharyyi (unigramy)"] = bhattacharyya_unigrams_distance(str11, str12)
    data.loc[0, "Odleglosc Bhattacharyyi (bigramy)"] = bhattacharyya_bigrams_distance(str11, str12)
    data.loc[0, "Odleglosc Bhattacharyyi (trigramy)"] = bhattacharyya_trigrams_distance(str11, str12)
    data.loc[0, "Wzgledny najdluzszy wspolny podciag"] = relative_lcs(str11, str12)
    data.loc[0, "Odleglosc Szymkiewicza - Simpsona (unigramy)"] = Szymkiewicz_Simpson_unigrams(str11, str12)
    data.loc[0, "Odleglosc Szymkiewicza - Simpsona (bigramy)"] = Szymkiewicz_Simpson_bigrams(str11, str12)
    data.loc[0, "Odleglosc Szymkiewicza - Simpsona (trigramy)"] = Szymkiewicz_Simpson_trigrams(str11, str12)
    data.loc[0, "Odleglosc Dice - Sorensena (unigramy)"] = Dice_Sorensen_unigrams(str11, str12)
    data.loc[0, "Odleglosc Dice - Sorensena (bigramy)"] = Dice_Sorensen_bigrams(str11, str12)
    data.loc[0, "Odleglosc Dice - Sorensena (trigramy)"] = Dice_Sorensen_trigrams(str11, str12)

    # Obliczenie prawdopodobieństw plagiatu dla każdej funkcji podobieństwa
    data.loc[0, "Wzgledna odleglosc Hamminga - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Wzgledna odleglosc Hamminga"], u1[0], s1[0])
    data.loc[0, "Odleglosc Jaro - prawdopodobieństwo"] = norm.cdf(data.loc[0, "Odleglosc Jaro"], u1[1], s1[1])
    data.loc[0, "Odleglosc Jaro - Winklera - prawdopodobieństwo"] = norm.cdf(data.loc[0, "Odleglosc Jaro - Winklera"],
                                                                             u1[2], s1[2])
    data.loc[0, "Odleglosc Levenshteina - prawdopodobieństwo"] = norm.cdf(data.loc[0, "Odleglosc Levenshteina"], u1[3],
                                                                          s1[3])
    data.loc[0, "Odleglosc Damerau - Levenshteina - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Damerau - Levenshteina"], u1[4], s1[4])
    data.loc[0, "Odleglosc Tversky'ego (unigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Tversky'ego (unigramy)"], u1[5], s1[5])
    data.loc[0, "Odleglosc Tversky'ego (bigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Tversky'ego (bigramy)"], u1[6], s1[6])
    data.loc[0, "Odleglosc Tversky'ego (trigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Tversky'ego (trigramy)"], u1[7], s1[7])
    data.loc[0, "Odleglosc Jaccarda (unigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Jaccarda (unigramy)"], u1[8], s1[8])
    data.loc[0, "Odleglosc Jaccarda (bigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Jaccarda (bigramy)"], u1[9], s1[9])
    data.loc[0, "Odleglosc Jaccarda (trigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Jaccarda (trigramy)"], u1[10], s1[10])
    data.loc[0, "Odleglosc Hellingera (unigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Hellingera (unigramy)"], u1[11], s1[11])
    data.loc[0, "Odleglosc Hellingera (bigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Hellingera (bigramy)"], u1[12], s1[12])
    data.loc[0, "Odleglosc Hellingera (trigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Hellingera (trigramy)"], u1[13], s1[13])
    data.loc[0, "Odleglosc Bhattacharyyi (unigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Bhattacharyyi (unigramy)"], u1[14], s1[14])
    data.loc[0, "Odleglosc Bhattacharyyi (bigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Bhattacharyyi (bigramy)"], u1[15], s1[15])
    data.loc[0, "Odleglosc Bhattacharyyi (trigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Bhattacharyyi (trigramy)"], u1[16], s1[16])
    data.loc[0, "Wzgledny najdluzszy wspolny podciag - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Wzgledny najdluzszy wspolny podciag"], u1[17], s1[17])
    data.loc[0, "Odleglosc Szymkiewicza - Simpsona (unigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Szymkiewicza - Simpsona (unigramy)"], u1[18], s1[18])
    data.loc[0, "Odleglosc Szymkiewicza - Simpsona (bigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Szymkiewicza - Simpsona (bigramy)"], u1[19], s1[19])
    data.loc[0, "Odleglosc Szymkiewicza - Simpsona (trigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Szymkiewicza - Simpsona (trigramy)"], u1[20], s1[20])
    data.loc[0, "Odleglosc Dice - Sorensena (unigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Dice - Sorensena (unigramy)"], u1[21], s1[21])
    data.loc[0, "Odleglosc Dice - Sorensena (bigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Dice - Sorensena (unigramy)"], u1[22], s1[22])
    data.loc[0, "Odleglosc Dice - Sorensena (trigramy) - prawdopodobieństwo"] = norm.cdf(
        data.loc[0, "Odleglosc Dice - Sorensena (unigramy)"], u1[23], s1[23])

    prawdopodobienstwo = 0
    for j in range(len(wagi)):
        prawdopodobienstwo = prawdopodobienstwo + data.iloc[0, 26 + j] * wagi[j]

    data.loc[0, "Prawdopodobieństwo plagiatu"] = prawdopodobienstwo
    return prawdopodobienstwo

# for l in range(len(data2)):
#    print(l)
#    data2.loc[l, "Prawdopodobienstwo"] = similarity(data2.loc[l, "Kod 1"], data2.loc[l, "Kod 2"])

# data2.to_csv('similarity5.csv')