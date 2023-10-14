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

    
        
    def create_client_file():
        # Crée un fichier vide pour les clients
        with open("clients.txt", "w") as file:
            file.write("")
    def save_file(self):
        with open("clients.txt", "a") as file:
            file.write(f"{self.id},{self.full_name},{self.address},{self.phone},{self.email},{self.cin}\n")
    def update(self):
        conn = sqlite3.connect("db/my_database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE clients SET FullName=?, address=?, phone=?, email=?, CIN=? WHERE id=?",
                       (self.full_name, self.address, self.phone, self.email, self.cin, self.id))
        conn.commit()
        conn.close()
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
                file.write(f"{client.id},{client.full_name},{client.address},{client.phone},{client.email},{client.cin}\n")
    def delete(self):
        conn = sqlite3.connect("db/my_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id=?", (self.id,))
        conn.commit()
        conn.close()
    @staticmethod
    def delete_file(client_id):
        clients = Client.get_all_file()
        clients = [client for client in clients if client.id != client_id]
        with open("clients.txt", "w") as file:
            for client in clients:
                file.write(f"{client.id},{client.full_name},{client.address},{client.phone},{client.email},{client.cin}\n")
    @staticmethod
    def get_all():
        conn = sqlite3.connect("db/my_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()
        conn.close()
        return [Client(*client) for client in clients]
    @staticmethod
    def get_all_file():
        clients = []
        try:
            with open("clients.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    client_data = line.strip().split(',')
                    client = Client(int(client_data[0]), client_data[1], client_data[2], client_data[3], client_data[4], client_data[5])
                    clients.append(client)
        except FileNotFoundError:
            print("Aucun fichier de clients trouvé. Création d'un nouveau...")
            Client.create_client_file()
        return clients
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
    @staticmethod
    def get_one_file(client_id):
        clients = Client.get_all_file()
        for client in clients:
            if client.id == client_id:
                return client
        return None

def main():
    while True:
        print("Choose an operation:")
        print("1. Save a client")
        print("2. Update a client")
        print("3. Delete a client")
        print("4. Get all clients")
        print("5. Get one client by ID")
        print("6. Quit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            client_id = int(input("Enter client ID: "))
            full_name = input("Enter client full name: ")
            address = input("Enter client address: ")
            phone = input("Enter client phone: ")
            email = input("Enter client email: ")
            cin = input("Enter client CIN: ")
            client = Client(client_id, full_name, address, phone, email, cin)
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
        elif choice == "5":
            client_id = int(input("Enter the client ID you want to retrieve: "))
            client = Client.get_one_file(client_id)
            if client:
                client.display_info()
            else:
                print("Client not found.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-6).")

if __name__ == "__main__":
    main()