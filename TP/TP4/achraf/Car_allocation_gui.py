import wx
import wx.grid

class MyForm(wx.Frame):
    def __init__(self):
        super().__init__(None, wx.ID_ANY, "Car Allocation App", size=(851, 359))

        panel = wx.Panel(self)

        self.tabWidget = wx.Notebook(panel)
        self.allocation_part = wx.Panel(self.tabWidget)

        # Creating widgets
        self.Button_update_allocation = wx.Button(self.allocation_part, label="Update allocation")
        self.Button_create_allocation = wx.Button(self.allocation_part, label="Create allocation")
        self.Button_delete_allocation = wx.Button(self.allocation_part, label="Delete allocation")

        self.Date = wx.StaticText(self.allocation_part, label="Date:")
        self.Price = wx.StaticText(self.allocation_part, label="Price:")
        self.Days = wx.StaticText(self.allocation_part, label="Days:")
        self.Client_id = wx.StaticText(self.allocation_part, label="Client id:")
        self.Car_id = wx.StaticText(self.allocation_part, label="Car id:")

        self.line_date = wx.TextCtrl(self.allocation_part)
        self.line_price = wx.TextCtrl(self.allocation_part)
        self.line_days = wx.TextCtrl(self.allocation_part)
        self.line_client_id = wx.TextCtrl(self.allocation_part)
        self.line_car_id = wx.TextCtrl(self.allocation_part)

        # Creating a grid
        self.tableWidget = wx.grid.Grid(self.allocation_part)

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

        self.allocation_part.SetSizer(sizer)

        self.tabWidget.AddPage(self.allocation_part, "Tab 1")
        self.tab_2 = wx.Panel(self.tabWidget)
        self.tabWidget.AddPage(self.tab_2, "Tab 2")

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(self.tabWidget, 1, wx.EXPAND)
        panel.SetSizer(sizer_main)

        self.Show()

if __name__ == "__main__":
    app = wx.App()
    form = MyForm()
    app.MainLoop()
