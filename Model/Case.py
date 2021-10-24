import copy

class Case :
    def __init__(self, value, domain):
        # Création des 16 cases
        self.value = value
        self.domain = domain
    
    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value
    
    def removeFromDomain(self, value):
        if(value in self.domain):
            self.domain.remove(value)
            return True
        return False
    
    def addToDomain(self, value):
        if(value not in self.domain):
            self.domain.append(value)
    
    def getDomain(self):
        return copy.copy(self.domain)