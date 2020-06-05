from PyQt5.QtCore import *
from PyQt5.QtGui import *
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

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.accept()

    def accept(self):
        try:
            self.dba.connectDB(self.host.text(), self.port.text(),
                               self.login.text(), self.password.text(),
                               self.name.text(), self.structure.text())
            self.close()
        except Exception as e:
            self.dba.errorMessage(str(e))

    def reject(self):
        self.close()


class DBApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        self.db = None
        super().__init__()
        self.columnsAssortment = ['id', 'name', 'stock', 'price']
        self.columnsOrders = [
            'id', 'item', 'quantity', 'creation_time', 'last_modification_time'
        ]
        self.setupUi(self)
        self.w = connectWindow(self)
        self.actionConnect.triggered.connect(self.w.show)
        self.addButtonAssortment.clicked.connect(self.addRecordToAssortment)
        self.addButtonOrders.clicked.connect(self.addRecordToOrders)
        self.deleteButtonAssortment.clicked.connect(self.delAssortmentByName)
        self.deleteButtonOrders.clicked.connect(self.delOrders)
        self.searchButtonAssortment.clicked.connect(self.search)
        self.tableWidgetAssortment.itemChanged.connect(self.updateDataAssortment)
        self.tableWidgetAssortment.setColumnCount(4)
        self.tableWidgetAssortment.setHorizontalHeaderLabels(
            self.columnsAssortment)
        self.tableWidgetOrders.setColumnCount(5)
        self.tableWidgetOrders.setHorizontalHeaderLabels(self.columnsOrders)
        self.tabledataAssortment = None
        self.tabledataOrders = None

    def connectDB(self, host, port, login, password, name, structureURL):
        self.db = DB(host, port, login, password, name, structureURL)
        print(self.db.getOrders())
        try:
            self.tabledataAssortment = self.db.getAssortment()
            self.setDataToTable(self.columnsAssortment,
                                self.tableWidgetAssortment,
                                self.tabledataAssortment)
            self.tabledataOrders = self.db.getOrders()
            self.setDataToTable(self.columnsOrders, self.tableWidgetOrders,
                                self.tabledataOrders)
        except Exception as e:
            self.errorMessage(str(e))

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
        if data is None or len(data) == 0:
            table.setRowCount(0)
            return
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

    def addRecordToAssortment(self):
        if self.db is None:
            self.errorMessage("The database is not connected")
            return
        if len(self.nameAssortment.text()) == 0 or len(
                self.stockAssortment.text()) == 0 or len(
                    self.priceAssortment.text()) == 0:
            self.errorMessage("Not all fields are filled in")
        else:
            try:
                self.db.addItem(self.nameAssortment.text(),
                                self.stockAssortment.text(),
                                self.priceAssortment.text())
                self.tabledataAssortment = self.db.getAssortment()
                self.setDataToTable(self.columnsAssortment,
                                    self.tableWidgetAssortment,
                                    self.tabledataAssortment)
            except Exception as e:
                self.errorMessage(str(e))

    def addRecordToOrders(self):
        if self.db is None:
            self.errorMessage("The database is not connected")
            return
        if len(self.ItemOrders.text()) == 0 or len(
                self.QuantityOrders.text()) == 0:
            self.errorMessage("Not all fields are filled in")
        else:
            try:
                self.db.addOrder(self.ItemOrders.text(),
                                 self.QuantityOrders.text())
                self.tabledataOrders = self.db.getOrders()
                self.setDataToTable(self.columnsOrders, self.tableWidgetOrders,
                                    self.tabledataOrders)
            except Exception as e:
                self.errorMessage(str(e))

    def search(self):
        if self.db is None:
            self.errorMessage("The database is not connected")
            return
        text = self.nameSAssortment.text()
        if not text:
            self.tabledataAssortment = self.db.getAssortment()
            self.setDataToTable(self.columnsAssortment,
                                    self.tableWidgetAssortment,
                                    self.tabledataAssortment)
            return
        try:
            self.tabledataAssortment = self.db.search(text)
            self.setDataToTable(self.columnsAssortment,
                                    self.tableWidgetAssortment,
                                    self.tabledataAssortment)
        except Exception as e:
            self.errorMessage(str(e))

    def delAssortmentByName(self):
        if self.db is None:
            self.errorMessage("The database is not connected")
            return
        name = self.nameSAssortment.text()
        if (len(name)>0):
            try:
                self.db.deleteByName(name)
                self.tabledataAssortment = self.db.getAssortment()
                self.setDataToTable(self.columnsAssortment,
                                    self.tableWidgetAssortment,
                                    self.tabledataAssortment)
            except Exception as e:
                self.errorMessage(str(e))
            self.saved = False
        else:
            self.delAssortment()

    def delAssortment(self):
        try:
            for i in self.tableWidgetAssortment.selectedIndexes():
                print(self.tabledataAssortment)
                self.db.deleteItem(self.tabledataAssortment[i.row()]['id'])
                self.tabledataAssortment = self.db.getAssortment()
                self.setDataToTable(self.columnsAssortment,
                                    self.tableWidgetAssortment,
                                    self.tabledataAssortment)
        except Exception as e:
            self.errorMessage(str(e))

    def delOrders(self):
        if self.db is None:
            self.errorMessage("The database is not connected")
            return
        try:
            for i in self.tableWidgetOrders.selectedIndexes():
                print(self.tabledataOrders)
                self.db.deleteOrder(self.tabledataOrders[i.row()]['id'])
                self.tabledataOrders = self.db.getOrders()
                self.setDataToTable(self.columnsOrders, self.tableWidgetOrders,
                                    self.tabledataOrders)
        except Exception as e:
            self.errorMessage(str(e))
            
            
    def updateDataAssortment(self, item):
    	if not self.settingdata:
    		if item.column() == 1:
    			self.db.updateItemName(self.tabledataAssortment[item.row()]['id'], item.text())