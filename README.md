# IA_Sudoku
Création CSP pour le jeu du Sudoku

Lancez main.py pour lancer notre programme. On propose alors à l'utilisateur d'entrer la taille du sudoku à résoudre.
Attention au Sudoku mis dans le fichier sudoku.txt si vous souhaitez utiliser notre programme pour résoudre le vôtre, il faut que sa taille soit cohérente avec la taille entrée, car notre programme ne gère pour l'instant pas cette situation.
Bien entendu, la taille par défaut est 9x9, et est la taille du sudoku mis au départ dans sudoku.txt

Pour entrer votre propre sudoku, veuillez entrer les nombres à la suite, sans mettre de tiret ou de barre verticale ( | ), ou tout caractère autre que des chiffres, auquel cas le programme risque de ne pas fonctionner. Les espaces sont autorisés bien évidemment.

Il faut modifier l'intérieur du code pour changer les heuristiques et les fonctions de check voulues. Pour forwardChecking et AC3, il n'y a qu'à changer le nom de la fonction à utiliser dans un "if" de backTracking. Si l'on ne veut pas utiliser de fonction de check, il n'y a qu'à rajouter <"True or " - nom de la fonction> dans le "if".

Concernant LCV, il n'y a qu'à lire les commentaires de backTracking.

Pour MRV et degreeHeuristic, il faut regarder la fonction chooseIndex qui explique tout.

Bon sudoku !