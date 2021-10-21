import copy
import math

class Grille :

    def __init__(self):
        # Création des 16 cases
        self.taille = 4
        self.length = self.taille*self.taille
        self.grille = []
        self.domain = list(range(1,self.taille+1))

        for i in range(self.taille):
            for j in range(self.taille):
                self.grille.append(0)

    # get the case of the grid with the coordinates "i" and "j"
    def get_case(self,i, j):
        return i*self.taille + j



    # main function of the program
    def backTracking(self):

        # We check the completion of the sudoku
        if (self.checkCompletion()):
            return True

        # We get the list of index to explore and check if the value is equal to 0 (value not yet assigned)
        indexChosen =  self.chooseIndexList()

        for currentDomainValue in len(self.domain):

            # --------------------
            # If The value we want to assign is consistent with indexChosen, continue the program
            # else, wait for another iteration of the for loop
            # --------------------

            self.grille[indexChosen] = currentDomainValue

            result = self.backTracking(self)

            if (result != False):
                return result

            # If it leads nowhere (failure), we put the value of the chosen index back to 0
            self.grille[indexChosen] = 0

        return False



    # We create a list of index to explore, sorted according to the heuristics
    def chooseIndexList(self):
        # Put here the heuristics
        return self.grille



    # Checking the completion of the sudoku
    def checkCompletion(self):
        sudokuCompleted = True
        for i in self.length:
            if (self.grille[i] == 0):
                sudokuCompleted = False

        return sudokuCompleted
        
    def degreeHeuristic(self) :
        selectedCases = []
        for i in self.length:
            if (self.grille[i] == 0): 
                selectedCases.add(i)
        maxSum = 0
        returnValues = []
        
        for case in selectedCases:
            neighboursCase = fonctionAlex(case)
            sumNeighboursNull = 0
            
            for neighbours in neighboursCase :
                if self.grille[neighbours] == 0:
                    sumNeighboursNull += 1
            if sumNeighboursNull == maxSum:
                returnValues.add(case)
            if(sumNeighboursNull > maxSum):
                maxSum = sumNeighboursNull
                returnValues = []
                returnValues.add(case)
        return returnValues
                    
    def MRV(self) :
        minTaille = self.taille
        returnValues = []
        for i in self.length:
            if (self.grille[i] == 0): 
                domainPossible = self.getDomainPossible(i)
                if len(domainPossible) == minTaille:
                    returnValues.add(i)
                if len(domainPossible) < minTaille:
                    minTaille = len(domainPossible)
                    returnValues = []
                    returnValues.add(i)
        return returnValues
                    
                
    def getDomainPossible(self, index):
        domainPossible = copy.deepcopy(self.domain)
        neighboursCase = fonctionAlex(index) ;
        for i in neighboursCase:
            domainPossible.remove(self.grille[i])
        return domainPossible


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
