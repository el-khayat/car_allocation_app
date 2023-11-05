import xml.etree.ElementTree as ET

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
