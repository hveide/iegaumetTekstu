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
    print(teksts)

if __name__ == "__main__":
    ievade()