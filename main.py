import csv
from PyQt6.QtWidgets import QMessageBox, QApplication, QMainWindow, QWidget
from PyQt6.uic import loadUi

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.textEdit_2 = None
        self.textEdit = None
        loadUi("login_usr.ui", self)  # Pastikan nama file benar

        # Hubungkan tombol login dengan handle_login
        self.login_btn.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.textEdit.text()
        password = self.textEdit_2.text()

        if self.check_login(username, password):
            QMessageBox.information(self, "Login Success", f"Welcome, {username}!")
            self.open_main_window()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password.")

    def check_login(self, username, password):
        file_path = "login.csv"

        print("Starting check_login...")
        try:
            # Buka file dengan encoding UTF-8 dan delimiter titik koma (;)
            with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter=';')

                # Validasi kolom header dalam CSV
                if "username" not in reader.fieldnames or "password" not in reader.fieldnames:
                    print("File CSV tidak valid.")
                    try:
                        QMessageBox.critical(self, "Error",
                                             "File CSV tidak valid. Header harus berisi 'username' dan 'password'.")
                    except Exception as e:
                        print(f"QMessageBox Error: {e}")
                    return False

                # Pencarian data login
                for row in reader:
                    print(f"Checking row: {row}")
                    if row["username"] == username and row["password"] == password:
                        print("Login berhasil!")
                        return True

        except FileNotFoundError:
            print(f"File '{file_path}' tidak ditemukan.")
            try:
                QMessageBox.critical(self, "Error", f"File '{file_path}' tidak ditemukan.")
            except Exception as e:
                print(f"QMessageBox Error: {e}")
            return False
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            try:
                QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {e}")
            except Exception as e:
                print(f"QMessageBox Error: {e}")
            return False

        print("Login gagal.")
        return False

    def open_main_window(self):
        self.main_window = MainApp()
        self.main_window.show()
        self.close()

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("utama.ui", self)

if __name__ == "__main__":
    app = QApplication([])
    login_app = LoginApp()
    login_app.show()
    app.exec()
