import os
import sqlite3
import time


# ------------------------- Defining the class Client ------------------------ #
class Client:
    def __init__(self, client_id, full_name, address, phone, email, cin):
        self.id = client_id
        self.full_name = full_name
        self.address = address
        self.phone = phone
        self.email = email
        self.cin = cin

    def display_info(self):
        print(
            f"Client ID: {self.id},Full Name: {self.full_name}, Address: {self.address},Phone: {self.phone}, Email: {self.email}, CIN: {self.cin}"
        )

    # ---------------------------------------------------------------------------- #
    #                            Save client to databaes                           #
    # ---------------------------------------------------------------------------- #

    def save(self):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clients (FullName, address, phone, email, CIN) VALUES (?, ?, ?, ?, ?)",
            (self.full_name, self.address, self.phone, self.email, self.cin),
        )
        print("Client saved successfully.")
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    # ---------------------------------------------------------------------------- #
    #                                 update client                                #
    # ---------------------------------------------------------------------------- #

    def update(self):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clients SET FullName=?, address=?, phone=?, email=?, CIN=? WHERE id=?",
            (self.full_name, self.address, self.phone, self.email, self.cin, self.id),
        )
        conn.commit()
        conn.close()

    # ---------------------------------------------------------------------------- #
    #                                 delete clint                                 #
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def delete(id):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id=?", (id,))
        conn.commit()
        conn.close()

    # ---------------------------------------------------------------------------- #
    #                                get all cilent                                #
    # ---------------------------------------------------------------------------- #

    @staticmethod
    def get_all():
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()
        conn.close()
        return [Client(*client) for client in clients]

    # ---------------------------------------------------------------------------- #
    #                                get ine client                                #
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def get_one(client_id):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id=?", (client_id,))
        client = cursor.fetchone()
        conn.close()
        if client:
            return Client(*client)
        else:
            return None


class Car:
    def __init__(self, car_id, name, model, price, is_disponible, nbr_places):
        self.id = car_id
        self.name = name
        self.model = model
        self.price = price
        self.is_disponible = is_disponible
        self.nbr_places = nbr_places

    def display_info(self):
        print(
            f"Car ID: {self.id},Name: {self.name}, Model: {self.model},Price: ${self.price}, Available: {'Yes' if self.is_disponible else 'No'}, Number of Places: {self.nbr_places},"
        )

    def save(self):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cars (name, model, price, is_disponible, nbr_places) VALUES (?, ?, ?, ?, ?)",
            (self.name, self.model, self.price, self.is_disponible, self.nbr_places),
        )
        print("Car saved successfully.")
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    def update(self):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cars SET name=?, model=?, price=?, is_disponible=?, nbr_places=? WHERE id=?",
            (
                self.name,
                self.model,
                self.price,
                self.is_disponible,
                self.nbr_places,
                self.id,
            ),
        )
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE id=?", (self.id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars")
        cars = cursor.fetchall()
        conn.close()
        return [Car(*car) for car in cars]

    @staticmethod
    def get_one(car_id):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars WHERE id=?", (car_id,))
        car = cursor.fetchone()
        conn.close()
        if car:
            return Car(*car)
        else:
            return None


class Allocation:
    def __init__(
        self,
        allocation_id,
        allocation_date,
        allocation_price,
        allocation_nbr_days,
        client_id,
        car_id,
    ):
        self.id = allocation_id
        self.date = allocation_date
        self.price = allocation_price
        self.nbr_days = allocation_nbr_days
        self.client_id = client_id
        self.car_id = car_id

    # ----------------------------------------------save  in database and file-----------------------------------------------------

    def save(self):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO allocations (date, price, nbr_days, client_id, car_id) VALUES (?, ?, ?, ?, ?)",
            (self.date, self.price, self.nbr_days, self.client_id, self.car_id),
        )
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    # ---------------------------------------------------------------------------------------------------
    # -------------------------------------------Update in databse and in file--------------------------------------------------------
    def update(self):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE allocations SET date=?, price=?, nbr_days=?, client_id=?, car_id=? WHERE id=?",
            (
                self.date,
                self.price,
                self.nbr_days,
                self.client_id,
                self.car_id,
                self.id,
            ),
        )
        conn.commit()
        conn.close()

    # ---------------------------------------------------------------------------------------------------
    # ----------------------------------------------delete in database and file-----------------------------------------------------
    @classmethod
    def delete(cls, allocation_id):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM allocations WHERE id=?", (allocation_id,))
        conn.commit()
        conn.close()

    # ---------------------------------------------------------------------------------------------------
    # ----------------------------------------get all in database and file-----------------------------------------------------------
    @staticmethod
    def get_all_allocations():
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM allocations")
        rows = cursor.fetchall()
        conn.close()

        allocations = []
        for row in rows:
            allocation = Allocation(row[0], row[1], row[2], row[3], row[4], row[5])
            allocations.append(allocation)

        return allocations

    # ---------------------------------------------------------------------------------------------------
    # ----------------------------------------get by id in database and file-----------------------------------------------------------
    @classmethod
    def get_allocation_by_id(cls, allocation_id):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM allocations WHERE id=?", (allocation_id,))
        row = cursor.fetchone()
        conn.close()
        if row is not None:
            return cls(*row)
        else:
            return None


# ---------------------------------------define the test method to cars-----------------------------------
def test_car():
    while True:
        print("Choose an operation:")
        print("1. Save a car")
        print("2. Update a car")
        print("3. Delete a car")
        print("4. Get all cars")
        print("5. Get one car by ID")
        print("6. Go back to the main menu 🔙")

        choice = input("Enter your choice (1-6): ")
        os.system("cls")
        if choice == "1":
            name = input("Enter the name of teh car: ")
            model = input("Enter the Model of ther car: ")
            price = input("Enter the car price : ")
            nbr = input("Enter the car numbers of places: ")
            car = Car(None, name, model, price, True, nbr)
            car.save()
        elif choice == "2":
            car_id = int(input("Enter the car ID you want to update: "))
            car = Car.get_one(car_id)
            if car:
                car.price = input("Enter the new price: $ ")
                car.name = input("Enter the new name ")
                car.model = input("Enter the new model ")
                car.nbr_places = input("Enter the new nbr places ")
                car.update()
                print(f"Car with ID {car_id} updated successfully.")
            else:
                print("Car not found.")
        elif choice == "3":
            car_id = int(input("Enter the car ID you want to delete: "))
            car = Car.get_one(car_id)
            if car:
                car.delete()
                print(f"Car with ID {car_id} deleted successfully.")
            else:
                print("Car not found.")
        elif choice == "4":
            cars = Car.get_all()
            for car in cars:
                car.display_info()
            input("Press enter to return to the menu.")
            os.system("cls")
        elif choice == "5":
            car_id = int(input("Enter the car ID you want to retrieve: "))
            car = Car.get_one(car_id)
            if car:
                car.display_info()
            else:
                print("Car not found.")
            input("Press enter to return to the menu.")
            os.system("cls")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-6).")
        time.sleep(0.5)
        os.system("cls")


# ---------------------------------------------------------------------------------------------------


def test_client():
    while True:
        print("Choose an operation:")
        print("1. Save a client")
        print("2. Update a client")
        print("3. Delete a client")
        print("4. Get all clients")
        print("5. Get one client by ID")
        print("6. Go back to the main menu 🔙 ")

        choice = input("Enter your choice (1-6): ")
        os.system("cls")
        if choice == "1":
            full_name = input("Enter client full name: ")
            address = input("Enter client address: ")
            phone = input("Enter client phone: ")
            email = input("Enter client email: ")
            cin = input("Enter client CIN: ")
            client = Client(None, full_name, address, phone, email, cin)
            client.save()
            print("Client saved successfully.")
        elif choice == "2":
            client_id = int(input("Enter the client ID you want to update: "))
            updated_client = Client.get_one(client_id)
            if updated_client:
                updated_client.full_name = input("Enter the new full name: ")
                updated_client.address = input("Enter the new address: ")
                updated_client.phone = input("Enter the new phone: ")
                updated_client.email = input("Enter the new email: ")
                updated_client.cin = input("Enter the new CIN: ")
                updated_client.update()
                print("Client updated successfully.")
            else:
                print("Client not found.")
        elif choice == "3":
            client_id = int(input("Enter the client ID you want to delete: "))
            Client.delete(client_id)
            print("Client deleted successfully.")
        elif choice == "4":
            clients = Client.get_all()
            for client in clients:
                client.display_info()
            input("Press enter to return to the menu.")
            os.system("cls")
        elif choice == "5":
            client_id = int(input("Enter the client ID you want to retrieve: "))
            client = Client.get_one(client_id)
            if client:
                client.display_info()
            else:
                print("Client not found.")
            input("Press enter to return to the menu.")
            os.system("cls")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-6).")
        time.sleep(0.5)
        os.system("cls")


# ---------------------------------------------------------------------------------------------------
def test_allocation():
    while True:
        print("\n Allocation Management :")
        print("1. Create a new allocation")
        print("2. Update an allocation")
        print("3. Delete an allocation")
        print("4. View all allocations")
        print("5. View allocation by ID")
        print("6. Go back to the main menu 🔙")

        choice = input("Enter your choice (1/2/3/4/5/6): ")
        time.sleep(1)
        os.system("cls")
        if choice == "1":
            create_allocation()
        elif choice == "2":
            update_allocation()
        elif choice == "3":
            delete_allocation()
        elif choice == "4":
            view_all_allocations()
            input("Press enter to return to the menu.")
            os.system("cls")
        elif choice == "5":
            view_allocation_by_id()
            input("Press enter to return to the menu.")
            os.system("cls")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")
        time.sleep(1)
        os.system("cls")


def create_allocation():
    allocation_date = input("Enter the allocation date: ")
    allocation_price = float(input("Enter the allocation price: "))
    allocation_nbr_days = int(input("Enter the number of days: "))
    client_id = int(input("Enter the client ID: "))
    car_id = int(input("Enter the car ID: "))
    try:
        new_allocation = Allocation(
            None,
            allocation_date,
            allocation_price,
            allocation_nbr_days,
            client_id,
            car_id,
        )
        new_allocation.save()
        print("Allocation created successfully.")
    except Exception as e:
        print(f"Error: {e}")


def update_allocation():
    allocation_id = input("Enter the allocation ID to update: ")
    allocation = Allocation.get_allocation_by_id(allocation_id)
    print(allocation.id)
    if allocation is not None:
        try:
            # Prompt the user for updated information
            new_date = input(
                "Enter the updated date (press Enter to keep it unchanged): "
            )
            new_price = input(
                "Enter the updated price (press Enter to keep it unchanged): "
            )
            new_nbr_days = input(
                "Enter the updated number of days (press Enter to keep it unchanged): "
            )
            new_client_id = input(
                "Enter the updated client ID (press Enter to keep it unchanged): "
            )
            new_car_id = input(
                "Enter the updated car ID (press Enter to keep it unchanged): "
            )

            # Check if the user provided any input for updating
            if new_date:
                allocation.date = new_date
            if new_price:
                print(new_price)
                allocation.price = float(new_price)
            if new_nbr_days:
                allocation.nbr_days = int(new_nbr_days)
            if new_client_id:
                allocation.client_id = int(new_client_id)
            if new_car_id:
                allocation.car_id = int(new_car_id)

            allocation.update()
            print("Allocation updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Allocation not found.")


def delete_allocation():
    allocation_id = input("Enter the allocation ID to delete: ")
    allocation = Allocation.get_allocation_by_id(allocation_id)
    if allocation is not None:
        Allocation.delete(allocation_id)
        print("Allocation deleted.")
    else:
        print("Allocation not found.")


def view_all_allocations():
    allocations = Allocation.get_all_allocations()
    if allocations:
        for allocation in allocations:
            print(
                f"ID: {allocation.id}, Date: {allocation.date}, Price: {allocation.price}, Days: {allocation.nbr_days}, Client ID: {allocation.client_id}, Car ID: {allocation.car_id}"
            )
    else:
        print("No allocations found.")


def view_allocation_by_id():
    allocation_id = input("Enter the allocation ID to view: ")
    allocation = Allocation.get_allocation_by_id(allocation_id)
    if allocation is not None:
        print(
            f"ID: {allocation.id}, Date: {allocation.date}, Price: {allocation.price}, Days: {allocation.nbr_days}, Client ID: {allocation.client_id}, Car ID: {allocation.car_id}"
        )
    else:
        print("Allocation not found.")

    ########################################################

    return None


# ---------------------------------------------------------------------------------------------------


def main_test():
    #####################################################
    print(f"Craeting ##########.")
    time.sleep(1)
    os.system("cls")
    # Create an SQLite database
    conn = sqlite3.connect("car_allocation.db")
    cursor = conn.cursor()

    # Define the tables and schema
    query = """ CREATE TABLE IF NOT EXISTS clients ( id INTEGER PRIMARY KEY, FullName TEXT, address TEXT, phone TEXT, email TEXT, CIN TEXT )"""
    cursor.execute(query)

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        model TEXT NOT NULL,
        price REAL NOT NULL,
        is_disponible INTEGER NOT NULL,
        nbr_places INTEGER NOT NULL
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS allocations (
            id INTEGER PRIMARY KEY,
            date TEXT,
            price REAL,
            nbr_days INTEGER,
            client_id INTEGER,
            car_id INTEGER,
            FOREIGN KEY (client_id) REFERENCES clients (id),
            FOREIGN KEY (car_id) REFERENCES cars (id)
        )
    """
    )

    # Save changes and close the connection
    conn.commit()
    conn.close()

    # Your database setup and class definitions go here

    while True:
        print()
        print("#### Welcome to Car allocation managment ####")
        time.sleep(1)
        os.system("cls")
        print()
        print("+-------------------------------------------+")
        print("Choose an operation:")

        print("1. Manage your  cars")
        print("2. Manage your clients")
        print("3. Manage your allocations")

        print("4. Quit")

        choice = input("Enter your choice (1-4): ")
        os.system("cls")
        if choice == "1":
            test_car()
        elif choice == "2":
            test_client()
        elif choice == "3":
            test_allocation()
        elif choice == "4":
            print("Goodbye!")
            break
        time.sleep(2)
        os.system("cls")


main_test()
