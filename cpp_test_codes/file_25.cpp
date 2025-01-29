//program to demonstrates the use of #if, #elif, #else,
// and #endif  preprocessor directives.
#include <stdio.h>

// defining PI
#define PI 3.14159

int main()
{

#ifdef PI
    printf(""PI is defined\n"");

#elif defined(SQUARE)
    printf(""Square is defined\n"");
#else
    #error ""Neither PI nor SQUARE is defined""
#endif

#ifndef SQUARE
    printf(""Square is not defined"");
#else
    cout << ""Square is defined"" << endl;
#endif

    return 0;
}",Advanced
"#include <stdio.h>

// defining MIN_VALUE

#define MIN_VALUE 10


int main() {
    // Undefining and redefining MIN_VALUE
printf(""Min value is: %d\n"",MIN_VALUE);

//undefining max value
#undef MIN_VALUE

// again redefining MIN_VALUE
#define MIN_VALUE 20

    printf(""Min value after undef and again redefining it: %d\n"", MIN_VALUE);

    return 0;
}