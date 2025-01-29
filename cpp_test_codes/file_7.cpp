#include<iostream>
using namespace std;

int main()
{
	double a{}, b{}, c{};
	double x1{}, x2{}, delta{};

	cout << "Wspolczynniki funkcji kwadratowej" << endl;
	cout << "Podaj a: ";
	cin >> a;
	cout << "Podaj b: ";
	cin >> b;
	cout << "Podaj c: ";
	cin >> c;

	// funkcja kwadratowa
	if (a != 0)
	{
		cout << endl << "**********************************************" << endl;
		cout << "Funkcja kwadratowa: f(x) = ";

		if (a == -1)
		{
			cout << "-x^2 ";
		}

		if (a == 1)
		{
			cout << "x^2 ";
		}

		if (a != -1 && a != 1)
		{
			cout << a << "x^2 ";
		}



		if (b < 0)
		{
			if (b == -1)
				cout << "- x ";
			else
				cout << b << "x ";
		}

		if (b > 0)
		{
			if (b == 1)
				cout << "+ x ";
			else
				cout << "+ " << b << "x ";
		}


		if (c < 0)
		{
			cout << c << endl;
		}
		else if (c > 0)
			cout << "+ " << c << endl;
		else
			cout << endl;

		cout << "**********************************************" << endl << endl;

		delta = b * b - 4.0 * a * c;
		if (delta > 0)
		{
			x1 = (-b - sqrt(delta)) / (2.0 * a);
			x2 = (-b + sqrt(delta)) / (2.0 * a);
			cout << "Funkcja posiada dwa miejsca zerowe, x1 = " << x1 << ", x2 = " << x2 << endl;

		}

		if (delta == 0)
		{
			x1 = -b / (2.0 * a);
			cout << "Funkcja posiada jedno miejsce zerowe, rowne x0 = " << x1 << endl;
		}

		if (delta < 0)
		{
			cout << "Funkcja nie posiada miejsc zerowych." << endl;
		}
	}


	system("pause");
}