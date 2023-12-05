import wx
import wx.grid
import sqlite3

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
            conn = sqlite3.connect("TP/TP4/achraf/car_allocation.db")
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
            conn = sqlite3.connect("TP/TP4/achraf/car_allocation.db")
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
            conn = sqlite3.connect("TP/TP4/achraf/car_allocation.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM allocations WHERE id=?", (self.id,))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            self.show_database_error(str(e))

    def show_database_error(self, error_message):
        dlg = wx.MessageDialog(None, error_message, "Database Error", wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()


class MyForm(wx.Frame):
    def __init__(self):
        super().__init__(None, wx.ID_ANY, "Car Allocation App", size=(600, 600))

        panel = wx.Panel(self)
        # self.tableWidget = wx.grid.Grid(panel)
         

        # Creating widgets
        self.Button_update_allocation = wx.Button(panel, label="Update allocation")
        self.Button_create_allocation = wx.Button(panel, label="Create allocation")
        self.Button_delete_allocation = wx.Button(panel, label="Delete allocation")

        self.Date = wx.StaticText(panel, label="Date:")
        self.Price = wx.StaticText(panel, label="Price:")
        self.Days = wx.StaticText(panel, label="Days:")
        self.Client_id = wx.StaticText(panel, label="Client id:")
        self.Car_id = wx.StaticText(panel, label="Car id:")

        self.line_date = wx.TextCtrl(panel)
        self.line_price = wx.TextCtrl(panel)
        self.line_days = wx.TextCtrl(panel)
        self.line_client_id = wx.TextCtrl(panel)
        self.line_car_id = wx.TextCtrl(panel)

        # Creating a grid
        self.tableWidget = wx.grid.Grid(panel)

        # Adding widgets to sizers
        sizer = wx.GridBagSizer(5, 5)

        sizer.Add(self.Button_create_allocation, pos=(0, 0))
        sizer.Add(self.Button_update_allocation, pos=(0, 1))
        sizer.Add(self.Button_delete_allocation, pos=(0, 2))

        grid = wx.FlexGridSizer(6, 2, 5, 5)
        grid.Add(self.Date, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.line_date)
        grid.Add(self.Price, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.line_price)
        grid.Add(self.Days, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.line_days)
        grid.Add(self.Client_id, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.line_client_id)
        grid.Add(self.Car_id, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.line_car_id)
        grid.Add((10, 10))  # Spacer

        sizer.Add(grid, pos=(1, 0), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(self.tableWidget, pos=(2, 0), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.create_allocation, self.Button_create_allocation)
        self.Bind(wx.EVT_BUTTON, self.update_allocation, self.Button_update_allocation)
        self.Bind(wx.EVT_BUTTON, self.delete_allocation, self.Button_delete_allocation)

        self.populate_table()

        self.Show()

    def create_allocation(self, event):
        # Get data from input fields
        date = self.line_date.GetValue()
        price = self.line_price.GetValue()
        days = self.line_days.GetValue()
        client_id = self.line_client_id.GetValue()
        car_id = self.line_car_id.GetValue()

        # Validate data (you may need to implement your validation logic)
        if not date or not price or not days or not client_id or not car_id:
            dlg = wx.MessageDialog(None, "All fields are required.", "Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        # Convert 'days' to an integer
        try:
            days = int(days)
        except ValueError:
            dlg = wx.MessageDialog(None, "Days must be a valid number.", "Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        allocation = Allocation(None, date, price, days, client_id, car_id)
        allocation.save()

        # Clear input fields after saving
        self.line_date.Clear()
        self.line_price.Clear()
        self.line_days.Clear()
        self.line_client_id.Clear()
        self.line_car_id.Clear()

            # Fetch the latest added allocation from the database
        try:
            conn = sqlite3.connect("TP/TP4/achraf/car_allocation.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, date, price, nbr_days, client_id, car_id FROM allocations ORDER BY id DESC LIMIT 1")
            new_allocation_data = cursor.fetchone()
            conn.close()

            # Append the new allocation data to the table
            if new_allocation_data:
                row_position = self.tableWidget.GetNumberRows()
                self.tableWidget.AppendRows(1)
                for col, value in enumerate(new_allocation_data):
                    self.tableWidget.SetCellValue(row_position, col, str(value))

        except sqlite3.Error as e:
            dlg = wx.MessageDialog(None, str(e), "Database Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def update_allocation(self, event):
        selected_row = self.tableWidget.GetSelectedRows()
        if not selected_row:
            dlg = wx.MessageDialog(None, "Please select a row to update.", "Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        allocation_id = int(self.tableWidget.GetCellValue(selected_row[0], 0))
        
        # Get data from input fields
        updated_date = self.line_date.GetValue()
        updated_price = self.line_price.GetValue()
        updated_days = self.line_days.GetValue()
        updated_client_id = self.line_client_id.GetValue()
        updated_car_id = self.line_car_id.GetValue()

        # Validate data (similar to the create_allocation method)
        # ...

        # Update the data in the database
        allocation = Allocation(allocation_id, updated_date, updated_price, updated_days, updated_client_id, updated_car_id)
        allocation.update()

        # Update the row in the table with the new data
        for col, value in enumerate([allocation_id, updated_date, updated_price, updated_days, updated_client_id, updated_car_id]):
            self.tableWidget.SetCellValue(selected_row[0], col, str(value))

        # Clear input fields after update
        self.line_date.Clear()
        self.line_price.Clear()
        self.line_days.Clear()
        self.line_client_id.Clear()
        self.line_car_id.Clear()



    def delete_allocation(self, event):
        selected_row = self.tableWidget.GetSelectedRows()
        if not selected_row:
            dlg = wx.MessageDialog(None, "Please select a row to delete.", "Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        allocation_id = int(self.tableWidget.GetCellValue(selected_row[0], 0))
        reply = wx.MessageBox("Are you sure you want to delete this allocation?", "Delete Allocation", wx.YES_NO | wx.ICON_QUESTION)
        if reply == wx.YES:
            allocation = Allocation(allocation_id, None, None, None, None, None)
            allocation.delete()

            self.tableWidget.DeleteRows(selected_row[0])
        
    def populate_table(self):
            try:
                conn = sqlite3.connect("TP/TP4/achraf/car_allocation.db")
                cursor = conn.cursor()
                cursor.execute("SELECT id, date, price, nbr_days, client_id, car_id FROM allocations")
                data = cursor.fetchall()
                conn.close()

                if self.tableWidget.GetNumberCols() == 0 and self.tableWidget.GetNumberRows() == 0:
                    self.tableWidget.CreateGrid(len(data), 6)
                    self.tableWidget.SetColLabelValue(0, "ID")
                    self.tableWidget.SetColLabelValue(1, "Date")
                    self.tableWidget.SetColLabelValue(2, "Price")
                    self.tableWidget.SetColLabelValue(3, "Days")
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
