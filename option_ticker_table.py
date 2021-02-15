import tdameritrade as td
import os

from PyQt5.QtWidgets import QApplication
import PyQt5.QtWidgets as qt

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

    def __init__(self, refreshToken):
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

        self.connectInfo = (refreshtoken)

    def add(self, text=''):
        return 0

    def onConnectButtonClicked(self, _):
        #check connection status if not connected connect.
        return 0

    def closeEvent(self, ev):
        return 0

if __name__ == '__main__':
    refreshtoken = open(os.path.expanduser('~/.r_token'), 'r')
    tdclient = td.TDClient(client_id=os.getenv('TDAMERITRADE_CLIENT_ID'), refresh_token=refreshtoken)

    print(tdclient.search('AAPL'))
    # test connection
    app = QApplication([])

    window = Window(refreshtoken)
    window.resize(600, 400)
    window.show()
#   tdapp.run()

    app.exec_()
