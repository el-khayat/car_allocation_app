from tkinter import *
import xml.etree.ElementTree as ET
from tkinter.ttk import Treeview
from random import randint

# Chemin du fichier XML
path = "clients.xml"

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

    def save(self):
        try:
            root = None
            try:
                tree = ET.parse(path)
                root = tree.getroot()
            except (FileNotFoundError, ET.ParseError):
                root = ET.Element("clients")

            new_client = ET.Element('client')
            new_client.set('id', str(self.id))

            full_name = ET.Element('full_name')
            full_name.text = self.full_name
            address = ET.Element('address')
            address.text = self.address
            phone = ET.Element('phone')
            phone.text = self.phone
            email = ET.Element('email')
            email.text = self.email
            cin = ET.Element('cin')
            cin.text = self.cin

            new_client.append(full_name)
            new_client.append(address)
            new_client.append(phone)
            new_client.append(email)
            new_client.append(cin)

            root.append(new_client)
            tree = ET.ElementTree(root)
            tree.write(path)

        except Exception as e:
            print(f"Error saving client to XML: {e}")

    @staticmethod
    def delete(client_id):
        try:
            tree = ET.parse(path)
        except FileNotFoundError:
            return False

        root = tree.getroot()

        client_to_delete = None
        for client_element in root.findall('client'):
            id = client_element.get('id')
            if id == str(client_id):
                client_to_delete = client_element
                break

        if client_to_delete is not None:
            root.remove(client_to_delete)
            tree.write(path)
            return True
        else:
            return False

    def update(self):
        try:
            tree = ET.parse(path)
        except FileNotFoundError:
            return False

        root = tree.getroot()

        client_to_update = None
        for client_element in root.findall('client'):
            id = client_element.get('id')
            if id == str(self.id):
                client_to_update = client_element
                break

        if client_to_update is not None:
            client_to_update.find('full_name').text = self.full_name
            client_to_update.find('address').text = self.address
            client_to_update.find('phone').text = self.phone
            client_to_update.find('email').text = self.email
            client_to_update.find('cin').text = self.cin
            tree.write(path)
            return True
        else:
            return False

    @staticmethod
    def get_all():
        try:
            tree = ET.parse(path)
        except FileNotFoundError:
            return []

        root = tree.getroot()
        clients = []

        for client_element in root.findall('client'):
            id = client_element.get('id')
            full_name = client_element.find('full_name').text
            address = client_element.find('address').text
            phone = client_element.find('phone').text
            email = client_element.find('email').text
            cin = client_element.find('cin').text
            client = Client(id, full_name, address, phone, email, cin)
            clients.append(client)
        return clients

    @staticmethod
    def get_one(client_id):
        try:
            tree = ET.parse(path)
        except FileNotFoundError:
            return None

        root = tree.getroot()

        for client_element in root.findall('client'):
            id = client_element.get('id')
            if id == str(client_id):
                full_name = client_element.find('full_name').text
                address = client_element.find('address').text
                phone = client_element.find('phone').text
                email = client_element.find('email').text
                cin = client_element.find('cin').text
                client = Client(id, full_name, address, phone, email, cin)
                return client
        return None

def clearForm():
    full_name_text.delete(1.0, END)
    address_text.delete(1.0, END)
    phone_text.delete(1.0, END)
    email_text.delete(1.0, END)
    cin_text.delete(1.0, END)

def addClient():
    full_name = full_name_text.get("1.0", END).strip()
    address = address_text.get("1.0", END).strip()
    phone = phone_text.get("1.0", END).strip()
    email = email_text.get("1.0", END).strip()
    cin = cin_text.get("1.0", END).strip()
    id = randint(1, 1000)
    client = Client(id, full_name, address, phone, email, cin)
    client.save()
    print("Client saved successfully")

    clearForm()
    refreshTable()

def updateClient():
    full_name = full_name_text.get("1.0", END).strip()
    address = address_text.get("1.0", END).strip()
    phone = phone_text.get("1.0", END).strip()
    email = email_text.get("1.0", END).strip()
    cin = cin_text.get("1.0", END).strip()

    client = Client(current_id, full_name, address, phone, email, cin)
    client.update()
    client.display_info()
    global actionStatus
    actionStatus = 'Add'
    btnAction.config(text="Add", command=addClient ,bg="orange")
    clearForm()
    refreshTable()

# root = Tk()
# root.title("Client Management")
# root.config(bg="#344560")
# root.geometry("1250x400")

root = Tk()
root.title("Client Management")
root.iconbitmap("clients.ico")
root.config(bg="black")  # Changer la couleur de fond en noir
root.geometry("1250x400")


current_id = 0
actionStatus = "Add"

frameRoot = Frame(root, bd=5)
frameForm = LabelFrame(frameRoot, text="Client Form")

labelFullName = Label(frameForm, text="Full Name", height=1)
full_name_text = Text(frameForm, width=20, height=1)

labelAddress = Label(frameForm, text="Address", height=1, width=10, padx=0, pady=0)
address_text = Text(frameForm, width=20, height=1)

labelPhone = Label(frameForm, text="Phone", height=1, width=10, padx=0, pady=0)
phone_text = Text(frameForm, width=20, height=1)

labelEmail = Label(frameForm, text="Email", height=1, width=10, padx=0, pady=0)
email_text = Text(frameForm, width=20, height=1)

labelCIN = Label(frameForm, text="CIN", height=1, width=10, padx=0, pady=0)
cin_text = Text(frameForm, width=20, height=1)

btnAction = Button(frameForm, text="Add", bg="orange", command=addClient)

labelFullName.grid(column=0, row=0, padx=10, pady=10)
labelAddress.grid(column=1, row=0, padx=10, pady=10)
labelPhone.grid(column=2, row=0, padx=10, pady=10)
labelEmail.grid(column=3, row=0, padx=10, pady=10)
labelCIN.grid(column=4, row=0, padx=10, pady=10)

full_name_text.grid(column=0, row=1, padx=10, pady=10)
address_text.grid(column=1, row=1, padx=10, pady=10)
phone_text.grid(column=2, row=1, padx=10, pady=10)
email_text.grid(column=3, row=1, padx=10, pady=10)
cin_text.grid(column=4, row=1, padx=10, pady=10)
btnAction.grid(column=5, row=1, padx=10, pady=10)

table = Treeview(frameRoot, columns=('id', 'full_name', 'address', 'phone', 'email', 'cin'), show="headings")
table.heading('id', text='ID')
table.heading('full_name', text='Full Name')
table.heading('address', text='Address')
table.heading('phone', text='Phone')
table.heading('email', text='Email')
table.heading('cin', text='CIN')

table.column('id', width=30, anchor='center')
table.column('full_name', anchor='center')
table.column('address', anchor='center')
table.column('phone', anchor='center')
table.column('email', anchor='center')
table.column('cin', anchor='center')

def refreshTable():
    for item in table.get_children():
        table.delete(item)
    for client in Client.get_all():
        table.insert("", "end", values=(client.id, client.full_name, client.address, client.phone, client.email, client.cin))

refreshTable()

def delete_client():
    for i in table.selection():
        client_id = table.item(i, 'values')[0]
        if client_id:
            Client.delete(client_id)
    refreshTable()

def update_client():
    if len(table.selection()) == 1:
        for i in table.selection():
            global current_id
            current_id = table.item(i, 'values')[0]

            full_name_text.delete(1.0, END)
            full_name_text.insert(1.0, table.item(i, 'values')[1])

            address_text.delete(1.0, END)
            address_text.insert(1.0, table.item(i, 'values')[2])

            phone_text.delete(1.0, END)
            phone_text.insert(1.0, table.item(i, 'values')[3])

            email_text.delete(1.0, END)
            email_text.insert(1.0, table.item(i, 'values')[4])

            cin_text.delete(1.0, END)
            cin_text.insert(1.0, table.item(i, 'values')[5])

            btnAction.config(text="Update",bg="orange", command=updateClient)
            global actionStatus
            actionStatus = 'Update'

frameRoot.pack()
frameForm.grid(column=0, row=0, padx=10, pady=10)
table.grid(column=0, row=2, padx=10, pady=10)

frameAction = Frame(frameRoot,)
frameAction.grid(column=0, row=1, padx=10)

btnDelete = Button(frameAction, text="Delete",bg="orange", command=delete_client)
btnDelete.grid(column=0, row=1, padx=10, pady=10)

btnUpdate = Button(frameAction, text="Update", bg="orange",command=update_client)
btnUpdate.grid(column=1, row=1, padx=10, pady=10)

root.mainloop()
