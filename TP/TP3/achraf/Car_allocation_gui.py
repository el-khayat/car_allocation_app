# Form implementation generated from reading ui file 'C:\Users\Administrator\Desktop\ihm\car_allocation_app\TP\TP3\achraf\Car_allocation_gui.ui'
#
# Created by: PyQt6 UI code generator 6.6.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(851, 359)
        self.tabWidget = QtWidgets.QTabWidget(parent=Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 826, 335))
        self.tabWidget.setObjectName("tabWidget")
        self.allocation_part = QtWidgets.QWidget()
        self.allocation_part.setObjectName("allocation_part")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.allocation_part)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Button_update_allocation = QtWidgets.QPushButton(parent=self.allocation_part)
        self.Button_update_allocation.setObjectName("Button_update_allocation")
        self.gridLayout_3.addWidget(self.Button_update_allocation, 1, 0, 1, 1)
        self.Button_create_allocation = QtWidgets.QPushButton(parent=self.allocation_part)
        self.Button_create_allocation.setObjectName("Button_create_allocation")
        self.gridLayout_3.addWidget(self.Button_create_allocation, 0, 2, 1, 1)
        self.Button_delete_allocation = QtWidgets.QPushButton(parent=self.allocation_part)
        self.Button_delete_allocation.setObjectName("Button_delete_allocation")
        self.gridLayout_3.addWidget(self.Button_delete_allocation, 2, 2, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(3, 3, 11, 9)
        self.horizontalLayout.setSpacing(57)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Date = QtWidgets.QLabel(parent=self.allocation_part)
        self.Date.setObjectName("Date")
        self.horizontalLayout.addWidget(self.Date)
        self.Price = QtWidgets.QLabel(parent=self.allocation_part)
        self.Price.setObjectName("Price")
        self.horizontalLayout.addWidget(self.Price)
        self.Days = QtWidgets.QLabel(parent=self.allocation_part)
        self.Days.setObjectName("Days")
        self.horizontalLayout.addWidget(self.Days)
        self.Client_id = QtWidgets.QLabel(parent=self.allocation_part)
        self.Client_id.setObjectName("Client_id")
        self.horizontalLayout.addWidget(self.Client_id)
        self.Car_id = QtWidgets.QLabel(parent=self.allocation_part)
        self.Car_id.setObjectName("Car_id")
        self.horizontalLayout.addWidget(self.Car_id)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 6)
        self.line_client_id = QtWidgets.QLineEdit(parent=self.allocation_part)
        self.line_client_id.setObjectName("line_client_id")
        self.gridLayout.addWidget(self.line_client_id, 1, 3, 1, 1)
        self.line_car_id = QtWidgets.QLineEdit(parent=self.allocation_part)
        self.line_car_id.setObjectName("line_car_id")
        self.gridLayout.addWidget(self.line_car_id, 1, 5, 1, 1)
        self.line_date = QtWidgets.QLineEdit(parent=self.allocation_part)
        self.line_date.setObjectName("line_date")
        self.gridLayout.addWidget(self.line_date, 1, 0, 1, 1)
        self.line_days = QtWidgets.QLineEdit(parent=self.allocation_part)
        self.line_days.setObjectName("line_days")
        self.gridLayout.addWidget(self.line_days, 1, 2, 1, 1)
        self.line_price = QtWidgets.QLineEdit(parent=self.allocation_part)
        self.line_price.setObjectName("line_price")
        self.gridLayout.addWidget(self.line_price, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(parent=self.allocation_part)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.gridLayout_3.addWidget(self.tableWidget, 2, 0, 1, 1)
        self.tabWidget.addTab(self.allocation_part, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Button_update_allocation.setText(_translate("Form", "Update allocation"))
        self.Button_create_allocation.setText(_translate("Form", "Create allocation"))
        self.Button_delete_allocation.setText(_translate("Form", "Delete allocation"))
        self.Date.setText(_translate("Form", "Date :"))
        self.Price.setText(_translate("Form", "Price :"))
        self.Days.setText(_translate("Form", "Days :"))
        self.Client_id.setText(_translate("Form", "Client id :"))
        self.Car_id.setText(_translate("Form", "Car id :"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "ID ALLOCATION"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "DATE"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "PRICE"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "DAYS"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "CLIENT_ID"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "CAR_ID"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.allocation_part), _translate("Form", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Tab 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
