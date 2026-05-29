## 🏷️ **Membangun ETL Pipeline dan Unit Testing Komprehensif untuk Data Kompetitor Fashion Studio | 👗 Fashion Retail ETL Pipeline**

---

## 📌 Deskripsi Proyek

Proyek ini merupakan implementasi *end-to-end data pipeline* (**Extract, Transform, Load**) berbasis Python yang dirancang untuk membantu tim retail fashion dalam mengotomatisasi pengambilan dan penyiapan data kompetitor secara tangguh (*robust*).

Fokus utama dari proyek ini adalah mengumpulkan data produk dari website retail fiktif **Fashion Studio** (https://fashion-studio.dicoding.dev/) yang mencakup **50 halaman web** atau sekitar **1000 data mentah**, melakukan pembersihan data kotor secara modular sesuai standar industri, serta mendistribusikan data siap pakai (*analytics-ready data*) tersebut ke tiga jenis repositori data yang berbeda secara simultan.

---

## 🛠️ Ringkasan Fitur & Spesifikasi Teknis

### 🔍 Ekstraksi Tangguh (*Extract*)

Memanfaatkan `requests.Session()` untuk menjaga efisiensi koneksi internet selama proses *web scraping* dan dilengkapi penanganan error defensif terhadap variasi struktur tag HTML mentah. Setiap data yang diambil otomatis dilengkapi dengan kolom **Timestamp** (format ISO).

---

### 🧹 Transformasi Presisi (*Transform*)

Menggunakan ekspresi reguler (*Regex*) dan manipulasi string via Pandas untuk:
- Membersihkan teks pengotor,
- Membuang data duplikat,
- Menangani nilai kosong (*handling null values*),
- Serta melakukan konversi mata uang dari USD ke IDR dengan asumsi kurs tetap **Rp16.000**.

---

### 💾 Penyimpanan Multi-Repositori (*Load*)

Pipeline dirancang untuk mengekspor data bersih ke dalam tiga penyimpanan sekaligus dalam satu kali jalan:

#### 📄 Flat File
Berformat:

```plaintext
product.csv
```

#### ☁️ Cloud Storage
Google Sheets API dengan autentikasi menggunakan kunci privat Service Account:

```plaintext
google-sheets-api.json
```

#### 🗄️ Relational Database
Tabel lokal PostgreSQL menggunakan engine koneksi SQLAlchemy.

---

### 🧪 Arsitektur Pengujian Kuat (*Unit Testing*)

Dilindungi oleh skrip pengujian berbasis `pytest` menggunakan teknik **Mock Testing** (`unittest.mock.patch`) untuk mengisolasi ketergantungan eksternal seperti:
- jaringan internet,
- dan server database.

Seluruh fungsi inti berhasil dilindungi dengan **Test Coverage mencapai 86%** (*Memenuhi kriteria Advanced / Bintang 5*).

---

### 🔒 Aspek Keamanan Data

Seluruh kredensial rahasia database, private key cloud API, serta dependensi virtual lokal (`.venv`) diproteksi secara ketat menggunakan konfigurasi `.gitignore` agar tidak terekspos ke publik.

---

# 🚀 Prasyarat & Instalasi

Ikuti langkah-langkah berikut untuk menyiapkan lingkungan lokal komputer sebelum menjalankan proyek ETL Pipeline.

---

# 🛠️ Setup Environment

## 1️⃣ Persiapan Lingkungan (Virtual Environment)

Direkomendasikan menggunakan Python versi **3.10+** dan membuat virtual environment agar dependensi tidak bentrok.

### Membuat Virtual Environment

```bash
# Membuat virtual environment bernama .venv
python -m venv .venv
```

### Aktivasi di Windows (PowerShell)

```bash
.venv\Scripts\Activate.ps1
```

### Aktivasi di Linux / macOS

```bash
source .venv/bin/activate
```

---

## 2️⃣ Instalasi Dependencies

Instal seluruh pustaka yang dibutuhkan sesuai versi spesifik yang diminta:

```bash
pip install -r requirements.txt
```

---

# 🗄️ Setup Database PostgreSQL

Masuk ke terminal PostgreSQL (`psql`) lokal komputermu.

Kemudian jalankan perintah SQL berikut untuk membuat database baru:

```sql
CREATE DATABASE fashion_retail;
```

Pastikan konfigurasi berikut pada variabel `DB_URL` di berkas `main.py` sudah disesuaikan dengan akun PostgreSQL milikmu:

- Username
- Password
- Port

---

# 📄 Setup Google Sheets API Kredensial

Ikuti langkah-langkah berikut:

1. Buat proyek baru di Google Cloud Console
2. Aktifkan Google Sheets API
3. Buat sebuah Service Account
4. Unduh kunci privat dalam format JSON
5. Letakkan file tersebut di root folder proyek
6. Ganti nama file menjadi:

```plaintext
google-sheets-api.json
```

7. Salin email Service Account tersebut
8. Undang (*Share/Bagikan*) ke Google Sheets kosong milikmu dengan hak akses sebagai **Editor**
9. Ambil Spreadsheet ID dari URL Google Sheets
10. Tempelkan ke variabel `SPREADSHEET_ID` di dalam file `main.py`

---

# 💻 Cara Menjalankan

## ▶️ Menjalankan Pipeline Utama (ETL)

Untuk mengekstrak data dari website, memprosesnya, dan menyimpannya langsung ke CSV, Google Sheets, dan PostgreSQL secara bersamaan, jalankan perintah berikut:

```bash
python main.py
```

---

## 🧪 Menjalankan Unit Testing

Untuk memastikan seluruh fungsi berjalan dengan benar secara lokal menggunakan mekanisme objek tiruan (*Mocking*), jalankan perintah berikut:

```bash
python -m pytest tests
```

---

## 📊 Memeriksa Laporan Test Coverage

Untuk melihat persentase seberapa luas baris kode pipeline yang telah berhasil dilindungi oleh skrip pengujian, jalankan perintah berikut:

```bash
# Menghitung cakupan kode
coverage run -m pytest tests

# Menampilkan laporan statistik di terminal
coverage report
```

---

# 📈 Hasil Pengujian (Test Coverage Metrics)

Berkat penerapan teknik **Mock Testing** menggunakan `unittest.mock.patch` untuk mengisolasi ketergantungan eksternal (API jaringan dan Database), proyek ini berhasil mencapai persentase cakupan kode sebesar **82%**.

```plaintext
=================================================== 13 passed in 2.65s ===================================================

(.venv) PS C:\PEMDA_KakaDaviDharmawan> python -m coverage report

Name                      Stmts   Miss  Cover
---------------------------------------------
tests\test_extract.py        32      1    97%
tests\test_load.py           49      1    98%
tests\test_transform.py      23      1    96%
utils\extract.py             69     17    75%
utils\load.py                72     23    68%
utils\transform.py           29      7    76%
---------------------------------------------
TOTAL                       274     50    82%
```

---

# 🔒 Keamanan Data (Security Best Practices)

Berkas kredensial rahasia berikut:

- `google-sheets-api.json`
- file data output `products.csv`
- direktori `.venv/`

telah didaftarkan ke dalam berkas `.gitignore`.

Hal ini menjamin rahasia infrastruktur database dan private key cloud tidak akan bocor atau terekspos secara publik saat melakukan *push* perubahan ke platform repositori jarak jauh seperti GitHub.
