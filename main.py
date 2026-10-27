import sys
from controllers.buku_controller import BukuController
from controllers.anggota_controller import AnggotaController

if __name__ == "__main__":
    # Jalankan Data Anggota (default) atau Data Buku melalui argumen:
    # Contoh:
    #   python main.py          -> Menjalankan Data Anggota (seperti pada screenshot)
    #   python main.py buku     -> Menjalankan Data Buku
    #   python main.py anggota  -> Menjalankan Data Anggota
    if len(sys.argv) > 1 and "buku" in sys.argv[1].lower():
        app = BukuController()
    else:
        app = AnggotaController()
        
    app.run()