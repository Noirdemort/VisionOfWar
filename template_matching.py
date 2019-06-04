import cv2
import os
import numpy as np
from PyQt5.QtWidgets import *
import sys



class RecordsShow(QWidget):

    def __init__(self):
        super().__init__()
        self.initiate()

    def initiate(self):

        self.setWindowTitle("Lockheed Phoenix Thunder-bird")
        self.setGeometry(700, 500, 500, 500)

        self.h1 = QHBoxLayout()
        self.h3 = QHBoxLayout()

        # for h1
        upload = QPushButton("Upload")
        pred = QPushButton("Analyze!")
        self.locate = QLineEdit()

        upload.clicked.connect(self.open)
        pred.clicked.connect(self.predict)

        self.h1.addWidget(upload)
        self.h1.addWidget(self.locate)
        self.h1.addWidget(pred)

        # for h3
        exit = QPushButton("Exit")
        exit.clicked.connect(qApp.quit)
        self.h3.addWidget(exit)

        # final view
        self.v = QVBoxLayout()
        self.v.addLayout(self.h1)
        self.v.addLayout(self.h3)
        self.setLayout(self.v)

    def open(self):
        self.fileName = QFileDialog.getOpenFileName(self, 'OpenFile')
        self.locate.setText(self.fileName[0])

    def predict(self):
        setForce = []
        img_rgb = cv2.imread(self.locate.text())
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        color_dictionary = {
            "navy": (0, 0, 255),
            "airforce": (50, 100, 150),
            "missiles": (150, 50, 200),
            "tanks": (0, 255, 0),
            "sigint": (255, 255, 255),
            "explosion_and_disasters": (0, 0, 0)
        }
        for i in os.listdir("."):
            print(i)
            try:
                for j in os.listdir("./" + i):
                    try:
                        a = "./" + i + '/' + j
                        template = cv2.imread(a, 0)
                        w, h = template.shape[::-1]
                        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                        threshold = 0.785
                        loc = np.where(res >= threshold)
                        for pt in zip(*loc[::-1]):
                            setForce.append(i)
                            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), color_dictionary[i], 1)
                    except Exception as q:
                        print("-------> ", q)
            except Exception as e:
                print(e)

        # cv2.imshow('Detected', img_rgb)
        status = "Alert"
        cv2.imwrite("latest.png", img_rgb)
        os.system("open latest.png")
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        setForce = list(set(setForce))
        if setForce==[]:
            setForce = "nothing"
            status = "Relax"
        self.locate.setText('')
        w = QMessageBox()
        w.setText("{}! You have got a {} in the area.".format(status, str(setForce)))
        w.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wint = RecordsShow()
    wint.show()
    sys.exit(app.exec_())
