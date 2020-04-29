import sys
import time

from PyQt5.Qt import QApplication
from PyQt5.QtCore import Qt
from box import MainWindowB, Box

def show_gui():
    print("__main__ calling")
    app = QApplication(sys.argv)

    # disable mouse-cursor
    app.setOverrideCursor(Qt.BlankCursor)

    MainWindow = MainWindowB()
    test = Box(MainWindow)
    MainWindow.show()
    return app.exec_()

# start of main
res = -1
while res != 0:
    start_time = time.time()
    try:
        res = show_gui()
    except:
        res = -1
    stop_time = time.time()
    if (res != 0) and (stop_time < (start_time + 5)):
        # serious bug, we just can just stop the application
        res = 0
        print("Fast error. Try calling box.py directly for more information")
