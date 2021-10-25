import copy
import math
import time
from Case import *

class Grille :

    def __init__(self):
        # Création des 16 cases
        self.taille = 12
        self.length = self.taille*self.taille
        self.grille = []
        self.domainsBrain = []
        self.domain = list(range(1,self.taille+1))

        for i in range(self.taille):
            for j in range(self.taille):
                newCase = Case(0, copy.copy(self.domain))
                self.grille.append(newCase)
        
                

    def printSudoku(self):
        for i in range(self.taille):
            if(i%math.sqrt(self.taille) == 0):
                print("")
            line = ""
            for j in range(self.taille):
                if(j%math.sqrt(self.taille) == 0):
                    line += " "
                if(self.grille[self.getCase(i, j)].getValue() != 0):
                    line += str(self.grille[self.getCase(i, j)].getValue()) + "|"
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
        #time.sleep(1)
        # We check the completion of the sudoku
        if (self.checkCompletion()):
            return True

        # We get the list of index to explore
        indexChosen =  self.chooseIndex()

        for currentDomainValue in (self.leastConstrainingValue(indexChosen)):

            if (currentDomainValue != float('inf')):
                
                if(self.forwardChecking(indexChosen, currentDomainValue)):
                    self.grille[indexChosen].setValue(currentDomainValue)
                    x, y =self.getIndice(indexChosen)
                    constraints = self.getCaseConstraint(x, y)
                    for constraint in constraints:
                        self.grille[constraint].removeFromDomain(currentDomainValue)

                    result = self.backTracking()

                    if (result != False):
                        return result

                    # If it leads nowhere (failure), we put the value of the chosen index back to 0
                    self.grille[indexChosen].setValue(0)
                    
                    x, y =self.getIndice(indexChosen)
                    constraints = self.getCaseConstraint(x, y)
                    for constraint in constraints:
                        self.grille[constraint].addToDomain(currentDomainValue)
                else:
                    self.printSudoku()
                    print("Index: " + str(self.getIndice(indexChosen)) + " value: " + str(currentDomainValue) + " will no be extended !")
                    return False

        return False


    def forwardChecking(self, index, value):
        i, j = self.getIndice(index)
        casesWithConstraint = self.getCaseConstraint(i, j)
        for case in casesWithConstraint:
            domains = self.getDomainPossible(case)
            if(value in domains):
                domains.remove(value)
            if(len(domains) == 0):
                print(str(self.getIndice(case)) + " will be blocked !")
                return False
        return True

    
    def AC3(self, index, value):
        grilleCopy = copy.deepcopy(self.grille)
        x, y = self.getIndice(index)
        constraints = self.getCaseConstraint(x, y)
        
        constraintsCouple = []
        for constraint in constraints:  
            if(grilleCopy[constraint].getValue() == 0):
                constraintsCouple.append((constraint, value))
        
        while len(constraintsCouple) != 0:
            constraint = constraintsCouple.pop()
            if(grilleCopy[constraint[0]].removeFromDomain(constraint[1])):
            
                constraintDomain = grilleCopy[constraint[0]].getDomain()
                if(len(constraintDomain) == 1):
                    x, y = self.getIndice(constraint[0])
                    for newConstraint in self.getCaseConstraint(x, y):
                        if(grilleCopy[newConstraint].getValue() == 0):
                            constraintsCouple.append((newConstraint, constraintDomain[0]))
                elif(len(constraintDomain) == 0):
                    return False
        return True

    # We create a list of index to explore, sorted according to the heuristics
    def chooseIndex(self):
        #self.printSudoku()
        #print(self.degreeHeuristic()[0])
        return self.degreeHeuristic(self.MRV())[0]



    # Checking the completion of the sudoku
    def checkCompletion(self):
        sudokuCompleted = True
        for i in range(self.length):
            if (self.grille[i].getValue() == 0):
                sudokuCompleted = False

        return sudokuCompleted



    def checkConsistency(self, currentCase, valueToTest):
        consistencyOk = True
        i, j = self.getIndice(currentCase)
        casesWithConstraint = self.getCaseConstraint(i, j)
        for case in casesWithConstraint:
            if (self.grille[case].getValue() == valueToTest):
                consistencyOk = False
        return consistencyOk


    def leastConstrainingValue(self, indexChosen):

        # Array containing the number of neighbours constrained given a value
        numberOfCaseConstrainedByDomainValue = []

        # Array to return
        leastConstrainingValueDomain = []

        for i in range(len(self.domain)):

            # i begins at 0 and ends at len(self.domain) - 1
            currentDomainValue = i+1

            # If The value we want to assign is consistent with indexChosen, continue the program
            # else, wait for another iteration of the for loop
            if (self.checkConsistency(indexChosen, currentDomainValue)):

                numberOfCaseConstrained = 0

                # We put this temporary value to find the number of case constrained by this value
                self.grille[indexChosen] = currentDomainValue 

                coordinatesOfChosenIndex = self.getIndice(indexChosen)

                # We get the neighbours of the current case
                neighboursOfChosenIndex = self.getCaseConstraint(coordinatesOfChosenIndex[0], coordinatesOfChosenIndex[1])

                # for each neighbour, we want to see if it's already constrained by another neighbour
                # which contains the same value as currentDomainValue (if so, it won't change the number of possible values for this neighbour )
                for neighbour in neighboursOfChosenIndex:

                    if (self.grille[neighbour] != 0):

                        alreadyConstrainedByOtherCase = False

                        coordinatesOfNeighbour = self.getIndice(neighbour)

                        # We get the neighbours of the chosen value's neighbours
                        neighboursOfNeighbours = self.getCaseConstraint(coordinatesOfNeighbour[0], coordinatesOfNeighbour[1])

                        for neighbourOfNeighbour in neighboursOfNeighbours:

                            if (i == self.grille[neighbourOfNeighbour]):
                                alreadyConstrainedByOtherCase = True
                        
                        # If the neighbour is not constrained by another neighbour, our currentDomainValue is affecting its number of possible values
                        if (not alreadyConstrainedByOtherCase):
                            numberOfCaseConstrained += 1

                # We want to revert the change to the grid, so that we can test with another value
                self.grille[indexChosen] = 0

                numberOfCaseConstrainedByDomainValue.append(numberOfCaseConstrained)

            else:
                numberOfCaseConstrainedByDomainValue.append(float('inf'))

        for i in range(len(numberOfCaseConstrainedByDomainValue)):

            # Index of the maximum number of values possible for future variables
            indexOfMinimumCaseConstrained = numberOfCaseConstrainedByDomainValue.index(min(numberOfCaseConstrainedByDomainValue))

            # we want a value contained in [1,9] (indexOfMaximumNumberOfValuePossible is in [0,8])
            leastConstrainingValue = indexOfMinimumCaseConstrained + 1

            # We put the value which allows the maximum number of values possible for other variables in front of the others
            leastConstrainingValueDomain.append(leastConstrainingValue)

            # To ensure we don't evaluate the same index again, we put the value contained to infinity
            numberOfCaseConstrainedByDomainValue[indexOfMinimumCaseConstrained] = float('inf')
        
        return leastConstrainingValueDomain


        
    def degreeHeuristic(self, selectedCases) :
        #selectedCases = []
        #for i in range(self.length):
        #    if (self.grille[i].getValue() == 0): 
        #        selectedCases.append(i)
        maxSum = 0
        returnValues = []
        
        for case in selectedCases:
            i, j = self.getIndice(case)
            neighboursCase = self.getCaseConstraint(i, j)
            sumNeighboursNull = 0
            
            for neighbours in neighboursCase :
                if self.grille[neighbours].getValue() == 0:
                    sumNeighboursNull += 1
            if sumNeighboursNull == maxSum:
                returnValues.append(case)
            if(sumNeighboursNull > maxSum):
                maxSum = sumNeighboursNull
                returnValues = []
                returnValues.append(case)
        return returnValues
                    
    def MRV(self) :
        minTaille = self.taille
        returnValues = []
        for i in range(self.length):
            if (self.grille[i].getValue() == 0): 
                domainPossible = self.getDomainPossible(i)
                if len(domainPossible) == minTaille:
                    returnValues.append(i)
                if len(domainPossible) < minTaille:
                    minTaille = len(domainPossible)
                    returnValues = []
                    returnValues.append(i)
        return returnValues
                    

    def getDomainPossible(self, index):
        return self.grille[index].getDomain()
# =============================================================================
#         domainPossible = copy.deepcopy(self.domain)
#         i, j = self.getIndice(index)
#         neighboursCase = self.getCaseConstraint(i, j)
#         for i in neighboursCase:
#             if(self.grille[i].getValue() in domainPossible):
#                 domainPossible.remove(self.grille[i].getValue())
#         return domainPossible
# 
# =============================================================================

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
print(sudoku.getIndice(1))
sudoku.printSudoku()
sudoku.backTracking()
sudoku.printSudoku()