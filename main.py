
class Grille :
    
    def __init__(self):
        # Création des 16 cases
        self.caseList = []

        for i in range(4):
            for j in range(4):
                self.caseList.append((i,j))