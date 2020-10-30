#gui dep
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QLineEdit, QProgressBar,
            QMessageBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QMessageBox, QToolButton, QComboBox, QErrorMessage)
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import (QFile, QPoint, QRect, QSize,
        Qt, QProcess, QThread, pyqtSignal)
from PyQt5.QtGui import QIcon, QFont, QClipboard, QPixmap, QImage
import sys
import pafy, requests
#icon taskbar

try:
    from PyQt5.QtWinExtras import QtWin
    myappid = 'youtube.python.download.program'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)    
except ImportError:
    pass
class Worker(QThread):
    _signal = pyqtSignal(int)
    def __init__(self):
        super(Worker, self).__init__()

    def run(self, total, recvd, ratio, rate, eta):
        worker = Worker()
        worker._signal.emit(ratio)

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

        self.StartDl.clicked.connect(self.cmdDownload)
        self.ProgressBar.setMaximum(1.0)
        self.SaveLoc.setText('/tmp')

        self.show()

    #def progress(self, total, recvd, ratio, rate, eta):
        #self.ProgressBar.setValue(ratio)
    def signal_accept(self, msg):
        self.ProgressBar.setValue(int(msg))

    def cmdClear(self):
        self.DLink.clear()
        self.SaveLoc.clear()
        self.VTitle.clear()
        image = QImage()
        self.thumb.setPixmap(QPixmap(image))
        self.ProgressBar.setValue(0.0)

    def cmdQuality(self):
        self.url = self.DLink.text()
        self.VTitle.clear()
        image = QImage()
        self.thumb.setPixmap(QPixmap(image))
        if not self.DLink.text() == "":
            error_dialog = QErrorMessage()
            error_dialog.showMessage('No text provided!')
            self.video = pafy.new(self.url)
            self.VTitle.setText(self.video.title)
            image = QImage()
            image.loadFromData(requests.get(self.video.bigthumbhd).content)
            self.thumb.setPixmap(QPixmap(image))

        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Error!')


    def cmdDownload(self):
        path = self.SaveLoc.text()
        url = self.DLink.text()
        worker = Worker()
        progress = worker._signal.connect(self.signal_accept)     
        if  self.SaveLoc.text() == "":
            error_dialog = QErrorMessage()
            error_dialog.showMessage('No save location provided!')
        else:
            video = pafy.new(url)
            bs = video.getbest()
            bs.download(filepath=path, quiet=False, callback=worker.start(), meta=False, remux_audio=False)


    def cmdDlLoc(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        fileName = dlg.getExistingDirectory()
        if fileName:
            self.SaveLoc.setText(fileName)





app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('icons/yt.png'))
window = UI()
app.exec_()