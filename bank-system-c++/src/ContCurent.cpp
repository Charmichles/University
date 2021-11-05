#include "ContCurent.h"

ContCurent::ContCurent(std::string d, std::string t, double s, int g, std::vector<std::pair<std::pair<std::string, std::string>, double>> i) : Cont(d, t, s) {
    gratuit = g;
    istoric = i;
}

ContCurent::ContCurent(const ContCurent& c) : Cont(c) {
    gratuit = c.gratuit;
    istoric = c.istoric;
}

void ContCurent::afisare(std::ostream& out) {
    out << cod << " | " << data << " | " << titular << " | " << sold << '\n';
    out << "Tranzactii gratuite ramase: " << gratuit << '\n';
    out << "Istoric:\n";
    for (auto p1 : istoric) {
        out << p1.first.first << " | " << p1.first.second << " | " << p1.second << '\n';
    }
    out << '\n' << '\n';
}

void ContCurent::depunere(std::string d, double s) {
    sold += s;
    istoric.push_back(make_pair(make_pair(d, "depunere"), s));
}

void ContCurent::retragere(std::string d, double s) {
    sold -= s;
    istoric.push_back(make_pair(make_pair(d, "retragere"), s));
}

ContCurent& ContCurent::operator = (const ContCurent& c) {
    data = c.data;
    titular = c.titular;
    sold = c.sold;
    cod = c.cod;
    gratuit = c.gratuit;
    istoric = c.istoric;
    return *this;
}

ContCurent::~ContCurent() {
    gratuit = 0;
    istoric.clear();
}

void ContCurent::citire(std::istream& in) {
    in >> data >> titular >> sold >> gratuit;
    istoric.push_back(make_pair(make_pair(data, "start"), sold));
}

std::istream& operator >> (std::istream& in, ContCurent& c) {
    c.citire(in);
    return in;
}
