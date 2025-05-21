import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

class StegoTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganografi Programı")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)
        
        # Ana sekme kontrolü
        self.tab_control = ttk.Notebook(root)
        
        # Şifre Gizleme Sekmesi
        self.encode_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.encode_tab, text="Metin Gizle")
        
        # Şifre Çıkarma Sekmesi
        self.decode_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.decode_tab, text="Metin Çıkar")
        
        self.tab_control.pack(expand=1, fill="both")
        
        # Şifre Gizleme Sekmesi Bileşenleri
        self.setup_encode_tab()
        
        # Şifre Çıkarma Sekmesi Bileşenleri
        self.setup_decode_tab()
        
        # Uygulama durumu
        self.image_path = None
        self.encoded_image_path = None
        self.stego_image_path = None
    
    def setup_encode_tab(self):
        # Ana çerçeve
        main_frame = ttk.Frame(self.encode_tab, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Sol panel - Resim seçimi ve önizleme
        left_frame = ttk.LabelFrame(main_frame, text="Resim Seçimi", padding=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Resim önizleme alanı
        self.encode_preview = ttk.Label(left_frame, text="Resim burada görüntülenecek")
        self.encode_preview.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Resim seçme butonu
        self.select_image_btn = ttk.Button(left_frame, text="Resim Seç", command=self.select_image)
        self.select_image_btn.pack(fill="x", padx=5, pady=5)
        
        # Sağ panel - Metin giriş ve şifreleme
        right_frame = ttk.LabelFrame(main_frame, text="Gizlenecek Metin", padding=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Metin alanı
        ttk.Label(right_frame, text="Gizlenecek Metni Girin:").pack(anchor="w", padx=5, pady=2)
        self.secret_text = tk.Text(right_frame, height=10, width=40)
        self.secret_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Şifreleme butonu
        self.encode_btn = ttk.Button(right_frame, text="Metni Gizle", command=self.encode_message)
        self.encode_btn.pack(fill="x", padx=5, pady=5)
        
        # Kaydetme durumu
        self.encode_status = ttk.Label(right_frame, text="")
        self.encode_status.pack(fill="x", padx=5, pady=5)
    
    def setup_decode_tab(self):
        # Ana çerçeve
        main_frame = ttk.Frame(self.decode_tab, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Sol panel - Şifreli resim seçimi ve önizleme
        left_frame = ttk.LabelFrame(main_frame, text="Şifreli Resim Seçimi", padding=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Resim önizleme alanı
        self.decode_preview = ttk.Label(left_frame, text="Şifreli resim burada görüntülenecek")
        self.decode_preview.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Resim seçme butonu
        self.select_stego_btn = ttk.Button(left_frame, text="Şifreli Resim Seç", command=self.select_stego_image)
        self.select_stego_btn.pack(fill="x", padx=5, pady=5)
        
        # Sağ panel - Şifre çözme ve sonuç
        right_frame = ttk.LabelFrame(main_frame, text="Gizli Mesaj", padding=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Şifre çözme butonu
        self.decode_btn = ttk.Button(right_frame, text="Mesajı Çıkar", command=self.decode_message)
        self.decode_btn.pack(fill="x", padx=5, pady=5)
        
        # Çözülmüş metin alanı
        ttk.Label(right_frame, text="Çıkarılan Gizli Mesaj:").pack(anchor="w", padx=5, pady=2)
        self.decoded_text = tk.Text(right_frame, height=10, width=40)
        self.decoded_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Durum etiketi
        self.decode_status = ttk.Label(right_frame, text="")
        self.decode_status.pack(fill="x", padx=5, pady=5)
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Resim Seç",
            filetypes=[("PNG Dosyaları", "*.png"), ("Tüm Dosyalar", "*.*")]
        )
        
        if file_path:
            try:
                self.image_path = file_path
                self.display_image(self.encode_preview, file_path)
                self.root.title(f"StegoTool - {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Hata", f"Resim yüklenirken hata oluştu: {str(e)}")
    
    def select_stego_image(self):
        file_path = filedialog.askopenfilename(
            title="Şifreli Resim Seç",
            filetypes=[("PNG Dosyaları", "*.png"), ("Tüm Dosyalar", "*.*")]
        )
        
        if file_path:
            try:
                self.stego_image_path = file_path
                self.display_image(self.decode_preview, file_path)
            except Exception as e:
                messagebox.showerror("Hata", f"Resim yüklenirken hata oluştu: {str(e)}")
    
    def display_image(self, label, image_path):
        img = Image.open(image_path)
        
        # Görüntü boyutunu ayarla (maks 300x300)
        img.thumbnail((300, 300))
        
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo  # Referansı sakla
    
    def encode_message(self):
        if not self.image_path:
            messagebox.showwarning("Uyarı", "Lütfen önce bir resim seçin!")
            return
        
        secret_text = self.secret_text.get("1.0", "end-1c")
        if not secret_text:
            messagebox.showwarning("Uyarı", "Lütfen gizlenecek bir metin girin!")
            return
        
        try:
            # Yeni resmin kaydedileceği yeri seç
            save_path = filedialog.asksaveasfilename(
                title="Şifreli Resmi Kaydet",
                defaultextension=".png",
                filetypes=[("PNG Dosyaları", "*.png")]
            )
            
            if not save_path:
                return
            
            # Resmi yükle
            img = Image.open(self.image_path)
            
            # Resmin RGB formatına dönüştürülmesi
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Mesajı ikili sisteme dönüştür
            binary_message = ''.join(format(ord(char), '08b') for char in secret_text)
            binary_message += '00000000'  # Bitiş işareti (NULL karakter)
            
            # Resim verilerini al
            pixels = list(img.getdata())
            
            # Mesajı piksellere gizle
            new_pixels = []
            pixel_index = 0
            binary_index = 0
            
            # Mesajı gizle
            while binary_index < len(binary_message) and pixel_index < len(pixels):
                r, g, b = pixels[pixel_index]
                
                # Kırmızı kanalın en az önemli bitini değiştir
                if binary_index < len(binary_message):
                    r = r & ~1 | int(binary_message[binary_index])
                    binary_index += 1
                
                # Yeşil kanalın en az önemli bitini değiştir
                if binary_index < len(binary_message):
                    g = g & ~1 | int(binary_message[binary_index])
                    binary_index += 1
                
                # Mavi kanalın en az önemli bitini değiştir
                if binary_index < len(binary_message):
                    b = b & ~1 | int(binary_message[binary_index])
                    binary_index += 1
                
                new_pixels.append((r, g, b))
                pixel_index += 1
            
            # Kalan pikselleri ekle
            new_pixels.extend(pixels[pixel_index:])
            
            # Yeni resmi oluştur
            new_img = Image.new(img.mode, img.size)
            new_img.putdata(new_pixels)
            
            # Yeni resmi kaydet
            new_img.save(save_path)
            
            self.encoded_image_path = save_path
            self.encode_status.config(text=f"Metin başarıyla gizlendi ve kaydedildi:\n{os.path.basename(save_path)}")
            
            messagebox.showinfo("Başarılı", "Mesaj başarıyla resme gizlendi!")
        
        except Exception as e:
            messagebox.showerror("Hata", f"Mesaj gizlenirken bir hata oluştu: {str(e)}")
    
    def decode_message(self):
        if not self.stego_image_path:
            messagebox.showwarning("Uyarı", "Lütfen önce şifreli bir resim seçin!")
            return
        
        try:
            # Resmi yükle
            img = Image.open(self.stego_image_path)
            
            # Resmin piksellerini al
            pixels = list(img.getdata())
            
            # Gizli mesajı çıkar
            binary_message = ""
            
            for r, g, b in pixels:
                # Her pikselin en az önemli bitlerini al
                binary_message += str(r & 1)
                binary_message += str(g & 1)
                binary_message += str(b & 1)
                
                # Yeterli bit toplandı mı kontrol et
                if len(binary_message) >= 8 and binary_message[-8:] == "00000000":
                    break
            
            # Binary mesajı 8'li gruplara böl
            binary_chunks = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
            
            # Her 8'li grubu karaktere dönüştür
            decoded_text = ""
            for chunk in binary_chunks:
                if len(chunk) == 8:
                    if chunk == "00000000":  # Bitiş işareti
                        break
                    decoded_text += chr(int(chunk, 2))
            
            # Çözülmüş metni göster
            self.decoded_text.delete("1.0", "end")
            self.decoded_text.insert("1.0", decoded_text)
            
            self.decode_status.config(text="Mesaj başarıyla çıkarıldı!")
        
        except Exception as e:
            messagebox.showerror("Hata", f"Mesaj çıkarılırken bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StegoTool(root)
    root.mainloop()