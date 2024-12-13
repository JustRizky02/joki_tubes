import csv
from PyQt6.QtWidgets import QMainWindow, QComboBox, QLabel, QPushButton, QMessageBox
from PyQt6.uic import loadUi


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("utama.ui", self)  # Pastikan file UI sesuai
        self.init_ui()

    def init_ui(self):
        # Akses widget dari file UI
        self.combo_awal = self.findChild(QComboBox, "comboBox")
        self.combo_akhir = self.findChild(QComboBox, "comboBox_2")
        self.combo_golongan = self.findChild(QComboBox, "comboBox_3")
        self.tarif_label = self.findChild(QLabel, "label_3")
        self.exit_button = self.findChild(QPushButton, "keluar_btn")

        # Hubungkan tombol keluar ke fungsi close
        self.exit_button.clicked.connect(self.close)

        # Load data ke ComboBox
        self.load_data()

    def load_data(self):
        try:
            with open("dataset/tarif_tol_cileunyi.csv", mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                gerbang_awal = set()
                gerbang_akhir = set()
                golongan = {"Golongan I", "Golongan II", "Golongan III", "Golongan IV", "Golongan V"}

                for row in reader:
                    gerbang_awal.add(row["tujuan_awal"])
                    gerbang_akhir.add(row["tujuan_akhir"])

                # Isi ComboBox dengan data unik
                self.combo_awal.addItems(sorted(gerbang_awal))
                self.combo_akhir.addItems(sorted(gerbang_akhir))
                self.combo_golongan.addItems(sorted(golongan))
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "File CSV 'tarif_tol_bervariasi.csv' tidak ditemukan.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {e}")
