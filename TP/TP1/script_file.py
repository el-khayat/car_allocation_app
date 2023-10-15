import os
import random
import time
import subprocess

# Specify the library you want to install
library_to_install = "colorama"

# Use subprocess to run the pip install command
try:
    subprocess.check_call(["pip", "install", library_to_install])
except subprocess.CalledProcessError:
    print(f"Failed to install {library_to_install}.")
from colorama import Fore, Style, init

init(autoreset=True)

# Log colored text


# Initialize colorama
def print_error(message):
    print(f"{Fore.RED}{Style.BRIGHT}{message}{Style.RESET_ALL}")


def print_success(message):
    print(f"{Fore.GREEN}{Style.BRIGHT}{message}{Style.RESET_ALL}")


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

    def create_client_file():
        # Crée un fichier vide pour les clients
        with open("clients.txt", "w") as file:
            file.write("")

    def save_file(self):
        with open("clients.txt", "a") as file:
            file.write(
                f"{self.id},{self.full_name},{self.address},{self.phone},{self.email},{self.cin}\n"
            )

    # ---------------------------------------------------------------------------- #
    #                                 update client                                #
    # ---------------------------------------------------------------------------- #

    def update_file(self):
        clients = self.get_all_file()
        for i, client in enumerate(clients):
            if client.id == self.id:
                clients[i].id = self.id
                clients[i].full_name = self.full_name
                clients[i].address = self.address
                clients[i].phone = self.phone
                clients[i].email = self.email
                clients[i].cin = self.cin
        with open("clients.txt", "w") as file:
            for client in clients:
                file.write(
                    f"{client.id},{client.full_name},{client.address},{client.phone},{client.email},{client.cin}\n"
                )

    # ---------------------------------------------------------------------------- #
    #                                 delete clint                                 #
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def delete_file(client_id):
        clients = Client.get_all_file()
        clients = [client for client in clients if client.id != client_id]
        with open("clients.txt", "w") as file:
            for client in clients:
                file.write(
                    f"{client.id},{client.full_name},{client.address},{client.phone},{client.email},{client.cin}\n"
                )

    # ---------------------------------------------------------------------------- #
    #                                get all cilent                                #
    # ---------------------------------------------------------------------------- #

    @staticmethod
    def get_all_file():
        clients = []
        try:
            with open("clients.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    client_data = line.strip().split(",")
                    client = Client(
                        int(client_data[0]),
                        client_data[1],
                        client_data[2],
                        client_data[3],
                        client_data[4],
                        client_data[5],
                    )
                    clients.append(client)
        except FileNotFoundError:
            print("Aucun fichier de clients trouvé. Création d'un nouveau...")
            Client.create_client_file()
        return clients

    # ---------------------------------------------------------------------------- #
    #                                get ine client                                #
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def get_one_file(client_id):
        clients = Client.get_all_file()
        for client in clients:
            if client.id == client_id:
                return client
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

    def create_car_file():
        # Create an empty car file
        with open("cars.txt", "w") as file:
            file.write("")

    def save_file(car):
        with open("cars.txt", "a") as file:
            file.write(
                f"{car.id},{car.name},{car.model},{car.price},{car.is_disponible},{car.nbr_places}\n"
            )

    def update_file(self):
        cars = Car.get_all_file()
        for i, car in enumerate(cars):
            if car.id == self.id:
                cars[i].id = self.id
                cars[i].price = self.price
                cars[i].name = self.name
                cars[i].model = self.model
                cars[i].is_disponible = self.is_disponible
                cars[i].nbr_places = self.nbr_places
        with open("cars.txt", "w") as file:
            for car in cars:
                file.write(
                    f"{car.id},{car.name},{car.model},{car.price},{car.is_disponible},{car.nbr_places}\n"
                )

    @staticmethod
    def delete_file(car_id):
        cars = Car.get_all_file()
        cars = [car for car in cars if car.id != car_id]
        with open("cars.txt", "w") as file:
            for car in cars:
                file.write(
                    f"{car.id},{car.price},{car.name},{car.model},{car.is_disponible},{car.nbr_places}\n"
                )

    @staticmethod
    def get_all_file():
        cars = []
        try:
            with open("cars.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    car_data = line.strip().split(",")
                    car = Car(
                        int(car_data[0]),
                        car_data[1],
                        car_data[2],
                        float(car_data[3]),
                        bool(car_data[4]),
                        int(car_data[5]),
                    )
                    cars.append(car)
        except FileNotFoundError:
            print("No car file found. Creating a new one...")
            Car.create_car_file()
        return cars

    @staticmethod
    def get_one_file(car_id):
        cars = Car.get_all_file()
        for car in cars:
            if car.id == car_id:
                return Car(
                    car_id,
                    car.price,
                    car.name,
                    car.model,
                    car.is_disponible,
                    car.nbr_places,
                )
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

    def save_file(self):
        with open("allocations.txt", "a") as file:
            allocation_data = f"{self.id},{self.date},{self.price},{self.nbr_days},{self.client_id},{self.car_id}\n"
            file.write(allocation_data)

    # ---------------------------------------------------------------------------- #
    #                               update allocation                              #
    # ---------------------------------------------------------------------------- #

    def update_file(self):
        with open("allocations.txt", "r") as file:
            lines = file.readlines()
        with open("allocations.txt", "w") as file:
            for line in lines:
                data = line.split(",")
                if int(data[0]) == self.id:
                    line = f"{self.id},{self.date},{self.price},{self.nbr_days},{self.client_id},{self.car_id}\n"
                file.write(line)

    # ---------------------------------------------------------------------------------------------------
    # ----------------------------------------------delete in database and file-----------------------------------------------------

    @classmethod
    def delete_file(cls, allocation_id):
        with open("allocations.txt", "r") as file:
            lines = file.readlines()

        with open("allocations.txt", "w") as file:
            for line in lines:
                data = line.split(",")
                if int(data[0]) != int(
                    allocation_id
                ):  # Convert allocation_id to an integer
                    file.write(line)

    # ---------------------------------------------------------------------------------------------------
    # ----------------------------------------get all in database and file-----------------------------------------------------------

    @classmethod
    def get_all_allocations_file(cls):
        allocations = []
        with open("allocations.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                allocations.append(
                    cls(
                        int(data[0]),
                        data[1],
                        float(data[2]),
                        int(data[3]),
                        int(data[4]),
                        int(data[5]),
                    )
                )
        return allocations

    # ---------------------------------------------------------------------------------------------------
    # ----------------------------------------get by id in database and file-----------------------------------------------------------
    @classmethod
    def get_allocation_by_id_file(cls, allocation_id):
        with open("allocations.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if int(data[0]) == int(allocation_id):
                    return cls(
                        int(data[0]),
                        data[1],
                        float(data[2]),
                        int(data[3]),
                        int(data[4]),
                        int(data[5]),
                    )
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
            car = Car(random.randint(1000, 100000), name, model, price, True, nbr)
            car.save_file()
        elif choice == "2":
            car_id = int(input("Enter the car ID you want to update: "))
            car = Car.get_one_file(car_id)
            if car:
                car.price = input("Enter the new price: $ ")
                car.name = input("Enter the new name ")
                car.model = input("Enter the new model ")
                car.nbr_places = input("Enter the new nbr places ")
                car.update_file()
                print(f"Car with ID {car_id} updated successfully.")
            else:
                print("Car not found.")
        elif choice == "3":
            car_id = int(input("Enter the car ID you want to delete: "))
            car = Car.get_one_file(car_id)
            if car:
                Car.delete_file(car.id)
                print(f"Car with ID {car_id} deleted successfully.")
            else:
                print("Car not found.")
        elif choice == "4":
            cars = Car.get_all_file()
            for car in cars:
                car.display_info()
            input("Press enter to return to the menu.")
            os.system("cls")
        elif choice == "5":
            car_id = int(input("Enter the car ID you want to retrieve: "))
            car = Car.get_one_file(car_id)
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
            client = Client(
                random.randint(1000, 100000), full_name, address, phone, email, cin
            )
            client.save_file()
            print("Client saved successfully.")
        elif choice == "2":
            client_id = int(input("Enter the client ID you want to update: "))
            updated_client = Client.get_one_file(client_id)
            if updated_client:
                updated_client.full_name = input("Enter the new full name: ")
                updated_client.address = input("Enter the new address: ")
                updated_client.phone = input("Enter the new phone: ")
                updated_client.email = input("Enter the new email: ")
                updated_client.cin = input("Enter the new CIN: ")
                updated_client.update_file()
                print("Client updated successfully.")
            else:
                print("Client not found.")
        elif choice == "3":
            client_id = int(input("Enter the client ID you want to delete: "))
            Client.delete_file(client_id)
            print("Client deleted successfully.")
        elif choice == "4":
            clients = Client.get_all_file()
            for client in clients:
                client.display_info()
            input("Press any key to return to the menu.")
            os.system("cls")
        elif choice == "5":
            client_id = int(input("Enter the client ID you want to retrieve: "))
            client = Client.get_one_file(client_id)
            if client:
                client.display_info()
            else:
                print("Client not found.")
            input("Press any key to return to the menu.")
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
            random.randint(1000, 100000),
            allocation_date,
            allocation_price,
            allocation_nbr_days,
            client_id,
            car_id,
        )
        new_allocation.save_file()
        print("Allocation created successfully.")
    except Exception as e:
        print(f"Error: {e}")


def update_allocation():
    allocation_id = input("Enter the allocation ID to update: ")
    allocation = Allocation.get_allocation_by_id_file(allocation_id)

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
                allocation.price = float(new_price)
            if new_nbr_days:
                allocation.nbr_days = int(new_nbr_days)
            if new_client_id:
                allocation.client_id = int(new_client_id)
            if new_car_id:
                allocation.car_id = int(new_car_id)

            allocation.update_file()
            print("Allocation updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Allocation not found.")


def delete_allocation():
    allocation_id = input("Enter the allocation ID to delete: ")
    allocation = Allocation.get_allocation_by_id_file(allocation_id)
    if allocation is not None:
        Allocation.delete_file(allocation_id)
        print("Allocation deleted.")
    else:
        print("Allocation not found.")


def view_all_allocations():
    allocations = Allocation.get_all_allocations_file()
    if allocations:
        for allocation in allocations:
            print(
                f"ID: {allocation.id}, Date: {allocation.date}, Price: {allocation.price}, Days: {allocation.nbr_days}, Client ID: {allocation.client_id}, Car ID: {allocation.car_id}"
            )
    else:
        print("No allocations found.")


def view_allocation_by_id():
    allocation_id = input("Enter the allocation ID to view: ")
    allocation = Allocation.get_allocation_by_id_file(allocation_id)
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

    # Your database setup and class definitions go here

    while True:
        print()
        time.sleep(1)
        os.system("cls")
        print()
        # print(f"{Fore.RED}This is red text{Style.RESET_ALL}")
        # print(f"{Fore.GREEN}This is green text{Style.RESET_ALL}")
        print_error("+-------------------------------------------+")
        print_error(f"|    Welcome to Car allocation managment    |")
        print_error(f"|___________________________________________|")
        print()
        print()
        print("Choose an operation:                      ")
        print()
        print_success("1. Manage your  cars")
        print_success("2. Manage your clients")
        print_success("3. Manage your allocations")

        print_error("4. Quit")

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
