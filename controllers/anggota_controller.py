import tkinter.messagebox as messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView

class AnggotaController:
    def __init__(self):
        self.model = AnggotaModel()
        self.view = AnggotaView()
        self.selected_id = None

        # Binding tombol ke fungsi
        self.view.btn_simpan.configure(command=self.simpan_data)
        if hasattr(self.view, 'btn_perbarui'):
            self.view.btn_perbarui.configure(command=self.perbarui_data)
        elif hasattr(self.view, 'btn_update'):
            self.view.btn_update.configure(command=self.perbarui_data)

        if hasattr(self.view, 'btn_hapus'):
            self.view.btn_hapus.configure(command=self.hapus_data)
        elif hasattr(self.view, 'btn_delete'):
            self.view.btn_delete.configure(command=self.hapus_data)

        # Event listener klik tabel
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_data)

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_anggota = self.model.get_all_anggota()
        for anggota in data_anggota:
            self.view.tabel.insert("", "end", values=(anggota['id_anggota'], anggota['nama'], anggota['alamat']))

    def bersihkan_form(self):
        self.view.entry_nama.delete(0, 'end')
        self.view.entry_alamat.delete(0, 'end')
        self.selected_id = None

    def pilih_data(self, event=None):
        selected = self.view.tabel.selection()
        if selected:
            values = self.view.tabel.item(selected[0], 'values')
            self.selected_id = values[0]
            
            self.view.entry_nama.delete(0, 'end')
            self.view.entry_nama.insert(0, values[1])
            self.view.entry_alamat.delete(0, 'end')
            self.view.entry_alamat.insert(0, values[2])

    def simpan_data(self):
        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.create_anggota(nama, alamat)
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data anggota.")

    def perbarui_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data anggota yang akan diperbarui!")
            return

        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_anggota(self.selected_id, nama, alamat)
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal memperbarui data anggota.")

    def hapus_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data anggota yang akan dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus anggota ini?"):
            berhasil = self.model.delete_anggota(self.selected_id)
            if berhasil:
                messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
                self.bersihkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Gagal menghapus data anggota.")

    def run(self):
        self.view.mainloop()

if __name__ == "__main__":
    app = AnggotaController()
    app.run()