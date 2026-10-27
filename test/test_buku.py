from unittest.mock import MagicMock
from models.buku_model import BukuModel

def test_create_buku_berhasil():
    model = BukuModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

    assert hasil is True
    mock_cursor.execute.assert_called_once()
    model.conn.commit.assert_called_once()

# --- FUNGSI UJI BARU (TUGAS 3) ---
def test_get_all_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Menyiapkan data dummy return_value dari fetchall()
    data_dummy = [
        {'id_buku': 1, 'judul': 'Buku Testing 1', 'penulis': 'Penulis A', 'tahun_terbit': 2026},
        {'id_buku': 2, 'judul': 'Buku Testing 2', 'penulis': 'Penulis B', 'tahun_terbit': 2025}
    ]
    mock_cursor.fetchall.return_value = data_dummy

    # Melakukan eksekusi fungsi
    hasil = model.get_all_buku()

    # Memverifikasi hasil pengujian
    assert hasil == data_dummy
    assert len(hasil) == 2
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchall.assert_called_once()