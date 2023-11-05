import sys
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox
import sqlite3 
from Car_allocation_gui import Ui_Form  # Import your generated UI class

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
            conn = sqlite3.connect("TP/TP3/achraf/car_allocation.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO allocations (date, price, nbr_days, client_id, car_id) VALUES (?, ?, ?, ?, ?)",
                (self.date, self.price, self.nbr_days, self.client_id, self.car_id)
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            self.show_database_error(str(e))

    def update(self):
        try:
            conn = sqlite3.connect("TP/TP3/achraf/car_allocation.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE allocations SET date=?, price=?, nbr_days=?, client_id=?, car_id=? WHERE id=?",
                (self.date, self.price, self.nbr_days, self.client_id, self.car_id, self.id)
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            self.show_database_error(str(e))

    def delete(self):
        try:
            conn = sqlite3.connect("TP/TP3/achraf/car_allocation.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM allocations WHERE id=?", (self.id,))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            self.show_database_error(str(e))

    def show_database_error(self, error_message):
        QMessageBox.critical(None, "Database Error", error_message)

class MyForm(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Initialize the UI
        # Connect the "Create Allocation" button to the create_allocation method
        self.Button_create_allocation.clicked.connect(self.create_allocation)
        # Connect the "Update Allocation" button to the update_allocation method
        self.Button_update_allocation.clicked.connect(self.update_allocation)

        # Initialize a variable to store the selected allocation ID for updating
        self.selected_allocation_id = None

        self.Button_delete_allocation.clicked.connect(self.delete_allocation)

        # Populate the table with data
        self.populate_table()

    def create_allocation(self):
        # Get data from input fields
        date = self.line_date.text()
        price = self.line_price.text()
        days = self.line_days.text()
        client_id = self.line_client_id.text()
        car_id = self.line_car_id.text()

        # Validate data (you may need to implement your validation logic)
        if not date or not price or not days or not client_id or not car_id:
            QMessageBox.critical(self, "Error", "All fields are required.")
            return

        # Check if an allocation ID is selected for updating
        if self.selected_allocation_id is not None:
            # Update the existing allocation
            allocation = Allocation(self.selected_allocation_id, date, price, days, client_id, car_id)
            allocation.update()
            # Clear the selected allocation ID
            self.selected_allocation_id = None
        else:
            # Create a new Allocation object and save it
            allocation = Allocation(None, date, price, days, client_id, car_id)
            allocation.save()

        # Clear input fields after saving or updating
        self.line_date.clear()
        self.line_price.clear()
        self.line_days.clear()
        self.line_client_id.clear()
        self.line_car_id.clear()

        # Populate the table with updated data
        self.populate_table()


        
    def update_allocation(self):
        # Check if a row is selected in the table
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.critical(self, "Error", "Please select a row to update.")
            return

        # Get the data from the selected row
        allocation_id = self.tableWidget.item(selected_row, 0).text()
        date = self.tableWidget.item(selected_row, 1).text()
        price = self.tableWidget.item(selected_row, 2).text()
        days = self.tableWidget.item(selected_row, 3).text()
        client_id = self.tableWidget.item(selected_row, 4).text()
        car_id = self.tableWidget.item(selected_row, 5).text()

        # Update the input fields with the selected data for editing
        self.line_date.setText(date)
        self.line_price.setText(price)
        self.line_days.setText(days)
        self.line_client_id.setText(client_id)
        self.line_car_id.setText(car_id)

        # Set the selected allocation ID for updating
        self.selected_allocation_id = allocation_id



    def delete_allocation(self):
        # Check if a row is selected in the table
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.critical(self, "Error", "Please select a row to delete.")
            return

        # Get the allocation ID from the selected row
        allocation_id = int(self.tableWidget.item(selected_row, 0).text())

        # Ask for confirmation before deleting
        reply = QMessageBox.question(self, "Delete Allocation", "Are you sure you want to delete this allocation?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # Delete the allocation from the database
            allocation = Allocation(allocation_id, None, None, None, None, None)
            allocation.delete()

            # Remove the selected row from the table
            self.tableWidget.removeRow(selected_row)
       

    def populate_table(self):
            try:
                conn = sqlite3.connect("TP/TP3/achraf/car_allocation.db")
                cursor = conn.cursor()
                cursor.execute("SELECT id, date, price, nbr_days, client_id, car_id FROM allocations")
                data = cursor.fetchall()
                conn.close()

                self.tableWidget.setRowCount(len(data))
                self.tableWidget.setColumnCount(6)  # Assuming you want to display 6 columns

                for row, row_data in enumerate(data):
                    for col, col_data in enumerate(row_data):
                        item = QTableWidgetItem(str(col_data))
                        self.tableWidget.setItem(row, col, item)

            except sqlite3.Error as e:
                self.show_database_error(str(e))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    form.populate_table()
    form.update_allocation
    sys.exit(app.exec())
