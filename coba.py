import csv

file_path = "login.csv"
login_data = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Mengubah delimiter dari ";" ke ","
            reader = csv.reader(file, delimiter=';')
            updated_rows = [','.join(row).split(',') for row in reader]
            for row in updated_rows:
                if len(row) >= 2:
                    username, password = row[0], row[1]
                    login_data[username] = password
    except FileNotFoundError:
        print("File login.csv tidak ditemukan.")
    return login_data
