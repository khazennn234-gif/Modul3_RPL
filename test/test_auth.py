from unittest.mock import MagicMock, patch
from models.user_model import UserModel

def test_hash_password_konsisten():
    password_asli = "admin123"
    hash_1 = UserModel.hash_password(password_asli)
    hash_2 = UserModel.hash_password(password_asli)
    
    # Memastikan hasil hash tidak sama dengan plain text dan bersifat konsisten
    assert hash_1 != password_asli
    assert hash_1 == hash_2
    assert len(hash_1) == 64 # Panjang karakter standar SHA-256

def test_autentikasi_pengguna_berhasil():
    model = UserModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    
    # Simulasi kembalian data dari database ketika username & password cocok
    mock_cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "petugas",
        "role": "admin"
    }
    model.conn.cursor.return_value = mock_cursor
    
    hasil = model.autentikasi("petugas", "admin123")
    
    assert hasil is not None
    assert hasil["username"] == "petugas"
    assert hasil["role"] == "admin"

def test_register_user_berhasil():
    model = UserModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor
    
    password_plain = "anggota123"
    hasil = model.register_user("anggota_baru", password_plain, "anggota")
    
    assert hasil is True
    mock_cursor.execute.assert_called_once()
    
    # Memastikan password yang disimpan di database adalah hash SHA-256, bukan plain text
    args, _ = mock_cursor.execute.call_args
    query, params = args
    assert "INSERT INTO" in query
    assert params[0] == "anggota_baru"
    assert params[1] == UserModel.hash_password(password_plain)
    assert params[1] != password_plain
    assert len(params[1]) == 64
    assert params[2] == "anggota"
    
    model.conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_otorisasi_role_anggota_mengunci_tombol_aksi():
    # Menguji tombol simpan, perbarui, dan hapus terkunci (disabled) untuk role anggota
    with patch("controllers.buku_controller.BukuView") as mock_view_class, \
         patch("controllers.buku_controller.BukuModel"):
        mock_view = MagicMock()
        mock_view_class.return_value = mock_view
        
        from controllers.buku_controller import BukuController
        controller = BukuController(user_role="anggota")
        
        mock_view.btn_simpan.configure.assert_called_with(state="disabled", text="Akses Terkunci (Khusus Admin)")
        mock_view.btn_update.configure.assert_called_with(state="disabled")
        mock_view.btn_delete.configure.assert_called_with(state="disabled")

def test_logout_menutup_jendela_dan_membuka_login():
    # Menguji tombol logout menutup jendela buku dan membuka kembali form login
    with patch("controllers.buku_controller.BukuView") as mock_view_class, \
         patch("controllers.buku_controller.BukuModel"), \
         patch("controllers.auth_controller.AuthController") as mock_auth_class:
        mock_view = MagicMock()
        mock_view_class.return_value = mock_view
        
        from controllers.buku_controller import BukuController
        controller = BukuController(user_role="admin")
        controller.logout()
        
        mock_view.destroy.assert_called_once()
        mock_auth_class.assert_called_once()
