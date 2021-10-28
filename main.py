from Model.Grille import *
import sys


def main():
    print("--- Bienvenue sur notre travail de création CSP pour le jeu du Sudoku ! ---")
    print("Quelle taille de sudoku voulez-vous résoudre ?")
    lancerJeu = False
    while(lancerJeu == False) :
        print("Attention au sudoku de départ renseigné dans sudoku.txt en prenant la taille !")
        entree = int(input("Tapez 1 pour 4x4 \nTapez 2 pour 9x9\nTapez 3 pour 16x16\nTapez 4 pour quitter\n"))
        if(entree == 1):
            taille = 4
            lancerJeu = True
        elif(entree == 2):
            taille = 9
            lancerJeu = True
        elif(entree == 3):
            taille = 16
            lancerJeu = True
        elif(entree == 4):
            sys.exit()
        else:
            print("Merci de rentrer une donnée valide.")
        
    if (lancerJeu):
        sudoku = Grille(taille)
        print("\nSudoku de départ :")
        sudoku.printSudoku()
        print("--------------------\n")
        sudoku.backTracking()
        print("Sudoku de fin :")
        sudoku.printSudoku()

        print("nombre d'appels à backtracking : ", sudoku.nbAppel)

if __name__ == "__main__":
    main()
    