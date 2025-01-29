#include <iostream>
#include <cmath>

using namespace std;

int main()
{
    float a{}, b{}, c{}, x{}, y{}, delta{}, x1{}, x2{};

    cout << "Wspolczynniki funkcji kwadratowej\n";
    cout << "Podaj a: ";
    cin >> a;
    cout << "Podaj b: ";
    cin >> b;
    cout << "Podaj c: ";
    cin >> c;

    if (a == 0)
    {
        cout << "To funkcja liniowa!";
    }

    else
    {
        cout << "******************************************" << endl;
        cout << "Podaj x: ";
        cin >> x;
        cout << "******************************************" << endl;
        cout << "Funkcja kwadratowa: f(x) = ";

        //a
        if (a < 0)
        {
            cout << " - ";
        }
        if (abs(a) != 1)
        {
            cout << abs(a);
        }
        cout << "x^2";

        //b
        if (b != 0)
        {
            if (b > 0)
            {
                cout << " + ";
            }
            else
            {
                cout << " - ";
            }
            if (abs(b) != 1)
            {
                cout << abs(b);
            }
            cout << "x";
        }

        //c
        if (c > 0)
        {
            cout << " + ";
        }
        else if (c < 0)
        {
            cout << " - ";
        }
        if (c != 0)
        {
            cout << abs(c);
        }

        cout << "\n******************************************" << endl;
        y = (a * x * x) + (b * x) + c;
        cout << "f(" << x << ") = " << y << endl;
        cout << "******************************************" << endl;

        delta = b * b - 4 * a * c;

        if (delta > 0)
        {
            cout << "Funkcja posiada dwa miejsca zerowe." << endl;
            x1 = (-b - sqrt(delta)) / (2 * a);
            x2 = (-b + sqrt(delta)) / (2 * a);
            cout << "Miejsca zerowe funkcji: x1 = " << x1 << " i x2 = " << x2 << endl;
        }
        else if (delta == 0)
        {
            cout << "Funkcja posiada jedno miejsce zerowe." << endl;
            x1 = -b / (2 * a);
            cout << "Miejsce zerowe funkcji: x0 = " << x1 << endl;
        }
        else
        {
            cout << "Funkcja mie posiada miejsc zerowych." << endl;
        }
    }
}