#include <iostream>
#include <cmath>
using namespace std;

int main()
{
    float a{}, b{}, c{}, p{}, P{};
    cout << "Podaj a: ";
    cin >> a;
    cout << "Podaj b: ";
    cin >> b;
    cout << "Podaj c: ";
    cin >> c;


    if ((a + b > c) && (a + c > b) && (b + c > a))
    {

        p = (a + b + c) / 2;

        P = sqrt(p * (p - a) * (p - b) * (p - c));

        cout << "\nPole = " << P;
    }

    else
    {
        cout << "taki trojkat nie istnieje";
    }
}
