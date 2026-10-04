from models.buku_model import BukuModel
from models.anggota_model import AnggotaModel

model_anggota = AnggotaModel()
model = BukuModel()

# 1. Menguji fungsi Create (menambah buku baru)
print("Menambahkan data buku...")
model.create_buku("Pemrograman Python MVC", "Guido van Rossum", 2023)
print("Data berhasil disimpan ke Laragon MySQL!")

# 2. Menguji fungsi Read (menampilkan data)
print("\n=== Daftar Buku ===")
daftar_buku = model.get_all_buku()
for buku in daftar_buku:
    print(f"[{buku['id_buku']}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")
    

# 3. Menguji fungsi Update (mengubah data buku)
print("\n=== Menguji fungsi Update ===")
# Misal kita mengubah buku dengan id_buku = 1
model.update_buku(1, "The Witcher", "Andrzej Sapkowski", 1986)
print("Data buku dengan ID 1 berhasil diubah!")

# 4. Menguji fungsi Delete (menghapus data buku)
print("\n=== Menguji fungsi Delete ===")
# Misal kita menghapus buku dengan id_buku = 2 (Pastikan ID 2 ada di database Anda)
model.delete_buku(3) 
print("Data buku dengan ID 3 berhasil dihapus!")

# 5. Menampilkan kembali data setelah Update dan Delete
print("\n=== Daftar Buku Setelah Diperbarui ===")
daftar_buku = model.get_all_buku()
for buku in daftar_buku:
    print(f"[{buku['id_buku']}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")
    
    

# Menambah data anggota baru
print("Menambahkan data anggota...")
model_anggota.create_anggota("Ferdi Atreus", "BTN baliase")
print("Data anggota berhasil disimpan!\n")

print("=== Daftar Anggota ===")
daftar_anggota = model_anggota.get_all_anggota()
for anggota in daftar_anggota:
    print(f"[{anggota['id_anggota']}] {anggota['nama']} - {anggota['alamat']}")