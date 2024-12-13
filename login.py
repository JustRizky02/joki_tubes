import csv
from fileinput import close

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
        self.pushButton.clicked.connect(self.tutup)

    def tutup(self):
        app.closeAllWindows()

    def handle_login(self):
        username = self.textEdit.toPlainText()
        password = self.lineEdit.text()

        if self.check_login(username, password):
            QMessageBox.information(self, "Berhasil Login", f"Selamat Datang, {username}!")
            self.open_main_window()
        else:
            QMessageBox.critical(self, "Gagal Login", "nama pengguna atau password tidak valid.")

    def check_login(self, username, password):
        file_path = "dataset/login.csv"

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

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("utama.ui", self)

        # Panggil fungsi untuk memuat data CSV ke dalam ComboBox
        self.load_csv_data()

        # Hubungkan ComboBox dengan fungsi update_tarif
        self.comboBox.currentIndexChanged.connect(self.update_tarif)
        self.comboBox_2.currentIndexChanged.connect(self.update_tarif)
        self.comboBox_3.currentIndexChanged.connect(self.update_tarif)

        # Hubungkan tombol dengan fungsi
        self.pushButton.clicked.connect(self.handle_payment)

        self.pushButton_2.clicked.connect(self.kembaliLogin)

        # Sembunyikan tombol pushButton_3 di awal
        self.pushButton_3.setVisible(False)

        # Hubungkan tombol pushButton_3 dengan fungsi cetak resi
        self.pushButton_3.clicked.connect(self.print_receipt)

    def kembaliLogin(self):
        self.LoginApp = LoginApp()
        self.LoginApp.show()
        self.close()

    def load_csv_data(self):
        file_path = "dataset/tarif_tol_cileunyi.csv"

        try:
            with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                tujuan_awal_set = set()
                tujuan_akhir_set = set()

                for row in reader:
                    tujuan_awal_set.add(row["tujuan_awal"])
                    tujuan_akhir_set.add(row["tujuan_akhir"])

                self.comboBox.addItems(sorted(tujuan_awal_set))
                self.comboBox_2.addItems(sorted(tujuan_akhir_set))

                golongan_headers = [field for field in reader.fieldnames if field.startswith("golongan_")]
                self.comboBox_3.addItems(golongan_headers)

        except FileNotFoundError:
            print(f"File '{file_path}' tidak ditemukan.")
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat data: {e}")

    def update_tarif(self):
        file_path = "dataset/tarif_tol_cileunyi.csv"

        tujuan_awal = self.comboBox.currentText()
        tujuan_akhir = self.comboBox_2.currentText()
        golongan = self.comboBox_3.currentText()

        if not (tujuan_awal and tujuan_akhir and golongan):
            self.label_8.setText("Pilih semua opsi untuk menampilkan tarif.")
            return

        try:
            with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if row["tujuan_awal"] == tujuan_awal and row["tujuan_akhir"] == tujuan_akhir:
                        tarif = row.get(golongan, "Data tidak ditemukan")
                        self.label_8.setText(f"Rp. {tarif}")
                        return

                self.label_8.setText("Data tidak ditemukan.")

        except FileNotFoundError:
            print(f"File '{file_path}' tidak ditemukan.")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

    def handle_payment(self):
        try:
            saldo = int(self.textEdit_3.toPlainText())
            tarif_text = self.label_8.text().replace("Rp. ", "").replace(",", "")
            tarif = int(tarif_text) if tarif_text.isdigit() else 0

            if saldo < tarif:
                QMessageBox.warning(self, "Saldo Tidak Cukup", "Saldo Anda tidak mencukupi untuk melakukan transaksi.")
                self.label_9.setText("-")
                self.pushButton_3.setVisible(False)
            else:
                sisa_saldo = saldo - tarif
                self.label_9.setText(f"Rp. {sisa_saldo}")
                self.pushButton_3.setVisible(True)
                QMessageBox.information(self, "Saldo Cukup", "Saldo Cukup")

        except ValueError:
            QMessageBox.critical(self, "Input Error", "Pastikan saldo yang dimasukkan adalah angka valid.")
            self.label_9.setText("-")
            self.pushButton_3.setVisible(False)

    def print_receipt(self):
        reply = QMessageBox.question(self, "Konfirmasi Cetak", "Apakah Anda ingin mencetak resi?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                tujuan_awal = self.comboBox.currentText()
                tujuan_akhir = self.comboBox_2.currentText()
                golongan = self.comboBox_3.currentText()
                tarif_text = self.label_8.text()
                saldo_awal = self.textEdit_3.toPlainText()
                sisa_saldo = self.label_9.text()

                receipt_content = (
                    f"=========== STRUK PEMBAYARAN ===========\n"
                    f"Tujuan Awal     : {tujuan_awal}\n"
                    f"Tujuan Akhir    : {tujuan_akhir}\n"
                    f"Golongan Kendaraan: {golongan}\n"
                    f"Tarif           : {tarif_text}\n"
                    f"Saldo Awal      : Rp. {saldo_awal}\n"
                    f"Sisa Saldo      : {sisa_saldo}\n"
                    f"========================================\n"
                )

                with open("resi_pembayaran.txt", "w", encoding="utf-8") as file:
                    file.write(receipt_content)

                QMessageBox.information(self, "Berhasil", "Resi berhasil dicetak ke file 'resi_pembayaran.txt'.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat mencetak resi: {e}")




if __name__ == "__main__":
    app = QApplication([])
    login_app = LoginApp()
    login_app.show()
    app.exec()
