from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Customer:
    customerID: int
    custFirstName: str = ""
    custLastName: str = ""
    
    @property
    def fullName(self):
        return f"{self.custFirstName} {self.custLastName}"
    
@dataclass
class Game:
    gameID: int
    customerID: int
    gameTitle:str = ""
    checkoutDate: datetime = None
    dueDate: datetime = None
        
def main():  
        
    print("Bye!")

if __name__ == "__main__":
    main()
