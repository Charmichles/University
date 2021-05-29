# PENTRU AUTOMATE DETERMINISTICE

# Structura de date:
# dictionar cu key: numele starii curente
#              value: dictionar cu key: numele starii urmatoare
#                                  value: dictionar cu key: litera cuvant
#                                                      value: dictionar cu key: litera pentru pop
#                                                                          value: lista de tupluri (litera_push1, litera_push2, ...)

# Date de intrare sub forma:
#   stare_initiala
#   lista_stari_finale
#   nr_tranzitii
#   De nr_tranzitii ori:
#       stare_curenta stare_tranzitie 
#       nr_moduri
#       De nr_moduri ori:
#           litera_cuvant litera_pop lista_litere_push

# Caractere speciale:
# $ - capul stivei
# & - caracterul vid

def validate(test, idx, stare, stack):
    global pda, stari_finale
    if idx == len(test) and stare in stari_finale:
        return True
    elif idx == len(test):
        # sa caute pentru caracterul & in starile urmatoare
        for starea_urmatoare in pda[stare]:
            for litera_urmatoare in pda[stare][starea_urmatoare]:
                if litera_urmatoare == '&' and stack[-1] in pda[stare][starea_urmatoare][litera_urmatoare]:
                    return validate(test, idx, starea_urmatoare, stack)
    else:
        for starea_urmatoare in pda[stare]:
            for litera_urmatoare in pda[stare][starea_urmatoare]:
                if litera_urmatoare == test[idx]:
                    for litera_pop in pda[stare][starea_urmatoare][litera_urmatoare]:
                        # sa tin cont cand nu poppeaza nimic, adica caracterul &
                        if (litera_pop == stack[-1] or litera_pop == '&'):
                            if (litera_pop != '&'):
                                stack.pop(-1)
                            for lista_push in pda[stare][starea_urmatoare][litera_urmatoare][litera_pop]:
                                # sa tin cont cand nu pusheaza nimic, adica caracterul &
                                for litera_push in reversed(lista_push):
                                    if litera_push != '&':
                                        stack.append(litera_push)
                                return validate(test, idx + 1, starea_urmatoare, stack)

input_file_name = "pda.txt"
input_file = open(input_file_name, 'r')
pda = {}
stare_initiala = input_file.readline().replace("\n", "")
stari_finale = set(input_file.readline().split())
nr_tranzitii = int(input_file.readline())
for _ in range(nr_tranzitii):
    stari = input_file.readline().split()
    if stari[0] not in pda:
        pda[stari[0]] = {}
    pda[stari[0]][stari[1]] = {}
    nr_moduri = int(input_file.readline())
    for __ in range(nr_moduri):
        mod = input_file.readline().split()
        if mod[0] not in pda[stari[0]][stari[1]]:
            pda[stari[0]][stari[1]][mod[0]] = {}
        if mod[1] not in pda[stari[0]][stari[1]][mod[0]]:
            pda[stari[0]][stari[1]][mod[0]][mod[1]] = []
        pda[stari[0]][stari[1]][mod[0]][mod[1]].append(tuple(mod[2:]))

n = int(input("Nr. teste: "))
for _ in range(n):
    test = input("Cuvantul testat este: ")
    if validate(test, 0, stare_initiala, ['$']) == True:
        print("Cuvantul {} este acceptat de catre automatul dat.".format(test))
    else:
        print("Cuvantul {} nu este acceptat de catre automatul dat.".format(test))

