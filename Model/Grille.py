
class Grille :
    
    def __init__(self):
        # Création des 16 cases
        self.grille = []

        for i in range(4):
            for j in range(4):
                self.grille.append(0)
        
    def get_case(i, j):
        return i*4 + j
    
    
        