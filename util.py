import asyncio
from typing import AsyncIterator, Awaitable, Callable, Iterator, List, Union

def patchAsyncio():
    """Patch asyncio to allow nested event loops."""
    import nest_asyncio
    nest_asyncio.apply()

def startLoop():
    """Use nested asyncio event loop for Jupyter notebooks."""
    patchAsyncio()

def run(*awaitables: Awaitable, timeout: float = None):
    """
    By default run the event loop forever.

    When awaitables (like Tasks, Futures or coroutines) are given then
    run the event loop until each has completed and return their results.

    An optional timeout (in seconds) can be given that will raise
    asyncio.TimeoutError if the awaitables are not ready within the
    timeout period.
    """
    loop = asyncio.get_event_loop()
    if not awaitables:
        if loop.is_running():
            return
        loop.run_forever()
        result = None
        all_tasks = (
            asyncio.all_tasks(loop)  # type: ignore
            if sys.version_info >= (3, 7) else asyncio.Task.all_tasks())
        if all_tasks:
            # cancel pending tasks
            f = asyncio.gather(*all_tasks)
            f.cancel()
            try:
                loop.run_until_complete(f)
            except asyncio.CancelledError:
                pass
    else:
        if len(awaitables) == 1:
            future = awaitables[0]
        else:
            future = asyncio.gather(*awaitables)
        if timeout:
            future = asyncio.wait_for(future, timeout)
        task = asyncio.ensure_future(future)

        def onError(_):
            task.cancel()

        globalErrorEvent.connect(onError)
        try:
            result = loop.run_until_complete(task)
        except asyncio.CancelledError as e:
            raise globalErrorEvent.value() or e
        finally:
            globalErrorEvent.disconnect(onError)

    return result

def useQt(qtLib: str = 'PyQt5', period: float = 0.01):
    """
    Run combined Qt5/asyncio event loop.

    Args:
        qtLib: Name of Qt library to use, can be 'PyQt5' or 'PySide2'.
        period: Period in seconds to poll Qt.
    """
    def qt_step():
        loop.call_later(period, qt_step)
        if not stack:
            qloop = QEventLoop()
            timer = QTimer()
            timer.timeout.connect(qloop.quit)
            stack.append((qloop, timer))
        qloop, timer = stack.pop()
        timer.start(0)
        qloop.exec_()
        timer.stop()
        stack.append((qloop, timer))
        qApp.processEvents()

    if qtLib not in ('PyQt5', 'PySide2'):
        raise RuntimeError(f'Unknown Qt library: {qtLib}')
    if qtLib == 'PyQt5':
        from PyQt5.Qt import QApplication, QTimer, QEventLoop
    else:
        from PySide2.QtWidgets import QApplication
        from PySide2.QtCore import QTimer, QEventLoop
    global qApp
    qApp = QApplication.instance() or QApplication(sys.argv)  # type: ignore
    loop = asyncio.get_event_loop()
    stack: list = []
    qt_step()
