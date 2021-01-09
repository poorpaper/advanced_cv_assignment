# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI2.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QProgressBar, QVBoxLayout, QHBoxLayout


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1354, 741)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(820, 505, 510, 185))
        self.groupBox.setObjectName("groupBox")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(50, 30, 121, 16))
        self.checkBox.setObjectName("checkBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(50, 60, 181, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 90, 181, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(50, 120, 181, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(320, 30, 151, 121))
        self.pushButton_4.setObjectName("pushButton_4")
        self.screen1 = QtWidgets.QLabel(self.centralwidget)
        self.screen1.setGeometry(QtCore.QRect(20, 10, 640, 480))
        self.screen1.setObjectName("screen1")
        self.screen2 = QtWidgets.QLabel(self.centralwidget)
        self.screen2.setGeometry(QtCore.QRect(680, 10, 640, 480))
        self.screen2.setObjectName("screen2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(20, 510, 780, 180))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 778, 178))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.textLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.textLabel.setGeometry(QtCore.QRect(0, 0, 780, 180))
        self.textLabel.setObjectName("textLabel")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1354, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionCamera = QtWidgets.QAction(MainWindow)
        self.actionCamera.setObjectName("actionCamera")
        self.actionVideo = QtWidgets.QAction(MainWindow)
        self.actionVideo.setObjectName("actionVideo")
        self.actionPicture = QtWidgets.QAction(MainWindow)
        self.actionPicture.setObjectName("actionPicture")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        # self.actionKinect = QtWidgets.QAction(MainWindow)
        # self.actionKinect.setObjectName("actionKinect")
        self.actionPictures = QtWidgets.QAction(MainWindow)
        self.actionPictures.setObjectName("actionPictures")
        self.menuFile.addAction(self.actionCamera)
        self.menuFile.addAction(self.actionVideo)
        # self.menuFile.addAction(self.actionKinect)
        self.menuFile.addAction(self.actionPictures)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Options"))
        self.checkBox.setText(_translate("MainWindow", "Ouput Landmarks"))
        self.pushButton.setText(_translate("MainWindow", "Open Input Directory"))
        self.pushButton_2.setText(_translate("MainWindow", "Open Output Directory"))
        self.pushButton_3.setText(_translate("MainWindow", "Exit"))
        self.pushButton_4.setText(_translate("MainWindow", "No Input"))
        self.screen1.setText(_translate("MainWindow", "No Signal"))
        self.screen2.setText(_translate("MainWindow", "No Signal"))
        self.textLabel.setText(_translate("MainWindow", ""))
        self.menuFile.setTitle(_translate("MainWindow", "Input"))
        self.actionCamera.setText(_translate("MainWindow", "Camera"))
        self.actionVideo.setText(_translate("MainWindow", "Video"))
        # self.actionKinect.setText(_translate("MainWindow", "Kinect"))
        self.actionPictures.setText(_translate("MainWindow", "Pictures"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

        self.screen1.setAlignment(Qt.AlignCenter)
        self.screen2.setAlignment(Qt.AlignCenter)
        self.pushButton.setDisabled(True)
        self.pushButton_2.setDisabled(True)
        self.textLabel.setWordWrap(True)


class ProgressBar(QDialog):
    def __init__(self, fileIndex, filenum, parent=None):
        super(ProgressBar, self).__init__(parent)

        self.filenum = filenum

        self.resize(350, 100)
        self.setWindowTitle(self.tr("Processing progress"))
        self.TipLabel = QLabel(self.tr("Processing:" + "  " + str(fileIndex) + "/" + str(filenum)))
        self.FeatLabel = QLabel(self.tr("Extract feature:"))

        self.FeatProgressBar = QProgressBar(self)
        self.FeatProgressBar.setMinimum(0)
        self.FeatProgressBar.setMaximum(100)  # 总进程换算为100

        self.FeatProgressBar.setValue(0)  # 进度条初始值为0

        TipLayout = QHBoxLayout()
        TipLayout.addWidget(self.TipLabel)

        FeatLayout = QHBoxLayout()
        FeatLayout.addWidget(self.FeatLabel)
        FeatLayout.addWidget(self.FeatProgressBar)

        layout = QVBoxLayout()
        layout.addLayout(FeatLayout)
        layout.addLayout(TipLayout)

        self.setLayout(layout)
        self.show()

    def setValue(self, value):
        self.FeatProgressBar.setValue(value)

    def changeValue(self, value):
        self.FeatProgressBar.setValue(value * 100 / self.filenum)
        self.TipLabel.setText(self.tr("Processing:" + "  " + str(value) + "/" + str(self.filenum)))

    def onCancel(self, event):
        self.close()