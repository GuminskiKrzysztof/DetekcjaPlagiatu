#include <iostream>
#include <cmath>
#include <set>
using namespace std;

const int wielkosc_planszy = 8;

// Utworzenie planszy o wymiarach wielkości planszy - standardowo 8x8
int plansza[wielkosc_planszy][wielkosc_planszy];

// Funkcja, która zapisuje początkowy układ planszy
void konwersjaPlanszyNaTablice(int tab[wielkosc_planszy][wielkosc_planszy], int rozmiar)
{
    // wyjaśnienie oznaczeń pionków i figur na planszy gry
    // 0 - puste pole
    // 1 - biały pionek
    // 11 - biała dama
    // 2 - czerwony pionek
    // 22 - czerwona dama

    for (int i = 0; i < rozmiar; i++)
    {
        for (int j = 0; j < rozmiar; j++)
        {
            if (((j + j) % 2) == 0)
            {
                tab[i][j] = 0;
            }
        }
    }
    // ustawienie białych figur na planszy
    const int bdamy = 11;
    const int bpionki = 1;
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < rozmiar; j++)
        {
            // warunek spełniony dla ustawianych dam
            if (((i + j) % 2 == 0) && (i == 0))
            {
                tab[i][j] = bdamy;
            }
            // warunek spełniony dla ustawianych pionkow
            else if (((i + j) % 2 == 0))
            {
                tab[i][j] = bpionki;
            }
        }
    }
    // ustawienie czerwonych figur na planszy
    const int czdamy = 22;
    const int czpionki = 2;
    for (int i = 5; i < rozmiar; i++)
    {
        for (int j = 0; j < rozmiar; j++)
        {
            // warunek spełniony dla ustawianych dam
            if (((i + j) % 2 == 0) && (i == rozmiar - 1))
            {
                tab[i][j] = czdamy;
            }
            // warunek spełniony dla ustawianych pionkow
            else if (((i + j) % 2 == 0))
            {
                tab[i][j] = czpionki;
            }
        }
    }
}