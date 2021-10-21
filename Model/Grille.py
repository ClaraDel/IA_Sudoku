import math

class Grille :

    def __init__(self):
        # Création des 16 cases
        self.taille = 4
        self.grille = []
        self.domain = list(range(1,self.taille+1))

        for i in range(self.taille):
            for j in range(self.taille):
                self.grille.append(0)




    # get the case of the grid with the coordinates "i" and "j"
    def get_case(self,i, j):
        return i*self.taille + j



    # the main function of the program
    def backTracking(self, currentIndexChosen, currentDomainValue):

        # We assign the domainValue chosen by the previous "iteration" of backTracking to the chosen index
        self.grille[currentIndexChosen] = currentDomainValue

        # We check the completion of the sudoku
        if (self.checkCompletion()):
            print("You have won !")

        # We get the list of index to explore and check if the value is equal to 0 (value not yet assigned)
        for index in len(self.chooseIndexList()):
            if (self.grille[index] == 0):

                # Check if the domain value is possible for this index, if not, check for another value
                for domainValue in len(self.domain):
                    self.backTracking(self, index, self.domain[domainValue])

                    # If no value was found for this index, do : grille[currentIndexChosen] = 0



    # We create a list of index to explore, sorted according to the heuristics
    def chooseIndexList(self):
        # Put here the heuristics
        return self.grille



    # Checking the completion of the sudoku
    def checkCompletion(self):
        sudokuCompleted = True
        for i in self.grille:
            if (self.grille[i] == 0):
                sudokuCompleted = False

        return sudokuCompleted





    def getCaseConstraint(self,grille,x,y):
        cases = []
        for i in range(self.taille):
            if(i != x):
                cases.append((i,y))
            if(i != y):
                cases.append((x,i))

        nbColonne = int(math.sqrt(self.taille))
        moduloX = x%nbColonne
        minX = x-x%nbColonne
        minY = y-y%nbColonne
        for posX in range(nbColonne):
            if moduloX==posX:
                for i in range(nbColonne):
                    if (minY+i)!=y:
                        for j in range(nbColonne):
                            if (minX+j)!=x:
                                cases.append((minX+j,minY+i))

        return cases
