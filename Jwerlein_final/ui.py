import db
from business import Customer, Game
from datetime import datetime, date, timedelta

def display_customers():
    # Refresh the list of games and customers
    customers = db.get_customers()
    games = db.get_games()

    # Make sure the customers list is not empty
    if customers is None:
        print("There are currently no customers in the rental list.")        
    else:
        print("-" * 80)
        print("CustomerID   Name\tCheckout Date\t Due Date\t Game Title\tGameID")
        print("-" * 80)
        # Loop through each customer and display each game rented  with due dates and checkout dates
        for customer in customers:
            # Set a boolean flag to check if a customer has games
            customer_has_games = False;
            for game in games:
                if game.customerID == customer.customerID:
                    game_id = game.gameID
                    game_title = game.gameTitle
                    checkout_date = game.checkoutDate
                    due_date = game.dueDate
                    print(f"   {customer.customerID}\t{customer.custFirstName} {customer.custLastName}\t  {checkout_date}" + \
                      f"\t {due_date}\t {game_title} \t  {game_id}")
                    
                    # Set the flag to true if the customer has at least one game
                    customer_has_games = True

            if not customer_has_games:
                print(f"   {customer.customerID}\t{customer.custFirstName} {customer.custLastName}\t    N/A\t\t   N/A\t\t     N/A\t N/A")
    print()   

def display_separator():
    line = "*" * 80
    print(line)

def display_title(title):
    centered_title = title.center(80)
    display_separator()
    print(centered_title)
    display_separator()   
                    
def add_customer(customers):    
    cust_first_name = input("First name: ").title()
    cust_last_name = input("Last name: ").title()
    # Verify input
    if(cust_first_name.isspace() or cust_first_name == "" or cust_last_name.isspace() or cust_last_name == "" ):
       print("Please enter your first and last name.")
       add_customer(customers)
    else:
        # Get customerID for newly inserted customer
        customer_id = db.add_customer(cust_first_name, cust_last_name)
        
        # Create new instance of customer set gameID to zero until a game is added.
        new_customer = Customer(customerID = customer_id, custFirstName = cust_first_name, custLastName = cust_last_name)

        customers.append(new_customer)
        print(f"{new_customer.fullName} was added with CustomerID: {customer_id}.\n")

def remove_customer(customers):
    customer_id = input("Customer ID: ")
    # Verify input
    if(customer_id.isnumeric()):
        try:
            # Cast as an int to get the customerID and customer's fullName
            customer_id = int(customer_id)
            # Get the removed customers full_name 
            if(db.get_customer_id(customer_id)): 
                full_name = get_full_name(customer_id)
                # Delete the games associated with the customer then the customer
                db.delete_games(customer_id)
                db.delete_customer(customer_id)
                print(f"{full_name} was removed.\n")
            else:
                print("Customer ID is invalid. Please try again.\n")
                remove_customer(customers)
        except Exception as e:
            print(f"An error occurred: {e}.\n")
    else:
        print("Please enter a valid number.\n")
        remove_customer(customers)

def rent_game():
    customer_id = input("Enter customer ID: ")

    # Check for a valid customerID
    if not customer_id.isdigit() or not db.get_customer_id(customer_id):
        print("Invalid customer ID.")
        return
    
    game_title = input("Enter game title: ").title()

    # Check if a title is provided
    if not game_title.strip():
        print("Please enter a valid game title.")
        return

    # Check if title has been rented out
    due_date = db.find_due_date(game_title)

    #if it has then display message based on due date
    if due_date:
        
        # Convert due_date to datetime.date
        due_date = due_date.date()

        # Calculate the number of days until its due ensuring the number of days is positive
        days_due = abs(time_span_days(due_date))
        
        # Check if it is overdue or when it should be returned.
        if due_date > datetime.now().date():
            print(f"{game_title} is not available, it will be back in {days_due} days.")
            return
        else:
            print(f"{game_title} is not available, it should have been back {days_due} days ago.")
    else:
        game_id = db.insert_game(customer_id, game_title)
        due_date = db.find_due_date(game_title)
        due_date = due_date.strftime("%m/%d/%y")
        full_name = get_full_name(customer_id)
        print(f"{full_name} has rented {game_title} it is due {due_date}.\n")

# Method for calculating days overdue or days til due
def time_span_days(due_date):
    days_due = (due_date - date.today()).days
    return days_due
  
def get_full_name(customer_id):
     # Get the customer's name
    customer_first_name, customer_last_name = db.get_customer_name(customer_id)
    full_name = f"{customer_first_name} {customer_last_name}"
    return full_name    

def return_game():   
    customer_id = input("Customer ID: ")

    if customer_id.isnumeric():
        games = db.find_games(customer_id)
        # Verify customer has games to return
        if not games:
            full_name = get_full_name(customer_id)
            print(f"{full_name} does not have any games rented.")        
        else:
            # Display all games the customer has rented
            for game in games:
                game_id = game.gameID
                game_title = game.gameTitle
                checkout_date = game.checkoutDate
                
                # Convert to datetime.date object
                due_date = game.dueDate.date()
                
                full_name = get_full_name(customer_id)
                
                # Calculate the number of days until its due ensuring the number of days is positive
                days_due = abs(time_span_days(due_date))

                # Check if it was due today
                if due_date == datetime.now().date():
                    print(f"\n{full_name} rented Title: {game_title} with GameID: {game_id} on {checkout_date}.\n\nIt was due today.\n")
                # Check if it was due yesterday
                elif due_date == (datetime.now().date() + timedelta(days=1)):
                    print(f"\n{full_name} rented Title: {game_title} with GameID: {game_id} on {checkout_date}.\n\nIt was due tommorrow.\n")      
                # Check if it is early
                elif due_date == (datetime.now().date() - timedelta(days=1)):
                    print(f"\n{full_name} rented Title: {game_title} with GameID: {game_id} on {checkout_date}.\n\nIt is {days_due} day early.\n")
                # Format days if it was due more than one day ago
                elif due_date < datetime.now().date():
                    print(f"\n{full_name} rented Title: {game_title} with GameID: {game_id} on {checkout_date}.\n\nIt was due {days_due} days ago.\n")   
                # Format for more than one day early
                else:
                    print(f"\n{full_name} rented Title: {game_title} with GameID: {game_id} on {checkout_date}.\n\nIt is {days_due} days early.\n")
                    
                game_id = input("Enter the returned GameID: ")
                # Verify input
                if game_id.isnumeric():
                    game_id = int(game_id)
                    # Delete the game from the database if it has matching gameID's
                    if game_id == game.gameID:
                        db.delete_game_by_game_id(game_id)
                        print(f"\n{game_title} has been returned")
                    else:
                        print("\nThat is not the correct GameID.")
                else:
                    print("Please enter a valid number")          
    else:
        print(f"Please enter a valid CustomerID.")

def display_overdue():
    # Refresh the list of games and customers
    customers = db.get_customers()
    games = db.get_late_games()

    # Make sure the customers list is not empty
    if customers is None:
        print("There are currently no customers in the rental list.")
    elif games is None:
        print("There are currently no overdue games.")
    else:
        print("-" * 80)
        print("Days Late   Checkout    Due\tGameID\Game Title\tID Name")
        print("-" * 80)

        # For each late game match the customer by customer ID
        for game in games:           
            game_id = game.gameID
            game_title = game.gameTitle
            checkout_date = game.checkoutDate
            due_date = game.dueDate.date()

            for customer in customers:
                if game.customerID == customer.customerID:
                    days_due = abs(time_span_days(due_date))
                    due_date = due_date.strftime("%m/%d/%y")
                    print(f"    {days_due}\t    {checkout_date}  {due_date}\t{game_id} {game_title}\t\t{customer.customerID} {customer.custFirstName} {customer.custLastName}")
    print()
    
def display_menu():
    print()
    print("MENU OPTIONS")
    print("1 – Display Customers")
    print("2 – Add Customer")
    print("3 – Remove Customer")
    print("4 – Rent Game")
    print("5 – Return Game")
    print("6 – Display late games")
    print("7 - Show Menu")
    print("8 - Exit Program")
    print()

def main():
    title = "Video Game Rental Manager"
    display_title(title)
    display_menu()
    db.connect()
    customers = db.get_customers()       
    display_separator()
    
    while True:
        try:
            option = int(input("Menu option: "))
        except ValueError:
            option = -1
            
        if option == 1:
            display_customers()
        elif option == 2:
            add_customer(customers)
            customers = db.get_customers()
        elif option == 3:
            remove_customer(customers)
        elif option == 4:
            rent_game()
        elif option == 5:
            return_game()
        elif option == 6:
            display_overdue()
        elif option == 7:
            display_menu()
        elif option == 8:
            db.close()
            print("Bye!")
            break
        else:
            print("Not a valid option. Please try again.\n")
            display_menu()

if __name__ == "__main__":
    main()
