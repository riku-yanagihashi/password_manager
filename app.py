import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel, QDialog, QTableWidget, QTableWidgetItem, QTextEdit
from PyQt5.QtCore import Qt

class MyPasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("My Password Manager")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.register_button = QPushButton("新規登録", self)
        self.layout.addWidget(self.register_button)
        self.register_button.clicked.connect(self.showRegistrationDialog)

        # 登録情報を表示するためのテーブルウィジェット
        self.password_table = QTableWidget()
        self.password_table.setColumnCount(3)  # 3列: メールアドレス/ユーザー名、パスワード、表示ボタン
        self.password_table.setHorizontalHeaderLabels(["メールアドレス/ユーザー名", "パスワード", "表示"])
        self.layout.addWidget(self.password_table)

        # 登録情報を読み込み表示
        self.loadEntries()

    def showRegistrationDialog(self):
        self.register_dialog = RegistrationDialog(self)
        self.register_dialog.accepted.connect(self.loadEntries)  # 登録後に情報を再読み込み
        self.register_dialog.exec()

    def loadEntries(self):
        # データベースから登録情報を読み込む
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS entries (email_username TEXT, password TEXT)")
        cursor.execute("SELECT * FROM entries")
        entries = cursor.fetchall()
        conn.close()

        # テーブルウィジェットに登録情報を表示
        self.password_table.setRowCount(len(entries))
        for row, entry in enumerate(entries):
            email_username, password = entry
            self.password_table.setItem(row, 0, QTableWidgetItem(email_username))
            password_item = QTableWidgetItem("******")
            password_item.setFlags(password_item.flags() | Qt.ItemIsEditable)  # パスワードセルを編集可能に設定
            self.password_table.setItem(row, 1, password_item)
            show_button = QPushButton("表示", self)
            show_button.clicked.connect(lambda _, r=row: self.showPassword(r))  # ボタンがクリックされたらパスワードを表示
            self.password_table.setCellWidget(row, 2, show_button)

    def showPassword(self, row):
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        password_text = cursor.execute(f"SELECT password FROM entries WHERE rowid = {row+1}").fetchone()[0]
        print("showPassword() called")
        dialog = QDialog(self)
        dialog.setWindowTitle("パスワード表示")
        dialog.setGeometry(200, 200, 300, 100)
        password_label = QLabel(f"パスワード: {password_text}")
        layout = QVBoxLayout()
        layout.addWidget(password_label)
        dialog.setLayout(layout)
        dialog.exec()

class RegistrationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新規登録")
        self.setGeometry(200, 200, 300, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.email_username_label = QLabel("メールアドレスまたはユーザー名:")
        self.layout.addWidget(self.email_username_label)
        self.email_username_input = QLineEdit()
        self.layout.addWidget(self.email_username_input)

        self.password_label = QLabel("パスワード:")
        self.layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.save_button = QPushButton("保存", self)
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.saveEntry)

    def saveEntry(self):
        email_username = self.email_username_input.text()
        password = self.password_input.text()

        # データベースに接続し、エントリを保存
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS entries (email_username TEXT, password TEXT)")
        cursor.execute("INSERT INTO entries (email_username, password) VALUES (?, ?)", (email_username, password))
        conn.commit()
        conn.close()

        # ダイアログを閉じる
        self.accept()

def main():
    app = QApplication(sys.argv)
    window = MyPasswordManager()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
