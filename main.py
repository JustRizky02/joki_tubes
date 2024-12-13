import csv
from fileinput import close

# Import modul dan kelas PyQt6 yang diperlukan
from PyQt6.QtWidgets import QMessageBox, QApplication, QMainWindow, QWidget
from PyQt6.uic import loadUi

# Kelas LoginApp menangani antarmuka dan logika aplikasi untuk login
class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.textEdit_2 = None  # Placeholder untuk field text tambahan
        self.textEdit = None  # Placeholder untuk field text tambahan
        loadUi("login_usr.ui", self)  # Memuat file antarmuka login

        # Menghubungkan tombol login dan tombol tutup dengan fungsi masing-masing
        self.login_btn.clicked.connect(self.handle_login)
        self.pushButton.clicked.connect(self.tutup)

    # Fungsi untuk menutup aplikasi
    def tutup(self):
        app.closeAllWindows()

    # Fungsi untuk menangani proses login
    def handle_login(self):
        username = self.textEdit.toPlainText()  # Mengambil username dari textEdit
        password = self.lineEdit.text()  # Mengambil password dari lineEdit

        # Periksa kredensial login
        if self.check_login(username, password):
            QMessageBox.information(self, "Berhasil Login", f"Selamat Datang, {username}!")  # Notifikasi sukses
            self.open_main_window()  # Membuka jendela utama
        else:
            QMessageBox.critical(self, "Gagal Login", "Nama pengguna atau password tidak valid.")  # Notifikasi gagal

    # Fungsi untuk memvalidasi username dan password dari file CSV
    def check_login(self, username, password):
        file_path = "dataset/login.csv"  # Lokasi file CSV yang menyimpan data login

        try:
            # Membuka file CSV dengan format yang benar
            with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter=';')

                # Validasi kolom header pada CSV
                if "username" not in reader.fieldnames or "password" not in reader.fieldnames:
                    QMessageBox.critical(self, "Error", "File CSV tidak valid.")
                    return False

                # Iterasi untuk mencocokkan data login
                for row in reader:
                    if row["username"] == username and row["password"] == password:
                        return True

        # Penanganan jika file tidak ditemukan atau terjadi kesalahan lain
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"File '{file_path}' tidak ditemukan.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {e}")

        return False

    # Fungsi untuk membuka jendela utama
    def open_main_window(self):
        self.main_window = MainApp()  # Membuat instance MainApp
        self.main_window.show()  # Menampilkan jendela utama
        self.close()  # Menutup jendela login

# Kelas MainApp menangani fitur utama aplikasi
class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("utama.ui", self)  # Memuat file antarmuka utama

        # Memuat data dari file CSV ke dalam ComboBox
        self.load_csv_data()

        # Menghubungkan perubahan pada ComboBox dengan fungsi yang relevan
        self.comboBox.currentIndexChanged.connect(self.update_tarif)
        self.comboBox_2.currentIndexChanged.connect(self.update_tarif)
        self.comboBox_3.currentIndexChanged.connect(self.update_tarif)

        # Menghubungkan tombol dengan fungsi masing-masing
        self.pushButton.clicked.connect(self.handle_payment)
        self.pushButton_2.clicked.connect(self.kembaliLogin)

        # Menyembunyikan tombol pushButton_3 di awal
        self.pushButton_3.setVisible(False)
        self.pushButton_3.clicked.connect(self.print_receipt)

    # Fungsi untuk kembali ke jendela login
    def kembaliLogin(self):
        self.LoginApp = LoginApp()
        self.LoginApp.show()
        self.close()

    # Fungsi untuk memuat data dari file CSV
    def load_csv_data(self):
        file_path = "dataset/tarif_tol_cileunyi.csv"

        try:
            with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                # Mengumpulkan data tujuan awal dan akhir
                tujuan_awal_set = set()
                tujuan_akhir_set = set()

                for row in reader:
                    tujuan_awal_set.add(row["tujuan_awal"])
                    tujuan_akhir_set.add(row["tujuan_akhir"])

                self.comboBox.addItems(sorted(tujuan_awal_set))
                self.comboBox_2.addItems(sorted(tujuan_akhir_set))

                # Memasukkan golongan kendaraan ke ComboBox
                golongan_headers = [field for field in reader.fieldnames if field.startswith("golongan_")]
                self.comboBox_3.addItems(golongan_headers)

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"File '{file_path}' tidak ditemukan.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat memuat data: {e}")

    # Fungsi untuk memperbarui tarif tol berdasarkan pilihan
    def update_tarif(self):
        # Mengambil data pilihan dari ComboBox
        tujuan_awal = self.comboBox.currentText()
        tujuan_akhir = self.comboBox_2.currentText()
        golongan = self.comboBox_3.currentText()

        if not (tujuan_awal and tujuan_akhir and golongan):
            self.label_8.setText("Pilih semua opsi untuk menampilkan tarif.")
            return

        # Membaca file CSV untuk menemukan tarif yang sesuai
        try:
            with open("dataset/tarif_tol_cileunyi.csv", mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if row["tujuan_awal"] == tujuan_awal and row["tujuan_akhir"] == tujuan_akhir:
                        tarif = row.get(golongan, "Data tidak ditemukan")
                        self.label_8.setText(f"Rp. {tarif}")
                        return

                self.label_8.setText("Data tidak ditemukan.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {e}")

    # Fungsi untuk menangani pembayaran
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
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Pastikan saldo yang dimasukkan adalah angka valid.")
            self.label_9.setText("-")
            self.pushButton_3.setVisible(False)

    # Fungsi untuk mencetak resi pembayaran
    def print_receipt(self):
        reply = QMessageBox.question(self, "Konfirmasi Cetak", "Apakah Anda ingin mencetak resi?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Membuat konten resi dari data transaksi
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

                # Menyimpan resi ke file
                with open("resi_pembayaran.txt", "w", encoding="utf-8") as file:
                    file.write(receipt_content)

                QMessageBox.information(self, "Berhasil", "Resi berhasil dicetak ke file 'resi_pembayaran.txt'.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat mencetak resi: {e}")

# Entry point aplikasi
if __name__ == "__main__":
    app = QApplication([])  # Membuat aplikasi
    login_app = LoginApp()  # Membuat instance jendela login
    login_app.show()  # Menampilkan jendela login
    app.exec()  # Menjalankan event loop aplikasi
