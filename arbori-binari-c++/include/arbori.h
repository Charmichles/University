#ifndef ARBORI_H
#define ARBORI_H

#include <iostream>

class Nod {
  public:
    Nod(int info = -1, int nr_copii = 0, Nod* copii = nullptr) : info{info}, nr_copii{nr_copii}, copii{copii} {}
    void adaugaCopil(int);
    void afisCopii(std::ostream&);
    Nod* getCopil(int);
    int getNrCopii();
    int getInfo();
    void setNrCopii(int);
    void setInfo(int);
    void stergeCopii(Nod*);
    ~Nod();
  private:
    int info;
    int nr_copii;
    Nod* copii[10];
  friend std::istream& operator >> (std::istream&, Nod*&);
};

class Arbore {
  public:
    Arbore(int nr_noduri = 0) : nr_noduri{nr_noduri} {}
    int getNrNoduri();
    ~Arbore();
  protected:
    int nr_noduri;
};

class Arbore_oarecare : public Arbore {
  public:
    Arbore_oarecare(int nr_noduri = 0, int rad_info = 0) : Arbore{nr_noduri}, rad{new Nod(rad_info)} {}
    Nod* getRad();
    virtual ~Arbore_oarecare();
  private:
    void afisDFS(Nod*, std::ostream&);
    void afisBFS(Nod*, std::ostream&);
    virtual void afis(std::ostream&);
    virtual void citire(std::istream&);
  protected:
    Nod* rad;
  friend std::ostream& operator << (std::ostream&, Arbore_oarecare*&);
  friend std::istream& operator >> (std::istream&, Arbore_oarecare*&);

};

class Arbore_binar : public Arbore_oarecare {
  public:
      Arbore_binar(int nr_noduri = 0, int rad_info = 0) : Arbore_oarecare{nr_noduri, rad_info} {}
      ~Arbore_binar() {}
  private:
    void afisInorder(Nod*, std::ostream&);
    void afisPostorder(Nod*, std::ostream&);
    void afisPreorder(Nod*, std::ostream&);
    void afis(std::ostream&);
    void citire(std::istream&);
  friend std::ostream& operator << (std::ostream&, Arbore_binar*&);
  friend std::istream& operator >> (std::istream&, Arbore_binar*&);
};

#endif // ARBORI_H
