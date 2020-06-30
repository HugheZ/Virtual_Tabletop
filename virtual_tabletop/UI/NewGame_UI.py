# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/NewGame.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_newGame(object):
    def setupUi(self, newGame):
        newGame.setObjectName("newGame")
        newGame.setWindowModality(QtCore.Qt.ApplicationModal)
        newGame.resize(300, 460)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(newGame.sizePolicy().hasHeightForWidth())
        newGame.setSizePolicy(sizePolicy)
        newGame.setMinimumSize(QtCore.QSize(300, 460))
        newGame.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(newGame)
        self.gridLayout.setObjectName("gridLayout")
        self.nameEdit = QtWidgets.QLineEdit(newGame)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 0, 1, 1, 4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        self.heightLabel = QtWidgets.QLabel(newGame)
        self.heightLabel.setObjectName("heightLabel")
        self.gridLayout.addWidget(self.heightLabel, 3, 2, 1, 1)
        self.hInchLabel = QtWidgets.QLabel(newGame)
        self.hInchLabel.setObjectName("hInchLabel")
        self.gridLayout.addWidget(self.hInchLabel, 3, 4, 1, 1)
        self.widthSpin = QtWidgets.QSpinBox(newGame)
        self.widthSpin.setObjectName("widthSpin")
        self.gridLayout.addWidget(self.widthSpin, 3, 3, 1, 1)
        self.wInchLabel = QtWidgets.QLabel(newGame)
        self.wInchLabel.setObjectName("wInchLabel")
        self.gridLayout.addWidget(self.wInchLabel, 2, 4, 1, 1)
        self.filesGroup = QtWidgets.QGroupBox(newGame)
        self.filesGroup.setObjectName("filesGroup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.filesGroup)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.previewUpload = QtWidgets.QToolButton(self.filesGroup)
        self.previewUpload.setObjectName("previewUpload")
        self.gridLayout_2.addWidget(self.previewUpload, 0, 2, 1, 1)
        self.BoardUpload = QtWidgets.QToolButton(self.filesGroup)
        self.BoardUpload.setObjectName("BoardUpload")
        self.gridLayout_2.addWidget(self.BoardUpload, 2, 2, 1, 1)
        self.boardImgSource = QtWidgets.QLineEdit(self.filesGroup)
        self.boardImgSource.setText("")
        self.boardImgSource.setReadOnly(True)
        self.boardImgSource.setObjectName("boardImgSource")
        self.gridLayout_2.addWidget(self.boardImgSource, 2, 1, 1, 1)
        self.previewImg = QtWidgets.QLabel(self.filesGroup)
        self.previewImg.setText("")
        self.previewImg.setPixmap(QtGui.QPixmap(":/icons/not-found.png"))
        self.previewImg.setScaledContents(True)
        self.previewImg.setObjectName("previewImg")
        self.gridLayout_2.addWidget(self.previewImg, 1, 0, 1, 3)
        self.boardImg = QtWidgets.QLabel(self.filesGroup)
        self.boardImg.setText("")
        self.boardImg.setPixmap(QtGui.QPixmap(":/icons/not-found.png"))
        self.boardImg.setScaledContents(True)
        self.boardImg.setObjectName("boardImg")
        self.gridLayout_2.addWidget(self.boardImg, 3, 0, 1, 3)
        self.requiredImg = QtWidgets.QLabel(self.filesGroup)
        self.requiredImg.setObjectName("requiredImg")
        self.gridLayout_2.addWidget(self.requiredImg, 2, 0, 1, 1)
        self.previewImgSource = QtWidgets.QLineEdit(self.filesGroup)
        self.previewImgSource.setText("")
        self.previewImgSource.setReadOnly(True)
        self.previewImgSource.setObjectName("previewImgSource")
        self.gridLayout_2.addWidget(self.previewImgSource, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.filesGroup, 4, 0, 1, 5)
        self.widthLabel = QtWidgets.QLabel(newGame)
        self.widthLabel.setObjectName("widthLabel")
        self.gridLayout.addWidget(self.widthLabel, 2, 2, 1, 1)
        self.dimensionsLabel = QtWidgets.QLabel(newGame)
        self.dimensionsLabel.setObjectName("dimensionsLabel")
        self.gridLayout.addWidget(self.dimensionsLabel, 2, 0, 1, 1)
        self.nameLabel = QtWidgets.QLabel(newGame)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.heightSpin = QtWidgets.QSpinBox(newGame)
        self.heightSpin.setObjectName("heightSpin")
        self.gridLayout.addWidget(self.heightSpin, 2, 3, 1, 1)
        self.dialogButtons = QtWidgets.QDialogButtonBox(newGame)
        self.dialogButtons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.dialogButtons.setCenterButtons(False)
        self.dialogButtons.setObjectName("dialogButtons")
        self.gridLayout.addWidget(self.dialogButtons, 5, 0, 1, 5)

        self.retranslateUi(newGame)
        QtCore.QMetaObject.connectSlotsByName(newGame)
        newGame.setTabOrder(self.nameEdit, self.heightSpin)
        newGame.setTabOrder(self.heightSpin, self.widthSpin)
        newGame.setTabOrder(self.widthSpin, self.previewImgSource)
        newGame.setTabOrder(self.previewImgSource, self.previewUpload)
        newGame.setTabOrder(self.previewUpload, self.boardImgSource)
        newGame.setTabOrder(self.boardImgSource, self.BoardUpload)

    def retranslateUi(self, newGame):
        _translate = QtCore.QCoreApplication.translate
        newGame.setWindowTitle(_translate("newGame", "New Game"))
        self.nameEdit.setPlaceholderText(_translate("newGame", "New Game"))
        self.heightLabel.setText(_translate("newGame", "Height"))
        self.hInchLabel.setText(_translate("newGame", "in."))
        self.wInchLabel.setText(_translate("newGame", "in."))
        self.filesGroup.setTitle(_translate("newGame", "Files"))
        self.previewUpload.setText(_translate("newGame", "..."))
        self.BoardUpload.setText(_translate("newGame", "..."))
        self.boardImgSource.setPlaceholderText(_translate("newGame", "Board Img. (*.png, *.jpg, *.gif)"))
        self.requiredImg.setText(_translate("newGame", "*"))
        self.previewImgSource.setPlaceholderText(_translate("newGame", "Preview Img. (*.png, *.jpg)"))
        self.widthLabel.setText(_translate("newGame", "Width"))
        self.dimensionsLabel.setText(_translate("newGame", "Dimensions"))
        self.nameLabel.setText(_translate("newGame", "Game Name"))
import resources_rc