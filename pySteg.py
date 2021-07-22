# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
import stegAPP
from PIL import Image
import random
import os

class Ui_MainWindow(object):
    def __init__(self): #reset defaults
        self.message = ""
        self.maxchars = 0

        self.encodingEncode = "s"
        self.encodingDecode = "s"

        self.choseimage = False
        self.enteredtext = False

        self.imagepath = None

    def resetDefaults(self):
        self.buttonEncode.setEnabled(False)
        self.buttonDecode.setEnabled(False)

    def askOpenImageEncode(self):
        picturesdir = os.path.expanduser('~') + "\\Pictures"
        self.imagepath = QtWidgets.QFileDialog.getOpenFileName(caption='Select Input Image',directory=picturesdir,filter='Image Files (*.png *.jpg)')[0]
        pixmap = QPixmap(self.imagepath)
        self.imageDisplayEncode.setPixmap(pixmap.scaled(self.imageDisplayEncode.size(), QtCore.Qt.KeepAspectRatio))
        self.choseimage = True

        self.maxchars = self.calculateMaxCharacters(self.encodingEncode)
        print(self.maxchars)

        self.updateEncode()

    def getMessage(self):
        self.message = self.msgInputBox.toPlainText()


    def updateEncode(self):
        if self.choseimage and self.enteredtext:
            self.buttonEncode.setEnabled(True)
        else:
            self.buttonEncode.setEnabled(False)

        optionindex = self.encodingDropdownEncode.currentIndex()

        bitsperchar = ["8 BpC","6 BpC"]
        descriptions = ["Allows the standard set of characters","Allows only 0-9, a-z A-Z, and a period"]

        self.encodingDiscriptionEncode.setText(descriptions[optionindex])
        self.encodingValueEncode.setText(bitsperchar[optionindex])

        self.encodingEncode = "sb"[self.encodingDropdownEncode.currentIndex()]

        # Fetch os directory.
        path = self.imagepath if self.imagepath != None else ""

        path = path.rsplit('/', 1)[-1]

        self.displayImagePathEncode.setText(path)



    def enterText(self):
        if self.msgInputBox.toPlainText() == "":
            self.enteredtext = False
        else:
            self.enteredtext = True

        self.updateEncode()

    def setEncodingProgressbar(self,percent):
        self.progressBarEncoding.setProperty("value", percent)

    def encode(self):
        self.getMessage()


        self.setEncodingProgressbar(random.randrange(30))

        if len(self.message) > self.maxchars:
            self.raiseImageFull()
            return

        try:
            stegAPP.steganography(self.imagepath, self.message, self.encodingEncode)
        except stegAPP.IllegalCharacter:
            self.raiseIllegalCharacter()


        self.setEncodingProgressbar(100)

        self.msgInputBox.clear()


    # D E C O D E

    def updateDecode(self):
        if self.choseimage:
            self.buttonDecode.setEnabled(True)
        else:
            self.buttonDecode.setEnabled(False)
        optionindex = self.encodingDropdownDecode.currentIndex()

        bitsperchar = ["8 BpC","6 BpC"]
        descriptions = ["Allows the standard set of characters","Allows only 0-9, a-z A-Z, and a period"]

        self.encodingDiscriptionDecode.setText(descriptions[optionindex])
        self.encodingValueDecode.setText(bitsperchar[optionindex])

        self.encodingDecode = "sb"[self.encodingDropdownDecode.currentIndex()]

        # Fetch os directory.
        path = self.imagepath if self.imagepath != None else ""

        path = path.rsplit('/', 1)[-1]

        self.displayImagePathDecode.setText(path)

    def askOpenImageDecode(self):
        picturesdir = os.path.expanduser('~') + "\\Pictures"
        self.imagepath = QtWidgets.QFileDialog.getOpenFileName(caption='Select Input Image',directory=picturesdir,filter='Image Files (*.png *.jpg)')[0]
        pixmap = QPixmap(self.imagepath)
        self.imageDisplayDecode.setPixmap(pixmap.scaled(self.imageDisplayDecode.size(), QtCore.Qt.KeepAspectRatio))
        self.choseimage = True

        self.updateDecode()

    def setDecodingProgressbar(self,percent):
        self.progressBarDecoding.setProperty("value", percent)

    def decode(self):

        self.setDecodingProgressbar(random.randrange(30))

        try:
            message = stegAPP.readImage(self.imagepath, self.encodingDecode)
        except stegAPP.NoMessage:
            self.raiseNoMessage()

        self.setDecodingProgressbar(100)

        self.textDisplay.setPlainText(message)

    # C O M M O N

    def calculateMaxCharacters(self,encoding):
        """Returns the maximum characters allowed for the input image selected."""
        try:
            img = Image.open(self.imagepath)
            x, y = img.size
            if encoding == "s":
                return 3*x*y//4
            elif encoding == "b":
                return x*y
        except:
            pass



    def raiseIllegalCharacter(self):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Illegal Character")
        msgbox.setText("An illegal character was used. Try to use the standard encoding option if this error persists.")
        msgbox.setInformativeText("pySteg currently only supports the english alphabet with standard ASCII characterset.")
        msgbox.setIcon(QtWidgets.QMessageBox.Critical)
        msgbox.exec_()

    def raiseNoMessage(self):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("No Message")
        msgbox.setText("The input image chosen contains no message generated by pySteg OR the encoding option selected is not the encoding option that was found in the image file.")
        msgbox.setInformativeText("Try the other encoding option. If it does not return an output, the image contains no message generated by pySteg.")
        msgbox.setIcon(QtWidgets.QMessageBox.Information)
        msgbox.exec_()

    def raiseImageFull(self):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Message is too large")
        msgbox.setText("The input image is not large enough to contain the message.")
        msgbox.setInformativeText("The operation has been stopped.")
        msgbox.setIcon(QtWidgets.QMessageBox.Information)
        msgbox.exec_()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(703, 320)
        MainWindow.setMinimumSize(QtCore.QSize(703, 320))
        MainWindow.setMaximumSize(QtCore.QSize(703, 320))
        font = QtGui.QFont()
        font.setPointSize(9)
        MainWindow.setFont(font)
        MainWindow.setMouseTracking(False)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setAnimated(True)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        print(os.getcwd())
        MainWindow.setWindowIcon(QIcon("icon.png"))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        # E N C O D E

        self.encodeDecodeTab = QtWidgets.QTabWidget(self.centralwidget)
        self.encodeDecodeTab.setGeometry(QtCore.QRect(10, 10, 685, 288))
        self.encodeDecodeTab.setObjectName("encodeDecodeTab")

        self.encodeTab = QtWidgets.QWidget()
        self.encodeTab.setObjectName("encodeTab")

        self.msgInputBox = QtWidgets.QPlainTextEdit(self.encodeTab)
        self.msgInputBox.setGeometry(QtCore.QRect(420, 10, 251, 119))
        self.msgInputBox.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.msgInputBox.setObjectName("msgInputBox")
        self.msgInputBox.textChanged.connect(self.enterText)

        self.buttonEncode = QtWidgets.QPushButton(self.encodeTab)
        self.buttonEncode.setGeometry(QtCore.QRect(520, 180, 151, 41))
        self.buttonEncode.setObjectName("buttonEncode")
        self.buttonEncode.clicked.connect(self.encode)

        self.encodingValueEncode = QtWidgets.QLabel(self.encodeTab)
        self.encodingValueEncode.setGeometry(QtCore.QRect(520, 140, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.encodingValueEncode.setFont(font)
        self.encodingValueEncode.setObjectName("encodingValueEncode")

        self.imageDisplayEncode = QtWidgets.QLabel(self.encodeTab)
        self.imageDisplayEncode.setGeometry(QtCore.QRect(10, 10, 391, 210))
        self.imageDisplayEncode.setFrameShape(QtWidgets.QFrame.Box)
        self.imageDisplayEncode.setText("")
        self.imageDisplayEncode.setObjectName("imageDisplayEncode")
        self.imageDisplayEncode.setAlignment(QtCore.Qt.AlignCenter)

        self.encodingDropdownEncode = QtWidgets.QComboBox(self.encodeTab)
        self.encodingDropdownEncode.setGeometry(QtCore.QRect(420, 140, 91, 31))
        self.encodingDropdownEncode.setObjectName("encodingDropdownEncode")
        self.encodingDropdownEncode.addItem("")
        self.encodingDropdownEncode.addItem("")
        self.encodingDropdownEncode.currentTextChanged.connect(self.updateEncode)

        self.progressBarEncoding = QtWidgets.QProgressBar(self.encodeTab)
        self.progressBarEncoding.setGeometry(QtCore.QRect(10, 230, 661, 21))
        self.progressBarEncoding.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBarEncoding.setProperty("value", 0)
        self.progressBarEncoding.setInvertedAppearance(False)
        self.progressBarEncoding.setObjectName("progressBarEncoding")

        self.encodingDiscriptionEncode = QtWidgets.QLabel(self.encodeTab)
        self.encodingDiscriptionEncode.setGeometry(QtCore.QRect(560, 140, 111, 31))
        self.encodingDiscriptionEncode.setWordWrap(True)
        self.encodingDiscriptionEncode.setObjectName("encodingDiscriptionEncode")

        self.selectImageEncode = QtWidgets.QPushButton(self.encodeTab)
        self.selectImageEncode.setGeometry(QtCore.QRect(420, 180, 91, 41))
        self.selectImageEncode.setObjectName("selectImageEncode")
        self.selectImageEncode.clicked.connect(self.askOpenImageEncode)

        self.encodeDecodeTab.addTab(self.encodeTab, "")


        # D E C O D E

        self.decodeTab = QtWidgets.QWidget()
        self.decodeTab.setObjectName("decodeTab")

        self.imageDisplayDecode = QtWidgets.QLabel(self.decodeTab)
        self.imageDisplayDecode.setGeometry(QtCore.QRect(10, 10, 391, 210))
        self.imageDisplayDecode.setFrameShape(QtWidgets.QFrame.Box)
        self.imageDisplayDecode.setText("")
        self.imageDisplayDecode.setObjectName("imageDisplayDecode")
        self.imageDisplayDecode.setAlignment(QtCore.Qt.AlignCenter)

        self.encodingDropdownDecode = QtWidgets.QComboBox(self.decodeTab)
        self.encodingDropdownDecode.setGeometry(QtCore.QRect(420, 10, 91, 31))
        self.encodingDropdownDecode.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.encodingDropdownDecode.setAcceptDrops(False)
        self.encodingDropdownDecode.setObjectName("encodingDropdownDecode")
        self.encodingDropdownDecode.addItem("")
        self.encodingDropdownDecode.addItem("")
        self.encodingDropdownDecode.currentTextChanged.connect(self.updateDecode)

        self.encodingValueDecode = QtWidgets.QLabel(self.decodeTab)
        self.encodingValueDecode.setGeometry(QtCore.QRect(520, 10, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.encodingValueDecode.setFont(font)
        self.encodingValueDecode.setObjectName("encodingValueDecode")

        self.encodingDiscriptionDecode = QtWidgets.QLabel(self.decodeTab)
        self.encodingDiscriptionDecode.setGeometry(QtCore.QRect(560, 10, 111, 31))
        self.encodingDiscriptionDecode.setWordWrap(True)
        self.encodingDiscriptionDecode.setObjectName("encodingDiscriptionDecode")

        self.buttonDecode = QtWidgets.QPushButton(self.decodeTab)
        self.buttonDecode.setGeometry(QtCore.QRect(520, 50, 151, 41))
        self.buttonDecode.setObjectName("buttonDecode")
        self.buttonDecode.clicked.connect(self.decode)

        self.progressBarDecoding = QtWidgets.QProgressBar(self.decodeTab)
        self.progressBarDecoding.setGeometry(QtCore.QRect(10, 230, 661, 21))
        self.progressBarDecoding.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBarDecoding.setProperty("value", 0)
        self.progressBarDecoding.setInvertedAppearance(False)
        self.progressBarDecoding.setObjectName("progressBarDecoding")

        self.textDisplay = QtWidgets.QTextBrowser(self.decodeTab)
        self.textDisplay.setGeometry(QtCore.QRect(420, 100, 251, 119))
        self.textDisplay.setObjectName("textDisplay")

        self.selectImageDecode = QtWidgets.QPushButton(self.decodeTab)
        self.selectImageDecode.setGeometry(QtCore.QRect(420, 50, 91, 41))
        self.selectImageDecode.setObjectName("selectImageDecode")
        self.selectImageDecode.clicked.connect(self.askOpenImageDecode)

        self.encodeDecodeTab.addTab(self.decodeTab, "")


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 703, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.displayImagePathDecode = QtWidgets.QLabel(self.decodeTab)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.displayImagePathDecode.setFont(font)
        self.displayImagePathDecode.setGeometry(QtCore.QRect(14, 202, 384, 14))
        self.displayImagePathDecode.setObjectName("displayImagePathDecode")

        self.displayImagePathEncode = QtWidgets.QLabel(self.encodeTab)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.displayImagePathEncode.setFont(font)
        self.displayImagePathEncode.setGeometry(QtCore.QRect(14, 202, 384, 14))
        self.displayImagePathEncode.setObjectName("displayImagePathEncode")





        self.retranslateUi(MainWindow)
        self.encodeDecodeTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.resetDefaults()



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "pySteg"))
        self.buttonEncode.setText(_translate("MainWindow", "Encode"))
        self.encodingValueEncode.setText(_translate("MainWindow", "8 BpC"))
        self.encodingDropdownEncode.setItemText(0, _translate("MainWindow", "Standard"))
        self.encodingDropdownEncode.setItemText(1, _translate("MainWindow", "Compact"))
        self.encodingDiscriptionEncode.setText(_translate("MainWindow", "Allows the standard set of characters"))
        self.selectImageEncode.setText(_translate("MainWindow", "Select Image"))
        self.encodeDecodeTab.setTabText(self.encodeDecodeTab.indexOf(self.encodeTab), _translate("MainWindow", "Encode"))
        self.encodingDropdownDecode.setItemText(0, _translate("MainWindow", "Standard"))
        self.encodingDropdownDecode.setItemText(1, _translate("MainWindow", "Compact"))
        self.encodingValueDecode.setText(_translate("MainWindow", "8 BpC"))
        self.encodingDiscriptionDecode.setText(_translate("MainWindow", "Allows the standard set of characters"))
        self.buttonDecode.setText(_translate("MainWindow", "Decode"))
        self.selectImageDecode.setText(_translate("MainWindow", "Select Image"))
        self.encodeDecodeTab.setTabText(self.encodeDecodeTab.indexOf(self.decodeTab), _translate("MainWindow", "Decode"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
