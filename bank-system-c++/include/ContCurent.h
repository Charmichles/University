#ifndef CONTCURENT_H
#define CONTCURENT_H

#include "Cont.h"

class ContCurent : public Cont {
  public:
    ContCurent(std::string = "", std::string = "", double = 0, int = 30, std::vector<std::pair<std::pair<std::string, std::string>, double>> = {});
    ContCurent(const ContCurent&);
    void afisare(std::ostream&);
    void depunere(std::string, double);
    void retragere(std::string, double);
    ContCurent& operator = (const ContCurent&);
    ~ContCurent();
  private:
    int gratuit;
    std::vector<std::pair<std::pair<std::string, std::string>, double>> istoric;
    void citire(std::istream&);
  friend std::istream& operator >> (std::istream&, ContCurent&);
};

#endif
