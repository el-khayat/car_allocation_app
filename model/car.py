import sqlite3

class Car:
    def __init__(self, car_id, price, name, model, is_disponible, nbr_places):
        self.id = car_id
        self.price = price
        self.name = name
        self.model = model
        self.is_disponible = is_disponible
        self.nbr_places = nbr_places

    def display_info(self):
        print("Car information:")
        print(f"Car ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Model: {self.model}")
        print(f"Price: ${self.price}")
        print(f"Available: {'Yes' if self.is_disponible else 'No'}")
        print(f"Number of Places: {self.nbr_places}")

    def save(self):
        print("Saving the car...")
        conn = sqlite3.connect("cars.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cars (name, model, price, is_disponible, nbr_places) VALUES (?, ?, ?, ?, ?)",
                       (self.name, self.model, self.price, self.is_disponible, self.nbr_places))
        print("Car saved successfully.")
        conn.commit()
        self.id = cursor.lastrowid;
        print(f"Car ID: {self.id}")
        conn.close()
    
    def create_car_file():
    # Create an empty car file
     with open("cars.txt", "w") as file:
        file.write("")
    
    def save_file(car):
        with open("cars.txt", "a") as file:
         file.write(f"{car.id},{car.price},{car.name},{car.model},{car.is_disponible},{car.nbr_places}\n")

    def update(self):
        conn = sqlite3.connect("cars.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE cars SET name=?, model=?, price=?, is_disponible=?, nbr_places=? WHERE id=?",
                       (self.name, self.model, self.price, self.is_disponible, self.nbr_places, self.id))
        conn.commit()
        conn.close()

    def update_file(self):
        cars = self.get_all_file()
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
                file.write(f"{car.id},{car.price},{car.name},{car.model},{car.is_disponible},{car.nbr_places}\n")


    def delete(self):
        conn = sqlite3.connect("cars.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE id=?", (self.id,))
        conn.commit()
        conn.close()
    @staticmethod
    def delete_file(car_id):
        cars = Car.get_all_file()
        cars = [car for car in cars if car.id != car_id]
        with open("cars.txt", "w") as file:
            for car in cars:
                file.write(f"{car.id},{car.price},{car.name},{car.model},{car.is_disponible},{car.nbr_places}\n")

    @staticmethod
    def get_all():
        conn = sqlite3.connect("cars.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars")
        cars = cursor.fetchall()
        conn.close()
        return [Car(*car) for car in cars]
    @staticmethod
    def get_all_file():
        cars = []
        try:
            with open("cars.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    car_data = line.strip().split(',')
                    car = Car(int(car_data[0]), float(car_data[1]), car_data[2], car_data[3], bool(car_data[4]), int(car_data[5]))
                    cars.append(car)
        except FileNotFoundError:
            print("No car file found. Creating a new one...")
            Car.create_car_file()
        return cars
    
    @staticmethod
    def get_one(car_id):
        conn = sqlite3.connect("cars.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars WHERE id=?", (car_id,))
        car = cursor.fetchone()
        conn.close()
        if car:
            return Car(*car)
        else:
            return None
    @staticmethod
    def get_one_file(car_id):
        cars = Car.get_all_file()
        for car in cars:
            if car.id == car_id:
                return Car(car_id, car.price, car.name, car.model, car.is_disponible, car.nbr_places)
        return None
