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
                

    def printSudoku(self):
        for i in range(self.taille):
            line = "|"
            for j in range(self.taille):
                if(self.grille[self.getCase(i, j)] != 0):
                    line += str(self.grille[self.getCase(i, j)]) + "|"
                else:
                    line += " |"
            print(line)
        print("")
                

    # get the case of the grid with the coordinates "i" and "j"
    def getCase(self, i, j):
        return i*self.taille + j
    
    def getIndice(self, case):
        return case//self.taille, case%self.taille


    # main function of the program
    def backTracking(self):

        # We check the completion of the sudoku
        if (self.checkCompletion()):
            return True

        # We get the list of index to explore and check if the value is equal to 0 (value not yet assigned)
        indexChosen =  self.chooseIndex()

        for i in range(len(self.domain)):

            # i begins at 0 and ends at len(self.domain) - 1
            currentDomainValue = i+1

            # If The value we want to assign is consistent with indexChosen, continue the program
            # else, wait for another iteration of the for loop
            if (self.checkConsistency(indexChosen, currentDomainValue)):

                self.grille[indexChosen] = currentDomainValue

                result = self.backTracking()

                if (result != False):
                    return result

                # If it leads nowhere (failure), we put the value of the chosen index back to 0
                self.grille[indexChosen] = 0

        return False



    # We create a list of index to explore, sorted according to the heuristics
    def chooseIndex(self):
        return self.MRV()[0]



    # Checking the completion of the sudoku
    def checkCompletion(self):
        sudokuCompleted = True
        for i in range(self.length):
            if (self.grille[i] == 0):
                sudokuCompleted = False

        return sudokuCompleted



    def checkConsistency(self, currentCase, valueToTest):
        consistencyOk = True
        i, j = self.getIndice(currentCase)
        casesWithConstraint = self.getCaseConstraint(i, j)
        for case in casesWithConstraint:
            if (self.grille[case] == valueToTest):
                consistencyOk = False
        return consistencyOk


        
    def degreeHeuristic(self) :
        selectedCases = []
        for i in self.length:
            if (self.grille[i] == 0): 
                selectedCases.add(i)
        maxSum = 0
        returnValues = []
        
        for case in selectedCases:
            i, j = self.getIndice(case)
            neighboursCase = self.getCaseConstraint(i, j)
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
        for i in range(self.length):
            if (self.grille[i] == 0): 
                domainPossible = self.getDomainPossible(i)
                if len(domainPossible) == minTaille:
                    returnValues.append(i)
                if len(domainPossible) < minTaille:
                    minTaille = len(domainPossible)
                    returnValues = []
                    returnValues.append(i)
        return returnValues
                    
                
    def getDomainPossible(self, index):
        domainPossible = copy.deepcopy(self.domain)
        i, j = self.getIndice(index)
        neighboursCase = self.getCaseConstraint(i, j)
        for i in neighboursCase:
            if(self.grille[i] in domainPossible):
                domainPossible.remove(self.grille[i])
        return domainPossible


    def getCaseConstraint(self, x, y):
        cases = []
        for i in range(self.taille):
            if(i != x):
                cases.append(self.getCase(i,y))
            if(i != y):
                cases.append(self.getCase(x,i))

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


sudoku = Grille()
sudoku.printSudoku()
sudoku.backTracking()
sudoku.printSudoku()