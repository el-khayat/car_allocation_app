from tkinter import * 
import xml.etree.ElementTree as ET
from tkinter.ttk import Treeview
from random import randint

# ---------------------------------------------------------------------------- #
#                                   Class Car                                  #
# ---------------------------------------------------------------------------- #

# Load the existing XML file or create a new one if it doesn't exist
file  = "D:\Master QL\S3\IHM\Project\car_allocation_app\mine\cars.xml"
# try:
# except FileNotFoundError:
# If the file doesn't exist, create a new XML structure


class Car:
    def __init__(self, car_id, price, name, model, is_disponible, nbr_places):
        self.id = car_id
        self.price = price
        self.name = name
        self.model = model
        self.is_disponible = is_disponible
        self.nbr_places = nbr_places

    def display_info(self):
        print(
            f"Car ID: {self.id},Name: {self.name}, Model: {self.model},Price: ${self.price}, Available: {'Yes' if self.is_disponible else 'No'}, Number of Places: {self.nbr_places},"
        )
    def save(self):
        try:
            root = None
            try:
                tree = ET.parse(file)
                root = tree.getroot()
            except (FileNotFoundError, ET.ParseError):
                root = ET.Element("cars")

            new_car = ET.Element('car')
            new_car.set('id', str(self.id))

            name = ET.Element('name')
            name.text = self.name
            model = ET.Element('model')
            model.text = self.model
            price = ET.Element('price')
            price.text = self.price  
            is_disponible = ET.Element('is_disponible')
            is_disponible.text = self.is_disponible  
            nbr_places = ET.Element('nbr_places')
            nbr_places.text = self.nbr_places

            # Add name and age elements to the new user element
            new_car.append(name)
            new_car.append(price)
            new_car.append(model)
            new_car.append(is_disponible)
            new_car.append(nbr_places)


            root.append(new_car)
            tree = ET.ElementTree(root)
            tree.write(file)

        except Exception as e:
            print(f"Error saving allocation to XML: {e}")

    def update(self):
        try:
            tree = ET.parse(file)
        except FileNotFoundError:
            return False  # Return False if the file doesn't exist

        root = tree.getroot()

        user_to_update = None
        for user_element in root.findall('car'):
            user_id = user_element.get('id')
            if int(user_id) == int(self.id):
                user_to_update = user_element
                break

        if user_to_update is not None:
            print("user_to_update",user_to_update)
            user_to_update.find('name').text = self.name
            user_to_update.find('model').text = self.model
            user_to_update.find('price').text = self.price
            user_to_update.find('is_disponible').text = self.is_disponible
            user_to_update.find('nbr_places').text = self.nbr_places
            tree.write(file)
            return True  # Return True if the user was successfully updated
        else:
            return False  # Return False if the user with the specified ID is not found
    @staticmethod
    def delete(id):
        try:
            tree = ET.parse(file)
        except FileNotFoundError:
            return False  # Return False if the file doesn't exist

        root = tree.getroot()

        car_to_delete = None
        for car_element in root.findall('car'):
            car_id = car_element.get('id')
            if int (car_id) == int(id):
                car_to_delete = car_element
                break
        if car_to_delete is not None:
            root.remove(car_to_delete)
            tree.write(file)
            return True  # Return True if the car was successfully deleted
        else:
            return False  # Return False if the car with the specified ID is not found

    @staticmethod
    def get_all():
        try:
            tree = ET.parse(file)
        except FileNotFoundError:
            return []
        
        root = tree.getroot()
        cars = []

        for car_element in root.findall('car'):
            id = car_element.get('id')
            name = car_element.find('name').text
            model = car_element.find('model').text
            price = car_element.find('price').text
            is_disponible = car_element.find('is_disponible').text
            nbr_places = car_element.find('nbr_places').text
            car = Car(id, price ,name, model,  is_disponible, nbr_places)
            cars.append(car)
        return cars
    
    @staticmethod
    def get_one(car_id):
        try:
            tree = ET.parse(file)
        except FileNotFoundError:
            return [] 
        root = tree.getroot()
        for car_element in root.findall('car'):
            id = car_element.get('id')
            if int(id) == int(car_id):
                name = car_element.find('name').text
                model = car_element.find('model').text
                price = car_element.find('price').text
                is_disponible = car_element.find('is_disponible').text
                nbr_places = car_element.find('nbr_places').text
                car = Car(id, price ,name, model,  is_disponible, nbr_places)
                return car
        return None





# defining the root 
root = Tk()
root.title("Mine")
root.config(bg="#344560")
root.geometry("1250x400")

# ---------------------------------------------------------------------------- #
#                               Global variables                               #
# ---------------------------------------------------------------------------- #


current_id  = 0 
actionStatu = "Add"


# Functions 
def clearForm():
    name_text.delete(1.0,END)
    model_text.delete(1.0,END)
    price_text.delete(1.0,END)
    price_is_dispo.delete(1.0,END)
    price_nbr_place.delete(1.0,END)
    return None

def addCar():
    name = name_text.get("1.0", END).strip()
    model = model_text.get("1.0", END).strip()
    price = price_text.get("1.0", END).strip()
    is_dispo = price_is_dispo.get("1.0", END).strip()
    nbr_place = price_nbr_place.get("1.0", END).strip()
    id = randint(1,1000)
    car = Car(id, price,name, model, is_dispo, nbr_place)
    car.save()
    print("Car saved successfully")
    
    clearForm()
    refreshTable()
def updateCar():
    #id = id_text.get("1.0", END).strip()
    name = name_text.get("1.0", END).strip()
    model = model_text.get("1.0", END).strip()
    price = price_text.get("1.0", END).strip()
    is_dispo = price_is_dispo.get("1.0", END).strip()
    nbr_place = price_nbr_place.get("1.0", END).strip()

    car = Car(current_id, price,name, model, is_dispo, nbr_place)
    car.update()
    car.display_info()
    global actionStatu
    actionStatu = 'Add'
    btnAction.config(text="Add",command=addCar)
    clearForm()
    refreshTable()
    return None

# defining the frame
frameRoot = Frame(root, 
              bd=5)


frameForm = LabelFrame(frameRoot,text="Form")

labelName = Label(frameForm,text="Name",height=1)
name_text  = Text(frameForm,
                    width=20,
                    height=1)

labelModel = Label(frameForm,text="Model",height=1,width=10,padx=0,pady=0)
model_text  = Text(frameForm,
                    width=20,
                    height=1)

labelPrice = Label(frameForm,text="Price",height=1,width=10,padx=0,pady=0)
price_text  = Text(frameForm,
                    width=20,
                    height=1)
labelDispo = Label(frameForm,text="Dispo",height=1,width=10,padx=0,pady=0)
price_is_dispo  = Text(frameForm,
                    width=20,
                    height=1)
labelNbrPlace = Label(frameForm,text="NbrPlace",height=1,width=10,padx=0,pady=0)
price_nbr_place  = Text(frameForm,
                    width=20,
                    height=1)
btnAction = Button(frameForm, 
             text="Add", 
             bg="#344560", 
             fg="#fff",
             command=addCar)

labelName.grid(column=0, row=0, padx=10, pady=10)
labelModel.grid(column=1, row=0, padx=10, pady=10)
labelPrice.grid(column=2, row=0, padx=10, pady=10)
labelDispo.grid(column=3, row=0, padx=10, pady=10)
labelNbrPlace.grid(column=4, row=0, padx=10, pady=10)

name_text.grid(column=0, row=1, padx=10, pady=10)
model_text.grid(column=1, row=1, padx=10, pady=10)
price_text.grid(column=2, row=1, padx=10, pady=10)
price_is_dispo.grid(column=3, row=1, padx=10, pady=10)
price_nbr_place.grid(column=4, row=1, padx=10, pady=10)
btnAction.grid(column=5, row=1, padx=10, pady=10)

# creating tabele 

table = Treeview(frameRoot,columns=('id','name','model','price','is_despo','nbr_place'),show="headings")
table.heading('id', text='id')
table.heading('name', text='Name')
table.heading('model', text='Model')
table.heading('price', text='Price')
table.heading('is_despo', text='Dispo')
table.heading('nbr_place', text='NbrPlace')

table.column('id',width=30,anchor='center')
table.column('name',anchor='center')
table.column('model',anchor='center')
table.column('price',anchor='center')
table.column('is_despo',anchor='center')
table.column('nbr_place',anchor='center')

def refreshTable():
    for item in table.get_children():
        table.delete(item)
    for car in Car.get_all():
        car.display_info()
        table.insert("", "end", values=(car.id, car.name, car.model, car.price, car.is_disponible, car.nbr_places))
refreshTable()
def delete_car():
    for i in table.selection():
        id = table.item(i)['values'][0]
        Car.delete(id)
    refreshTable()

def update_car():
    if len(table.selection()) >1:
        return None
    for i in table.selection():
        global current_id
        current_id = table.item(i)['values'][0]

        # name_text.insert(0,table.item(i)['values'][1])
        name_text.delete(1.0,END)
        name_text.insert(1.0,table.item(i)['values'][1])
        
        model_text.delete(1.0,END)
        model_text.insert(1.0,table.item(i)['values'][2])

        price_text.delete(1.0,END)
        price_text.insert(1.0,table.item(i)['values'][3])
        price_is_dispo.delete(1.0,END)
        price_is_dispo.insert(1.0,table.item(i)['values'][4])
        price_nbr_place.delete(1.0,END)
        price_nbr_place.insert(1.0,table.item(i)['values'][5])
        btnAction.config(text="Update",command=updateCar)
        global actionStatu
        actionStatu = 'Update'
    # Car.delete(id)

frameRoot.pack()
frameForm.grid(column=0, row=0, padx=10, pady=10)
table.grid(column=0, row=2, padx=10, pady=10)

frameAction = Frame(frameRoot,)
frameAction.grid(column=0, row=1, padx=10)

btnDelete = Button(frameAction,text="Delete",command=delete_car)
btnDelete.grid(column=0, row=1, padx=10, pady=10)

btnUpdate = Button(frameAction,text="Update",command=update_car)
btnUpdate.grid(column=1, row=1, padx=10, pady=10)

root.mainloop()


