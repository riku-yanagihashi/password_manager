# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MyPasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("My Password Manager")
        self.setGeometry(100, 100, 400, 300)

        # ボタンを作成し、ウィンドウに追加
        button = QPushButton("Click me!", self)
        button.setGeometry(150, 150, 100, 40)
        button.clicked.connect(self.onButtonClick)

    def onButtonClick(self):
        print("ボタンがクリックされました！")

def main():
    app = QApplication(sys.argv)
    window = MyPasswordManager()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
