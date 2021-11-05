#include <iostream>

#include "Banca.h"

int main() {
    std::cout << "Modul de introducere a datelor pentru GestiuneConturi este: numele locatiei si cate conturi sunt deschise la acea locatie.\n";
    std::cout << "Pentru GestiuneConturi<Cont> putem introduce daca vrem ContEcon sau ContCurent, iar pentru restul doar tipul declarat.\n";
    std::cout << "Pentru ContEcon se citeste pe rand: data de start, numele titularului, soldul de start, rata dobanzii, perioada dobanzii, cate intrari are istoricul(0 pentru cont nou).\n";
    std::cout << "Pentru ContCurent se citeste pe rand: data de start, numele titularului, soldul de start si numarul de tranzactii gratuite ramase.\n";
    GestionareConturi<Cont> g;
    std::cin >> g;
    g.afisare(std::cout);
    auto c = g.getconturi();
    for (x : c) {
        Cont* t = g.findcont(x.first);
        t->depunere("05-10-2020", 150);
        ContCurent* m = dynamic_cast<ContCurent*>(t);
        if (m) {
            m->retragere("05-10-2020", 50);
        }
    }
    g.afisare(std::cout);
    return 0;
}
