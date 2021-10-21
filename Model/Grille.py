class Grille :

    def __init__(self):
        # Création des 16 cases
        self.taille = 4
        self.grille = []
        self.domain = list(range(1,self.taille+1))

        for i in range(self.taille):
            for j in range(self.taille):
                self.grille.append(0)

    def get_case(self,i, j):
        return i*self.taille + j

    def backTracking(self, currentIndexChosen, currentDomainValue):

        self.grille[currentIndexChosen] = currentDomainValue

        for index in self.chooseIndexList():
            if (self.grille[index] == 0):
                for domainValue in self.domain:
                    self.backTracking(self, index, self.domain[domainValue])

    def chooseIndexList(self):
        return self.grille
