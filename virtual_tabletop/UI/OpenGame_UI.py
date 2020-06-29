# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/OpenGame.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_openGame(object):
    def setupUi(self, openGame):
        openGame.setObjectName("openGame")
        openGame.resize(300, 32)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(openGame.sizePolicy().hasHeightForWidth())
        openGame.setSizePolicy(sizePolicy)
        openGame.setMaximumSize(QtCore.QSize(300, 16777215))
        self.horizontalLayout = QtWidgets.QHBoxLayout(openGame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gameName = QtWidgets.QLabel(openGame)
        self.gameName.setObjectName("gameName")
        self.horizontalLayout.addWidget(self.gameName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeButton = QtWidgets.QPushButton(openGame)
        self.closeButton.setMaximumSize(QtCore.QSize(20, 16777215))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)

        self.retranslateUi(openGame)
        QtCore.QMetaObject.connectSlotsByName(openGame)

    def retranslateUi(self, openGame):
        _translate = QtCore.QCoreApplication.translate
        openGame.setWindowTitle(_translate("openGame", "Form"))
        self.gameName.setText(_translate("openGame", "NAME"))
        self.closeButton.setText(_translate("openGame", "X"))
