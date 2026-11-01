# Sistem Informasi Manajemen Perpustakaan

Aplikasi desktop manajemen data buku dan anggota perpustakaan yang dibangun menggunakan **Python** dan **CustomTkinter** dengan menerapkan arsitektur **Model-View-Controller (MVC)**, sistem keamanan autentikasi & otorisasi berbasis peran (*Role-Based Access Control* / RBAC), serta integrasi *Continuous Integration* (CI) menggunakan **GitHub Actions**, **Flake8**, dan **Pytest**.

---

## 📌 Deskripsi Singkat Aplikasi

Sistem Manajemen Perpustakaan dirancang untuk mempermudah pengelolaan inventaris buku dan data anggota perpustakaan. Aplikasi ini membedakan hak akses pengguna menjadi dua peran:
1. **Admin**: Memiliki hak akses penuh untuk melihat, menambah (*Create*), memperbarui (*Update*), dan menghapus (*Delete*) data koleksi buku.
2. **Anggota**: Memiliki hak akses baca (*Read-only*). Form input serta tombol aksi (Simpan, Update, Delete) otomatis terkunci (*disabled*) demi keamanan integritas data.

### Fitur Utama:
- **Autentikasi & Otorisasi RBAC**: Sistem login aman dengan validasi role (`admin` dan `anggota`).
- **Enkripsi Password**: Kata sandi pengguna diubah menjadi *hash* SHA-256 secara otomatis saat pendaftaran dan verifikasi login.
- **Pencegahan SQL Injection**: Seluruh query basis data menggunakan *Parameterized Queries*.
- **Antarmuka Grafis Modern**: Dibangun dengan CustomTkinter yang responsif dan konsisten.
- **CI/CD Pipeline**: Pengujian otomatis (*unit tests*) dengan Pytest dan pengecekan sintaks/kualitas kode dengan Flake8 pada setiap *push* atau *pull request* ke branch `main`.

---

## 📂 Struktur Direktori Proyek (Arsitektur MVC)

```text
Modul 3/
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml         # Konfigurasi GitHub Actions CI Pipeline
├── config/
│   └── database.py                 # Konfigurasi koneksi ke basis data MySQL
├── controllers/
│   ├── anggota_controller.py       # Pengendali logika untuk modul Anggota
│   ├── auth_controller.py          # Pengendali autentikasi dan alur login/logout
│   └── buku_controller.py          # Pengendali logika buku & otorisasi hak akses
├── dist/
│   └── AplikasiPerpustakaan.exe    # File executable mandiri hasil build PyInstaller
├── models/
│   ├── anggota_model.py            # Model data dan query tabel anggota
│   ├── buku_model.py               # Model data dan query CRUD tabel buku
│   └── user_model.py               # Model autentikasi, hashing SHA-256, & registrasi user
├── test/
│   ├── test_auth.py                # Unit test autentikasi, registrasi, otorisasi, & logout
│   └── test_buku.py                # Unit test operasi create & get all buku
├── views/
│   ├── anggota_view.py             # Tampilan GUI untuk manajemen anggota
│   ├── buku_view.py                # Tampilan GUI manajemen buku & tombol Logout
│   └── login_view.py               # Tampilan GUI formulir login pengguna
├── .gitignore                      # Daftar berkas/folder yang diabaikan oleh Git
├── AplikasiPerpustakaan.spec       # Spesifikasi PyInstaller untuk build executable
├── main.py                         # Titik masuk utama aplikasi (menjalankan AuthController)
├── main_anggota.py                 # Titik masuk mandiri untuk modul anggota
├── README.md                       # Dokumentasi teknis aplikasi
├── requirements.txt                # Daftar pustaka dan dependensi Python
└── test_model.py                   # Skrip pengujian manual model database
```

---

## ⚙️ Panduan Instalasi & Konfigurasi Database MySQL

### 1. Prasyarat Sistem
- Python versi 3.10 atau yang lebih baru.
- MySQL Server (dapat menggunakan **Laragon**, **XAMPP**, atau MySQL Standalone).
- Git (opsional, untuk *version control*).

### 2. Konfigurasi Basis Data MySQL
Pastikan servis MySQL telah aktif, lalu buat basis data bernama `perpustakaan` dan eksekusi skrip SQL berikut untuk membuat tabel dan data awal:

```sql
CREATE DATABASE IF NOT EXISTS perpustakaan;
USE perpustakaan;

-- 1. Tabel users untuk autentikasi dan role-based access
CREATE TABLE IF NOT EXISTS users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL, -- Menyimpan hash SHA-256 (64 karakter)
    role ENUM('admin', 'anggota') NOT NULL
);

-- 2. Tabel buku untuk katalog inventaris perpustakaan
CREATE TABLE IF NOT EXISTS buku (
    id_buku INT AUTO_INCREMENT PRIMARY KEY,
    judul VARCHAR(255) NOT NULL,
    penulis VARCHAR(255) NOT NULL,
    tahun_terbit INT NOT NULL
);

-- 3. Tabel anggota untuk data keanggotaan
CREATE TABLE IF NOT EXISTS anggota (
    id_anggota INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    alamat TEXT NOT NULL
);

-- Data Pengguna Awal (Password default: admin123 dan anggota123 yang telah di-hash SHA-256)
-- Hash 'admin123'   : 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9
-- Hash 'anggota123' : 0192023a7bbd73250516f069df18b500eb3ac6e346c48589cb88a3e97d9157f9
INSERT INTO users (username, password, role) VALUES 
('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin'),
('anggota', '0192023a7bbd73250516f069df18b500eb3ac6e346c48589cb88a3e97d9157f9', 'anggota')
ON DUPLICATE KEY UPDATE username=username;
```

Konfigurasi koneksi database terdapat pada berkas `config/database.py`:
```python
self.host = 'localhost'
self.db_name = 'perpustakaan'
self.username = 'root'
self.password = ''  # Sesuaikan jika MySQL Anda memiliki password
```

### 3. Instalasi Dependensi Python
Buka terminal pada direktori proyek, disarankan membuat dan mengaktifkan virtual environment terlebih dahulu:

```bash
# Windows
python -m venv env
env\Scripts\activate

# Instal seluruh dependensi proyek
pip install -r requirements.txt
```

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Menjalankan Aplikasi Utama (Login & Sistem Perpustakaan)
```bash
python main.py
```
Gunakan akun berikut untuk menguji perbedaan otorisasi:
- **Akun Admin**: Username: `admin` | Password: `admin123` *(Akses penuh)*
- **Akun Anggota**: Username: `anggota` | Password: `anggota123` *(Akses terkunci/read-only)*

### 2. Menjalankan Modul Manajemen Anggota
```bash
python main_anggota.py
```

### 3. Menjalankan Pengecekan Kualitas Kode (Flake8 Linter)
```bash
flake8 models/ controllers/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

### 4. Menjalankan Pengujian Otomatis (Pytest Unit Testing)
```bash
python -m pytest -v
```

### 5. Menjalankan File Executable (.exe)
Aplikasi dapat dijalankan langsung tanpa interpreter Python melalui file yang telah dibuild:
```text
dist/AplikasiPerpustakaan.exe
```
File executable ini juga tersedia pada menu **Releases (v1.0.0)** di repositori GitHub ini.
