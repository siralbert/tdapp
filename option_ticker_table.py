import tdameritrade as td
from ib_insync import *

import os
import asyncio

import util
import wrapper

from PyQt5.QtWidgets import QApplication
import PyQt5.QtWidgets as qt
from PyQt5.QtGui import QPalette
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

class TickerTable(qt.QTableWidget):
    headers = [
        'symbol', 'last', 'mark', 'adjOptValue', 'adj', 'size', 'option_symbol', 'BUY', 'SELL'
    ]

    """
    TODO: Define settings

    delta - The minimum delta when buying long calls.  Affects 'extra' extrinsic value of option and execution speed of option orders.

    """

    def __init__(self, parent=None):
        qt.QTableWidget.__init__(self, parent)
        self.conId2Row = {}
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.setAlternatingRowColors(True)

    def addTicker(self, ticker):
        row = self.rowCount()
        self.insertRow(row)
#        self.conId2Row get connection id by calling tdclient's equivalent of ib's reqMktData
#     TODO: add qt.QPushButton('BUY') and qt.QPushButton('SE')
        for col in range(len(self.headers)):
            item = qt.QTableWidgetItem('-')
            self.setItem(row, col, item)
        item = self.item(row, 0)
        item.setText(ticker)
        item = self.item(row, 5) # col 'size'
        item.setText('1')

        # Adding BUY and SELL buttons and connect corresponding slots/callback functions
        buyButton = qt.QPushButton('BUY')
        self.setCellWidget(row,len(self.headers)-2, buyButton)
        buyButton.clicked.connect(self.onBuyButtonClicked)

        sellButton = qt.QPushButton('SELL')
        self.setCellWidget(row,len(self.headers)-1, sellButton)
        sellButton.clicked.connect(self.onSellButtonClicked)

        self.resizeColumnsToContents()

    def clearTickers(self):
        self.setRowCount(0)
        self.conId2Row.clear()

    def onBuyButtonClicked(self,_):

#### if just the ticker is given:
# automatically get option symbol for next Friday to input into placeIBTrade()
        ticker = 'AAPL'
#  col = 'symbol', row = ADD code to get row of Buy Button

        option_symbol = getOptionSymbol(ticker)
        print (option_symbol)
# convert PG_121319C108 to  [expiry_date] [strike] [C] using regular expressions
        IB_list = []
        IB_list = tdapi_to_IB(option_symbol)
        print(IB_list)

        print('\n' + tdapi_to_tos(option_symbol) + '\n')
#placeIBTrade(args.ticker, dateIB, strike, 'C', c.midpoint(option_symbol)) # in ADP_120619C250 format(tdapi)
        if args.tdapi:
            c.placeOrder(args.order_type + stradd, args.size, option_symbol, 'LIMIT', c.midpoint(option_symbol, args.order_type))
#        c.placeOrder(args.order_type + stradd, args.size, option_symbol, 'LIMIT', 0.05)
        else:
            placeIBTrade(IB_list[0], IB_list[1], IB_list[2], IB_list[3], c.midpoint(option_symbol, args.order_type))
# return ToS option symbol Ex] .ADP191206C250 instead of (ADP_120619C250)
# Copy and paste into ToS Watchlist
        print('\n' + tdapi_to_tos(option_symbol))
        return

    def onSellButtonClicked(self,_):
        return


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

        # Initialize TDClient which connects to the TD API
        self.connectInfo = (clientId, refreshToken)
        self.tdclient = td.TDClient(*self.connectInfo)

    def add(self, text=''):
        text = text or self.edit.text()
        if text:
            ticker = text
            self.table.addTicker(ticker)
            self.edit.setText(text)

    def onConnectButtonClicked(self, _):
        #check connection status if not connected connect.
#        tdclient = td.TDClient(*self.connectInfo)
        if not self.tdclient.isConnected():
            self.table.clearTickers()
            self.connectButton.setText('Connect')
            exit()
#            print(tdclient.search('AAPL'))
        else:

            print(self.tdclient.accounts(positions=True))

            self.connectButton.setText('Disconnect')
            for symbol in ('AAPL', 'TSLA', 'VZ'):
                self.add(f"{symbol}")
            self.add("Stock('ORCL', 'SMART', 'USD')")

        return 0

    def closeEvent(self, ev):
        asyncio.get_event_loop().stop()
        return 0

if __name__ == '__main__':
    refreshToken = open(os.path.expanduser('~/.r_token'), 'r')
    clientId = os.getenv("TDAMERITRADE_CLIENT_ID")

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

    util.patchAsyncio()
    util.useQt()

    window = Window(clientId, refreshToken)
    window.resize(600, 400)
    window.show()

#    tdapp.run()
    util.run()

    app.exec_()
