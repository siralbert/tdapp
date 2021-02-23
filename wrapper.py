"""Socket client for communicating with TD Ameritrade API."""""""""

import asyncio
import io
import logging
import sys
from datetime import date, datetime, time as time_, timedelta, timezone
from typing import AsyncIterator, Awaitable, Callable, Iterator, List, Union

#import eventkit as ev
from eventkit import Event

#globalErrorEvent = ev.Event()

from connection import Connection
from objects import ConnectionStats

__all__ = ['Client']


class TDClient:
    """
    A fully asynchronous client created for developers who wish to create a
    simple, and reliable GUI to use for interfacing with the TD Ameritrade API.

    The client uses timkpaine/tdameritrade's TDClient for authentication and to
    send API requests for stock quotes, option quotes, account positions, etc.

    The client uses an asyncio event loop for running Tasks, Coroutines,
    and Functions.  Useful stock/option trading algorithms can be created and
    inserted as a function in this class.

    The client has the following methods:

    *``TDClient.connect()``  will block until it receives a
    """

    events = ('apiStart', 'apiEnd', 'apiError', 'throttleStart', 'throttleEnd')

    (DISCONNECTED, CONNECTING, CONNECTED) = range(3)

    def __init__(self, wrapper):
        self.wrapper = wrapper
        self.decoder = Decoder(wrapper, 0)
        self.apiStart = Event('apiStart')
        self.apiEnd = Event('apiEnd')
        self.apiError = Event('apiError')
        self.throttleStart = Event('throttleStart')
        self.throttleEnd = Event('throttleEnd')
#        self._logger = logging.getLogger('ib_insync.client')

        self.conn = Connection()
        self.conn.hasData += self._onSocketHasData
        self.conn.disconnected += self._onSocketDisconnected

      # extra optional wrapper methods
        self._priceSizeTick = getattr(wrapper, 'priceSizeTick', None)
        self._tcpDataArrived = getattr(wrapper, 'tcpDataArrived', None)
        self._tcpDataProcessed = getattr(wrapper, 'tcpDataProcessed', None)
        self.host = ''
        self.port = -1
        self.clientId = -1
        self.optCapab = ''
        self.connectOptions = b''
        self.reset()

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_forever()

    def isConnected(self):
        return self.connState == Client.CONNECTED

    def isReady(self) -> bool:
        """Is the API connection up and running?"""""
        return self._apiReady

    def connectionStats(self) -> ConnectionStats:
        """Get statistics about the connection."""""
        if not self.isReady():
            raise ConnectionError('Not connected')
        """
        return ConnectionStats(
            self._startTime,
            time.time() - self._startTime,
            self._numBytesRecv, self.conn.numBytesSent,
            self._numMsgRecv, self.conn.numMsgSent
        )
        """


    def connect():
#            self, host: str, port: int, clientId: int,
#            timeout: Optional[float] = 2.0):
        """
        Connect to a running TWS or IB gateway application.

        Args:
            host: Host name or IP address.
            port: Port number.
            clientId: ID number to use for this client; must be unique per
                connection.
            timeout: If establishing the connection takes longer than
                ``timeout`` seconds then the ``asyncio.TimeoutError`` exception
                is raised. Set to 0 to disable timeout.
        """
 #       run(self.connectAsync(host, port, clientId, timeout))
        return


    def disconnect(self):
        """Disconnect from IB connection."""
        self._logger.info('Disconnecting')
        self.connState = Client.DISCONNECTED
        self.conn.disconnect()
        self.reset()
