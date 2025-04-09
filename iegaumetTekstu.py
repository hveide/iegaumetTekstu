import os, sys
def ievade():
    global teksts
    ievadeTeksts = input("Iekopējiet savu tekstu (Teksta beigās ievadiet Ctrl+Z + Enter) vai norādiet teksta faila nosaukumu (.txt): ")
    if ".txt" in ievadeTeksts:
        if os.path.exists(ievadeTeksts):
            with open(ievadeTeksts, "r") as f:
                teksts = f.read()
        else:
            print("Šāds fails neeksistē dotajā mapē.")
            ievade()
    elif ievadeTeksts == "":
        exit()
    else:
        lines = sys.stdin.readlines()
        teksts = ''.join(lines)
        teksts = ievadeTeksts + "\n" + teksts
    if teksts[-1] == "\n":
        teksts = teksts[:-1]
    macities(teksts)
def macities(teksts):
    rindkopas = teksts.split('\n')
    i = 0
    for rindkopa in rindkopas:
        if rindkopa == "":
            rindkopas.pop(i)
        i += 1
    fragments = []
    rindkopuIzvele = input("Izvēlaties rindkopas, kuras vēlaties mācīties, piemēram, 1, 1-3, vai p priekš pilna teksta: ")
    if rindkopuIzvele.isdigit():
        rindkopuIzvele = int(rindkopuIzvele) - 1
        try:
            fragments.append(rindkopas[rindkopuIzvele])
        except IndexError:
            print("Nepareizi ievadīts rindkopas numurs")
            macities(teksts)
    elif "-" in rindkopuIzvele:
        rindkopa1, rindkopa2 = rindkopuIzvele.split('-')
        try:
            rindkopa1 = int(rindkopa1) - 1
            rindkopa2 = int(rindkopa2) - 1
        except ValueError:
            print("Nepareiza rindkopu izvēle")
            macities(teksts)
        try:
            rindkopas[rindkopa1] # Kļuda ja ievada a-b, tad 1
            rindkopas[rindkopa2]
            fragments = rindkopas[rindkopa1:rindkopa2]
        except IndexError:
            print("Rindkopu izvēle pāriet rindkopu skaitu")
            macities(teksts)
    print(fragments)

if __name__ == "__main__":
    ievade()