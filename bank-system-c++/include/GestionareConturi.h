#ifndef GESTIONARECONTURI_H_INCLUDED
#define GESTIONARECONTURI_H_INCLUDED

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

template <class T>
class GestionareConturi {
  public:
    GestionareConturi(std::string = "", std::vector<T*> = {});
    void operator += (const T&);
    void afisare(std::ostream&);
    void delcont(std::string);
    void cerinta(std::ostream&);
    std::unordered_map<std::string, T*> getconturi() const;
    T* findcont(std::string);
    ~GestionareConturi();
  private:
    static int total;
    std::string nume;
    std::unordered_map<std::string, T*> conturi;
    void citire(std::istream&);
  template <class U> friend std::istream& operator >> (std::istream&, GestionareConturi<U>&);
};

template <class T> int GestionareConturi<T>::total = 0;

template <class T> std::unordered_map<std::string, T*> GestionareConturi<T>::getconturi() const {
    return conturi;
}

template <> void GestionareConturi<Cont>::cerinta(std::ostream& out) {
    out << "Sucursala: " << nume << '\n';
    bool flag = false;
    for (auto c : conturi) {
        ContEcon* p = dynamic_cast<ContEcon*>(c.second);
        if (p && p->getperioada() == "1an") {
            p->afisare(out);
            flag = true;
        }
    }
    if (flag == false) {
        out << "Nu exista conturi de economii cu perioada dobanzii 1 an.\n\n";
    }
}

template <> void GestionareConturi<ContEcon>::cerinta(std::ostream& out) {
    out << "Sucursala: " << nume << '\n';
    bool flag = false;
    for (auto c : conturi) {
        if (c.second->getperioada() == "1an") {
            c.second->afisare(out);
            flag = true;
        }
    }
    if (flag == false) {
        out << "Nu exista conturi de economii cu perioada dobanzii 1 an.\n\n";
    }
}

template <> void GestionareConturi<ContCurent>::cerinta(std::ostream& out) {
    out << "Sucursala: " << nume << '\n';
    out << "Acest catalog de conturi contine numai conturi curente, deci nu este nici un cont de economii cu perioada dobanzii 1 an.\n\n";
}

template<class T> void GestionareConturi<T>::delcont(std::string cod) {
    auto c = conturi.find(cod);
    delete c->second;
    total -= 1;
    conturi.erase(c);
}

template<class T> T* GestionareConturi<T>::findcont(std::string cod) {
    return conturi.find(cod)->second;
}

template <> void GestionareConturi<Cont>::citire(std::istream& in) {
    in >> nume;
    int n;
    in >> n;
    total += n;
    for (int i = 0; i < n; i++) {
        std::string tip;
        in >> tip;
        if (tip == "ContEcon") {
            Cont* c = new ContEcon;
            in >> *c;
            conturi.insert(make_pair(c->getcod(), c));
        }
        else if (tip == "ContCurent") {
            Cont* c = new ContCurent;
            in >> *c;
            conturi.insert(make_pair(c->getcod(), c));
        }
        else {/*throw exception*/}
    }
}

template <> void GestionareConturi<ContEcon>::citire(std::istream& in) {
    in >> nume;
    int n;
    in >> n;
    total += n;
    for (int i = 0; i < n; i++) {
        ContEcon* c = new ContEcon;
        in >> *c;
        conturi.insert(make_pair(c->getcod(), c));
    }
}

template <> void GestionareConturi<ContCurent>::citire(std::istream& in) {
    in >> nume;
    int n;
    in >> n;
    total += n;
    for (int i = 0; i < n; i++) {
        ContCurent* c = new ContCurent;
        in >> *c;
        conturi.insert(make_pair(c->getcod(), c));
    }
}

template <class T> std::istream& operator >> (std::istream& in, GestionareConturi<T>& g) {
    g.citire(in);
    return in;
}

template <class T> GestionareConturi<T>::GestionareConturi(std::string n, std::vector<T*> v) {
    nume = n;
    for (T* c : v) {
        total++;
        conturi.insert(make_pair(c->getcod(), c));
    }
}

template <class T> GestionareConturi<T>::~GestionareConturi() {
    total -= conturi.size();
    nume = "sters";
    for (auto c : conturi) {
        delete c.second;
    }
    conturi.clear();
}

template <class T> void GestionareConturi<T>::operator += (const T& c) {
    total++;
    conturi.insert(make_pair(c.getcod(), &c));
}

template <class T> void GestionareConturi<T>::afisare(std::ostream& out) {
    out << "Nr. de conturi: " << conturi.size() << " la sucursala: " << nume << '\n' << '\n';
    for (auto c : conturi) {
        c.second->afisare(out);
    }
}

#endif
