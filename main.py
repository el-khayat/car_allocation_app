#i change in the main to test the pull command
import sqlite3
from model.car import Car 


conn = sqlite3.connect("cars.db")
cursor = conn.cursor()

# Define the SQL query to create the 'cars' table
drop_casrs_table = "DROP TABLE IF EXISTS cars;"
cursor.execute(drop_casrs_table)

create_table_query = """
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    model TEXT NOT NULL,
    price REAL NOT NULL,
    is_disponible INTEGER NOT NULL,
    nbr_places INTEGER NOT NULL
);
"""
cursor.execute(create_table_query)
conn.commit()
conn.close()



def main():
    while True:
        print("Choose an operation:")
        print("1. Save a car")
        print("2. Update a car")
        print("3. Delete a car")
        print("4. Get all cars")
        print("5. Get one car by ID")
        print("6. Quit")
        
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            car = Car(None, 25000, "Toyota", "Camry", True, 5)
            car.save()
        elif choice == "2":
            car_id = int(input("Enter the car ID you want to update: "))
            car = Car.get_one(car_id)
            if car:
                # Update the car
                car.price = float(input("Enter the new price: $"))
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
        elif choice == "5":
            car_id = int(input("Enter the car ID you want to retrieve: "))
            car = Car.get_one(car_id)
            if car:
                car.display_info()
            else:
                print("Car not found.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-6).")

if __name__ == "__main__":
    main()
    ################################ 2nd part #########################################
def main():
    while True:
        print("Choose an operation:")
        print("1. Save a car")
        print("2. Update a car")
        print("3. Delete a car")
        print("4. Get all cars")
        print("5. Get one car by ID")
        print("6. Quit")
        
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            car_id = int(input("Enter car ID: "))
            price = float(input("Enter car price: $"))
            name = input("Enter car name: ")
            model = input("Enter car model: ")
            is_disponible = bool(int(input("Is car available? (1 for Yes, 0 for No): ")))
            nbr_places = int(input("Enter the number of places: "))
            car = Car(car_id, price, name, model, is_disponible, nbr_places)
            car.save_file()
            print("Car saved successfully.")
        elif choice == "2":
            car_id = int(input("Enter the car ID you want to update: "))
            updated_car = Car.get_one_file(car_id)
            if updated_car:
                updated_car.price = float(input("Enter the new price: $"))
                updated_car.name = input("Enter the new name: ")
                updated_car.model = input("Enter the new model: ")
                updated_car.is_disponible = bool(int(input("Is car available? (1 for Yes, 0 for No): ")))
                updated_car.nbr_places = int(input("Enter the new number of places: "))
                updated_car = Car(updated_car.id, updated_car.price, updated_car.name, updated_car.model, updated_car.is_disponible, updated_car.nbr_places)
                updated_car.update_file()
                print("Car updated successfully.")
            else:
                print("Car not found.")
        elif choice == "3":
            car_id = int(input("Enter the car ID you want to delete: "))
            Car.delete_file(car_id)
            print("Car deleted successfully.")
        elif choice == "4":
            cars = Car.get_all_file()
            for car in cars:
                car.display_info()
        elif choice == "5":
            car_id = int(input("Enter the car ID you want to retrieve: "))
            car = Car.get_one_file(car_id)
            if car:
                car.display_info()
            else:
                print("Car not found.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-6).")

if __name__ == "__main__":
    main()