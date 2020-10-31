#gui dep
from PyQt5 import uic
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QLineEdit,
            QProgressBar, QMessageBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel,
            QMessageBox, QToolButton, QComboBox, QErrorMessage, qApp)
from PyQt5.QtCore import (QFile, QPoint, QRect, QSize,
        Qt, QProcess, QThread, pyqtSignal, pyqtSlot, Q_ARG , Qt, QMetaObject, QObject)
from PyQt5.QtGui import QIcon, QFont, QClipboard, QPixmap, QImage
import pafy, requests, sys, os, youtube_dl
#icon taskbar
try:
    from PyQt5.QtWinExtras import QtWin
    myappid = 'youtube.python.download.program'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)    
except ImportError:
    pass
#pyinstaller
def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
  return os.path.join(os.path.abspath('.'), relative_path)

# Import .ui forms for the GUI using function resource_path()
yt_dl_gui = resource_path("main.ui")
yt_dl_icons = resource_path("./icons/yt.png")
#working dir and dldir
wd = os.getcwd()
tmp = ()
try: #make dir for downlaods
    os.mkdir(wd+'\\downloads\\')
    tmp = str(wd+"\\downloads\\")
except FileExistsError: #if folder already exists
    tmp = str(wd+"\\downloads\\")

#UI
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        UIFile = QFile(resource_path(yt_dl_gui))
        UIFile.open(QFile.ReadOnly)
        uic.loadUi(UIFile, self)
        UIFile.close()

        #buttons and bars
        self.Clear.clicked.connect(self.cmdClear)
        self.DlLoc.clicked.connect(self.cmdDlLoc)
        self.DLink.returnPressed.connect(self.MetaData)
        self.StartDl.clicked.connect(self.cmdDownload)
        self.ProgressBar.setMaximum(100)
        self.ProgressBar.setValue(0)
        self.SaveLoc.setText(tmp)
        self.actionExit.triggered.connect(qApp.quit)

        
        #Downloadthread
        self.downloader = DownLoader()
        thread = QThread(self)
        thread.start()
        self.downloader.progressChanged.connect(self.ProgressBar.setValue)
        self.downloader.finished.connect(self.on_finished)
        self.downloader.moveToThread(thread)

    @pyqtSlot()
    def on_finished(self):
        self.update_disables(False)


    @pyqtSlot()
    def cmdDownload(self):
        Yturl = self.DLink.text()
        if  self.SaveLoc.text() == "":
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Error")
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText('No save location provided!')
            error_dialog.exec_()
        elif self.DLink.text() =="":
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Error")
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText('No Downloadlink provided!')
            error_dialog.exec_()
        else:
            path = self.SaveLoc.text()
            video = pafy.new(Yturl)
            QMetaObject.invokeMethod(self.downloader, "start_download",
                Qt.QueuedConnection,
                Q_ARG(object, video),
                Q_ARG(str, path))
            self.update_disables(True)

    def update_disables(self, state):
        self.DLink.setDisabled(state)
        self.StartDl.setDisabled(state)

    def cmdClear(self):
        self.DLink.clear()
        self.SaveLoc.clear()
        self.VTitle.clear()
        image = QImage()
        self.thumb.setPixmap(QPixmap(image))
        self.ProgressBar.setValue(0)
        self.update_disables(False)

    def MetaData(self):
        self.url = self.DLink.text()
        self.VTitle.clear()
        image = QImage()
        self.thumb.setPixmap(QPixmap(image))
        if self.DLink.text() == "":
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Error")
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText('No Downloadlink provided!')
            error_dialog.exec_()
        else:
            self.video = pafy.new(self.url)
            self.VTitle.setText(self.video.title)
            image = QImage()
            image.loadFromData(requests.get(self.video.bigthumbhd).content)
            self.thumb.setPixmap(QPixmap(image))

    def cmdDlLoc(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        fileName = dlg.getExistingDirectory()
        if fileName:
            self.SaveLoc.setText(fileName)

class DownLoader(QObject):
    progressChanged = pyqtSignal(int)
    finished = pyqtSignal()

    @pyqtSlot(object, str)
    def start_download(self, video, path):
        try:
            bv = video.getbest()
            bv.download(filepath=path, quiet=False, callback=self.callback, meta=False, remux_audio=False)
        except OsError:
            pass

    def callback(self, total, recvd, ratio, rate, eta):
        val = int(ratio * 100)
        self.progressChanged.emit(val)
        if val == 100:
            self.finished.emit()



app = QApplication(sys.argv)
app.setWindowIcon(QIcon(resource_path(yt_dl_icons)))
window = UI()
window.show()
app.exec_()