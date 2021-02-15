import tdameritrade as td
import os

import util

from PyQt5.QtWidgets import QApplication
import PyQt5.QtWidgets as qt
from PyQt5.QtGui import QPalette
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

class TickerTable(qt.QTableWidget):
    headers = [
        'option_symbol', 'bid', 'ask', 'mark', 'int', 'ext', 'adj'
    ]

    def __init__(self, parent=None):
        qt.QTableWidget.__init__(self, parent)
        self.conId2Row = {}
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.setAlternatingRowColors(True)

    def addTicker(self, ticker):
        row = self.rowCount()
        self.insertRow(row)
        self.conId2Row

class Window(qt.QWidget):

    def __init__(self, clientId, refreshToken):
        qt.QWidget.__init__(self)
        self.edit = qt.QLineEdit('', self)
        self.edit.editingFinished.connect(self.add)
        self.table = TickerTable()
        self.connectButton = qt.QPushButton('Connect')
        self.connectButton.clicked.connect(self.onConnectButtonClicked)
        layout = qt.QVBoxLayout(self)
        layout.addWidget(self.edit)
        layout.addWidget(self.table)
        layout.addWidget(self.connectButton)

        self.connectInfo = (clientId, refreshToken)

    def add(self, text=''):
        return 0

    def onConnectButtonClicked(self, _):
        #check connection status if not connected connect.
        tdclient = td.TDClient(*self.connectInfo)
        print(tdclient.search('AAPL'))
        return 0

    def closeEvent(self, ev):
        return 0

if __name__ == '__main__':
    refreshToken = open(os.path.expanduser('~/.r_token'), 'r')
    clientId = os.getenv("TDAMERITRADE_CLIENT_ID")
#    tdclient = td.TDClient(client_id=os.getenv('TDAMERITRADE_CLIENT_ID'), refresh_token=refreshtoken)

#    print(tdclient.search('AAPL'))
    # test connection


    app = QApplication([])
    app.setStyle('Fusion')

    dark_palette = QPalette()

    dark_palette.setColor(QPalette.Window, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QtGui.QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(dark_palette)

    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white;  }")


    window = Window(clientId, refreshToken)
    window.resize(600, 400)
    window.show()
#   tdapp.run()

    app.exec_()
