from g04_parells_senars import startParellsSenars

def menu():
    print("========== MENÚ DE JOCS ==========")
    print("1. Jugar a Parells Senars")
    print("2. Sortir")

def main():
    while True:
        menu()
        opcio = input("Selecciona una opció: ")

        if opcio == "1":
            # Carreguem el teu joc
            startParellsSenars()
        elif opcio == "2":
            print("Sortint del programa. Adéu!")
            break
        else:
            print("Opció invàlida. Torna-ho a intentar.")

if name == "main":
    main()
