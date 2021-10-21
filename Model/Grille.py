class Grille :

    def __init__(self):
        # Création des 16 cases
        self.taille = 4
        self.grille = []
        self.domaine = list(range(1,self.taille+1))

        for i in range(self.taille):
            for j in range(self.taille):
                self.grille.append(0)

    def get_case(self,i, j):
        return i*self.taille + j

    def backTracking(self, indiceChoisi, valeurDomaine):

        self.grille[indiceChoisi] = valeurDomaine

        for i in self.grille:
            if (self.grille[i] == 0):
                for j in self.domaine:
                    self.backTracking(self, i, self.domaine[j])

    def chooseIndexList(self):
        
