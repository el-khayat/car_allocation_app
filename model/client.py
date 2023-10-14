import sqlite3

class Client:
    def __init__(self, client_id, full_name, address, phone, email, cin):
        self.id = client_id
        self.full_name = full_name
        self.address = address
        self.phone = phone
        self.email = email
        self.cin = cin

    def display_info(self):
        print("Client information:")
        print(f"Client ID: {self.id}")
        print(f"Full Name: {self.full_name}")
        print(f"Address: {self.address}")
        print(f"Phone: {self.phone}")
        print(f"Email: {self.email}")
        print(f"CIN: {self.cin}")

    def save(self):
        print("Saving the client...")
        conn = sqlite3.connect("db/my_database.db") 
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clients (FullName, address, phone, email, CIN) VALUES (?, ?, ?, ?, ?)",
                       (self.full_name, self.address, self.phone, self.email, self.cin))
        print("Client saved successfully.")
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    def update(self):
        conn = sqlite3.connect("db/my_database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE clients SET FullName=?, address=?, phone=?, email=?, CIN=? WHERE id=?",
                       (self.full_name, self.address, self.phone, self.email, self.cin, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect("db/my_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id=?", (self.id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect("db/my_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()
        conn.close()
        return [Client(*client) for client in clients]

    @staticmethod
    def get_one(client_id):
        conn = sqlite3.connect("db/my_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id=?", (client_id,))
        client = cursor.fetchone()
        conn.close()
        if client:
            return Client(*client)
        else:
            return None
