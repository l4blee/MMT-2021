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
    def __init__(self, amount: int):
        super(Window, self).__init__()
        self.proc_chance = 1  # 26 / 18 - 5; 12 / 19 -2
        loadUi('main.ui', self)

        self.places: list[tuple] = [(True, None) for _ in range(amount)]
        self.counter: int = 0
        self.start_time = datetime.now()

        print(self.places)

        self._thread = threading.Thread(target=self.loop, daemon=True)
        self._thread.start()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        print(f'{self.counter} cars have been staying on the parking')
        print(f'Elapsed time: {(datetime.now() - self.start_time).seconds}s')

    def loop(self):
        while True:
            for index, i in enumerate(self.places):
                car, timestamp = i
                if timestamp is not None and timestamp <= datetime.now():
                    self.places[index] = (True, None)
                    self.counter += 1
                    print(f'{car} has left place №{index}')

            seed = random.uniform(0, 1)
            if seed <= self.proc_chance:
                if any([i[0] for i in self.places]):
                    cars = [Car.get_random() for _ in range(3)]
                    car = random.choice(cars)

                    pos = random.choice([index for index, i in enumerate(self.places) if i[0] is True])

                    delta = random.randint(1, 5)
                    self.places[pos] = (car, datetime.now() + timedelta(seconds=delta))
                    print(f'{car} has occupied place №{pos} for {delta}s')
                    # print(self.places)
                else:
                    print('No places left')

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


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    total_length = 20
    parking_lot_size = 6.5

    window = Window(int(total_length / parking_lot_size))
    window.show()
    app.exec()
