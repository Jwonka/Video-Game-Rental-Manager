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

    # Property to dest due date 5 days after checkoutdate
    @property
    def dueDate(self):
        if self.checkoutDate:
            due_date = self.checkoutDate + timedelta(days=5)
            return due_date.strftime("%m-%d-%Y")
        else:
            return "N/A"
def main():  
        
    print("Bye!")

if __name__ == "__main__":
    main()
