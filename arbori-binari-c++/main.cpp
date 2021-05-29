#include <iostream>
#include <fstream>
#include "arbori.h"

using namespace std;

std::ofstream fout("output.txt");
std::ifstream fin("input.txt");

int main()
{
    int n;
    std::cout << "Cati arbori?\n";
    std::cin >> n;
    Arbore_oarecare* v[n];
    std::cout << "Arbori oarecare:\n";
    for (int i = 0; i < n / 2; i++) {
        int x;
        std::cout << "Cate noduri are arborele?\n";
        std::cin >> x;
        if (x < 1) continue;
        Arbore_oarecare* a = new Arbore_oarecare(x);
        try {std::cin >> a;}
        catch (const char* e) {std::cout << e << '\n'; i--; n--; continue;}
        v[i] = a;
    }
    std::cout << "Arbori binari:\n";
    for (int i = n / 2; i < n; i++) {
        int x;
        std::cout << "Cate noduri are arborele?\n";
        std::cin >> x;
        if (x < 1) continue;
        Arbore_oarecare* a = new Arbore_binar(x);
        try {std::cin >> a;}
        catch (const char* e) {std::cout << e << '\n'; i--; n--; continue;}
        v[i] = a;
    }
    for (int i = 0; i < n; i++) {
        std::cout << "Arborele: " << i + 1 << '\n' << v[i] << '\n';
    }
    return 0;
}
