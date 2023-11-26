import wx
import wx.grid
import sqlite3

path_to_db = "TP/TP4/mohamed/car_allocation.db"

conn = sqlite3.connect(path_to_db)
cursor = conn.cursor()

# Define the tables and schema

cursor.execute(
    """
    DROP TABLE IF EXISTS cars;
    """
)
cursor.execute(
    """

    CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    model TEXT NOT NULL,
    price REAL NOT NULL,
    is_disponible INTEGER NOT NULL,
    nbr_places INTEGER NOT NULL
    )
"""
)
cursor.execute(
    """
    INSERT INTO cars (name, model, price, is_disponible, nbr_places) VALUES ('BMW', 'X6', 1000, 1, 5),('DACIA', '2019', 1000, 1, 6),('BMW', 'X6', 1000, 1, 3)
    """
)
# Save changes and close the connection
conn.commit()
conn.close()
class Car:
    def __init__(self, car_id, name, model, price, is_disponible, nbr_places):
        self.id = car_id
        self.name = name
        self.model = model
        self.price = price
        self.is_disponible = is_disponible
        self.nbr_places = nbr_places

    def display_info(self):
        print(
            f"Car ID: {self.id},name: {self.name}, Model: {self.model},Price: ${self.price}, Available: {'Yes' if self.is_disponible else 'No'}, Number of Places: {self.nbr_places},"
        )

    def save(self):
        conn = sqlite3.connect(path_to_db)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cars (name, model, price, is_disponible, nbr_places) VALUES (?, ?, ?, ?, ?)",
            (self.name, self.model, self.price, self.is_disponible, self.nbr_places),
        )
        print("Car saved successfully.")
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    def update(self):
        conn = sqlite3.connect(path_to_db)
        cursor = conn.cursor()
        print("updating... : (insite)",self.id)
        cursor.execute(
            "UPDATE cars SET name=?, model=?, price=?, is_disponible=?, nbr_places=? WHERE id=?",
            (
                self.name,
                self.model,
                self.price,
                self.is_disponible,
                self.nbr_places,
                self.id,
            ),
        )
        conn.commit()
        conn.close()
    @staticmethod
    def delete(car_id):
        conn = sqlite3.connect(path_to_db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE id=?", (car_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect(path_to_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars")
        cars = cursor.fetchall()
        conn.close()
        return [Car(*car) for car in cars]

    @staticmethod
    def get_one(car_id):
        conn = sqlite3.connect(path_to_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars WHERE id=?", (car_id,))
        car = cursor.fetchone()
        conn.close()
        if car:
            return Car(*car)
        else:
            return None

    def show_database_error(self, error_message):
        dlg = wx.MessageDialog(None, error_message, "Database Error", wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()


class MyForm(wx.Frame):
    def __init__(self):
        super().__init__(None, wx.ID_ANY, "Car car App", size=(600, 600))

        panel = wx.Panel(self)
        # self.tableWidget = wx.grid.Grid(panel)
         

        # Creating widgets
        self.Button_update_car = wx.Button(panel, label="Update car")
        self.Button_create_car = wx.Button(panel, label="Create car")
        self.Button_delete_car = wx.Button(panel, label="Delete car")

        self.name = wx.StaticText(panel, label="name:")
        self.Model = wx.StaticText(panel, label="Model:")
        self.Price = wx.StaticText(panel, label="Price:")
        self.is_dispo = wx.StaticText(panel, label="Is Dispo:")
        self.Nbr_place = wx.StaticText(panel, label="number palces:")

        self.line_name = wx.TextCtrl(panel)
        self.line_price = wx.TextCtrl(panel)
        self.line_model = wx.TextCtrl(panel)
        self.line_is_dispo = wx.TextCtrl(panel)
        self.line_nbr_place = wx.TextCtrl(panel)

        # Creating a grid
        self.tableWidget = wx.grid.Grid(panel)

        # Adding widgets to sizers
        sizer = wx.GridBagSizer(5, 5)

        sizer.Add(self.Button_create_car, pos=(0, 0))
        sizer.Add(self.Button_update_car, pos=(0, 1))
        sizer.Add(self.Button_delete_car, pos=(0, 2))

        grid = wx.FlexGridSizer(6, 2, 5, 5)
        grid.Add(self.name, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.line_name)
        grid.Add(self.Price, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.line_price)
        grid.Add(self.Model, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.line_model)
        grid.Add(self.is_dispo, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.line_is_dispo)
        grid.Add(self.Nbr_place, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.line_nbr_place)
        grid.Add((10, 10))  # Spacer

        sizer.Add(grid, pos=(1, 0), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(self.tableWidget, pos=(2, 0), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.create_car, self.Button_create_car)
        self.Bind(wx.EVT_BUTTON, self.update_car, self.Button_update_car)
        self.Bind(wx.EVT_BUTTON, self.delete_car, self.Button_delete_car)

        self.populate_table()

        self.Show()

    def create_car(self, event):
        # Get data from input fields
        model = self.line_name.GetValue()
        price = self.line_price.GetValue()
        days = self.line_model.GetValue()
        client_id = self.line_is_dispo.GetValue()
        car_id = self.line_nbr_place.GetValue()

        # Validate data (you may need to implement your validation logic)
        if not model or not price or not days or not client_id or not car_id:
            dlg = wx.MessageDialog(None, "All fields are required.", "Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        # Convert 'days' to an integer
        try:
            days = int(days)
        except ValueError:
            dlg = wx.MessageDialog(None, "Model must be a valid number.", "Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        car = Car(None, model, price, days, client_id, car_id)
        car.save()

        # Clear input fields after saving
        self.line_name.Clear()
        self.line_price.Clear()
        self.line_model.Clear()
        self.line_is_dispo.Clear()
        self.line_nbr_place.Clear()

        # Populate the table with updated data
        self.populate_table()


    def update_car(self, event):
        selected_row = self.tableWidget.GetSelectedRows()
        if not selected_row:
            dlg = wx.MessageDialog(None, "Please select a row to update.", "Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        car_id = int(self.tableWidget.GetCellValue(selected_row[0], 0))
        
        # Get data from input fields
        updated_date = self.line_name.GetValue()
        updated_price = self.line_price.GetValue()
        updated_days = self.line_model.GetValue()
        updated_client_id = self.line_is_dispo.GetValue()
        updated_car_id = self.line_nbr_place.GetValue()

        # Validate data (similar to the create_car method)
        # ...

        # Update the data in the database
        car = Car(car_id, updated_date, updated_price, updated_days, updated_client_id, updated_car_id)
        car.update()

        # Update the row in the table with the new data
        for col, value in enumerate([car_id, updated_date, updated_price, updated_days, updated_client_id, updated_car_id]):
            self.tableWidget.SetCellValue(selected_row[0], col, str(value))

        # Clear input fields after update
        self.line_name.Clear()
        self.line_price.Clear()
        self.line_model.Clear()
        self.line_is_dispo.Clear()
        self.line_nbr_place.Clear()



    def delete_car(self, event):
        selected_row = self.tableWidget.GetSelectedRows()
        if not selected_row:
            dlg = wx.MessageDialog(None, "Please select a row to delete.", "Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        car_id = int(self.tableWidget.GetCellValue(selected_row[0], 0))
        reply = wx.MessageBox("Are you sure you want to delete this car?", "Delete car", wx.YES_NO | wx.ICON_QUESTION)
        if reply == wx.YES:
            car = Car(car_id, None, None, None, None, None)
            car.delete()

            self.tableWidget.DeleteRows(selected_row[0])
        
    def populate_table(self):
            try:
                conn = sqlite3.connect(path_to_db)
                cursor = conn.cursor()
                cursor.execute("SELECT id,name, model, price, is_disponible, nbr_places FROM cars")
                data = cursor.fetchall()
                conn.close()
                num_cols = self.tableWidget.GetNumberCols()
                num_rows = self.tableWidget.GetNumberRows()
                if self.tableWidget.GetNumberCols() > 0 :
                    # self.tableWidget.DeleteCols(0, num_cols)
                    self.tableWidget.DeleteRows(0, num_rows)

                # # Delete all columns

                if True:
                # if self.tableWidget.GetNumberCols() == 0 and self.tableWidget.GetNumberRows() == 0 or 1==1:
                    self.tableWidget.CreateGrid(len(data), 6)
                    self.tableWidget.SetColLabelValue(0, "ID")
                    self.tableWidget.SetColLabelValue(1, "name")
                    self.tableWidget.SetColLabelValue(2, "Price")
                    self.tableWidget.SetColLabelValue(3, "Model")
                    self.tableWidget.SetColLabelValue(4, "Client ID")
                    self.tableWidget.SetColLabelValue(5, "Car ID")

                    for row, row_data in enumerate(data):
                        for col, col_data in enumerate(row_data):
                            self.tableWidget.SetCellValue(row, col, str(col_data))

            except sqlite3.Error as e:
                dlg = wx.MessageDialog(None, str(e), "Database Error", wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()



if __name__ == "__main__":
    app = wx.App()
    form = MyForm()
    app.MainLoop()
