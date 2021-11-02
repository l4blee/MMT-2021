from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QLabel
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta
import time
import threading

from lane import Window as Lane
from markup import Window as Markup


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        total_length, ok = QInputDialog().getInt(self, '', 'Total length(m):')
        parking_lot_length, ok = QInputDialog().getDouble(self, '', 'Parking lot size(m):')
        test_time, ok = QInputDialog().getInt(self, '', 'Test time(s):')

        self.test_time = test_time
        self.timestamp = datetime.now() + timedelta(seconds=test_time)

        self.resize(600, 100)
        self.setWindowTitle('Answer')
        font = QFont('Montserrat', 14)

        f = QLabel(self)
        f.move(10, 10)
        self.f = f

        s = QLabel(self)
        s.move(10, 35)
        self.s = s

        t = QLabel(self)
        t.move(10, 60)
        self.t = t

        for i in ['f', 's', 't']:
            eval(f'self.{i}.setFont(font)')

        self.lane_win = Lane(self, total_length, test_time)
        self.markup_win = Markup(self, int(total_length / parking_lot_length), test_time)
        self._thread = threading.Thread(target=self.waitForRes, daemon=True)

        self.lane_win.show()
        self.markup_win.show()
        self._thread.start()

    def waitForRes(self):
        while datetime.now() <= self.timestamp:
            time.sleep(1)

        time.sleep(1)
        self.showAns()

    def showAns(self):
        self.f.setText(f'{self.lane_win.counter} cars have been staying on the lane parking')
        self.f.adjustSize()

        self.s.setText(f'{self.markup_win.counter} cars have been staying on the marked-up parking')
        self.s.adjustSize()

        self.t.setText(f'Elapsed time: {self.test_time}s')
        self.t.adjustSize()


if __name__ == '__main__':
    app = QApplication([])
    main_win = MainWindow()
    main_win.show()
    app.exec()
