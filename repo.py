import os
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyperclip  
from github import Github

def get_user_info():
    """Kullanıcı adını, e-postasını ve token'ı alır."""
    global username, email, token

    username = username_entry.get()
    email = email_entry.get()
    token = token_entry.get()

    # En azından bir alan doldurulmalı
    if not username and not email and not token:
        messagebox.showerror("Hata", "Lütfen en az bir alan doldurun.")
        return

    # Ev dizini ile github klasörünü birleştirin
    bilgiler_dosyasi = os.path.join(os.path.expanduser("~"), "github", "bilgiler.txt")

    # Dosyayı oku ve önceki değerleri al
    try:
        with open(bilgiler_dosyasi, "r") as f:
            eski_username, eski_email, eski_token = f.readline().strip().split(",")
    except FileNotFoundError:
        eski_username = ""
        eski_email = ""
        eski_token = ""

    # Yeni değerleri kullanarak eski değerleri güncelle
    if username:
        eski_username = username
    if email:
        eski_email = email
    if token:
        eski_token = token

    # Güncellenmiş bilgileri dosyaya yaz
    with open(bilgiler_dosyasi, "w") as f:
        f.write(f"{eski_username},{eski_email},{eski_token}")

    # Giriş alanlarını temizleyin
    username_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    token_entry.delete(0, tk.END)

    messagebox.showinfo("Bilgi", "Kullanıcı bilgileri kaydedildi!")

def create_project():
    """Yeni bir proje klasörü oluşturur ve Git işlemlerini gerçekleştirir."""
    repo_name = repo_name_entry.get()

    if not repo_name:
        messagebox.showerror("Hata", "Lütfen repo adını girin.")
        return

    # Kullanıcı bilgileri dosyasından oku
    try:
        # Ev dizini ile github klasörünü birleştirin
        bilgiler_dosyasi = os.path.join(os.path.expanduser("~"), "github", "bilgiler.txt")
        with open(bilgiler_dosyasi, "r") as f:
            username, email, token = f.readline().strip().split(",")
    except FileNotFoundError:
        # Eğer dosya yoksa, kullanıcı adı, e-posta ve token zorunludur
        username = username_entry.get()
        email = email_entry.get()
        token = token_entry.get()

        if not username or not email or not token:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

    try:
		
        # GitHub API'sine bağlan
        g = Github(token)
        user = g.get_user()

        # Yeni repo oluştur
        try:
            repo = user.create_repo(repo_name)
            messagebox.showinfo("Başarılı", f"GitHub deposu başarıyla oluşturuldu: {repo.html_url}")

        except Exception as e:
            # Eğer depo zaten varsa hata mesajı göster
            if "name already exists" in str(e):
                messagebox.showinfo("Bilgi", f"Depo zaten var! Zaten var olan bir depoya erişmek için 'git clone' kullanabilirsiniz.")
        

        # git clone ile kopyala
        
        
        subprocess.run(["git", "clone", f"git@github.com:{username}/{repo_name}.git"])
        os.chdir(repo_name)

        # Dosyalar oluştur
        with open("main.py", "w") as f:
            f.write("# Bu Python projesinin ana dosyası\n")

        with open("requirements.txt", "w") as f:
            f.write("requests\n")

        with open(".gitignore", "w") as f:
            f.write("venv/\n")

        with open("README.md", "w") as f:
            f.write("# Python Projem\n")

        print(f"{repo_name} adlı proje klasörü başarıyla oluşturuldu.")

        # Git başlatın
        subprocess.run(["git", "init"])
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "İlk commit"])
        subprocess.run(["git", "push", "-u", "origin", "main"])

        messagebox.showinfo("Başarılı", "Proje başarıyla oluşturuldu.")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

def generate_rsa():
    """keygen.py dosyasını çalıştırır."""
    try:
        # Ev dizini ile github klasörünü birleştirin
        keygen_dosyasi = os.path.join(os.path.expanduser("~"), "github", "keygen.py")
        subprocess.run(["python", keygen_dosyasi])
        # RSA değerini güncellemek için update_rsa_text()'i çağırın
        update_rsa_text() 
        messagebox.showinfo("Bilgi", "RSA anahtarı oluşturuldu.")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

def update_rsa_text():
    """id_rsa.pub dosyasındaki RSA değerini alır ve label'a yazar."""
    try:
        # Doğru dosya yolunu kullan
        ssh_dir = os.path.join(os.path.expanduser("~"), ".ssh")
        rsa_file = os.path.join(ssh_dir, "id_rsa.pub")
        with open(rsa_file, "r") as f:
            rsa_value = f.read()
            rsa_label.delete("1.0", tk.END)  # Mevcut metni sil
            rsa_label.insert(tk.END, rsa_value)  # Yeni metni ekle
    except FileNotFoundError:
        rsa_label.delete("1.0", tk.END)
        rsa_label.insert(tk.END, "RSA Anahtarı Oluşturulmadı")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

def copy_rsa():
    """RSA değerini panoya kopyalar."""
    try:
        rsa_value = rsa_label.get("1.0", tk.END)
        pyperclip.copy(rsa_value) 
        messagebox.showinfo("Bilgi", "RSA anahtarı panoya kopyalandı.")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
        
        
calisma_dizini = os.path.join(os.path.expanduser("~"), "github")        
os.chdir(calisma_dizini)
# Tkinter Penceresi Oluştur
window = tk.Tk()
window.title("GitHub Proje Oluşturucu")

# Kullanıcı Bilgileri
username_label = ttk.Label(window, text="GitHub Kullanıcı Adı:")
username_label.grid(row=0, column=0, padx=5, pady=5)
username_entry = ttk.Entry(window)
username_entry.grid(row=0, column=1, padx=5, pady=5)

email_label = ttk.Label(window, text="E-Posta:")
email_label.grid(row=1, column=0, padx=5, pady=5)
email_entry = ttk.Entry(window)
email_entry.grid(row=1, column=1, padx=5, pady=5)

token_label = ttk.Label(window, text="GitHub Personal Access Token:")
token_label.grid(row=2, column=0, padx=5, pady=5)
token_entry = ttk.Entry(window, show="*")
token_entry.grid(row=2, column=1, padx=5, pady=5)

save_button = ttk.Button(window, text="Kaydet", command=get_user_info)
save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Proje Oluşturma
repo_name_label = ttk.Label(window, text="Repo Adı:")
repo_name_label.grid(row=4, column=0, padx=5, pady=5)
repo_name_entry = ttk.Entry(window)
repo_name_entry.grid(row=4, column=1, padx=5, pady=5)

create_button = ttk.Button(window, text="Proje Oluştur", command=create_project)
create_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

# RSA Anahtarı Bölümü
rsa_label = tk.Text(window, wrap=tk.WORD, height=3, width=50)  # tk.Text kullanarak oluştur
rsa_label.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")

# Scrollbar oluşturma
scrollbar = tk.Scrollbar(window, command=rsa_label.yview)
scrollbar.grid(row=6, column=1, sticky="ns")

# Label'ın scrollbar'ı kullanmasını sağlama
rsa_label.config(yscrollcommand=scrollbar.set)

copy_button = ttk.Button(window, text="Kopyala", command=copy_rsa)
copy_button.grid(row=7, column=0, padx=5, pady=5)

generate_button = ttk.Button(window, text="Generate RSA", command=generate_rsa)
generate_button.grid(row=7, column=1, padx=5, pady=5)

# Başlangıçta RSA değerini güncelle
update_rsa_text()

window.mainloop()
