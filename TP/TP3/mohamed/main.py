from random import randint
import sys
from tkinter import END
from PyQt5 import QtWidgets,uic

import sqlite3

App = QtWidgets.QApplication(sys.argv)
Fen = uic.loadUi("./home.ui")

# ---------------------------------------------------------------------------- #
#                                calss (Entity)                                #
# ---------------------------------------------------------------------------- #

conn = sqlite3.connect("car_allocation.db")
cursor = conn.cursor()

# Define the tables and schema

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
    INSERT INTO cars (name, model, price, is_disponible, nbr_places) VALUES ('BMW', 'X6', 1000, 1, 5),('DACIA', '2019', 1000, 1, 6),('BMW', 'X6', 1000, 1, 3)
    """
)
# Save changes and close the connection
conn.commit()
conn.close()

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
        print("updating... : (insite)",self.id)
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
    @staticmethod
    def delete(car_id):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE id=?", (car_id,))
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


# ---------------------------------------------------------------------------- #
#                               global variables                               #
# ---------------------------------------------------------------------------- #

current_id  = 0 
actionStatu = "Add"

def refreshTable(table):
    table.clear()

    for row in Car.get_all():

        item = QtWidgets.QTreeWidgetItem(table)
        item.setText(0, str(row.id))
        item.setText(1, row.name)
        item.setText(2, row.model)
        item.setText(3, str(row.price))
        item.setText(4, "Yes" if True else "No")
        item.setText(5, str(row.nbr_places))

    # for car in Car.get_all():
    #     car.display_info()
    #     table.insert("", "end", values=(car.id, car.name, car.model, car.price, car.is_disponible, car.nbr_places))


def clearForm():
    Fen.name.setText("")
    Fen.model.setText("")
    Fen.price.setText("")
    Fen.isDispo.setText("")
    Fen.nbrPlace.setText("")
    return None

def addCar():
    name = Fen.name.text().strip()
    model = Fen.model.text().strip()
    price = Fen.price.text().strip()
    is_dispo = Fen.isDispo.text().strip()
    nbr_place = Fen.nbrPlace.text().strip()
    id = randint(1,1000)
    car = Car(id, name, model,price, is_dispo, nbr_place)
    car.save()
   # clearForm()
    refreshTable(Fen.table)

def validateForm():
    name = Fen.name.text().strip()
    model = Fen.model.text().strip()
    price = Fen.price.text().strip()
    is_dispo = Fen.isDispo.text().strip()
    nbr_place = Fen.nbrPlace.text().strip()
    if name and model and price and is_dispo and nbr_place:
        return True
    return False

def updateCar():
    #id = id_text.get("1.0", END).strip()
    print("updating... :",current_id)

    name = Fen.name.text().strip()
    model = Fen.model.text().strip()
    price = Fen.price.text().strip()
    is_dispo = Fen.isDispo.text().strip()
    nbr_place = Fen.nbrPlace.text().strip()

    # car = Car(current_id, name, model,price, is_dispo, nbr_place)
    car = Car.get_one(current_id)
    car.display_info()
    car.name = name
    car.model = model
    car.price = price
    car.is_disponible = is_dispo
    car.nbr_places = nbr_place

    car.update()

    global actionStatu
    actionStatu = 'Add'
    Fen.action.setText(actionStatu)
    Fen.action.clicked.disconnect(updateCar)
    Fen.action.clicked.connect(addCar)
    #clearForm()
    refreshTable(Fen.table)
    return None


def delete():
    table = Fen.table
    selected_item = table.currentItem()
    if selected_item:
        car_id = selected_item.text(0)
        Car.delete(car_id)
        refreshTable(table)

def changeToUpdate():
    global actionStatu
    actionStatu = 'Update'
    Fen.action.setText(actionStatu)

    Fen.action.clicked.disconnect(addCar)
    Fen.action.clicked.connect(updateCar)
    
    table = Fen.table

    selected_item = table.currentItem()
    if selected_item:
        car_id = selected_item.text(0)
        Fen.name.setText(selected_item.text(1))
        Fen.model.setText(selected_item.text(2))
        Fen.price.setText(selected_item.text(3))
        Fen.isDispo.setText(selected_item.text(4))
        Fen.nbrPlace.setText(selected_item.text(5))
        global current_id
        current_id = car_id
        print("id to update :",current_id)

    return None

refreshTable(Fen.table)
Fen.action.clicked.connect(addCar)
Fen.action.setText(actionStatu)
Fen.update.clicked.connect(changeToUpdate)
Fen.delete_2.clicked.connect(delete)
# print(Fen.table)  
Fen.show()
App.exec_()
sys.exit()