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

        # We get the list of index to explore
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
        # Put here the heuristics
        return 0



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


    def leastConstrainingValue(self, indexChosen):

        # Array containing the number of possible values for future variables, given a value
        numberOfCaseConstrainedByDomainValue = []

        # Array to return
        leastConstrainingValueDomain = []

        for i in range(len(self.domain)):

            # i begins at 0 and ends at len(self.domain) - 1
            currentDomainValue = i+1

            # If The value we want to assign is consistent with indexChosen, continue the program
            # else, wait for another iteration of the for loop
            if (self.checkConsistency(indexChosen, currentDomainValue)):

                # We put this temporary value to find the number of case constrained by this value
                self.grille[indexChosen] = currentDomainValue 

                # We get the neighbours of the current case
                neighboursOfChosenIndex = self.getCaseConstraint(self.getIndice(indexChosen))

                # for each neighbour, we want to see if it's already constrained by another neighbour
                # which contains the same value as currentDomainValue (if so, it won't change the number of possible values for this neighbour )
                for neighbour in neighboursOfChosenIndex:

                    alreadyConstrainedByOtherCase = False

                    # We get the neighbours of the chosen value's neighbours
                    neighboursOfNeighbours = self.getCaseConstraint(self.getIndice(neighbour))

                    for neighbourOfNeighbour in neighboursOfNeighbours:

                        if (i == self.grille[neighbourOfNeighbour]):
                            alreadyConstrainedByOtherCase = True
                    
                    # If the neighbour is not constrained by another neighbour, our currentDomainValue is affecting its number of possible values
                    if (not alreadyConstrainedByOtherCase):
                        numberOfCaseConstrainedByDomainValue[i] += 1

                # We want to revert the change to the grid, so that we can test with another value
                self.grille[indexChosen] = 0
        
        for i in range(len(numberOfCaseConstrainedByDomainValue)):

            # Index of the maximum number of values possible for future variables
            indexOfMinimumCaseConstrained = numberOfCaseConstrainedByDomainValue.index(min(numberOfCaseConstrainedByDomainValue))

            # we want a value contained in [1,9] (indexOfMaximumNumberOfValuePossible is in [0,8])
            leastConstrainingValue = indexOfMinimumCaseConstrained + 1

            # We put the value which allows the maximum number of values possible for other variables in front of the others
            leastConstrainingValueDomain[i] = leastConstrainingValue

            # To ensure we don't evaluate the same index again, we put the value contained to infinity
            numberOfCaseConstrainedByDomainValue[indexOfMinimumCaseConstrained] = float('inf')
        
        return leastConstrainingValueDomain


        
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
        i, j = self.getIndice(index)
        neighboursCase = self.getCaseConstraint(i, j)
        for i in neighboursCase:
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