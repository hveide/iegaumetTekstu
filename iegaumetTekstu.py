import os, sys, difflib
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
    turpinat = True
    while turpinat:
        turpinat = macities(teksts)
def macities(teksts):
    rindkopas = teksts.split('\n')
    i = 0
    for rindkopa in rindkopas:
        if rindkopa == "":
            rindkopas.pop(i)
        i += 1
    fragments = []
    rindkopuIzvele = input("Izvēlaties rindkopas, kuras vēlaties mācīties, piemēram, 1, 1-3, vai P priekš pilna teksta: ").upper()
    if rindkopuIzvele.isdigit():
        rindkopuIzvele = int(rindkopuIzvele) - 1
        try:
            fragments.append(rindkopas[rindkopuIzvele])
        except IndexError:
            print("Nepareizi ievadīts rindkopas numurs")
            return True
    elif "-" in rindkopuIzvele:
        rindkopa1, rindkopa2 = rindkopuIzvele.split('-')
        try:
            rindkopa1 = int(rindkopa1) - 1
            rindkopa2 = int(rindkopa2) - 1
        except ValueError:
            print("Nepareiza rindkopu izvēle")
            return True
        try:
            rindkopas[rindkopa1]
            rindkopas[rindkopa2]
            fragments = rindkopas[rindkopa1:rindkopa2+1]
        except IndexError:
            print("Rindkopu izvēle pāriet rindkopu skaitu")
            return True
    elif rindkopuIzvele == "P":
        fragments = rindkopas
    else:
        print("Nepareiza rindkopu izvēle.")
        return True
    fragments = "\n".join(fragments)
    varduIzvele = input("V priekš pilniem vārdiem, B priekš katra vārda pirmajiem burtiem: ").upper()
    if varduIzvele == "B":
        fragments = pirmieBurti(fragments)
    print("\n" + fragments + "\n")
    macitiesIzvele = input("Vai vēlaties mainīt teksta fragmentu? J/N: ").upper()
    if macitiesIzvele == "J":
        return True
    else:
        parbaudit(fragments)
def pirmieBurti(fragments):
    burti = []
    for rinda in fragments.split('\n'):
        rinda = rinda.strip()
        for vards in rinda.split(' '):
            burti.append(vards[0])
            if not vards.isalpha():
                burti.append(vards[-1])
        burti.append('\n')
    i = 0
    for burts in burti:
        if not burts.isalpha() and not burts.isdigit():
            burti[i-1] += burti.pop(i)
        i += 1
    parstradats = ' ' + ' '.join(burti)
    return parstradats

def parbaudit(fragments):
    ievade = """1. Loremtest ipsum dolor sit amet consectetur adipiscingtest elit. Quisque faucibus ex sapien vitae pellentesquetest sem placerat. In cursus mi pretium duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.
2. Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.
3. Lorem ipsum dolor sit amet contestsectetur adiptestiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.
4test. Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat.test In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.
5. Lorem ipsum dolor sitetstt amet consectetur adipiscing elit. Qutestisque fauctestibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."""
    ievade2 = """1. Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.
2. Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.
3. Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.
4. Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.
5. Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."""
    s = difflib.SequenceMatcher(None, fragments, ievade2)
    precizitate = round(s.ratio(), 3)
    print(f"Precizitāte ir {round(precizitate*100, 1)}%")
    print(s.get_matching_blocks())

if __name__ == "__main__":
    ievade()