#include <iostream>

using namespace std;

int main()
{
    float a{}, b{}, c{}, x{}, y{};

    cout << "Wspolczynniki funkcji kwadratowej\n";
    cout << "Podaj a: ";


    cin >> a;
    cout << "Podaj b: ";
    cin >> b;
    cout << "Podaj c: ";
    cin >> c;

    cout << "******************************************" << endl;
    cout << "Podaj x: ";
    cin >> x;


    cout << "******************************************" << endl;
    cout << "f(x) = " << a << "x^2 + " << b << "x + " << c << endl;
    cout << "******************************************" << endl;


    y = (a * x * x) + (b * x) + c;
    cout << "f(" << x << ") = " << y << endl;
    cout << "******************************************" << endl;
}