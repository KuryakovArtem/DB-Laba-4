from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5 import *
import design
import connectUI
from DB import DB

class connectWindow(QtWidgets.QMainWindow, connectUI.Ui_Connect):
	 def __init__(self, dba):
	 	super().__init__()
	 	self.setupUi(self)
	 	self.dba = dba
	 def accept(self):
	 	try:
	 		self.dba.connectDB(self.host.text(), self.port.text(), self.login.text(), self.password.text(), self.name.text(), self.structure.text())
	 	except Exception as e:
	 		self.dba.errorMessage(str(e))
	 	self.close()
	 def reject(self):
	 	self.close()

class DBApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        self.db = None
        super().__init__()
        self.columnsAssortment = ['id', 'name', 'stock', 'price']
        self.columnsOrders = ['id', 'item', 'quantity', 'creation_time', 'last_modification_time']
        self.setupUi(self)
        self.w = connectWindow(self)
        self.actionConnect.triggered.connect(self.w.show)    
        self.tableWidgetAssortment.setColumnCount(4)
        self.tableWidgetAssortment.setHorizontalHeaderLabels(self.columnsAssortment)
        self.tableWidgetOrders.setColumnCount(5)
        self.tableWidgetOrders.setHorizontalHeaderLabels(self.columnsOrders)
        
    def connectDB(self, host, port, login, password, name, structureURL):
    	self.db = DB(host, port, login, password, name, structureURL)
    	print (self.db.getOrders())
    	self.setDataToTable(self.columnsAssortment, self.tableWidgetAssortment, self.db.getAssortment())
    	self.setDataToTable(self.columnsOrders, self.tableWidgetOrders, self.db.getOrders())
    
    def updateData(self, item):
        if not self.settingdata:
            try:
                newdata = self.tabledata[item.row()].copy()
                id = newdata['id']
                newdata[self.columns[item.column()]] = item.text()
                rewritedata = newdata.copy()
                self.db.editRecord(id, newdata)
            except None as error:
                self.errorMessage(str(error))
                self.setDataToTable(self.tabledata)
                return
            self.tabledata[item.row()] = rewritedata
            self.saved = False

    def setDataToTable(self, columns, table, data):
        self.tabledata = data
        self.settingdata = True
        table.setRowCount(len(data))
        for rownum, row in enumerate(data):
            for colnum, col in enumerate(columns):
                table.setItem(rownum, colnum, QTableWidgetItem(str(row[col])))
        self.settingdata = False


    def errorMessage(self, error):
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Critical)
        dialog.setText(error)
        dialog.addButton(QMessageBox.Ok)
        dialog.exec()

    def addRecord(self):
        id = self.id.text()
        price = self.price.text()
        amount = self.amount.text()
        name = self.name.text()
        if id.isnumeric() and price and amount and name:
            try:
                self.db.addRecord({"id": int(id), "name": name, "amount": amount, "price": price})
            except Exception as error:
                self.errorMessage(str(error))
        self.settingdata = True
        self.setDataToTable(self.db.getRecords())
        self.settingdata = False
        self.saved = False

    def search(self):
        text = self.nameSD.text()
        if not text:
            self.setDataToTable(self.db.getRecords())
            return
        try:
            self.setDataToTable(self.db.getRecordsByName(text))
        except Exception as error:
            self.errorMessage(str(error))

    def delByName(self):
        name = self.nameSD.text()
        try:
            self.db.delRecordsByName(name)
        except Exception as error:
            self.errorMessage(str(error))
        self.setDataToTable(self.db.getRecords())
        self.saved = False