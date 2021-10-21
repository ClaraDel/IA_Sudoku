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
    def getCase(self, i, j):
        return i*self.taille + j
    
    def getIndice(self, case):
        return case//self.taille, case%self.taille


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
            neighboursCase = self.getCaseConstraint(self.getIndice(case))
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
        neighboursCase = self.getCaseConstraint(self.getIndice(index))
        for i in neighboursCase:
            domainPossible.remove(self.grille[i])
        return domainPossible


    def getCaseConstraint(self, x, y):
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
                                cases.append(self.getCase(minX+j,minY+i))

        return cases
