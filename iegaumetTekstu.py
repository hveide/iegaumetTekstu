import os, sys, difflib
def ievade():
    while True:
        try:
            ievadeTeksts = input("Iekopējiet savu tekstu (Teksta beigās ievadiet Ctrl+Z + Enter) vai norādiet teksta faila nosaukumu (.txt):\n")
        except EOFError:
            exit()
        if ".txt" in ievadeTeksts: # Programma atver teksta failu
            if os.path.exists(ievadeTeksts):
                with open(ievadeTeksts, "r", encoding="UTF-8") as f:
                    teksts = f.read()
            else:
                print(f"Šāds fails neeksistē dotajā mapē. ({os.getcwd()})")
                continue
        elif ievadeTeksts == "":
            exit()
        else:
            # Programma lasa lietotāja ievadi, atļaujot ievadē vairakas rindas
            rindas = sys.stdin.readlines()
            teksts = ''.join(rindas)
            teksts = ievadeTeksts + "\n" + teksts # Pievieno pirmo ievadīto rindu
            teksts = teksts.replace(chr(26), '') # Noņem ctrl+z simbolu, ja to nepareizi ievadīja
        if teksts.endswith("\n"):
            teksts = teksts[:-1] # Ja beidzas ar tukšu rindu, to nodzēš
        turpinat = True
        while turpinat: # Nodrošina programmas ciklu, kuru beidz, ja macities() atgriež False
            turpinat = macities(teksts)
        break
def macities(teksts):
    # Sadala ievadīto tekstu pa rindkopām, izdzēšot tukšās rindas
    rindkopas = teksts.split('\n')
    i = 0
    for rindkopa in rindkopas:
        if rindkopa == "":
            rindkopas.pop(i)
        i += 1
    fragments = []
    rindkopuIzvele = input("Izvēlaties rindkopas, kuras vēlaties mācīties, piemēram, 1, 1-3, vai P priekš pilna teksta: ").upper()
    if rindkopuIzvele.isdigit():
        if int(rindkopuIzvele) == 0:
            print("Nepareizi ievadīts rindkopas numurs")
            return True
        # Ja ievadīts skaitlis, izvēlas atbilstošo rindkopu, pārbaudot vai tā eksistē
        rindkopuIzvele = int(rindkopuIzvele) - 1
        try:
            fragments.append(rindkopas[rindkopuIzvele])
        except IndexError:
            print("Nepareizi ievadīts rindkopas numurs")
            return True # Atgriežas cikla sākumā
    elif "-" in rindkopuIzvele:
        # Izvēleta rindkopu grupa
        try:
            rindkopa1, rindkopa2 = rindkopuIzvele.split('-')
            # Pārveido par atbilsotsiem indeksiem, pārbaudot, ka ievadīti skaitļi
            if int(rindkopa1) <= 0 or int(rindkopa2) <= 0 or int(rindkopa2) < int(rindkopa1):
                print("Nepareiza rindkopu izvēle")
                return True
            rindkopa1 = int(rindkopa1) - 1
            rindkopa2 = int(rindkopa2) - 1
        except ValueError:
            print("Nepareiza rindkopu izvēle")
            return True
        try:
            # Pārbauda vai abas izvēlētās rindkopas eksistē un izvēlas atbilstošo rindkopu grupu
            rindkopas[rindkopa1]
            rindkopas[rindkopa2]
            fragments = rindkopas[rindkopa1:rindkopa2+1]
        except IndexError:
            print("Rindkopu izvēle pāriet rindkopu skaitu")
            return True
    elif rindkopuIzvele == "P":
        fragments = rindkopas # Izvēlētas visas rindkopas
    else:
        print("Nepareiza rindkopu izvēle.")
        return True
    fragments = "\n".join(fragments) # Pārveido fragments no saraksta uz tekstu, kas ir sadalīts rindās
    varduIzvele = input("V priekš pilniem vārdiem, B priekš katra vārda pirmajiem burtiem: ").upper()
    if varduIzvele == "B":
        radit = pirmieBurti(fragments) # Izveido atbilstošo tekstu, ko rādīt lietotājam
    elif varduIzvele == "V":
        radit = fragments
    else:
        print("Nepareiza izvēle")
        return True
    print("\n" + radit + "\n")
    macitiesIzvele = input("Vai vēlaties mainīt teksta fragmentu? J/N: ").upper()
    if macitiesIzvele == "J":
        return True # Atkārto ciklu
    elif macitiesIzvele == "N":
        parbaudit(fragments) # Programma turpinās uz lietotāja pārbaudi
    else:
        print("Nepareiza izvēle")
        return True
def pirmieBurti(fragments):
    burti = []
    for rinda in fragments.split('\n'): # Sadala fragmentu pa rindam
        rinda = rinda.strip()
        for vards in rinda.split(' '): # Sadala rindu pa vārdiem
            burti.append(vards[0]) # Izvēlas pirmo burtu no katra vārda
            if not vards.isalpha():
                burti.append(vards[-1]) # Pievieno pieturzīmes, ja vārdu neveido tikai burti
        burti.append('\n') # Pievieno rindu sadalījumu
    i = 0
    for burts in burti:
        if not burts.isalpha() and not burts.isdigit():
            burti[i-1] += burti.pop(i) # Pievieno pieturzīmes pie burta, nevis kā atsevišķu saraksta elementu
        i += 1
    parstradats = ' ' + ' '.join(burti) # Pārveido burtu sarakstu par tekstu
    return parstradats


def parbaudit(fragments):
    fragments = fragments.strip()
    for _ in range(20):
        print("\n") # Paslēpj parādīto teksta fragmentu
    print("Ievadiet iegaumēto tekstu (Beigās Ctrl+Z + Enter): ")
    rindas = sys.stdin.readlines() # Iegūst lietotāja ievadi, nodrošinot iespēju ievadīt rindās
    iegaumets = "".join(rindas)
    iegaumets = iegaumets.replace(chr(26), '') # Noņem ctrl+z simbolu, ja to nepareizi ievadīja

    if iegaumets.endswith('\n'):
        iegaumets = iegaumets[:-1] # Ja beidzas ar tukšu rindu, to nodzēš

    diffPrecizitate = difflib.SequenceMatcher(None, fragments, iegaumets) # Izveido SequenceMatcher objektu ar pilniem tekstiem
    precizitate = diffPrecizitate.ratio() # Nosaka abu tekstu līdzības precizitāti
    print(f"\nPrecizitāte: {precizitate*100:.1f}%")

    kludas = 0
    # Nosaka kļūdu skaitu atbilstosi nepareizo rakstzīmju skaitam
    for tag, i1, i2, j1, j2 in diffPrecizitate.get_opcodes(): 
        if tag != 'equal':
            kludas += max(i2 - i1, j2 - j1)
    print(f"Rakstzīmju kļūdu skaits: {kludas}")

    # Sadala teksta mainīgos pa rindām, attīra liekās atstarpes
    fragmentsRindas = [fragmentsRinda.strip() for fragmentsRinda in fragments.splitlines()]
    iegaumetsRindas = [iegaumetsRinda.strip() for iegaumetsRinda in iegaumets.splitlines()]
    diffRindas = difflib.SequenceMatcher(None, fragmentsRindas, iegaumetsRindas) # Izveido SequenceMatcher objektu pēc rindām
    irKludas = False
    labojums = []

    for tag, i1, i2, j1, j2 in diffRindas.get_opcodes(): # Izveidots cikls atbilstoši difflib dokumentācijai
        if tag == 'equal': # Nav kļūdu
            continue 
        irKludas = True
        if tag == 'replace': # Ievadītajā tekstā ir atšķirība
            if i1+1 == i2: # Kļūda ir tikai vienā rindā
                labojums.append(f"Kļūda {i2}. rindā:")
            else:
                labojums.append(f"Kļūdas no {i1+1}. līdz {i2}. rindai:")
            n = max(i2 - i1, j2 - j1) # Kļūdu skaits
            for k in range(n):
                # Nosaka atbilstošās kļūdainas rindas un parāda pareizo fragmentu kopā ar ievadīto kļūdaino rindu
                fragmentsIndex = i1 + k
                iegaumetsIndex = j1 + k
                if fragmentsIndex < i2:
                    fragmentsRinda = fragmentsRindas[fragmentsIndex]
                if iegaumetsIndex < j2:
                    iegaumetsRinda = iegaumetsRindas[iegaumetsIndex]
                labojums.append(f"+ {fragmentsRinda}")
                labojums.append(f"- {iegaumetsRinda}")

        elif tag == 'delete': # Ievadē trūkst rindas
            if i1+1 == i2: # Trūkst tikai viena rinda
                labojums.append(f"Trūkst ievade {i2}. rindā:")
            else:
                labojums.append(f"Trūkst ievade no {i1+1}. līdz {i2}. rindai:")
            for i in range(i1, i2):
                labojums.append(f"+ {fragmentsRindas[i]}") # Parāda, kuras rindas trūkst

        elif tag == 'insert': # Ievadītas liekas rindas
            if j1+1 == j2: # Tikai viena rinda
                labojums.append(f"Lieka ievade {j2}. rindā:")
            else:
                labojums.append(f"Lieka ievade no {j1+1}. līdz {j2}. rindai:")
            for j in range(j1, j2):
                labojums.append(f"- {iegaumetsRindas[j]}") # Parāda liekās rindas

    if not irKludas:
        print("Teksts iegaumēts bez kļūdām")
    else:
        print("\n".join(labojums).strip()) # Parāda pilno labojumu
    atkartot = input("Vai vēlaties turpināt mācīties? (J/N): ").upper()
    if atkartot == "J":
        ievade() # Atgriežas programmas sākumā
    else:
        exit()

if __name__ == "__main__":
    ievade()