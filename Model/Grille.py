class Grille :
    
    def __init__(self):
        # Création des 16 cases
        self.grille = []
        self.domaine = [1,2,3,4,5,6,7,8,9]

        for i in range(4):
            for j in range(4):
                self.grille.append(0)
                
    def get_case(i, j):
        return i*4 + j

    def backTracking(self, variable, valeurDomaine):
        for i in self.grille:
            if (self.grille[i] == 0):
                for j in self.domaine:
                    self.backTracking(self, self.grille[i], self.domaine[j])
