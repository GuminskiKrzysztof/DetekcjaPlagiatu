#include <iostream>
#include "funkcje.h"

using namespace std;


int main()
{

    int a;

    float b;

    int d;
	char n1[30];


	char n2[30];


	cout << "Podaj napis 1: ";


	cin.getline(n1, 30);


	cout << "Podaj napis 2: ";

	cin.getline(n2, 30);

	czyZnaleziono(n1, n2);
}