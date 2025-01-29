#include<iostream>
#include<iomanip>
using namespace std;

int main()
{
	int rozmiar = 0;
	cout << "Podaj liczbe: ";
	cin >> rozmiar;

	// wersja 1
	for (int i = 0; i < rozmiar; i++)
	{
		for (int j = 0; j < rozmiar - i; j++)
		{
			cout << "*";
		}
		cout << endl;
	}

	cout << endl;

	// wersja 2
	for (int i = rozmiar; i > 0; i--)
	{
		for (int j = 0; j < i; j++)
		{
			cout << "*";
		}
		cout << endl;
	}

	cout << endl;

	// wersja 3
	for (int i = rozmiar; i > 0; i--)
	{
		cout.width(i);
		cout.fill('*');
		cout << "" << endl;
	}

	cout << endl;
	system("pause");
}