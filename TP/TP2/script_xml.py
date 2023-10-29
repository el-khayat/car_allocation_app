import os
import time
import random
import subprocess
import xml.etree.ElementTree as ET

# Specify the library you want to install
library_to_install = "colorama"

# Use subprocess to run the pip install command
try:
    subprocess.check_call(["python", "-m", "pip", "install", library_to_install])
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


def print_info(message):
    BLUE = f"\033[38;2;179;237;245m"
    print(f"{BLUE}{Style.BRIGHT}{message}{Style.RESET_ALL}")




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

    def to_xml(self):
        allocation_elem = ET.Element("allocation")
        ET.SubElement(allocation_elem, "id").text = str(self.id)
        ET.SubElement(allocation_elem, "date").text = self.date
        ET.SubElement(allocation_elem, "price").text = str(self.price)
        ET.SubElement(allocation_elem, "nbr_days").text = str(self.nbr_days)
        ET.SubElement(allocation_elem, "client_id").text = str(self.client_id)
        ET.SubElement(allocation_elem, "car_id").text = str(self.car_id)
        return allocation_elem

    @classmethod
    def from_xml(cls, allocation_elem):
        allocation_id = int(allocation_elem.find("id").text)
        allocation_date = allocation_elem.find("date").text
        allocation_price = float(allocation_elem.find("price").text)
        allocation_nbr_days = int(allocation_elem.find("nbr_days").text)
        client_id = int(allocation_elem.find("client_id").text)
        car_id = int(allocation_elem.find("car_id").text)
        return cls(allocation_id, allocation_date, allocation_price, allocation_nbr_days, client_id, car_id)

    # ----------------------------------------------save  in database and file-----------------------------------------------------

    def save_to_xml(self, filename):
        try:
            root = None
            try:
                tree = ET.parse(filename)
                root = tree.getroot()
            except (FileNotFoundError, ET.ParseError):
                root = ET.Element("allocations")

            allocation_elem = self.to_xml()
            root.append(allocation_elem)

            tree = ET.ElementTree(root)
            tree.write(filename)

        except Exception as e:
            print(f"Error saving allocation to XML: {e}")
    # ---------------------------------------------------------------------------------------------------
    # -------------------------------------------Update in databse and in file--------------------------------------------------------
    @classmethod
    def update_from_xml(cls, filename, allocation_id, updated_data):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            for allocation_elem in root.findall(".//allocation"):
                id_elem = allocation_elem.find("id")
                if id_elem is not None and int(id_elem.text) == allocation_id:
                    # Update the allocation element with the updated data
                    for key, value in updated_data.items():
                        elem = allocation_elem.find(key)
                        if elem is not None:
                            elem.text = str(value)

                    tree.write(filename)
                    return True

            return False  # Allocation with the specified ID not found

        except Exception as e:
            print(f"Error updating allocation from XML: {e}")
            return False


    # ---------------------------------------------------------------------------------------------------
    # ----------------------------------------------delete in database and file-----------------------------------------------------
    @classmethod
    def delete_from_xml(cls, filename, allocation_id):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            for allocation_elem in root.findall("allocation"):
                if int(allocation_elem.find("id").text) == allocation_id:
                    root.remove(allocation_elem)
                    tree.write(filename)
                    print(f"Allocation with ID {allocation_id} deleted successfully.")
                    return

            print(f"Allocation with ID {allocation_id} not found in the XML file.")
        except Exception as e:
            print(f"Error deleting allocation from XML: {e}")

    # ---------------------------------------------------------------------------------------------------
    # ----------------------------------------get all in database and file-----------------------------------------------------------
    @staticmethod
    def get_all_allocations_from_xml(filename):
        allocations = []

        try:
            allocation_xml = ET.parse(filename).getroot()
            for allocation_elem in allocation_xml.findall("allocation"):
                allocation_id = int(allocation_elem.find("id").text)
                allocation_date = allocation_elem.find("date").text
                allocation_price = float(allocation_elem.find("price").text)
                allocation_nbr_days = int(allocation_elem.find("nbr_days").text)
                client_id = int(allocation_elem.find("client_id").text)
                car_id = int(allocation_elem.find("car_id").text)

                allocation = Allocation(allocation_id, allocation_date, allocation_price, allocation_nbr_days, client_id, car_id)
                allocations.append(allocation)

        except Exception as e:
            print(f"Error getting all allocations: {e}")

        return allocations
    # ---------------------------------------------------------------------------------------------------
    # ----------------------------------------get by id in database and file-----------------------------------------------------------
    @classmethod
    def get_allocation_by_id_from_xml(cls, filename, allocation_id):
        try:
            allocation_xml = ET.parse(filename).getroot()
            for allocation_elem in allocation_xml.findall("allocation"):
                if int(allocation_elem.find("id").text) == allocation_id:
                    allocation_id = int(allocation_elem.find("id").text)
                    allocation_date = allocation_elem.find("date").text
                    allocation_price = float(allocation_elem.find("price").text)
                    allocation_nbr_days = int(allocation_elem.find("nbr_days").text)
                    client_id = int(allocation_elem.find("client_id").text)
                    car_id = int(allocation_elem.find("car_id").text)
                    
                    return cls(allocation_id, allocation_date, allocation_price, allocation_nbr_days, client_id, car_id)
        except Exception as e:
            print(f"Error getting allocation by ID: {e}")

        return None

# ---------------------------------------define the test method to cars-----------------------------------


# ---------------------------------------------------------------------------------------------------

def test_allocation():
    while True:
        print_info("\n Allocation Management :")
        print()
        print()
        print_info("1. Create a new allocation")
        print_info("2. Update an allocation")
        print_info("3. Delete an allocation")
        print_info("4. View all allocations")
        print_info("5. View allocation by ID")
        print_error("6. Go back to the main menu 🔙")

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
            break
        else:
            print_error("Invalid choice. Please enter a valid option.")
        time.sleep(1)
        os.system("cls")

def create_allocation():
    allocation_date = input("Enter the allocation date: ")
    allocation_price = float(input("Enter the allocation price: "))
    allocation_nbr_days = int(input("Enter the number of days: "))
    client_id = int(input("Enter the client ID: "))
    car_id = int(input("Enter the car ID: "))
    
    try:
        # Create a new Allocation instance
        new_allocation = Allocation(
            random.randint(1000, 100000),
            allocation_date,
            allocation_price,
            allocation_nbr_days,
            client_id,
            car_id,
        )
        
        # Save the allocation to an XML file
        new_allocation.save_to_xml("allocations.xml")

        print("Allocation created and saved successfully.")
    except Exception as e:
        print(f"Error: {e}")

def update_allocation():
    allocation_id = input("Enter the allocation ID to update: ")

    try:
        allocation_id = int(allocation_id)
        allocation = Allocation.get_allocation_by_id_from_xml("allocations.xml", allocation_id)

        if allocation is not None:
            # Prompt the user for updated information
            new_date = input("Enter the updated date (press Enter to keep it unchanged): ")
            new_price = input("Enter the updated price (press Enter to keep it unchanged): ")
            new_nbr_days = input("Enter the updated number of days (press Enter to keep it unchanged): ")
            new_client_id = input("Enter the updated client ID (press Enter to keep it unchanged): ")
            new_car_id = input("Enter the updated car ID (press Enter to keep it unchanged): ")

            # Create a dictionary for updated data
            updated_data = {}
            if new_date:
                updated_data["date"] = new_date
            if new_price:
                updated_data["price"] = float(new_price)
            if new_nbr_days:
                updated_data["nbr_days"] = int(new_nbr_days)
            if new_client_id:
                updated_data["client_id"] = int(new_client_id)
            if new_car_id:
                updated_data["car_id"] = int(new_car_id)

            # Update the XML file with the modified allocation
            if allocation.update_from_xml("allocations.xml", allocation_id, updated_data):
                print("Allocation updated successfully.")
            else:
                print("Error updating allocation in the XML file.")
        else:
            print("Allocation not found.")
    except ValueError:
        print("Invalid allocation ID. Please enter a valid integer.")

def delete_allocation():
    allocation_id = int(input("Enter the allocation ID to delete: "))
    
    if Allocation.delete_from_xml("allocations.xml", allocation_id):
        print_success("Allocation deleted.")
    else:
        print_error("Allocation not found or an error occurred.")

def view_all_allocations():
    allocations = Allocation.get_all_allocations_from_xml("allocations.xml")
    if allocations:
        for allocation in allocations:
            print(
                f"ID: {allocation.id}, Date: {allocation.date}, Price: {allocation.price}, Days: {allocation.nbr_days}, Client ID: {allocation.client_id}, Car ID: {allocation.car_id}"
            )
    else:
        print("No allocations found.")

def view_allocation_by_id():
    allocation_id = input("Enter the allocation ID to view: ")
    allocation = Allocation.get_allocation_by_id_from_xml("allocations.xml", int(allocation_id))
    if allocation is not None:
        print(
            f"ID: {allocation.id}, Date: {allocation.date}, Price: {allocation.price}, Days: {allocation.nbr_days}, Client ID: {allocation.client_id}, Car ID: {allocation.car_id}"
        )
    else:
        print_error("Allocation not found.")

# Define your print_info, print_success, and print_error functions as needed

# Start your program
if __name__ == "__main__":
    test_allocation()

# ---------------------------------------------------------------------------------------------------
