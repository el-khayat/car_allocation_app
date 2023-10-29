import random
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import messagebox
from script_xml import Allocation

class AllocationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Allocation Management")

        self.create_ui()
        self.display_allocation_list()
        
        self.create_ui()


    
        
    def create_ui(self):
        # Labels and Entry fields arranged horizontally
        labels = ["Date:", "Price:", "Days:", "Client ID:", "Car ID:"]
        self.entries = []

        for i, label_text in enumerate(labels):
            tk.Label(self.root, text=label_text).grid(row=0, column=i)
            entry = tk.Entry(self.root)
            entry.grid(row=1, column=i)
            self.entries.append(entry)

        # Button placement in a separate column
        create_button = tk.Button(self.root, text="Create Allocation", command=self.create_allocation)
        create_button.grid(row=1, column=len(labels))  # Place in the column after "Car ID"

        update_button = tk.Button(self.root, text="Update Allocation", command=self.update_allocation)
        update_button.grid(row=3, columnspan=len(labels))

        delete_button = tk.Button(self.root, text="Delete Allocation", command=self.delete_allocation)
        delete_button.grid(row=4, columnspan=len(labels))


    def create_allocation(self):
        # Gather user input from the GUI
        allocation_date = self.entries[0].get()
        allocation_price = self.entries[1].get()
        allocation_nbr_days = self.entries[2].get()
        client_id = self.entries[3].get()
        car_id = self.entries[4].get()

        try:
            # Convert the input to the appropriate data types
            allocation_price = float(allocation_price)
            allocation_nbr_days = int(allocation_nbr_days)
            client_id = int(client_id)
            car_id = int(car_id)

            # Create a new Allocation instance
            new_allocation = Allocation(
                random.randint(1000, 100000),
                allocation_date,
                allocation_price,
                allocation_nbr_days,
                client_id,
                car_id,
            )

            # Save the allocation to an XML file
            new_allocation.save_to_xml("TP/TP2/achraf/allocations.xml")

            # Refresh the listbox to display the updated data
            self.display_allocation_list()

            print("Allocation created and saved successfully.")
        except Exception as e:
            print(f"Error: {e}") 

    def update_allocation(self):
        # Implement the update logic
        pass
        
    def delete_allocation(self):
        # Implement the delete logic
        pass

    def display_allocation_list(self):
            # Function to display XML data in a listbox
            allocations = self.read_xml_file("allocations.xml")  # Provide the path to your XML file
            if allocations:
                listbox = tk.Listbox(self.root)
                listbox.grid(row=5, column=0, columnspan=5, sticky='nsew')

                for allocation in allocations:
                    listbox.insert(tk.END, f"ID: {allocation['id']}, Date: {allocation['date']}, Price: {allocation['price']}, nb days: {allocation['nbr_days']}, id client: {allocation['client_id']}, id car: {allocation['car_id']}")

                # Add a scrollbar
                scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL)
                scrollbar.grid(row=5, column=5, sticky='ns')
                listbox.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=listbox.yview)


    xml_file = "TP/TP2/achraf/allocations.xml"
    @staticmethod
    def read_xml_file(xml_file):
        # Function to read the XML file and extract allocations
        allocations = []
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for allocation in root.findall('allocation'):
            allocation_data = {}
            for element in allocation:
                allocation_data[element.tag] = element.text
            allocations.append(allocation_data)
        return allocations

if __name__ == "__main__":
    root = tk.Tk()
    app = AllocationGUI(root)
    root.mainloop()