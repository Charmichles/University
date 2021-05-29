#ifndef CONTECON_H
#define CONTECON_H

#include "Cont.h"

class ContEcon : public Cont {
  public:
    ContEcon(std::string = "", std::string = "", double = 0, double = 0, std::string = "", std::vector<std::pair<std::string, double>> = {});
    ContEcon(const ContEcon&);
    void afisare(std::ostream&);
    void depunere(std::string, double);
    void actualizare(std::string);
    ContEcon& operator = (const ContEcon&);
    std::string getperioada() const;
    ~ContEcon();
  private:
    double rata;
    std::string perioada;
    std::string last_upd;
    std::vector<std::pair<std::string, double>> istoric;
    void citire(std::istream&);
  friend std::istream& operator >> (std::istream&, ContEcon&);
};

#endif
