#include <iostream>
#include <iomanip>
#include "funkcje.h"
#include <random>

using namespace std;

bool czyZnaleziono(char* n1, char* n2)
{
	for (int i = 0; i < 5 ; i++)
	{
		for (int j = 0; j < 3; j++)
		{
			if (n1[i] != n2[j])
			{
				break;


			}
			if (j == 2)
			{
				return true;


			}
		}
	}



	return false;



}