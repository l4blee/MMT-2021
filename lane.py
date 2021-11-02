import random
import threading
import time
from datetime import datetime, timedelta

from PIL import Image, ImageDraw
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi

from cars import Car


class Window(QtWidgets.QMainWindow):  # fixed parking
    def __init__(self, parent, length: int, test_time: int):
        super(Window, self).__init__()
        loadUi('main.ui', self)

        self.proc_chance = 1
        self.length = length
        self._parent = parent
        self.places: list[list] = [[True, None, length * 1000]]
        self.counter: int = 0
        self.test_time = test_time
        self.start_time = datetime.now()

        self._thread = threading.Thread(target=self.loop, daemon=True)
        self._thread.start()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self._parent.lane_win_counter = self.counter

    def loop(self):
        while True:
            if (datetime.now() - self.start_time).seconds == self.test_time:
                self.close()
                break

            for index, i in enumerate(self.places):
                car, timestamp, length = i
                if timestamp is not None and timestamp <= datetime.now():
                    if index == 0:
                        closest = self.places[index + 1]  # 1
                        if closest[0] is True:
                            self.places[1][2] += length
                            del self.places[index]
                        else:
                            self.places[index] = [True, None, length]
                    elif index == len(self.places) - 1:
                        closest = self.places[index - 1]  # -2
                        if closest[0] is True:
                            self.places[index - 1][2] += length
                            del self.places[index]
                        else:
                            self.places[index] = [True, None, length]
                    else:
                        left = self.places[index - 1]
                        right = self.places[index - 1]

                        if left[0] is True:
                            self.places[index - 1][2] += length
                            del self.places[index]
                        elif right[0] is True:
                            self.places[index + 1][2] += length
                            del self.places[index]
                        else:
                            self.places[index] = [True, None, length]

                    self.counter += 1
                    print(f'{car} has left place №{index}')

            # Grouping
            def check(places):
                trues = [index for index, i in enumerate(self.places) if i[0] is True]
                if len(trues) > 1:
                    for index, i in enumerate(trues[:-1]):
                        if trues[index + 1] == i + 1:
                            return True
                else:
                    return False

            while check(self.places):
                for index, i in enumerate(self.places):
                    if i[0] is True and self.places[index + 1][0] is True:
                        self.places[index][2] += self.places[index + 1][2]
                        del self.places[index + 1]
                        break

            seed = random.uniform(0, 1)
            if seed <= self.proc_chance:
                cars = [Car.get_random() for _ in range(3)]
                car = random.choice(cars)

                available_places = [index
                                    for index, i in enumerate(self.places)
                                    if i[0] is True and i[2] >= car.parking_gap * 2 + car.length]

                if len(available_places) == 0:
                    print('No places left')
                else:
                    pos = random.choice(available_places)

                    delta = random.randint(1, 5)

                    self.places.insert(
                        pos + 1,
                        [True, None, self.places[pos][2] - (car.parking_gap * 2 + car.length)]
                    )
                    self.places[pos] = [car,
                                        datetime.now() + timedelta(seconds=delta),
                                        car.parking_gap * 2 + car.length]

                    print(f'{car} has occupied place №{pos} for {delta}s')

                # print(self.places)

            # print()
            self.applyImage()
            time.sleep(1 / 3)

    def convertImage(self, img: Image.Image) -> QImage:
        data = img.tobytes('raw', 'RGBA')
        qim = QImage(data, img.size[0], img.size[1], QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)

        return pixmap

    def applyImage(self):
        width = self.width() / len(self.places)
        img = Image.new('RGBA', (self.width(), 100), color=(255, 255, 255, 0))
        drawer = ImageDraw.Draw(img)

        for index, i in enumerate(self.places):
            if isinstance(i[0], Car):
                drawer.ellipse(
                    (10 + index * width, 0, (index + 1) * width - 10, 100),
                    fill=(0, 0, 0, 255)
                )

        pixmap = self.convertImage(img)
        self.img.setPixmap(pixmap)

        self.total.setText(f'Total: {self.counter} cars,'
                           f' time: {(datetime.now() - self.start_time).seconds}s')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = Window(20)
    win.show()
    app.exec()
