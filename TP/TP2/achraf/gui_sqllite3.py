import random
import sqlite3
import tkinter as tk
from tkinter import messagebox

class Allocation:
    def __init__(self, allocation_id, allocation_date, allocation_price, allocation_nbr_days, client_id, car_id):
        self.id = allocation_id
        self.date = allocation_date
        self.price = allocation_price
        self.nbr_days = allocation_nbr_days
        self.client_id = client_id
        self.car_id = car_id


        
    def save(self):
        try:
            conn = sqlite3.connect("TP/TP2/achraf/car_allocation.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO allocations (date, price, nbr_days, client_id, car_id) VALUES (?, ?, ?, ?, ?)",
                (self.date, self.price, self.nbr_days, self.client_id, self.car_id)
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def update(self):
        try:
            conn = sqlite3.connect("TP/TP2/achraf/car_allocation.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE allocations SET date=?, price=?, nbr_days=?, client_id=?, car_id=? WHERE id=?",
                (self.date, self.price, self.nbr_days, self.client_id, self.car_id, self.id)
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def delete(self):
        try:
            conn = sqlite3.connect("TP/TP2/achraf/car_allocation.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM allocations WHERE id=?", (self.id,))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    
            
        

class AllocationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Allocation Management")
        self.create_ui()

    def create_ui(self):
        labels = ["Date:", "Price:", "Days:", "Client ID:", "Car ID"]
        self.entries = []

        # Create a Listbox to display existing allocations
        self.allocation_listbox = tk.Listbox(self.root, width=100)
        self.allocation_listbox.grid(row=7, column=0, columnspan=len(labels))

        # Populate the Listbox with existing allocations
        self.populate_allocation_listbox()

        for i, label_text in enumerate(labels):
            tk.Label(self.root, text=label_text).grid(row=0, column=i)
            entry = tk.Entry(self.root)
            entry.grid(row=1, column=i)
            self.entries.append(entry)

        create_button = tk.Button(self.root, text="Create Allocation", command=self.create_allocation)
        create_button.grid(row=1, column=len(labels))

       # Create an input field for the allocation ID
        self.input_field = tk.Entry(self.root)
        self.input_field.grid(row=2, column=0)

        # Create an input field for the allocation ID
        self.input_field2 = tk.Entry(self.root)
        self.input_field2.grid(row=3, column=0)

        # Change the "Update Allocation" button to fetch and populate the allocation
        update_button1 = tk.Button(self.root, text="enter the id for the update", command=self.fetch_and_populate_allocation)
        update_button1.grid(row=2, column=len(labels) - 4)

        update_button2 = tk.Button(self.root, text="Update Allocation", command=self.update_allocation)
        update_button2.grid(row=2, column=len(labels))  # Move this button one column to the left

        # Inside the __init__ method of AllocationGUI class, after creating other fields
        self.delete_id_entry = tk.Entry(self.root)
        self.delete_id_entry.grid(row=4, column=1)  # Adjust the row and column as needed

        delete_button = tk.Button(self.root, text="Delete Allocation", command=self.delete_allocation)
        delete_button.grid(row=4, column=2)  # Adjust the row and column as needed

    def fetch_and_populate_allocation(self):
            allocation_id = self.input_field.get()
            
            try:
                allocation_id = int(allocation_id)

                # Get the allocation by ID
                allocation = self.get_allocation_by_id(allocation_id)

                if allocation:
                    # Populate the entry fields with the retrieved data
                    for i, entry in enumerate(self.entries):
                        entry.delete(0, tk.END)
                        entry.insert(0, allocation[i + 1])  # Skip the ID column from the database
                else:
                    messagebox.showinfo("Allocation Not Found", f"No allocation found with ID {allocation_id}")
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))



    def populate_allocation_listbox(self):
        try:
            conn = sqlite3.connect("TP/TP2/achraf/car_allocation.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM allocations")
            allocations = cursor.fetchall()
            conn.close()

            self.allocation_listbox.delete(0, tk.END)

            for allocation in allocations:
                self.allocation_listbox.insert(tk.END, f"ID: {allocation[0]}, Date: {allocation[1]}, Price: {allocation[2]}, Days: {allocation[3]}, Id client: {allocation[4]}, Id car: {allocation[5]}")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def create_allocation(self):
        # Gather user input from the GUI
        allocation_date = self.entries[0].get()
        allocation_price = self.entries[1].get()
        allocation_nbr_days = self.entries[2].get()
        client_id = self.entries[3].get()
        car_id = self.entries[4].get()

        try:
            allocation_price = float(allocation_price)
            allocation_nbr_days = int(allocation_nbr_days)
            client_id = int(client_id)
            car_id = int(car_id)

            new_allocation = Allocation(
                random.randint(1000, 100000),
                allocation_date,
                allocation_price,
                allocation_nbr_days,
                client_id,
                car_id,
            )

            new_allocation.save()

            # Display a success message to the user
            messagebox.showinfo("Success", "Allocation created and saved successfully.")
            self.populate_allocation_listbox()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

            
    def get_allocation_by_id(self, allocation_id):
        try:
            conn = sqlite3.connect("TP/TP2/achraf/car_allocation.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM allocations WHERE id=?", (allocation_id,))
            allocation = cursor.fetchone()
            conn.close()
            return allocation
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            return None




    def update_allocation(self):
        allocation_id = self.input_field.get()

        try:
            allocation_id = int(allocation_id)

            # Get the allocation by ID
            allocation_data = self.get_allocation_by_id(allocation_id)

            if allocation_data:
                # Create a new Allocation object using the fetched data
                allocation = Allocation(allocation_id, allocation_data[1], allocation_data[2], allocation_data[3], allocation_data[4], allocation_data[5])

                # Update the allocation object with the data from the entry fields
                for i, entry in enumerate(self.entries[1:]):  # Skip the ID column
                    value = entry.get()
                    # Assuming that the entries correspond to date, price, days, client_id, car_id
                    if i == 0:
                        allocation.date = value
                    elif i == 1:
                        allocation.price = float(value)
                    elif i == 2:
                        allocation.nbr_days = int(value)
                    elif i == 3:
                        allocation.client_id = int(value)
                    elif i == 4:
                        allocation.car_id = int(value)

                # Call the update method of the allocation object to update the database
                allocation.update()

                # Display a success message to the user
                messagebox.showinfo("Success", f"Allocation with ID {allocation_id} updated successfully.")
                self.populate_allocation_listbox()
            else:
                messagebox.showinfo("Allocation Not Found", f"No allocation found with ID {allocation_id}")
        except (ValueError, sqlite3.Error) as e:
            messagebox.showerror("Input Error", str(e))


    def delete_allocation(self):
        # Gather user input from the GUI
        allocation_id = self.delete_id_entry.get()

        try:
            allocation_id = int(allocation_id)

            # Delete the allocation with the given ID
            deleted_allocation = Allocation(allocation_id, "", 0, 0, 0, 0)
            deleted_allocation.delete()

            # Display a success message to the user
            messagebox.showinfo("Success", f"Allocation with ID {allocation_id} deleted successfully.")
            self.populate_allocation_listbox()
        except (ValueError, sqlite3.Error) as e:
            messagebox.showerror("Input Error", str(e))       

if __name__ == "__main__":
    root = tk.Tk()
    app = AllocationGUI(root)
    root.mainloop()
