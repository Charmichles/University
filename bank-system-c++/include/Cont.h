#ifndef CONT_H
#define CONT_H

#include <iostream>
#include <string>
#include <vector>
#include <unordered_set>
#include <random>
#include <functional>
#include <time.h>

class Cont {
  public:
    Cont(std::string = "", std::string = "", double = 0);
    Cont(const Cont&);
    virtual void afisare(std::ostream&);
    virtual void depunere(std::string, double) = 0;
    Cont& operator = (const Cont&);
    std::string getcod() const;
    virtual ~Cont();
  protected:
    std::string data;
    std::string titular;
    double sold;
    std::string cod;
  private:
    static std::unordered_set<std::string> coduri;
    virtual void citire(std::istream&);
    std::string randcod();
  friend std::istream& operator >> (std::istream&, Cont&);
};

#endif
