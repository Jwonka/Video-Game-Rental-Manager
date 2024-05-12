import sqlite3
from contextlib import closing
from datetime import datetime, timedelta
from business import Customer, Game

conn = None

def connect():
    global conn
    if not conn:
        DB_FILE = "Final.sqlite"
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()
        
# Populate a customer list
def get_customers():
    customers = []
    query = '''SELECT customer.customerID, customer.custFirstName, customer.custLastName
               From customer'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    for row in results:
        customer = Customer(customerID=row['customerID'], custFirstName=row['custFirstName'], custLastName=row['custLastName'])
        customers.append(customer)
    return customers

# Populate a games list
def get_games():
    games = []
    query = '''SELECT games.customerID, games.gameID, games.gameTitle, games.checkoutDate, games.dueDate
               From games'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    for row in results:
        game = Game(customerID=row['customerID'], gameID=row['gameID'], gameTitle=row['gameTitle'], checkoutDate=row['CheckoutDate'], dueDate=row['dueDate'])
        games.append(game)
    return games

def add_customer(cust_first_name, cust_last_name):
    sql = '''INSERT INTO customer
                (custFirstName, custLastName)
             VALUES
                 (?,?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (cust_first_name, cust_last_name))
        conn.commit()
    return c.lastrowid
       
def get_customer_name(id):
    query = '''SELECT custFirstName, custLastName
               FROM customer
               WHERE customerID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (id,))
        row = c.fetchone()
        if row:
            first_name, last_name = row 
            return first_name, last_name
        else:
            return None
        
# Get the customer's ID from the database after inserting a new customer with only first and last name
def get_customer_id(id):
    query = '''SELECT customerID
               FROM customer
               WHERE customerID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (id,))
        row = c.fetchone()
        if row:
            return row[0]
        else:
            return None
       
def delete_customer(id):
    sql = '''DELETE
             FROM customer
             WHERE customerID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (id,))
        conn.commit()

# Delete games from the database before deleting the customer
def delete_games(id):
    sql = '''DELETE
             FROM games
             WHERE customerID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (id,))
        conn.commit()

# Delete games by gameID for returning games
def delete_game_by_game_id(id):
    sql = '''DELETE
             FROM games
             WHERE gameID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (id,))
        conn.commit()

# Inserts a game into the games table with an associated CustomerID
def insert_game(id, game_title):
    # Set current date and due date five days from current date
    current_date = datetime.now().strftime("%m/%d/%y")
    due_date = (datetime.now() + timedelta(days=5)).strftime("%m/%d/%y")
    
    # Insert Game
    sql = '''INSERT INTO games (customerID, gameTitle, checkoutDate, dueDate)
             VALUES (?, ?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (id, game_title, current_date, due_date))
        conn.commit()
    # Return inserted GameID
    return c.lastrowid

# Find if a game has already been rented by title
def find_due_date(game_title):
    query = '''SELECT dueDate
               From games
               WHERE gameTitle = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (game_title,))
        row = c.fetchone()
        if row:
            due_date = datetime.strptime(row['dueDate'], "%m/%d/%y")
            return due_date
        else:
            return None

# Get all the games a customer has rented
def find_games(id):
    games = []
    query = '''SELECT gameID, customerID, gameTitle, checkoutDate, dueDate
               From games
               WHERE customerID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (id,))
        results = c.fetchall()

    for row in results:
        due_date = datetime.strptime(row['dueDate'], "%m/%d/%y")
        game = Game(gameID=row['gameID'], customerID=row['customerID'], gameTitle=row['gameTitle'], checkoutDate=row['checkoutDate'], dueDate=due_date)
        games.append(game)
    return games

def main():
    connect()
    customers = get_customers()
    for customer in customers:
        print(customer.customerID, customer.Name, customer.checkoutDate,
              customer.dueDate)


if __name__ == "__main__":
    main()
    
