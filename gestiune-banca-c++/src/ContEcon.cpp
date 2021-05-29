#include "ContEcon.h"

ContEcon::ContEcon(std::string d, std::string t, double s, double r, std::string p, std::vector<std::pair<std::string, double>> i) : Cont(d, t, s) {
    rata = r;
    perioada = p;
    istoric = i;
    last_upd = d;
}

ContEcon::ContEcon(const ContEcon& c) : Cont(c) {
    rata = c.rata;
    perioada = c.perioada;
    istoric = c.istoric;
    last_upd = c.last_upd;
}

void ContEcon::afisare(std::ostream& out) {
    out << cod << " | " << data << " | " << titular << " | " << sold << '\n';
    out << rata << " o data la " << perioada << '\n';
    out << "Istoric:\n";
    for (auto p : istoric) {
        out << p.first << " | " << p.second << '\n';
    }
    out << '\n' << '\n';
}

void ContEcon::depunere(std::string d, double s) {
    sold += s;
    istoric.push_back(make_pair(d, sold));
}

void ContEcon::actualizare(std::string d) {
    /// sold += sold * rata daca d = last_upd + perioada
    /// last_upd = d
}

ContEcon& ContEcon::operator = (const ContEcon& c) {
    data = c.data;
    titular = c.titular;
    sold = c.sold;
    cod = c.cod;
    rata = c.rata;
    perioada = c.perioada;
    istoric = c.istoric;
    last_upd = c.last_upd;
    return *this;
}

std::string ContEcon::getperioada() const {
    return perioada;
}

ContEcon::~ContEcon() {
    rata = 0;
    perioada = "sters";
    last_upd = "sters";
    istoric.clear();
}

void ContEcon::citire(std::istream& in) {
    in >> data >> titular >> sold >> rata >> perioada;
    int n;
    in >> n;
    if (n == 0) {
        istoric.push_back(make_pair(data, sold));
    }
    for (int i = 0; i < n; i++) {
        std::string d;
        double s;
        in >> d >> s;
        istoric.push_back(make_pair(d, s));
    }
    last_upd = data;
}

std::istream& operator >> (std::istream& in, ContEcon& c) {
    c.citire(in);
    return in;
}
