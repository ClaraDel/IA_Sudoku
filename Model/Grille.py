import copy

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

    def get_case(self,i, j):
        return i*self.taille + j

    def backTracking(self, currentIndexChosen, currentDomainValue):

        self.grille[currentIndexChosen] = currentDomainValue

        if (self.checkCompletion()):
            print("You have won !")

        for index in len(self.chooseIndexList()):
            if (self.grille[index] == 0):
                for domainValue in self.domain:
                    self.backTracking(self, index, self.domain[domainValue])

    def chooseIndexList(self):
        # Put here the heuristics
        return self.grille

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