from lxml import etree

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
            f"Client ID: {self.id}, Full Name: {self.full_name}, Address: {self.address}, Phone: {self.phone}, Email: {self.email}, CIN: {self.cin}"
        )

    # ---------------------------------------------------------------------------- #
    #                            Save client to XML file                            #
    # ---------------------------------------------------------------------------- #

    @staticmethod
    def create_client_file():
        # Crée un fichier XML vide pour les clients
        root = etree.Element("clients")
        tree = etree.ElementTree(root)
        tree.write("clients.xml")

    def save_file(self):
        # Ajoute le client actuel au fichier XML
        try:
            tree = etree.parse("clients.xml")
            root = tree.getroot()
        except (etree.XMLSyntaxError, FileNotFoundError):
            # Crée un nouveau fichier XML si le fichier n'existe pas ou est mal formé
            root = etree.Element("clients")
            tree = etree.ElementTree(root)
        
        client = etree.SubElement(root, "client")
        client.set("id", str(self.id))
        
        full_name = etree.SubElement(client, "full_name")
        full_name.text = self.full_name
        
        address = etree.SubElement(client, "address")
        address.text = self.address
        
        phone = etree.SubElement(client, "phone")
        phone.text = self.phone
        
        email = etree.SubElement(client, "email")
        email.text = self.email
        
        cin = etree.SubElement(client, "cin")
        cin.text = self.cin
        
        tree.write("clients.xml")

    # ---------------------------------------------------------------------------- #
    #                                 Update client                                #
    # ---------------------------------------------------------------------------- #

    def update_file(self):
        clients = self.get_all_file()
        for i, client in enumerate(clients):
            if client.id == self.id:
                clients[i] = self
        self.write_clients_to_xml(clients)

    @staticmethod
    def write_clients_to_xml(clients):
        root = etree.Element("clients")
        for client in clients:
            client_element = etree.SubElement(root, "client")
            client_element.set("id", str(client.id))
            
            full_name = etree.SubElement(client_element, "full_name")
            full_name.text = client.full_name
            
            address = etree.SubElement(client_element, "address")
            address.text = client.address
            
            phone = etree.SubElement(client_element, "phone")
            phone.text = client.phone
            
            email = etree.SubElement(client_element, "email")
            email.text = client.email
            
            cin = etree.SubElement(client_element, "cin")
            cin.text = client.cin
        
        tree = etree.ElementTree(root)
        tree.write("clients.xml")

#     # ---------------------------------------------------------------------------- #
#     #                                 Delete client                                 #
#     # ---------------------------------------------------------------------------- #
    @staticmethod
    def delete_file(client_id):
        clients = Client.get_all_file()
        clients = [client for client in clients if client.id != client_id]
        Client.write_clients_to_xml(clients)

# ---------------------------------------------------------------------------- #
#                                 get_all_client                                #
# ---------------------------------------------------------------------------- #
    @staticmethod
    def get_all_file():
        # Lit tous les clients à partir du fichier XML et renvoie une liste d'objets Client
        clients = []
        try:
            tree = etree.parse("clients.xml")
            root = tree.getroot()
            for client_element in root.findall("client"):
                id = client_element.get("id")
                full_name = client_element.find("full_name").text
                address = client_element.find("address").text
                phone = client_element.find("phone").text
                email = client_element.find("email").text
                cin = client_element.find("cin").text
                client = Client(id, full_name, address, phone, email, cin)
                clients.append(client)
        except (etree.XMLSyntaxError, FileNotFoundError):
            # Crée un nouveau fichier XML si le fichier n'existe pas ou est mal formé
            pass
        return clients

# ---------------------------------------------------------------------------- #
#                                    getbyid                                   #
# ---------------------------------------------------------------------------- #
    @staticmethod
    def get_one_file(client_id):
        # Récupère la liste de tous les clients
        clients = Client.get_all_file()

        # Parcourt la liste des clients
        for client in clients:
            # Si l'ID du client correspond à l'ID recherché
            if client.id == client_id:
                # Renvoie le client trouvé
                return client

        # Si aucun client avec l'ID spécifié n'est trouvé, renvoie None
        return None










# ---------------------------------------------------------------------------- #
#                                  pour tester                                 #
# ---------------------------------------------------------------------------- #
Client.create_client_file()

# Exemple d'utilisation de la classe Client pour ajouter un client et afficher ses informations
client1 = Client("1", "bouchraessatti", "tetouane", "+212695559512", "bouchra@gmail.com", "L658581")
client1.save_file()
client1.display_info()

client2 = Client("2", "douaeessatti", "tetouane", "+0345678", "douae@gmail.com", "L158581")
client2.save_file()
client2.display_info()

client3 = Client("3", "ososessatti", "tetouane", "+212695559511", "oussama@gmail.com", "L6658511")
client3.save_file()
client3.display_info()

client4 = Client("4", "amani", "martil", "+098765454", "amani@gmail.com", "Lm6658511")
client4.save_file()
client4.display_info()

 # ---------------------------------------------------------------------------- #
 #                   Mettre à jour les informations du client                   #
 # ---------------------------------------------------------------------------- #
updated_info = Client("1", "fati", "456 Elm St", "555-987-6543", "john.smith@example.com", "B9876543")
updated_info.update_file()
# ---------------------------------------------------------------------------- #
#                         suppression par id de clients                        #
# ---------------------------------------------------------------------------- #
# Client.delete_file("2")

# ------------------ afficher les clients apres suppression ------------------ #
# print("Liste des clients après suppression :")
# all_clients = Client.get_all_file()
# for client in all_clients:
#     client.display_info()

 # ---------------------------------------------------------------------------- #
 #     Utilisez la méthode get_all_file pour récupérer la liste des clients     #
 # ---------------------------------------------------------------------------- #
# print("Liste des clients :")
# all_clients = Client.get_all_file()
# # Parcourez la liste des clients et affichez les détails de chaque client
# for client in all_clients:
#     client.display_info()

   

# ---------------------------------------------------------------------------- #
#                                    GETBYID                                   #
# ---------------------------------------------------------------------------- #
# client_id_to_find = "2"  # Remplacez ceci par l'ID du client que vous souhaitez trouver

# # Appelez la méthode pour essayer de récupérer le client
# found_client = Client.get_one_file(client_id_to_find)

# # Vérifiez si un client a été trouvé
# if found_client is not None:
#     print("Client trouvé :")
#     found_client.display_info()
# else:
#     print(f"Aucun client trouvé avec l'ID {client_id_to_find}")


