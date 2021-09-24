#initialize the patient classs object
class Patient(): 
    def __init__(self,file, givenName,familyName, homeOne, homeTwo, suburb, postCode): 
        self.file = file
        self.giveName = givenName
        self.familyName = familyName
        self.homeOne = homeOne
        self.homeTwo = homeTwo
        self.suburb = suburb
        self.postCode = postCode


