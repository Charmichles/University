#include "Cont.h"

std::unordered_set<std::string> Cont::coduri = {};

Cont::Cont(std::string d, std::string t, double s) {
    data = d;
    titular = t;
    sold = s;
    do {
        cod = randcod();
    } while (coduri.find(cod) != coduri.end());
    coduri.insert(cod);
}

Cont::Cont(const Cont& c) {
    data = c.data;
    titular = c.titular;
    sold = c.sold;
    cod = c.cod;
}

void Cont::afisare(std::ostream& out) {
    out << cod << " | " << data << " | " << titular << " | " << sold << '\n' << '\n';
}

Cont& Cont::operator = (const Cont& c) {
    data = c.data;
    titular = c.titular;
    sold = c.sold;
    cod = c.cod;
    return *this;
}

std::string Cont::getcod() const {
    return cod;
}

Cont::~Cont() {
    data = "sters";
    titular = "sters";
    sold = 0;
    coduri.erase(cod);
    cod = "sters";
}

std::string Cont::randcod() {
    std::string cod = "";
    auto seed = time(nullptr);
    std::default_random_engine generator (seed);
    std::uniform_int_distribution<int> distribution(0, 9);
    auto dice = std::bind (distribution, generator);
    for (int i = 0; i < 16; i++) {
        cod.push_back(static_cast<char>(dice() + '0'));
    }
    return cod;
}

void Cont::citire(std::istream& in) {
    in >> data >> titular >> sold;
}

std::istream& operator >> (std::istream& in, Cont& c) {
    c.citire(in);
    return in;
}
