#gui dep
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QLineEdit, QProgressBar,
            QMessageBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QMessageBox, QToolButton, QComboBox, QErrorMessage)
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import (QFile, QPoint, QRect, QSize,
        Qt, QProcess)
from PyQt5.QtGui import QIcon, QFont, QClipboard, QPixmap, QImage
import sys
import pafy, requests
from io import StringIO
from PIL import Image
#icon taskbar
try:
    from PyQt5.QtWinExtras import QtWin
    myappid = 'youtube.python.download.program'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)    
except ImportError:
    pass

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        UIFile = QtCore.QFile('main.ui')
        UIFile.open(QtCore.QFile.ReadOnly)
        uic.loadUi(UIFile, self)
        UIFile.close()


        #buttons
        self.Clear.clicked.connect(self.cmdClear)

        self.DlLoc.clicked.connect(self.cmdDlLoc)

        self.DLink.returnPressed.connect(self.cmdQuality)

        


        self.show()

    def cmdClear(self):
        self.DLink.clear()
        self.SaveLoc.clear()

    def cmdQuality(self):
        self.Quality.clear()
        self.url = self.DLink.text()
        self.Quality.clear()
        if not self.DLink.text() == "":
            error_dialog = QErrorMessage()
            error_dialog.showMessage('No text provided!')
            self.video = pafy.new(self.url)
            image = QImage()
            image.loadFromData(requests.get(self.video.bigthumbhd).content)
            self.thumb.setPixmap(QPixmap(image))
            self.streams = self.video.streams
            self.Qualist = []
            for i in self.streams: 
                self.Quality.addItem(str(i))
            
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Error!')

        

    def cmdDLink(self):
        print("Hello")

    def cmdDlLoc(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        fileName = dlg.getExistingDirectory()
        if fileName:
            self.SaveLoc.setText(fileName)
            self.OutFolder = fileName





app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('icons/yt.png'))
window = UI()
app.exec_()