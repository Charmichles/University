#include "arbori.h"

void Nod::adaugaCopil(int info) {
    if (nr_copii > 10) throw "MaxCopii";
    copii[nr_copii++] = new Nod(info);
}

void Nod::afisCopii(std::ostream& out = std::cout) {
    for (int i = 0; i < nr_copii; i++) out << copii[i]->info << ' ';
    out << '\n';
}

Nod* Nod::getCopil(int idx) {
    if (nr_copii == 0) return nullptr;
    if (idx < 0 || idx >= nr_copii) throw "InvalidIndexGet";
    return copii[idx];
}

int Nod::getNrCopii() {
    return nr_copii;
}

int Nod::getInfo() {
    return info;
}

void Nod::stergeCopii(Nod* start) {
    for (int i = 0; i < start->nr_copii; i++) stergeCopii(start->copii[i]);
    delete start;
}

void Nod::setInfo(int i) {
    info = i;
}

void Nod::setNrCopii(int nr) {
    nr_copii = nr;
}

std::istream& operator >> (std::istream& in, Nod*& n) {
    if (&in == &std::cin) {
        if (n->info != -1) std::cout << "Nodul curent contine: " << n->info << ". ";
        std::cout << "Introduceti ";
        if (n->info == -1) std::cout << " informatia din nod, ";
        std::cout << "numarul de copii si apoi copiii.\n";
    }
    int x, y;
    if (n->info == -1) {
        in >> x;
        n->info = x;
    }
    in >> y;
    for (int i = 0; i < y; i++) {
        in >> x;
        n->adaugaCopil(x);
    }
    return in;
}

Nod::~Nod() {
    info = 0;
    nr_copii = 0;
}

int Arbore::getNrNoduri() {
    return nr_noduri;
}

Arbore::~Arbore() {
    nr_noduri = 0;
}

void Arbore_oarecare::afisBFS(Nod* start, std::ostream& out = std::cout) {
    Nod* q[nr_noduri];
    int idx_start = 0, idx_end = 0;
    q[idx_end++] = start;
    while (idx_start < idx_end) {
        for (int i = 0; i < q[idx_start]->getNrCopii(); i++) q[idx_end++] = q[idx_start]->getCopil(i);
        out << q[idx_start++]->getInfo() << ' ';
    }
}

void Arbore_oarecare::afisDFS(Nod* start, std::ostream& out = std::cout) {
    for (int i = 0; i < start->getNrCopii(); i++) afisDFS(start->getCopil(i), out);
    out << start->getInfo() << ' ';
}

Nod* Arbore_oarecare::getRad() {
    return rad;
}

void Arbore_oarecare::afis(std::ostream& out = std::cout) {
    out << "DFS:\n";
    afisDFS(getRad(), out);
    out << '\n';
    out << "BFS:\n";
    afisBFS(getRad(), out);
    out << '\n';
}

void Arbore_oarecare::citire(std::istream& in = std::cin) {
    rad->stergeCopii(rad);
    Nod* n = new Nod;
    in >> n;
    rad = n;
    Nod* q[nr_noduri];
    int qsize = 0;
    q[qsize++] = rad;
    for (int i = 0; i < qsize; i++) {
        for (int j = 0; j < q[i]->getNrCopii(); j++) {
            n = q[i]->getCopil(j);
            in >> n;
            q[qsize++] = q[i]->getCopil(j);
        }
    }
}

Arbore_oarecare::~Arbore_oarecare() {
    rad->stergeCopii(rad);
}

void Arbore_binar::afisInorder(Nod* start, std::ostream& out = std::cout) {
    if (start == nullptr) return;
    afisInorder(start->getCopil(0));
    out << start->getInfo() << ' ';
    afisInorder(start->getCopil(1));
}

void Arbore_binar::afisPreorder(Nod* start, std::ostream& out = std::cout) {
    if (start == nullptr) return;
    out << start->getInfo() << ' ';
    afisPreorder(start->getCopil(0));
    afisPreorder(start->getCopil(1));
}

void Arbore_binar::afisPostorder(Nod* start, std::ostream& out = std::cout) {
    if (start == nullptr) return;
    afisPostorder(start->getCopil(0));
    afisPostorder(start->getCopil(1));
    out << start->getInfo() << ' ';
}

void Arbore_binar::afis(std::ostream& out = std::cout) {
    out << "Inorder:\n";
    afisInorder(getRad());
    out << '\n';
    out << "Preorder:\n";
    afisPreorder(getRad());
    out << '\n';
    out << "Postorder:\n";
    afisPostorder(getRad());
    out << '\n';
}

void Arbore_binar::citire(std::istream& in = std::cin) {
    rad->stergeCopii(rad);
    Nod* n = new Nod;
    in >> n;
    if (n->getNrCopii() > 2) throw "BinaryTreeStructureViolation";
    rad = n;
    Nod* q[nr_noduri];
    int qsize = 0;
    q[qsize++] = rad;
    for (int i = 0; i < qsize; i++) {
        for (int j = 0; j < q[i]->getNrCopii(); j++) {
            n = q[i]->getCopil(j);
            in >> n;
            if (n->getNrCopii() > 2) throw "BinaryTreeStructureViolation";
            q[qsize++] = q[i]->getCopil(j);
        }
    }
}

std::ostream& operator << (std::ostream& out, Arbore_binar*& a) {
    a->afis(out);
    return out;
}

std::ostream& operator << (std::ostream& out, Arbore_oarecare*& a) {
    a->afis(out);
    return out;
}

std::istream& operator >> (std::istream& in, Arbore_binar*& a) {
    a->citire(in);
    return in;
}

std::istream& operator >> (std::istream& in, Arbore_oarecare*& a) {
    a->citire(in);
    return in;
}
