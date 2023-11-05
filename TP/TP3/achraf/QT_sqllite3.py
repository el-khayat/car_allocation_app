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

        # Create an Allocation object and save it
        allocation = Allocation(None, date, price, days, client_id, car_id)
        allocation.save()

        # Clear input fields after saving
        self.line_date.clear()
        self.line_price.clear()
        self.line_days.clear()
        self.line_client_id.clear()
        self.line_car_id.clear()


        
    @pyqtSlot(QTableWidgetItem)
    def update_allocation(self, item):
        row = item.row()
        col = item.column()
        new_value = item.text()

        if col == 0:  # Assuming the first column is "id" and should not be changed
            return

        allocation_id = self.tableWidget.item(row, 0).text()  # Get the allocation_id from the first column

        try:
            conn = sqlite3.connect("TP/TP3/achraf/car_allocation.db")
            cursor = conn.cursor()

            if col == 1:
                # Update the 'date' column
                cursor.execute("UPDATE allocations SET date=? WHERE id=?", (new_value, allocation_id))
            elif col == 2:
                # Update the 'price' column
                cursor.execute("UPDATE allocations SET price=? WHERE id=?", (new_value, allocation_id))
            elif col == 3:
                # Update the 'nbr_days' column
                cursor.execute("UPDATE allocations SET nbr_days=? WHERE id=?", (new_value, allocation_id))
            elif col == 4:
                # Update the 'client_id' column
                cursor.execute("UPDATE allocations SET client_id=? WHERE id=?", (new_value, allocation_id))
            elif col == 5:
                # Update the 'car_id' column
                cursor.execute("UPDATE allocations SET car_id=? WHERE id=?", (new_value, allocation_id))

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            self.show_database_error(str(e))

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
    form.populate_table()  # Call the populate_table method to display data
    sys.exit(app.exec())
