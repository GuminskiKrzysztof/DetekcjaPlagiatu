#include <iostream>
#include <iomanip>
#include "funkcje.h"

using namespace std;

//Zadanie 5 - Labolatorium 3
void ile_moge_kupic(double zlotowki = 100)
{
	cout << "Za kwote "<<zlotowki << " zl mozesz zakupic:\n";
	cout << "******************************\n";
	cout.width(10);
	cout << fixed << setprecision(2) << zlotowki /euro << " euro\n";
	cout.width(10);
	cout << zlotowki /dolar << " dolarow\n";
	cout.width(10);
	cout << zlotowki /korona << " koron norweskich\n";
	cout << "******************************\n";
}

//Zadanie 2 - Labolatorium 4
int zliczLiteryA(char tekst[])
{
	int licznik = 0;
	int i = 0;
	while (tekst[i] != 0)
	{
		licznik++;
		i++;
	}
	return licznik;
}