#gui dep
from PyQt5 import uic
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QLineEdit,
            QProgressBar, QMessageBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel,
            QMessageBox, qApp, QStatusBar)
from PyQt5.QtCore import (QFile, QPoint, QRect, QSize,
        Qt, QProcess, QThread, pyqtSignal, pyqtSlot, Q_ARG , Qt, QMetaObject, QObject)
from PyQt5.QtGui import (QIcon, QPixmap, QImage)
import requests, sys, os, youtube_dl
from pytube import YouTube
from pytube.exceptions import *
from os.path import expanduser
from easysettings import EasySettings
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
yt_dl_gui = resource_path("gui.ui")
yt_dl_icons = resource_path("./icons/yt_bl.png")
userfold = expanduser("~")
config = EasySettings(userfold+"./yt_dl.conf")
wd = os.getcwd()
tmp = None

try:
    tmp = config.get("dlFolder")
    if tmp == "":
        tmp = (userfold+'\\downloads\\')
        config.set("dlFolder", str(tmp))
        config.save()
except Exception:
    tmp = config.get("dlFolder")


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
        self.DFolder.clicked.connect(self.cmdopenDL)
        self.SaveLoc.setText(tmp)
        self.statusBar().showMessage("Ready!")
        self.progress_bar = QProgressBar()
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

        
        #Downloadthread
        self.downloader = DownLoader()
        thread = QThread(self)
        thread.start()
        self.downloader.finished.connect(self.on_finished)
        self.downloader.statusmessage.connect(self.statusBar().showMessage)
        self.downloader.progress.connect(self.progress_bar.setValue)
        self.downloader.moveToThread(thread)

    def messageBox(self, type, message):
        error_dialog = QMessageBox()
        error_dialog.setWindowTitle(type)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.exec_()

    @pyqtSlot()
    def on_finished(self):
        self.update_disables(False)
        self.progress_bar.hide()

    @pyqtSlot()
    def cmdDownload(self):
        Yturl = self.DLink.text()
        if  self.SaveLoc.text() == "":
            self.messageBox('Error!','No save location provided!')
        elif self.DLink.text() =="":
            self.messageBox('Error!','No YouTube link or ID provided!')
        else:
            path = self.SaveLoc.text()
            QMetaObject.invokeMethod(self.downloader, "start_download",
                Qt.QueuedConnection,
                Q_ARG(object, Yturl),
                Q_ARG(str, path))
            self.update_disables(True)
            self.progress_bar.show()

    def update_disables(self, state):
        self.DLink.setDisabled(state)
        self.StartDl.setDisabled(state)
        self.progress_bar.setValue(0)

    def cmdClear(self):
        self.DLink.clear()
        self.VTitle.clear()
        image = QImage()
        self.thumb.setPixmap(QPixmap(image))
        self.update_disables(False)
        self.progress_bar.hide()

    def MetaData(self):
        self.url = self.DLink.text()
        self.VTitle.clear()
        image = QImage()
        self.thumb.setPixmap(QPixmap(image))
        if self.DLink.text() == "":
            self.messageBox('Error!','No YouTube link or ID provided!')
        else:
            try:
                self.video = YouTube(self.url)
                self.VTitle.setText(self.video.title)
                image = QPixmap()
                image.loadFromData(requests.get(self.video.thumbnail_url).content)
                scaled = image.scaled(768,432,Qt.KeepAspectRatio)
                self.thumb.setPixmap(scaled)
                self.statusBar().showMessage("Metadata loaded!")
            except OSError:
                pass
            except ValueError:
                pass


    def cmdDlLoc(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        fileName = dlg.getExistingDirectory()
        dlf = config.get("dlFolder")
        if fileName:
            self.SaveLoc.setText(fileName)
            config.set("dlFolder",str(fileName))
            config.save()

    def cmdopenDL(self):
        os.startfile(self.SaveLoc.text())



class DownLoader(QObject):
    finished = pyqtSignal()
    statusmessage = pyqtSignal(str)
    progress = pyqtSignal(int)

    @pyqtSlot(object, str)
    def start_download(self, url, path):
        try:
            yt = YouTube(url,on_progress_callback=self.on_progress)
            yt = yt.streams.get_highest_resolution()
            self.statusmessage.emit("Download Started!")
        except AgeRestrictedError:
            self.statusmessage.emit("Error!")
            pass
        except:
            self.statusmessage.emit("Error!")
            self.finished.emit()
        else:
            yt.download(output_path=path)
            self.statusmessage.emit("Download Completed!")
        self.finished.emit()
    
    def on_progress(self, stream, chunk, bytes_remaining):
        """Callback function"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        pct_completed = bytes_downloaded / total_size * 100        
        message = f"{round(bytes_downloaded/1000000)}/{round(total_size/1000000)} MB"
        self.statusmessage.emit(message)
        self.progress.emit(round(pct_completed))
        if round(pct_completed) == 100:
            self.finished.emit()




app = QApplication(sys.argv)
app.setWindowIcon(QIcon(yt_dl_icons))
window = UI()
window.show()
app.exec_()
