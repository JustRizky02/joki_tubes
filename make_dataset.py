import csv

# Data tarif tol
data = [
    {'tujuan_awal': 'Cileunyi', 'tujuan_akhir': 'Baros', 'golongan_1': 8100, 'golongan_2': 14200, 'golongan_3': 14300, 'golongan_4': 19100, 'golongan_5': 19200},
    {'tujuan_awal': 'Cileunyi', 'tujuan_akhir': 'Pasteur', 'golongan_1': 10600, 'golongan_2': 18600, 'golongan_3': 18700, 'golongan_4': 25100, 'golongan_5': 25200},
    {'tujuan_awal': 'Cileunyi', 'tujuan_akhir': 'Pasirkoja', 'golongan_1': 8200, 'golongan_2': 14100, 'golongan_3': 14200, 'golongan_4': 19200, 'golongan_5': 19300},
    {'tujuan_awal': 'Cileunyi', 'tujuan_akhir': 'Kopo', 'golongan_1': 6600, 'golongan_2': 11600, 'golongan_3': 11700, 'golongan_4': 15600, 'golongan_5': 15700},
    {'tujuan_awal': 'Cileunyi', 'tujuan_akhir': 'Moh. Toha', 'golongan_1': 5600, 'golongan_2': 9100, 'golongan_3': 9200, 'golongan_4': 12600, 'golongan_5': 12700},
    {'tujuan_awal': 'Cileunyi', 'tujuan_akhir': 'Buah Batu', 'golongan_1': 5700, 'golongan_2': 9200, 'golongan_3': 9300, 'golongan_4': 12700, 'golongan_5': 12800},

    {'tujuan_awal': 'Baros', 'tujuan_akhir': 'Pasteur', 'golongan_1': 3100, 'golongan_2': 5100, 'golongan_3': 5200, 'golongan_4': 7100, 'golongan_5': 7200},
    {'tujuan_awal': 'Baros', 'tujuan_akhir': 'Pasirkoja', 'golongan_1': 4200, 'golongan_2': 6100, 'golongan_3': 6200, 'golongan_4': 8100, 'golongan_5': 8200},
    {'tujuan_awal': 'Baros', 'tujuan_akhir': 'Kopo', 'golongan_1': 2000, 'golongan_2': 4000, 'golongan_3': 4000, 'golongan_4': 6000, 'golongan_5': 6000},
    {'tujuan_awal': 'Baros', 'tujuan_akhir': 'Moh. Toha', 'golongan_1': 2200, 'golongan_2': 4100, 'golongan_3': 4200, 'golongan_4': 6100, 'golongan_5': 6200},
    {'tujuan_awal': 'Baros', 'tujuan_akhir': 'Buah Batu', 'golongan_1': 2300, 'golongan_2': 4200, 'golongan_3': 4300, 'golongan_4': 6200, 'golongan_5': 6300},
    {'tujuan_awal': 'Baros', 'tujuan_akhir': 'Cileunyi', 'golongan_1': 2400, 'golongan_2': 4300, 'golongan_3': 4400, 'golongan_4': 6300, 'golongan_5': 6400},

    {'tujuan_awal': 'Pasteur', 'tujuan_akhir': 'Moh. Toha', 'golongan_1': 2600, 'golongan_2': 4100, 'golongan_3': 4200, 'golongan_4': 5100, 'golongan_5': 5200},
    {'tujuan_awal': 'Pasteur', 'tujuan_akhir': 'Pasirkoja', 'golongan_1': 2100, 'golongan_2': 3100, 'golongan_3': 3200, 'golongan_4': 4100, 'golongan_5': 4200},
    {'tujuan_awal': 'Pasteur', 'tujuan_akhir': 'Kopo', 'golongan_1': 2200, 'golongan_2': 3200, 'golongan_3': 3300, 'golongan_4': 4200, 'golongan_5': 4300},
    {'tujuan_awal': 'Pasteur', 'tujuan_akhir': 'Cileunyi', 'golongan_1': 2300, 'golongan_2': 3300, 'golongan_3': 3400, 'golongan_4': 4300, 'golongan_5': 4400},
    {'tujuan_awal': 'Pasteur', 'tujuan_akhir': 'Baros', 'golongan_1': 2400, 'golongan_2': 3400, 'golongan_3': 3500, 'golongan_4': 4400, 'golongan_5': 4500},
    {'tujuan_awal': 'Pasteur', 'tujuan_akhir': 'Buah Batu', 'golongan_1': 2500, 'golongan_2': 3500, 'golongan_3': 3600, 'golongan_4': 4500, 'golongan_5': 4600},

    {'tujuan_awal': 'Pasirkoja', 'tujuan_akhir': 'Moh. Toha', 'golongan_1': 2700, 'golongan_2': 4200, 'golongan_3': 4300, 'golongan_4': 5200, 'golongan_5': 5300},
    {'tujuan_awal': 'Pasirkoja', 'tujuan_akhir': 'Pasteur', 'golongan_1': 2800, 'golongan_2': 4300, 'golongan_3': 4400, 'golongan_4': 5300, 'golongan_5': 5400},
    {'tujuan_awal': 'Pasirkoja', 'tujuan_akhir': 'Kopo', 'golongan_1': 2900, 'golongan_2': 4400, 'golongan_3': 4500, 'golongan_4': 5400, 'golongan_5': 5500},
    {'tujuan_awal': 'Pasirkoja', 'tujuan_akhir': 'Cileunyi', 'golongan_1': 3000, 'golongan_2': 4500, 'golongan_3': 4600, 'golongan_4': 5500, 'golongan_5': 5600},
    {'tujuan_awal': 'Pasirkoja', 'tujuan_akhir': 'Baros', 'golongan_1': 3100, 'golongan_2': 4600, 'golongan_3': 4700, 'golongan_4': 5600, 'golongan_5': 5700},
    {'tujuan_awal': 'Pasirkoja', 'tujuan_akhir': 'Buah Batu', 'golongan_1': 3200, 'golongan_2': 4700, 'golongan_3': 4800, 'golongan_4': 5700, 'golongan_5': 5800},

    {'tujuan_awal': 'Kopo', 'tujuan_akhir': 'Moh. Toha', 'golongan_1': 3300, 'golongan_2': 4800, 'golongan_3': 4900, 'golongan_4': 5800, 'golongan_5': 5900},
    {'tujuan_awal': 'Kopo', 'tujuan_akhir': 'Pasteur', 'golongan_1': 3400, 'golongan_2': 4900, 'golongan_3': 5000, 'golongan_4': 5900, 'golongan_5': 6000},
    {'tujuan_awal': 'Kopo', 'tujuan_akhir': 'Pasirkoja', 'golongan_1': 3500, 'golongan_2': 5000, 'golongan_3': 5100, 'golongan_4': 6000, 'golongan_5': 6100},
    {'tujuan_awal': 'Kopo', 'tujuan_akhir': 'Cileunyi', 'golongan_1': 3600, 'golongan_2': 5100, 'golongan_3': 5200, 'golongan_4': 6100, 'golongan_5': 6200},
    {'tujuan_awal': 'Kopo', 'tujuan_akhir': 'Baros', 'golongan_1': 2000, 'golongan_2': 4000, 'golongan_3': 4000, 'golongan_4': 6000, 'golongan_5': 6000},
    {'tujuan_awal': 'Kopo', 'tujuan_akhir': 'Buah Batu', 'golongan_1': 3700, 'golongan_2': 5200, 'golongan_3': 5300, 'golongan_4': 6200, 'golongan_5': 6300},
]



# Nama file CSV
filename = "dataset/tarif_tol_cileunyi.csv"

# Menulis data ke file CSV
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['tujuan_awal', 'tujuan_akhir', 'golongan_1', 'golongan_2', 'golongan_3',
                                              'golongan_4', 'golongan_5'])

    # Menulis header
    writer.writeheader()

    # Menulis data
    writer.writerows(data)

print(f"File CSV berhasil dibuat: {filename}")
