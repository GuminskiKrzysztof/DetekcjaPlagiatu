import numpy as np
import pandas as pd
import math
import re
from scipy.stats import norm

# Pobranie ramki danych z kodami wykorzystywanymi do doboru wartosci wag
#data2 = pd.read_csv("C:\\Users\\Admin\\Desktop\\codes_to_weights_choose.csv")


# Funkcje obliczajace wartosci podobienstwa miedzy tekstami

def relative_hamming_distance(str1, str2):
    if str1 == str2:
        print("Oba ciągi znaków są takie same.")
        return 1

    if len(str1) < len(str2):
        for i in range(len(str2) - len(str1)):
            str1 += "|"
    elif len(str1) > len(str2):
        for i in range(len(str1) - len(str2)):
            str2 += "|"

    hamming_counter = 0

    for i in range(len(str1)):
        if str1[i] != str2[i]:
            hamming_counter += 1

    hamming_value = round(1 - hamming_counter / len(str1), 4)

    return hamming_value


def jaro_distance(str1, str2):
    if str1 == str2:
        print("Oba ciągi znaków są takie same.")
        return 1
    else:
        zakres_dopasowan = math.floor(max(len(str1), len(str2)) * 0.5) - 1

        licznik_p = 0

        dopasowania_1 = [0] * len(str1)
        dopasowania_2 = [0] * len(str2)

        for i in range(len(str1)):
            for j in range(max(0, i - zakres_dopasowan), min(len(str2), i + zakres_dopasowan + 1)):
                if (str1[i] == str2[j] and dopasowania_2[j] == 0):
                    dopasowania_1[i] = 1
                    dopasowania_2[j] = 1
                    licznik_p += 1
                    break

        if licznik_p == 0:
            return 0

        licznik_t = 0
        l = 0

        for k in range(len(str1)):
            if dopasowania_1[k] == 1:
                while dopasowania_2[l] == 0:
                    l += 1
                if str1[k] != str2[l]:
                    licznik_t += 1
                l += 1

        jaro_value = round(
            ((licznik_p / len(str1)) + (licznik_p / len(str2)) + ((licznik_p - licznik_t / 2) / licznik_p)) / 3, 4)

        return jaro_value


def jaro_winkler_distance(str1, str2):
    if str1 == str2:
        print("Oba ciągi znaków są takie same.")
        return 1
    else:
        zakres_dopasowan = math.floor(max(len(str1), len(str2)) * 0.5) - 1

        licznik_p = 0

        dopasowania_1 = [0] * len(str1)
        dopasowania_2 = [0] * len(str2)

        for i in range(len(str1)):
            for j in range(max(0, i - zakres_dopasowan), min(len(str2), i + zakres_dopasowan + 1)):
                if (str1[i] == str2[j] and dopasowania_2[j] == 0):
                    dopasowania_1[i] = 1
                    dopasowania_2[j] = 1
                    licznik_p += 1
                    break

        if licznik_p == 0:
            return 0

        licznik_t = 0
        l = 0

        for k in range(len(str1)):
            if dopasowania_1[k] == 1:
                while dopasowania_2[l] == 0:
                    l += 1
                if str1[k] != str2[l]:
                    licznik_t += 1
                l += 1

        jaro_value = ((licznik_p / len(str1)) + (licznik_p / len(str2)) + ((licznik_p - licznik_t / 2) / licznik_p)) / 3

        skala = 0.1
        rozmiar_prefiksu = 0

        for m in range(4):
            if str1[m] == str2[m]:
                rozmiar_prefiksu += 1
            else:
                break

        jaro_winkler_value = round(jaro_value + skala * rozmiar_prefiksu * (1 - jaro_value), 4)

        return jaro_winkler_value


def levenshtein_distance(str1, str2, maks):
    if len(str1) == 0 and len(str2) != 0:
        return len(str2)
    elif len(str1) != 0 and len(str2) == 0:
        return len(str1)

    if str1 == str2:
        return 1

    if str1[0] == str2[0]:
        str1 = str1[1:]
        str2 = str2[1:]
        return levenshtein_distance(str1, str2, maks)

    macierz = (np.zeros((len(str1) + 1, len(str2) + 1))).astype(int)

    for j in range(len(str1) + 1):
        macierz[j][0] = j

    for i in range(len(str2) + 1):
        macierz[0][i] = i

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                macierz[i][j] = min(macierz[i - 1][j] + 1, macierz[i][j - 1] + 1, macierz[i - 1][j - 1])
            else:
                macierz[i][j] = min(macierz[i - 1][j] + 1, macierz[i][j - 1] + 1, macierz[i - 1][j - 1] + 1)

    levenshtein_value = round(1 - macierz[len(str1), len(str2)] / maks, 4)

    return levenshtein_value


def damerau_levenshtein_distance(str1, str2, maks):
    if len(str1) == 0 and len(str2) != 0:
        return len(str2)
    elif len(str1) != 0 and len(str2) == 0:
        return len(str1)

    if str1 == str2:
        return 1

    macierz = (np.zeros((len(str1) + 1, len(str2) + 1))).astype(int)

    for j in range(len(str1) + 1):
        macierz[j][0] = j

    for i in range(len(str2) + 1):
        macierz[0][i] = i

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                macierz[i][j] = macierz[i - 1][j - 1]
            else:
                macierz[i][j] = min(macierz[i][j - 1] + 1, macierz[i - 1][j] + 1, macierz[i - 1][j - 1] + 1)

                if (i > 1 and j > 1 and str1[i - 1] == str2[j - 2] and str1[i - 2] == str2[j - 1]):
                    macierz[i][j] = min(macierz[i][j], macierz[i - 2][j - 2] + 1)

    damerau_levenshtein_value = round(1 - macierz[len(str1), len(str2)] / maks, 4)

    return damerau_levenshtein_value


def tversky_unigrams_distance(alpha, beta, str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 1])

    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 1])

    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    licznik_xy = 0
    for j in str1_dict:
        if j in str2_dict:
            if str1_dict[j] - str2_dict[j] > 0:
                licznik_xy += str1_dict[j] - str2_dict[j]
        else:
            licznik_xy += str1_dict[j]

    licznik_yx = 0
    for k in str2_dict:
        if k in str1_dict:
            if str2_dict[k] - str1_dict[k] > 0:
                licznik_yx += str2_dict[k] - str1_dict[k]
        else:
            licznik_yx += str2_dict[k]

    tversky_unigrams_value = round(licznik_wspolny / (licznik_wspolny + alpha * licznik_xy + beta * licznik_yx), 4)

    return tversky_unigrams_value


def tversky_bigrams_distance(alpha, beta, str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 2])

    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 2])

    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    licznik_xy = 0
    for j in str1_dict:
        if j in str2_dict:
            if str1_dict[j] - str2_dict[j] > 0:
                licznik_xy += str1_dict[j] - str2_dict[j]
        else:
            licznik_xy += str1_dict[j]

    licznik_yx = 0
    for k in str2_dict:
        if k in str1_dict:
            if str2_dict[k] - str1_dict[k] > 0:
                licznik_yx += str2_dict[k] - str1_dict[k]
        else:
            licznik_yx += str2_dict[k]

    tversky_bigrams_value = round(licznik_wspolny / (licznik_wspolny + alpha * licznik_xy + beta * licznik_yx), 4)

    return tversky_bigrams_value


def tversky_trigrams_distance(alpha, beta, str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 3])

    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 3])

    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    licznik_xy = 0
    for j in str1_dict:
        if j in str2_dict:
            if str1_dict[j] - str2_dict[j] > 0:
                licznik_xy += str1_dict[j] - str2_dict[j]
        else:
            licznik_xy += str1_dict[j]

    licznik_yx = 0
    for k in str2_dict:
        if k in str1_dict:
            if str2_dict[k] - str1_dict[k] > 0:
                licznik_yx += str2_dict[k] - str1_dict[k]
        else:
            licznik_yx += str2_dict[k]

    tversky_trigrams_value = round(licznik_wspolny / (licznik_wspolny + alpha * licznik_xy + beta * licznik_yx), 4)

    return tversky_trigrams_value


def jaccard_unigrams_distance(str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 1])

    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 1])

    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    licznik_xy = 0
    for j in str1_dict:
        if j in str2_dict:
            if str1_dict[j] - str2_dict[j] > 0:
                licznik_xy += str1_dict[j] - str2_dict[j]
        else:
            licznik_xy += str1_dict[j]

    licznik_yx = 0
    for k in str2_dict:
        if k in str1_dict:
            if str2_dict[k] - str1_dict[k] > 0:
                licznik_yx += str2_dict[k] - str1_dict[k]
        else:
            licznik_yx += str2_dict[k]

    jaccard_unigrams_value = round(licznik_wspolny / (licznik_wspolny + (licznik_xy + licznik_yx) * 0.5), 4)

    return jaccard_unigrams_value


def jaccard_bigrams_distance(str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 2])

    str1_dict = dict.fromkeys(str1_list, 0)

    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 2])

    str2_dict = dict.fromkeys(str2_list, 0)

    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    licznik_xy = 0
    for j in str1_dict:
        if j in str2_dict:
            if str1_dict[j] - str2_dict[j] > 0:
                licznik_xy += str1_dict[j] - str2_dict[j]
        else:
            licznik_xy += str1_dict[j]

    licznik_yx = 0
    for k in str2_dict:
        if k in str1_dict:
            if str2_dict[k] - str1_dict[k] > 0:
                licznik_yx += str2_dict[k] - str1_dict[k]
        else:
            licznik_yx += str2_dict[k]

    jaccard_bigrams_value = licznik_wspolny / (licznik_wspolny + (licznik_xy + licznik_yx) * 0.5)

    return round(jaccard_bigrams_value, 4)


def jaccard_trigrams_distance(str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 3])

    str1_dict = dict.fromkeys(str1_list, 0)

    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 3])

    str2_dict = dict.fromkeys(str2_list, 0)

    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    licznik_xy = 0
    for j in str1_dict:
        if j in str2_dict:
            if str1_dict[j] - str2_dict[j] > 0:
                licznik_xy += str1_dict[j] - str2_dict[j]
        else:
            licznik_xy += str1_dict[j]

    licznik_yx = 0
    for k in str2_dict:
        if k in str1_dict:
            if str2_dict[k] - str1_dict[k] > 0:
                licznik_yx += str2_dict[k] - str1_dict[k]
        else:
            licznik_yx += str2_dict[k]

    jaccard_bigrams_value = licznik_wspolny / (licznik_wspolny + (licznik_xy + licznik_yx) * 0.5)

    return round(jaccard_bigrams_value, 4)


def hellinger_unigrams_distance(str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1)):
        str1_list.append(str1[i])

    str1_dict = dict.fromkeys(str1_list, 0)

    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1 / len(str1)

    for j in range(len(str2)):
        str2_list.append(str2[j])

    str2_dict = dict.fromkeys(str2_list, 0)

    for j in range(len(str2_list)):
        str2_dict[str2_list[j]] += 1 / len(str2)

    str12 = str1 + str2

    str12_list = []

    for k in range(len(str12)):
        str12_list.append(str12[k])

    str12_dict = dict.fromkeys(str12_list, 0)

    hellinger_unigrams_sum = 0

    for item in str12_dict:
        if item in str1_dict and item not in str2_dict:
            hellinger_unigrams_sum += str1_dict[item]
        elif item not in str1_dict and item in str2_dict:
            hellinger_unigrams_sum += str2_dict[item]
        elif item in str1_dict and item in str2_dict:
            hellinger_unigrams_sum += pow(np.sqrt(str1_dict[item]) - np.sqrt(str2_dict[item]), 2)

    hellinger_unigrams_value = round(1 - np.sqrt(hellinger_unigrams_sum / 2), 4)

    return hellinger_unigrams_value


def hellinger_bigrams_distance(str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 2])

    str1_dict = dict.fromkeys(str1_list, 0)

    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1 / (len(str1) - 1)

    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 2])

    str2_dict = dict.fromkeys(str2_list, 0)

    for j in range(len(str2_list)):
        str2_dict[str2_list[j]] += 1 / (len(str2) - 1)

    str12 = str1 + str2

    str12_list = []

    for k in range(len(str12) - 1):
        if k != len(str1) - 1:
            str12_list.append(str12[k:k + 2])

    str12_dict = dict.fromkeys(str12_list, 0)

    hellinger_bigrams_sum = 0
    for item in str12_dict:
        if item in str1_dict and item not in str2_dict:
            hellinger_bigrams_sum += str1_dict[item]
        elif item not in str1_dict and item in str2_dict:
            hellinger_bigrams_sum += str2_dict[item]
        elif item in str1_dict and item in str2_dict:
            hellinger_bigrams_sum += pow(np.sqrt(str1_dict[item]) - np.sqrt(str2_dict[item]), 2)

    hellinger_bigrams_value = round(1 - np.sqrt(hellinger_bigrams_sum / 2), 4)

    return hellinger_bigrams_value


def hellinger_trigrams_distance(str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 3])

    str1_dict = dict.fromkeys(str1_list, 0)

    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1 / (len(str1) - 1)

    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 3])

    str2_dict = dict.fromkeys(str2_list, 0)

    for j in range(len(str2_list)):
        str2_dict[str2_list[j]] += 1 / (len(str2) - 1)

    str12 = str1 + str2

    str12_list = []

    for k in range(len(str12) - 1):
        if k != len(str1) - 1 or k != len(str1) - 2:
            str12_list.append(str12[k:k + 3])

    str12_dict = dict.fromkeys(str12_list, 0)

    hellinger_trigrams_sum = 0
    for item in str12_dict:
        if item in str1_dict and item not in str2_dict:
            hellinger_trigrams_sum += str1_dict[item]
        elif item not in str1_dict and item in str2_dict:
            hellinger_trigrams_sum += str2_dict[item]
        elif item in str1_dict and item in str2_dict:
            hellinger_trigrams_sum += pow(np.sqrt(str1_dict[item]) - np.sqrt(str2_dict[item]), 2)

    hellinger_trigrams_value = round(1 - np.sqrt(hellinger_trigrams_sum / 2), 4)

    return hellinger_trigrams_value


def bhattacharyya_unigrams_distance(str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1)):
        str1_list.append(str1[i])

    str1_dict = dict.fromkeys(str1_list, 0)

    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1 / len(str1)

    for j in range(len(str2)):
        str2_list.append(str2[j])

    str2_dict = dict.fromkeys(str2_list, 0)

    for j in range(len(str2_list)):
        str2_dict[str2_list[j]] += 1 / len(str2)

    str12 = str1 + str2

    str12_list = []

    for k in range(len(str12)):
        str12_list.append(str12[k])

    str12_dict = dict.fromkeys(str12_list, 0)

    bhattacharyya_unigrams_sum = 0

    for item in str12_dict:
        if item in str1_dict and item in str2_dict:
            bhattacharyya_unigrams_sum += np.sqrt(str1_dict[item] * str2_dict[item])

    bhattacharyya_unigrams_value = round(bhattacharyya_unigrams_sum, 4)

    return bhattacharyya_unigrams_value


def bhattacharyya_bigrams_distance(str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 2])

    str1_dict = dict.fromkeys(str1_list, 0)

    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1 / (len(str1) - 1)

    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 2])

    str2_dict = dict.fromkeys(str2_list, 0)

    for j in range(len(str2_list)):
        str2_dict[str2_list[j]] += 1 / (len(str2) - 1)

    str12 = str1 + str2

    str12_list = []

    for k in range(len(str12) - 1):
        if k != len(str1) - 1:
            str12_list.append(str12[k:k + 2])

    str12_dict = dict.fromkeys(str12_list, 0)

    bhattacharyya_bigrams_sum = 0

    for item in str12_dict:
        if item in str1_dict and item in str2_dict:
            bhattacharyya_bigrams_sum += np.sqrt(str1_dict[item] * str2_dict[item])

    bhattacharyya_bigrams_value = round(bhattacharyya_bigrams_sum, 4)

    return bhattacharyya_bigrams_value


def bhattacharyya_trigrams_distance(str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 3])

    str1_dict = dict.fromkeys(str1_list, 0)

    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1 / (len(str1) - 1)

    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 3])

    str2_dict = dict.fromkeys(str2_list, 0)

    for j in range(len(str2_list)):
        str2_dict[str2_list[j]] += 1 / (len(str2) - 1)

    str12 = str1 + str2

    str12_list = []

    for k in range(len(str12) - 1):
        if k != len(str1) - 1 and k != len(str1) - 2:
            str12_list.append(str12[k:k + 3])

    str12_dict = dict.fromkeys(str12_list, 0)

    bhattacharyya_trigrams_sum = 0

    for item in str12_dict:
        if item in str1_dict and item in str2_dict:
            bhattacharyya_trigrams_sum += np.sqrt(str1_dict[item] * str2_dict[item])

    bhattacharyya_trigrams_value = round(bhattacharyya_trigrams_sum, 4)

    return bhattacharyya_trigrams_value


def relative_lcs(str1, str2):
    lcs = 0

    for i in range(len(str1)):
        for j in range(len(str2)):

            przesuniecie = 0
            while i + przesuniecie < len(str1) and j + przesuniecie < len(str2) and str1[i + przesuniecie] == str2[
                j + przesuniecie]:
                przesuniecie += 1

            lcs = max(lcs, przesuniecie)

    rlcs_value = round(lcs / max(len(str1), len(str2)), 4)

    return rlcs_value


def Szymkiewicz_Simpson_unigrams(str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1)):
        str1_list.append(str1[i:i + 1])

    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    for j in range(len(str2)):
        str2_list.append(str2[j:j + 1])

    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    ss_unigrams_value = round(licznik_wspolny / min(len(str1), len(str2)), 4)

    return ss_unigrams_value


def Szymkiewicz_Simpson_bigrams(str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 2])

    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 2])

    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    ss_bigrams_value = round(licznik_wspolny / min(len(str1) - 1, len(str2) - 1), 4)

    return ss_bigrams_value


def Szymkiewicz_Simpson_trigrams(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()

    str1_list = []
    str2_list = []

    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 3])

    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 3])

    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    ss_trigrams_value = licznik_wspolny / min(len(str1) - 2, len(str2) - 4)

    return round(ss_trigrams_value, 4)


def Dice_Sorensen_unigrams(str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1)):
        str1_list.append(str1[i:i + 1])

    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    for j in range(len(str2)):
        str2_list.append(str2[j:j + 1])

    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    ds_unigrams_value = round(2 * licznik_wspolny / (len(str1) + len(str2)), 4)

    return ds_unigrams_value


def Dice_Sorensen_bigrams(str1, str2):
    str1_list = []
    str2_list = []

    for i in range(len(str1) - 1):
        str1_list.append(str1[i:i + 2])

    str1_dict = dict.fromkeys(str1_list, 0)
    for i in range(len(str1_list)):
        str1_dict[str1_list[i]] += 1

    for j in range(len(str2) - 1):
        str2_list.append(str2[j:j + 2])

    str2_dict = dict.fromkeys(str2_list, 0)
    for i in range(len(str2_list)):
        str2_dict[str2_list[i]] += 1

    licznik_wspolny = 0
    for i in str1_dict:
        if i in str2_dict:
            licznik_wspolny += min(str1_dict[i], str2_dict[i])

    ds_bigrams_value = round(2 * licznik_wspolny / (len(str1) + len(str2) - 2), 4)

    return ds_bigrams_value


def Dice_Sorensen_trigrams(str1, str2):
    # Zamiana dużych liter na małe, aby uniknąć niewykrycia dużego i małego takiego samego znaku
    str1 = str1.lower()
    str2 = str2.lower()

    # Utworzenie list przechowujących wszystkie dwuznaki ciągów znaków
    str1_list = []
    str2_list = []

    # Dodanie znaków z pierwszego ciągu dwuznaków do listy
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

    # Obliczenie wartości podobieństwa Dice - Sorensena opartej na bigramach
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

    # Ustalenie maksymalnej długosci tekstów po oczyszczeniu
    maks = max(len(str11), len(str12))

    data = pd.DataFrame(columns=('Kod 1', 'Kod 2'))

    data.loc[0] = [str11, str12]

    # Wartosci srednie dla kodow bedacych plagiatem
    u1 = [0.09086, 0.75045, 0.83799, 0.84966, 0.84972, 0.85207, 0.72868, 0.66559, 0.84288, 0.72096, 0.65865, 0.80210,
          0.56177, 0.46754, 0.95833, 0.79932, 0.70513, 0.19584, 0.89178, 0.76186, 0.69672, 0.84308, 0.72096, 0.65982]

    # Odchylenia standardowe dla kodow bedacych plagiatem
    s1 = [0.06512, 0.04076, 0.04585, 0.05361, 0.05353, 0.05082, 0.09358, 0.11874, 0.05353, 0.09498, 0.11963, 0.05160,
          0.09575, 0.10921, 0.02179, 0.08229, 0.11673, 0.13832, 0.04283, 0.08859, 0.11567, 0.05356, 0.09498, 0.11989]

    # Wagi obliczone na podstawie wartosci funkcji dla kodow bedacych i niebedacych plagiatem
    wagi = [0.0204, 0.0393, 0.037, 0.043, 0.043, 0.0377, 0.0502, 0.0509, 0.0395, 0.0509, 0.0512, 0.0309, 0.0441, 0.0491,
            0.0283, 0.0453, 0.05, 0.0342, 0.0194, 0.0453, 0.0486, 0.0395, 0.0509, 0.0512]

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


#for l in range(len(data2)):
#    print(l)
#    data2.loc[l, "Prawdopodobienstwo"] = similarity(data2.loc[l, "Kod 1"], data2.loc[l, "Kod 2"])

#data2.to_csv('similarity5.csv')