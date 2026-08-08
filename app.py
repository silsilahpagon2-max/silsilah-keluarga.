import csv
import json
import urllib.request
import re
from io import StringIO

# GANTI TEKS DI BAWAH INI DENGAN LINK CSV DARI GOOGLE SHEET ANDA
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQMwZJdFofpj_Rc5zNt9pGV6tf0-6RypoMz9GjTT_XVNHlplo8fasQRISSprkxAjYXgQa8BC4WMivWI/pub?gid=1181153402&single=true&output=csv"

def bersihkan_nama(nama):
    if not nama or nama.strip().lower() == 'n/a':
        return ""
    nama = nama.lower()
    nama = re.sub(r'[,.\'\"\-]', ' ', nama)
    nama = re.sub(r'\b(s\.?e|s\.?pd|s\.?kom|m\.?pd|h|hj|dr|prof)\b', '', nama)
    return "_".join(nama.split())

def ubah_link_foto(url_drive):
    """Mengubah link Google Drive dari Form menjadi link gambar yang bisa dibaca HTML"""
    if not url_drive:
        return ""
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url_drive)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    return url_drive

def main():
    print("Mengunduh data dari Google Sheets...")
    response = urllib.request.urlopen(CSV_URL)
    csv_data = response.read().decode('utf-8')
    reader = csv.DictReader(StringIO(csv_data))

    data_keluarga = []

    for row in reader:
        nama_asli = row.get("Nama Lengkap", "").strip()
        if not nama_asli:
            continue

        id_unik = bersihkan_nama(nama_asli)
        id_bapak = bersihkan_nama(row.get("Nama Lengkap BAPAK Kandung", ""))
        id_ibu = bersihkan_nama(row.get("Nama Lengkap IBU Kandung", ""))
        
        link_foto_mentah = row.get("Upload Foto Wajah", "").strip()
        link_foto_bersih = ubah_link_foto(link_foto_mentah)

        individu = {
            "id": id_unik,
            "nama": nama_asli,
            "jenis_kelamin": row.get("Jenis Kelamin", "").strip(),
            "tempat_lahir": row.get("Tempat Lahir", "").strip(),
            "tanggal_lahir": row.get("Tanggal Lahir", "").strip(),
            "id_bapak": id_bapak,
            "id_ibu": id_ibu,
            "status_pernikahan": row.get("Status Pernikahan", "").strip(),
            "pasangan": row.get("Nama Lengkap Pasangan (Suami/Istri)", "").strip(),
            "foto": link_foto_bersih
        }
        data_keluarga.append(individu)

    with open("data_keluarga.json", "w", encoding="utf-8") as f:
        json.dump(data_keluarga, f, indent=4, ensure_ascii=False)
    
    print("Berhasil! File data_keluarga.json telah diperbarui.")

if __name__ == "__main__":
    main()
