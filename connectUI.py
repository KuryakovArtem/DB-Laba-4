# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Connect.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Connect(object):
    def setupUi(self, Connect):
        Connect.setObjectName("Connect")
        Connect.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Connect)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtWidgets.QWidget(Connect)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 40, 266, 161))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.host = QtWidgets.QLineEdit(self.layoutWidget)
        self.host.setObjectName("host")
        self.verticalLayout.addWidget(self.host)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.name = QtWidgets.QLineEdit(self.layoutWidget)
        self.name.setObjectName("name")
        self.verticalLayout.addWidget(self.name)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.port = QtWidgets.QLineEdit(self.layoutWidget)
        self.port.setObjectName("port")
        self.verticalLayout.addWidget(self.port)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.login = QtWidgets.QLineEdit(self.layoutWidget)
        self.login.setObjectName("login")
        self.verticalLayout_2.addWidget(self.login)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.password = QtWidgets.QLineEdit(self.layoutWidget)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.verticalLayout_2.addWidget(self.password)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.structure = QtWidgets.QLineEdit(self.layoutWidget)
        self.structure.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.structure.setObjectName("structure")
        self.verticalLayout_2.addWidget(self.structure)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Connect)
        self.buttonBox.accepted.connect(Connect.accept)
        self.buttonBox.rejected.connect(Connect.reject)
        QtCore.QMetaObject.connectSlotsByName(Connect)

    def retranslateUi(self, Connect):
        _translate = QtCore.QCoreApplication.translate
        Connect.setWindowTitle(_translate("Connect", "Connect"))
        self.label.setText(_translate("Connect", "Host"))
        self.host.setText(_translate("Connect", "localhost"))
        self.label_2.setText(_translate("Connect", "DB name"))
        self.name.setText(_translate("Connect", "Weed"))
        self.label_3.setText(_translate("Connect", "Port"))
        self.port.setText(_translate("Connect", "5432"))
        self.label_4.setText(_translate("Connect", "Login"))
        self.label_5.setText(_translate("Connect", "Password"))
        self.label_6.setText(_translate("Connect", "Structure URL (.sql)"))
        self.structure.setText(_translate("Connect", "https://raw.githubusercontent.com/SharagaFun/DB-Laba-4/master/structure.sql"))
