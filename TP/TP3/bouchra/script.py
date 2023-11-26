from random import randint
import sys
from PyQt5 import QtWidgets, uic
import sqlite3

# Créez l'application PyQt
App = QtWidgets.QApplication(sys.argv)

# Chargez l'interface utilisateur à partir du fichier "home.ui"
Fen = uic.loadUi("./view.ui")
table = Fen.table

# Connexion à la base de données SQLite
conn = sqlite3.connect("car_allocation.db")
cursor = conn.cursor()

# Définition des tables et du schéma pour les clients
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    address TEXT,
    phone TEXT,
    email TEXT,
    cin TEXT
    )
"""

)

query  =   """
    INSERT INTO clients (full_name, address, phone, email, cin) VALUES
    ('essattibouchra', '123 tetouane', '08985-123-4567', 'bouchra@example.com', 'LBC123'),
    ('mohamedelkhayat', '456 beni ahmed ', '0690-987-6543', 'hamae@example.com', 'LYZ456')
    """

# cursor.execute(query)

conn.commit()
conn.close()

class Client:
    def __init__(self, client_id, full_name, address, phone, email, cin):
        self.id = client_id
        self.full_name = full_name
        self.address = address
        self.phone = phone
        self.email = email
        self.cin = cin

    def display_info(self):
        print(f"Client ID: {self.id}, Full Name: {self.full_name}, Address: {self.address}, Phone: {self.phone}, Email: {self.email}, CIN: {self.cin}")

    def save(self):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clients (full_name, address, phone, email, cin) VALUES (?, ?, ?, ?, ?)",
            (self.full_name, self.address, self.phone, self.email, self.cin),
        )
        print("client saved successfully.")
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()


    def update(self):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clients SET full_name=?, address=?, phone=?, email=?, cin=? WHERE id=?",
            (
                self.full_name,
                self.address,
                self.phone,
                self.email,
                self.cin,
                self.id,
            ),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(client_id):
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id=?", (client_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect("car_allocation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()
        conn.close()
        return [Client(*client) for client in clients]



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

# uhgjhuhghhuyjhbjh

current_id  = 0 
actionStatu = "Add"

def refreshClientsTable(table):
    table.clear()

    for row in Client.get_all():
        item = QtWidgets.QTreeWidgetItem(table)
        item.setText(0, str(row.id))
        item.setText(1, row.full_name)
        item.setText(2, row.address)
        item.setText(3, row.phone)
        item.setText(4, row.email)
        item.setText(5, row.cin)

def clearClientForm():
    Fen.full_name.setText("")
    Fen.address.setText("")
    Fen.phone.setText("")
    Fen.email.setText("")
    Fen.cin.setText("")
    return None

def addClient():
    full_name = Fen.full_name.text().strip()
    address = Fen.address.text().strip()
    phone = Fen.phone.text().strip()
    email = Fen.email.text().strip()
    cin = Fen.cin.text().strip()
    id = randint(1,1000)
    client = Client(id, full_name, address, phone, email, cin)
    client.save()
    refreshClientsTable(Fen.table)
    # clearClientForm()
    # validateform???

def updateClient():
    full_name = Fen.full_name.text().strip()
    address = Fen.address.text().strip()
    phone = Fen.phone.text().strip()
    email = Fen.email.text().strip()
    cin = Fen.cin.text().strip()

    print(full_name,address)
    client = Client.get_one(current_id)


    client.full_name = full_name
    client.address = address
    client.phone = phone
    client.email = email
    client.cin = cin
    client.update()

    refreshClientsTable(table)
    clearClientForm()


    global actionStatu
    actionStatu = 'Add'
    
    Fen.action.setText(actionStatu)
    Fen.action.clicked.disconnect(updateClient)
    Fen.action.clicked.connect(addClient)

def deleteClient():
    selected_item = table.currentItem()
    if selected_item:
        client_id = int(selected_item.text(0))
        Client.delete(client_id)
        refreshClientsTable(table)
        

def changeToUpdateClient():
    
    selected_item = table.currentItem()
    if selected_item:
        global actionStatu
        actionStatu = 'Update'
        
        Fen.action.setText(actionStatu)
        Fen.action.clicked.disconnect(addClient)
        Fen.action.clicked.connect(updateClient)


        client_id = int(selected_item.text(0))
        client = Client.get_one(client_id)

        Fen.full_name.setText(client.full_name)
        Fen.address.setText(client.address)
        Fen.phone.setText(client.phone)
        Fen.email.setText(client.email)
        Fen.cin.setText(client.cin)
        global current_id
        current_id = client_id

# Connectez les boutons et les actions associées
Fen.action.clicked.connect(addClient)
Fen.update.clicked.connect(changeToUpdateClient)
Fen.delete_2.clicked.connect(deleteClient)
# Fen.clientsTable.itemSelectionChanged.connect(changeToUpdateClient)

# Rafraîchissez la table des clients
refreshClientsTable(table)

# Affichez l'interface utilisateur
Fen.show()

# Exécutez l'application
App.exec_()
sys.exit()
