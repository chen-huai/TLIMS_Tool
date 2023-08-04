from TLIMS_Equipment_Data_Tool import *
from Config_Table import *
if __name__ == "__main__":
    import sys
    import os
    import time
    import random
    import pandas as pd
    import numpy as np
    import re

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myTable = MyTableWindow()
    myWin.show()
    myWin.getConfig()
    sys.exit(app.exec_())
