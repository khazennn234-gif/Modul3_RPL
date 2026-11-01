import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()
        self.selected_id = None  # Menyimpan id_buku yang sedang dipilih
        
        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")
        
        # Binding tombol simpan
        self.view.btn_simpan.configure(command=self.simpan_data)
        
        # Binding tombol perbarui / update
        if hasattr(self.view, 'btn_update'):
            self.view.btn_update.configure(command=self.perbarui_data)
        elif hasattr(self.view, 'btn_perbarui'):
            self.view.btn_perbarui.configure(command=self.perbarui_data)

        # Binding tombol hapus / delete
        if hasattr(self.view, 'btn_delete'):
            self.view.btn_delete.configure(command=self.hapus_data)
        elif hasattr(self.view, 'btn_hapus'):
            self.view.btn_hapus.configure(command=self.hapus_data)

        # Binding tombol logout
        if hasattr(self.view, 'btn_logout'):
            self.view.btn_logout.configure(command=self.logout)

        # Event listener klik baris tabel
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_data)
        
        # OTORISASI: Jika bukan admin (role anggota), kunci input dan tombol aksi
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            if hasattr(self.view, 'btn_update'):
                self.view.btn_update.configure(state="disabled")
            if hasattr(self.view, 'btn_delete'):
                self.view.btn_delete.configure(state="disabled")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")
            
        self.muat_data_tabel()
        
    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    def bersihkan_form(self):
        self.view.entry_judul.delete(0, 'end')
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_tahun.delete(0, 'end')
        self.selected_id = None

    def pilih_data(self, event=None):
        if self.user_role != "admin":
            return
        selected = self.view.tabel.selection()
        if selected:
            values = self.view.tabel.item(selected[0], 'values')
            self.selected_id = values[0]
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_judul.insert(0, values[1])
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_penulis.insert(0, values[2])
            self.view.entry_tahun.delete(0, 'end')
            self.view.entry_tahun.insert(0, values[3])
            
    def simpan_data(self):
        # Proteksi ganda di level controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return
            
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()
        
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
            
        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    def perbarui_data(self):
        # Proteksi ganda di level controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk memperbarui data!")
            return

        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data buku dari tabel yang ingin diperbarui!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if self.model.update_buku(self.selected_id, judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def hapus_data(self):
        # Proteksi ganda di level controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menghapus data!")
            return

        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data buku dari tabel yang ingin dihapus!")
            return

        konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data buku ini?")
        if konfirmasi:
            if self.model.delete_buku(self.selected_id):
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self.bersihkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    def logout(self):
        # Menutup jendela BukuView
        self.view.destroy()
        # Mengembalikan pengguna ke jendela LoginView melalui AuthController
        from controllers.auth_controller import AuthController
        auth_app = AuthController()
        auth_app.run()

    def run(self):
        self.view.mainloop()
