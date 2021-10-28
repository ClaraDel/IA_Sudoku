import copy
import math
import time
from Model.Case import *

class Grille :

    def __init__(self, taille):
       # Taille des sudoku
        self.taille = taille
        self.length = self.taille*self.taille

        self.nbAppel = 0
        
        # Le sudoku
        self.grille = []
        
        # Domaine possible pour chaque variable
        self.domain = list(range(1,self.taille+1))

        # Création du sudoku
        for i in range(self.length):
            newCase = Case(0, copy.copy(self.domain))
            self.grille.append(newCase)

        file = open('sudoku.txt', 'r')
        gridIndex = 0
        while 1:
            # read by character
            char = file.read(1)

            if not char:
                break

            if (char != '\n'):
                self.grille[gridIndex].setValue(int(char,10))
                if (char != '0'):
                    self.grille[gridIndex].cleanDomain()
                gridIndex += 1
        file.close()
        
        for i in range(self.length):
            if self.grille[i].getValue() == 0:
                x, y =self.getIndice(i)
                constraints = self.getCaseConstraint(x, y) #récupère les cases voisines qui influencent la case en cours
                for constraint in constraints:
                    if self.grille[constraint].getValue() != 0:
                        self.grille[i].removeFromDomain(self.grille[constraint].getValue())


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
        # We check the completion of the sudoku
        if (self.checkCompletion()):
            return True
        
        self.nbAppel += 1

        # We get the index to explore
        indexChosen =  self.chooseIndex()
        
        # Version LCV
        domainPossible = self.LCV(indexChosen)

        # Version sans LCV
        #domainPossible = self.domain

        for currentDomainValue in domainPossible:
        #for currentDomainValue in range(1, len(self.domain)+1):

            if (self.checkConsistency(indexChosen, currentDomainValue)):

                if (currentDomainValue != float('inf')):
                    
                    if(self.AC3(indexChosen, currentDomainValue)):

                        self.grille[indexChosen].setValue(currentDomainValue) #ajoute la valeur choisie par l'algorithme à la case en cours
                        
                        x, y =self.getIndice(indexChosen)
                        constraints = self.getCaseConstraint(x, y) #récupère les cases voisines qui sont influencées par la case en cours
                        neighboursDomainModified = []
                        for constraint in constraints:
                            if currentDomainValue in self.getDomainPossible(constraint):
                                self.grille[constraint].removeFromDomain(currentDomainValue) #on enlève la valeur aux domaines de toutes les cases voisines
                                neighboursDomainModified.append(constraint)
                        #self.printSudoku()

                        # On met en mémoire le domaine de la case avant de le mettre à 0
                        caseDomain = self.getDomainPossible(indexChosen)

                        # Le domaine de la case devient vide car on lui attribue une valeur
                        self.grille[indexChosen].cleanDomain()

                        result = self.backTracking() #on appelle de nouveau la fonction backtracking

                        if (result != False):
                            return result

                        # If it leads nowhere (failure), we put the value of the chosen index back to 0
                        self.grille[indexChosen].setValue(0)

                        # On remet le domaine que la case avait avant de lui mettre une valeur
                        self.grille[indexChosen].setDomain(caseDomain)

                        for constraint in neighboursDomainModified:
                            self.grille[constraint].addToDomain(currentDomainValue)
        
        return False



    def forwardChecking(self, index, value):
        i, j = self.getIndice(index)
        casesWithConstraint = self.getCaseConstraint(i, j)
        for case in casesWithConstraint:
            domains = copy.copy(self.getDomainPossible(case))
            if(value in domains):
                domains.remove(value)
            if(len(domains) == 0):
                #print(str(self.getIndice(case)) + " will be blocked !")
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

        # Configuration pour tester degreeHeuristic seul
        #list = []
        #for i in range(self.length):
          #  if (self.grille[i].getValue() == 0):
           #     list.append(self.grille[i])

        # Configuration pour tester LCV seul
        #for i in range(self.length):
         #   if (self.grille[i].getValue() == 0):
          #      return i

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



    def LCV(self, indexChosen):
        valueImpact = {}
        #print("case :",indexChosen )
        
        #Parcours des valeurs possibles dans cette case
        for i in self.grille[indexChosen].getDomain():
            #print("value :",i )
            # k est le nombre de voisin ayant la valeur dans leur domaine
            k=0
            
            # Parcours des voisins et incrément si la valeur i est dans le domaine de ceux ci
            # c-a-d le nombre de voisins que l'on va contraindre avec cette valeur
            for neighbour in self.getCaseConstraint(self.getIndice(indexChosen)[0],self.getIndice(indexChosen)[1]):
                if self.grille[neighbour].getValue() == 0:
                    #print("voisin :",neighbour," domaine : ",self.grille[neighbour].getDomain())
                    if(i in self.grille[neighbour].getDomain()):
                        k+=1
            # Mise en mémoire
            valueImpact[i]=k
        
        # Envoie des valeurs possibles à partir des valeurs trouvées
        x = dict(sorted(valueImpact.items(), key=lambda item: item[1]))
        
        #print(x)
        return list(x.keys())
                    

        
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


#sudoku = Grille(9)
#print("\nSudoku de départ :")
#sudoku.printSudoku()
#print("--------------------\n")
#sudoku.backTracking()
#print("Sudoku de fin :")
#sudoku.printSudoku()
#print(sudoku.nbRecurs)
#print(sudoku.getIndice(15)[0],sudoku.getIndice(15)[1])
#print(sudoku.getCaseConstraint(sudoku.getIndice(15)[0],sudoku.getIndice(15)[1]))
