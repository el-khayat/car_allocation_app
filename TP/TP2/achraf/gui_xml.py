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

        # Create and place an Entry widget for allocation ID
        self.id_input = tk.Entry(root)
        self.id_input.grid(row=2, column=1, padx=5, pady=5)
        
       # Create and place the "Update Allocation" button
        update_button = tk.Button(self.root, text="choose the id of the update", command=self.update_allocation)
        update_button.grid(row=2, column=0, padx=5, pady=5)


        self.text_input = tk.Entry(root)
        self.text_input.grid(row=4, column=0, padx=5, pady=5)

        self.update_button = tk.Button(self.root, text="Update", command=self.update_allocation)
        self.update_button.grid(row=2, column=0, columnspan=len(labels))

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
        # Get the ID entered by the user
        allocation_id = self.id_input.get()

        # Load the XML file
        tree = ET.parse("TP/TP2/achraf/allocations.xml")
        root = tree.getroot()

        # Find the allocation with the matching ID
        for allocation in root.findall("allocation"):
            id_element = allocation.find("id")
            if id_element.text == allocation_id:
                # Populate the input fields with existing data
                self.entries[0].delete(0, tk.END)  # Clear the current content
                self.entries[0].insert(0, allocation.find("date").text)
                self.entries[1].delete(0, tk.END)
                self.entries[1].insert(0, allocation.find("price").text)
                self.entries[2].delete(0, tk.END)
                self.entries[2].insert(0, allocation.find("nbr_days").text)
                self.entries[3].delete(0, tk.END)
                self.entries[3].insert(0, allocation.find("client_id").text)
                self.entries[4].delete(0, tk.END)
                self.entries[4].insert(0, allocation.find("car_id").text)
                
                # Update the "Update" button to save changes
                self.update_button.config(command=self.save_updated_allocation)

                # Optionally, provide a message to indicate the data has been loaded
                print(f"Allocation with ID {allocation_id} loaded for editing.")
                break
        else:
            print(f"Allocation with ID {allocation_id} not found.")

    def save_updated_allocation(self):
        # Get the ID entered by the user
        allocation_id = self.id_input.get()

        # Load the XML file
        tree = ET.parse("TP/TP2/achraf/allocations.xml")
        root = tree.getroot()

        # Find the allocation with the matching ID
        for allocation in root.findall("allocation"):
            id_element = allocation.find("id")
            if id_element.text == allocation_id:
                # Update the allocation data based on user input
                allocation.find("date").text = self.entries[0].get()
                allocation.find("price").text = self.entries[1].get()
                allocation.find("nbr_days").text = self.entries[2].get()
                allocation.find("client_id").text = self.entries[3].get()
                allocation.find("car_id").text = self.entries[4].get()

                # Save the modified XML back to the file
                tree.write("TP/TP2/achraf/allocations.xml")
                self.display_allocation_list()
                # Update the "Update" button to its original function
                self.update_button.config(command=self.update_allocation)
                # Optionally, provide a confirmation to the user
                print(f"Allocation with ID {allocation_id} has been updated.")
                break
        else:
            print(f"Allocation with ID {allocation_id} not found.")



    def delete_allocation(self):
        allocation_id = self.text_input.get()
        if not allocation_id:
            return

        tree = ET.parse("TP/TP2/achraf/allocations.xml")
        root = tree.getroot()

        for allocation in root.findall("allocation"):
            if allocation.find("id").text == allocation_id:
                root.remove(allocation)

        tree.write("TP/TP2/achraf/allocations.xml")

        # Refresh the listbox to display the updated data
        self.display_allocation_list()


    def display_allocation_list(self):
            # Function to display XML data in a listbox
            allocations = self.read_xml_file("TP/TP2/achraf/allocations.xml")  # Provide the path to your XML file
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



    @staticmethod
    def read_xml_file(xml_file):
        # Function to read the XML file and extract allocations
        xml_file = "TP/TP2/achraf/allocations.xml"
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