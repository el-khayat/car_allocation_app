from tkinter import *
from tkinter import ttk
from lxml import etree

path = "C:/Users/ss/Desktop/Master M2I/S3/IHM/CAR_ALLOCATION_APP/car_allocation_app/TP/TP2/BOUCHRA/clients.xml"

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

    @staticmethod
    def create_client_file():
        root = etree.Element("clients")
        tree = etree.ElementTree(root)
        tree.write(path)

    def save_file(self):
        try:
            tree = etree.parse(path)
            root = tree.getroot()
        except (etree.XMLSyntaxError, FileNotFoundError):
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
        root.append(client)
        tree.write(path)

def supprimer_client_xml(client_id):
    try:
        tree = etree.parse(path)
        root = tree.getroot()
        for client in root.findall("client"):
            if client.get("id") == client_id:
                root.remove(client)
        tree.write(path)
    except (etree.XMLSyntaxError, FileNotFoundError):
        pass

def ajouter_client():
    client_id = id_entry.get()
    full_name = full_name_entry.get()
    address = address_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    cin = cin_entry.get()

    tableau_clients.insert("", "end", values=(client_id, full_name, address, phone, email, cin, "Supprimer"))
    
    id_entry.delete(0, END)
    full_name_entry.delete(0, END)
    address_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)
    cin_entry.delete(0, END)

    nouveau_client = Client(client_id, full_name, address, phone, email, cin)
    nouveau_client.save_file()

def supprimer_client():
    selection = tableau_clients.selection()
    if selection:
        for item in selection:
            client_id = tableau_clients.item(item, "values")[0]
            supprimer_client_xml(client_id)
            tableau_clients.delete(item)

def afficher_clients():
    try:
        tree = etree.parse(path)
        root = tree.getroot()
        for client in root.findall("client"):
            client_id = client.get("id")
            full_name = client.find("full_name").text
            address = client.find("address").text
            phone = client.find("phone").text
            email = client.find("email").text
            cin = client.find("cin").text
            tableau_clients.insert("", "end", values=(client_id, full_name, address, phone, email, cin, "Supprimer"))
    except (etree.XMLSyntaxError, FileNotFoundError):
        pass

fenetre = Tk()
fenetre.title("Gestion des Clients")
fenetre.configure(bg="black")
fenetre.geometry("1200x900")
id_label = Label(fenetre, text="ID du Client:", bg="black", fg="white")
full_name_label = Label(fenetre, text="Full Name:", bg="black", fg="white")
address_label = Label(fenetre, text="Address:", bg="black", fg="white")
phone_label = Label(fenetre, text="Phone:", bg="black", fg="white")
email_label = Label(fenetre, text="Email:", bg="black", fg="white")
cin_label = Label(fenetre, text="CIN:", bg="black", fg="white")

id_entry = Entry(fenetre, bg="black", fg="white", highlightbackground="orange", highlightcolor="orange", insertbackground="white")
full_name_entry = Entry(fenetre, bg="black", fg="white", highlightbackground="orange", highlightcolor="orange", insertbackground="white")
address_entry = Entry(fenetre, bg="black", fg="white", highlightbackground="orange", highlightcolor="orange", insertbackground="white")
phone_entry = Entry(fenetre, bg="black", fg="white", highlightbackground="orange", highlightcolor="orange", insertbackground="white")
email_entry = Entry(fenetre, bg="black", fg="white", highlightbackground="orange", highlightcolor="orange", insertbackground="white")
cin_entry = Entry(fenetre, bg="black", fg="white", highlightbackground="orange", highlightcolor="orange", insertbackground="white")

ajouter_bouton = Button(fenetre, text="Ajouter Client", command=ajouter_client, bg="orange", fg="black")
supprimer_button = Button(fenetre, text="Supprimer Client", command=supprimer_client, bg="red", fg="white")

tableau_clients = ttk.Treeview(fenetre, columns=("ID", "Full Name", "Address", "Phone", "Email", "CIN", "Action"), show="headings", height=5)
tableau_clients.heading("ID", text="ID")
tableau_clients.heading("Full Name", text="Full Name")
tableau_clients.heading("Address", text="Address")
tableau_clients.heading("Phone", text="Phone")
tableau_clients.heading("Email", text="Email")
tableau_clients.heading("CIN", text="CIN")
tableau_clients.heading("Action", text="Action")

for item in tableau_clients.get_children():
    tableau_clients.insert(item, "end", values=("Supprimer",))

id_label.grid(row=0, column=0, padx=10, pady=10)
id_entry.grid(row=0, column=1, padx=10, pady=10)
full_name_label.grid(row=1, column=0, padx=10, pady=10)
full_name_entry.grid(row=1, column=1, padx=10, pady=10)
address_label.grid(row=2, column=0, padx=10, pady=10)
address_entry.grid(row=2, column=1, padx=10, pady=10)
phone_label.grid(row=3, column=0, padx=10, pady=10)
phone_entry.grid(row=3, column=1, padx=10, pady=10)
email_label.grid(row=4, column=0, padx=10, pady=10)
email_entry.grid(row=4, column=1, padx=10, pady=10)
cin_label.grid(row=5, column=0, padx=10, pady=10)
cin_entry.grid(row=5, column=1, padx=10, pady=10)
ajouter_bouton.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
supprimer_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
tableau_clients.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

Client.create_client_file()  # Crée le fichier XML initial
afficher_clients()  # Affiche les clients existants

fenetre.mainloop()
