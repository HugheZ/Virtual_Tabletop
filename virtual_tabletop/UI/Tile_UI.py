# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/Tile.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Tile(object):
    def setupUi(self, Tile):
        Tile.setObjectName("Tile")
        Tile.resize(150, 150)
        Tile.setMaximumSize(QtCore.QSize(150, 150))
        self.gridLayout = QtWidgets.QGridLayout(Tile)
        self.gridLayout.setObjectName("gridLayout")
        self.loadButton = QtWidgets.QPushButton(Tile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadButton.sizePolicy().hasHeightForWidth())
        self.loadButton.setSizePolicy(sizePolicy)
        self.loadButton.setMaximumSize(QtCore.QSize(16777215, 20))
        self.loadButton.setObjectName("loadButton")
        self.gridLayout.addWidget(self.loadButton, 2, 0, 1, 4)
        self.gameImage = QtWidgets.QLabel(Tile)
        self.gameImage.setText("")
        self.gameImage.setPixmap(QtGui.QPixmap(":/icons/not-found.png"))
        self.gameImage.setScaledContents(True)
        self.gameImage.setObjectName("gameImage")
        self.gridLayout.addWidget(self.gameImage, 1, 0, 1, 4)
        self.cloudAvailable = QtWidgets.QLabel(Tile)
        self.cloudAvailable.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cloudAvailable.sizePolicy().hasHeightForWidth())
        self.cloudAvailable.setSizePolicy(sizePolicy)
        self.cloudAvailable.setMaximumSize(QtCore.QSize(20, 20))
        self.cloudAvailable.setText("")
        self.cloudAvailable.setPixmap(QtGui.QPixmap(":/icons/stored-cloud.png"))
        self.cloudAvailable.setScaledContents(True)
        self.cloudAvailable.setObjectName("cloudAvailable")
        self.gridLayout.addWidget(self.cloudAvailable, 3, 2, 1, 1)
        self.localAvailable = QtWidgets.QLabel(Tile)
        self.localAvailable.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.localAvailable.sizePolicy().hasHeightForWidth())
        self.localAvailable.setSizePolicy(sizePolicy)
        self.localAvailable.setMaximumSize(QtCore.QSize(20, 20))
        self.localAvailable.setText("")
        self.localAvailable.setPixmap(QtGui.QPixmap(":/icons/stored-local.png"))
        self.localAvailable.setScaledContents(True)
        self.localAvailable.setObjectName("localAvailable")
        self.gridLayout.addWidget(self.localAvailable, 3, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.availableLabel = QtWidgets.QLabel(Tile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.availableLabel.sizePolicy().hasHeightForWidth())
        self.availableLabel.setSizePolicy(sizePolicy)
        self.availableLabel.setObjectName("availableLabel")
        self.gridLayout.addWidget(self.availableLabel, 3, 1, 1, 1)
        self.gameName = QtWidgets.QLabel(Tile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gameName.sizePolicy().hasHeightForWidth())
        self.gameName.setSizePolicy(sizePolicy)
        self.gameName.setMaximumSize(QtCore.QSize(16777215, 10))
        self.gameName.setAlignment(QtCore.Qt.AlignCenter)
        self.gameName.setObjectName("gameName")
        self.gridLayout.addWidget(self.gameName, 0, 0, 1, 4)

        self.retranslateUi(Tile)
        QtCore.QMetaObject.connectSlotsByName(Tile)

    def retranslateUi(self, Tile):
        _translate = QtCore.QCoreApplication.translate
        Tile.setWindowTitle(_translate("Tile", "Tile"))
        self.loadButton.setText(_translate("Tile", "Load Game"))
        self.availableLabel.setText(_translate("Tile", "Available:"))
        self.gameName.setText(_translate("Tile", "Game Name"))
import resources_rc
