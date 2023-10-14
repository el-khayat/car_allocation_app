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

    def update(self):
        conn = sqlite3.connect("cars.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE cars SET name=?, model=?, price=?, is_disponible=?, nbr_places=? WHERE id=?",
                       (self.name, self.model, self.price, self.is_disponible, self.nbr_places, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect("cars.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE id=?", (self.id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect("cars.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars")
        cars = cursor.fetchall()
        conn.close()
        return [Car(*car) for car in cars]

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
