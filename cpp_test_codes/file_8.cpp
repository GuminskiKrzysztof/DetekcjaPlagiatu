#include<iostream>
using namespace std;

int nr_wiersza = 0;
cout.width(3);
cout << nr_wiersza << ") ";
for (int i = 0; i < 101; i++)
{


	cout.width(3);
	if (i % 3 == 0)
		cout << i << " ";




	if (i % 10 == 0)
	{


		cout << endl;
		nr_wiersza++;
		cout.width(3);
		if (nr_wiersza <= 10)
				cout << nr_wiersza << ") ";
	}
}



cout << endl;