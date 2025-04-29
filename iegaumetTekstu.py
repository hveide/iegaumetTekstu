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
    for i in range(20):
        print("\n")
    print("Ievadiet iegaumēto tekstu (Beigās Ctrl+Z + Enter): ")
    lines = sys.stdin.readlines()
    iegaumets = "".join(lines)

    # Remove trailing newline often added by Ctrl+Z/D
    if iegaumets.endswith('\n'):
        iegaumets = iegaumets[:-1]

    diffPrecizitate = difflib.SequenceMatcher(None, fragments, iegaumets)
    precizitate = diffPrecizitate.ratio()
    print(f"\nPrecizitāte: {precizitate*100:.1f}%")

    kludas = 0
    for tag, i1, i2, j1, j2 in diffPrecizitate.get_opcodes():
        if tag != 'equal':
            kludas += max(i2 - i1, j2 - j1)
    print(f"Aptuvenais kļūdu skaits: {kludas}")

    fragmentsRindas = fragments.splitlines()
    iegaumetsRindas = iegaumets.splitlines()
    diffRindas = difflib.SequenceMatcher(None, fragmentsRindas, iegaumetsRindas)
    irKludas = False
    labojums = []

    for tag, i1, i2, j1, j2 in diffRindas.get_opcodes():
        if tag == 'equal':
            continue
        irKludas = True
        if labojums:
            labojums.append("---")

        if tag == 'replace':
            if i1+1 == i2:
                labojums.append(f"Kļūda {i2}. rindā:")
            else:
                labojums.append(f"Kļūdas no {i1+1}. līdz {i2}. rindai:")
            n = max(i2 - i1, j2 - j1)
            for k in range(n):
                fragmentsIndex = i1 + k
                iegaumetsIndex = j1 + k
                fragmentsRinda = fragmentsRindas[fragmentsIndex] if fragmentsIndex < i2 else "Kļūda ievadē"
                iegaumetsRinda = iegaumetsRindas[iegaumetsIndex] if iegaumetsIndex < j2 else "Kļūda ievadē"
                labojums.append(f"+ {fragmentsRinda}")
                labojums.append(f"- {iegaumetsRinda}")

        elif tag == 'delete':
            if i1+1 == i2:
                labojums.append(f"Trūkst ievade {i2}. rindā:")
            else:
                labojums.append(f"Trūkst ievade no {i1+1}. līdz {i2}. rindai:")
            for i in range(i1, i2):
                labojums.append(f"+ {fragmentsRindas[i]}")

        elif tag == 'insert':
            if j1+1 == j2:
                labojums.append(f"Lieka ievade {j2}. rindā:")
            else:
                labojums.append(f"Lieka ievade no {j1+1}. līdz {j2}. rindai:")
            for j in range(j1, j2):
                labojums.append(f"- {iegaumetsRindas[j]}")

    if not irKludas:
        print("Teksts iegaumēts bez kļūdām")
    else:
        print("\n".join(labojums).strip())
    atkartot = input("Vai vēlaties vēlreiz mācīties? (J/N): ").upper()
    if atkartot == "J":
        turpinat = True
        while turpinat:
            turpinat = macities(teksts)
    else:
        exit()

if __name__ == "__main__":
    ievade()