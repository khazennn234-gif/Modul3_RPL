import customtkinter as ctk
from tkinter import ttk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class BukuView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("800x500")

        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1) # Kolom Kiri (Form)
        self.grid_columnconfigure(1, weight=2) # Kolom Kanan (Tabel lebih lebar)
        self.grid_rowconfigure(0, weight=1)

        # ==================================
        # FRAME KIRI: FORMULIR INPUT BUKU
        # ==================================
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Data Buku", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Input
        self.entry_judul = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Judul Buku")
        self.entry_judul.pack(pady=8, padx=15, fill="x")

        self.entry_penulis = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Nama Penulis")
        self.entry_penulis.pack(pady=8, padx=15, fill="x")

        self.entry_tahun = ctk.CTkEntry(self.frame_kiri, placeholder_text="Tahun Terbit (Misal: 2024)")
        self.entry_tahun.pack(pady=8, padx=15, fill="x")

        # Tombol Aksi
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data", fg_color="green")
        self.btn_simpan.pack(pady=(15, 6), padx=15, fill="x")
        
        # Tombol Update / Perbarui
        self.btn_update = ctk.CTkButton(self.frame_kiri, text="Perbarui Data (Update)", fg_color="blue")
        self.btn_update.pack(pady=6, padx=15, fill="x")
        self.btn_perbarui = self.btn_update
        
        # Tombol Delete / Hapus
        self.btn_delete = ctk.CTkButton(self.frame_kiri, text="Hapus Data (Delete)", fg_color="red")
        self.btn_delete.pack(pady=6, padx=15, fill="x")
        self.btn_hapus = self.btn_delete

        # Tombol Logout
        self.btn_logout = ctk.CTkButton(self.frame_kiri, text="Logout", fg_color="#555555", hover_color="#333333", command=self.logout)
        self.btn_logout.pack(pady=(6, 15), padx=15, fill="x")

        # ==================================
        # FRAME KANAN: TABEL DAFTAR BUKU
        # ==================================
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Daftar Koleksi Buku", font=("Arial", 16, "bold")).pack(pady=15)

        # Styling Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=24,
                        fieldbackground="white")
        style.configure("Treeview.Heading",
                        background="#f9f9f9",
                        foreground="black",
                        font=("Arial", 10, "bold"))
        style.map("Treeview", background=[('selected', '#1f538d')], foreground=[('selected', 'white')])

        # Komponen Tabel (Treeview dari tkinter standar)
        kolom = ("id", "judul", "penulis", "tahun")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        # Konfigurasi Header Tabel
        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("penulis", text="Penulis")
        self.tabel.heading("tahun", text="Tahun")

        # Konfigurasi Lebar Kolom
        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("judul", width=150)
        self.tabel.column("penulis", width=120)
        self.tabel.column("tahun", width=80, anchor="center")

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

    def logout(self):
        # Menutup jendela BukuView
        self.destroy()
        # Mengembalikan pengguna ke jendela LoginView
        try:
            from controllers.auth_controller import AuthController
            app = AuthController()
            app.run()
        except Exception:
            from views.login_view import LoginView
            login = LoginView()
            login.mainloop()

# Blok eksekusi untuk menguji tampilan grafis
if __name__ == "__main__":
    app = BukuView()
    app.mainloop()
