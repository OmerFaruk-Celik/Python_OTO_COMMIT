#!/usr/bin/python3
import os
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyperclip
from github import Github
import re
from github3 import GitHub



statusRSA=False
def get_user_info():
    """Kullanıcı adını, e-postasını ve token'ı alır."""
    global bilgiler_dosyasi 
    global username, email, token

    username = username_entry.get()
    email = email_entry.get()
    token = token_entry.get()

    # En azından bir alan doldurulmalı
    if not username and not email and not token:
        messagebox.showerror("Hata", "Lütfen en az bir alan doldurun.")
        return

    # Ev dizini ile github klasörünü birleştirin


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
    if statusRSA:
        repo_name = repo_name_entry.get()

        if not repo_name:
            messagebox.showerror("Hata", "Lütfen repo adını girin.")
            return

        # Kullanıcı bilgileri dosyasından oku
        try:
            # Ev dizini ile github klasörünü birleştirin
            
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

        os.chdir("..")
    else:
        messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun ve aktif hale getirin.")

def generate_rsa():
    """keygen.py dosyasını çalıştırır."""
    if True:
        messagebox.showinfo("Bilgi", "RSA anahtarı zaten oluşturulmuş ve aktif.")
    else:
        try:
            # Ev dizini ile github klasörünü birleştirin
            keygen_dosyasi = os.path.join(os.path.expanduser("~"), "github", "MAIN","Python_OTO_COMMIT", "keygen.py")
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
    if True:
        try:
            rsa_value = rsa_label.get("1.0", tk.END)
            pyperclip.copy(rsa_value)
            messagebox.showinfo("Bilgi", "RSA anahtarı panoya kopyalandı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
    else:
        messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun.")

def download_repos():
    """Tüm repoları indirir."""
    global bilgiler_dosyasi 
    if statusRSA:
        try:
            # Ev dizini ile github klasörünü birleştirin

            with open(bilgiler_dosyasi, "r") as f:
                username, _, token = f.readline().strip().split(",")

            # Download işlemini başlat
            download_repos_from_github(token, username)

            messagebox.showinfo("Bilgi", "Tüm repolar indirildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
    else:
        messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun ve aktif hale getirin.")

def download_repos_from_github(token, username):
    """Belirtilen token ve kullanıcı adı ile GitHub'dan belirtilen repoları indirir."""

    gh = Github(token)
    user = gh.get_user(username)

    # ~/github dizinini kontrol et
    github_dir = os.path.expanduser("~/github")
    if not os.path.exists(github_dir):
        os.makedirs(github_dir)

    for repo in user.get_repos():
        repo_name = repo.name
        repo_url = f"git@github.com:{username}/{repo_name}.git"  # Git URL'si

        # Repo'nun zaten indirilmiş olup olmadığını kontrol et
        repo_path = os.path.join(github_dir, repo_name)
        if os.path.exists(repo_path):
            print(f"{repo_name} adlı repo zaten indirilmiş.")
            continue

        # Repo'yu indir
        try:
            subprocess.run(["git", "clone", repo_url])
            print(f"{repo_name} adlı repo başarıyla indirildi.")
        except Exception as e:
            print(f"{repo_name} adlı repo indirme sırasında hata oluştu: {e}")

def check_user_info():
    """Kullanıcı bilgileri dosyasını kontrol eder ve sonuçları gösterir."""
    global bilgiler_dosyasi 
    try:
        # Ev dizini ile github klasörünü birleştirin

        with open(bilgiler_dosyasi, "r") as f:
            username, email, token = f.readline().strip().split(",")

        # Kontrol sonuçlarını göster
        username_status_label.config(text=f"Kullanıcı Adı: {username}", foreground="green")
        email_status_label.config(text=f"E-Posta: {email}", foreground="green")
        if len(token) > 50:
            token = "Available"
        else:
            token = "No Found Any Token!"
        token_status_label.config(text=f"Token: {token}", foreground="green")

    except FileNotFoundError:
        # Dosya bulunamadıysa, tüm alanlar boş olacak
        username_status_label.config(text="Kullanıcı Adı:", foreground="red")
        email_status_label.config(text="E-Posta:", foreground="red")
        token_status_label.config(text="Token:", foreground="red")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

def sil_repo(token, username, repo_name):
    """Belirtilen token ve kullanıcı adı ile GitHub'dan belirtilen repoyu siler."""
    if statusRSA:
        gh = GitHub(token=token)

        try:
            repo = gh.repository(username, repo_name)
            # Silme işlemi onayı
            sonuc = messagebox.askyesno("Onay", f"{repo_name} adlı repoyu silmek istediğinizden emin misiniz?")
            if sonuc:
                repo.delete()
                print(f"{repo_name} adlı repo başarıyla silindi.")

                # Yerel dizindeki klasörü sil
                repo_path = os.path.join(os.path.expanduser("~/github"), repo_name)
                if os.path.exists(repo_path):
                    subprocess.run(["rm", "-rf", repo_path])
                    print(f"{repo_path} klasörü başarıyla silindi.")
            else:
                print(f"{repo_name} adlı repo silinmedi.")

        except Exception as e:
            print(f"Repo silinirken hata oluştu: {e}")
    else:
        messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun ve aktif hale getirin.")

def sil_repo_arayuz(): 
    """Repo silme arayüzünü oluşturur."""
    global bilgiler_dosyasi
    def sil():
        """Repo silme işlemini başlatır."""
        if statusRSA:
            repo_name = repo_entry.get()
            if not repo_name:
                messagebox.showerror("Hata", "Lütfen repo adını girin.")
                return

            # Kullanıcı bilgileri dosyasından oku
            try:
  
                with open(bilgiler_dosyasi, "r") as f:
                    username, _, token = f.readline().strip().split(",")

                # Token ve kullanıcı adının mevcut olup olmadığını kontrol et
                if not username or not token:
                    messagebox.showerror("Hata", "Lütfen önce kullanıcı bilgilerini girin.")
                    return

                sil_repo(token, username, repo_name)
                messagebox.showinfo("Bilgi", f"{repo_name} adlı repo başarıyla silindi.")
                repo_entry.delete(0, tk.END)

            except FileNotFoundError:
                messagebox.showerror("Hata", "Kullanıcı bilgileri dosyası bulunamadı.")
            except Exception as e:
                messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
        else:
            messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun ve aktif hale getirin.")

    # Pencere oluştur
    sil_pencere = tk.Toplevel(window)
    sil_pencere.title("Repo Sil")

    repo_label = ttk.Label(sil_pencere, text="Repo Adı:")
    repo_label.grid(row=0, column=0, padx=5, pady=5)
    repo_entry = ttk.Entry(sil_pencere)
    repo_entry.grid(row=0, column=1, padx=5, pady=5)

    sil_button = ttk.Button(sil_pencere, text="Sil", command=sil)
    sil_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

def fork_repo(token, username, repo_path):
    """Belirtilen token ve kullanıcı adı ile GitHub'dan belirtilen repoyu forklar."""
    if statusRSA:
        gh = GitHub(token=token)

        # Repo yolundan owner ve repo adını ayırma
        repo_path = repo_path.replace(".git", "")# .git uzantısını kaldır
        print(repo_path)
        match = re.search(r'github.com/([^/]+)/([^/]+)', repo_path)
        if match:
            owner = match.group(1)
            repo_name = match.group(2)
        else:
            print("Geçersiz repo yolu.")
            return

        # Forklama isteği gönderin
        fork = gh.repository(owner, repo_name).create_fork()

        print(f"Repo başarıyla forklandı: {fork.html_url}")
    else:
        messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun ve aktif hale getirin.")

def fork_project():
    """Forklama işlemini başlatır."""
    global bilgiler_dosyasi
    if statusRSA:
        try:
            # Ev dizini ile github klasörünü birleştirin
            
            with open(bilgiler_dosyasi, "r") as f:
                username, _, token = f.readline().strip().split(",")

            repo_path = fork_repo_entry.get()
            if not repo_path:
                messagebox.showerror("Hata", "Lütfen forklanacak repo'nun URL'sini veya yolunu girin.")
                return

            fork_repo(token, username, repo_path)
            messagebox.showinfo("Bilgi", "Repo başarıyla forklandı.")

        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
    else:
        messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun ve aktif hale getirin.")

def fork_repo_arayuz():
    """Repo forklama arayüzünü oluşturur."""
    global bilgiler_dosyasi 
    def fork():
        """Repo forklama işlemini başlatır."""
        if statusRSA:
            repo_path = fork_repo_entry.get()
            print(repo_path)
            if not repo_path:
                messagebox.showerror("Hata", "Lütfen forklanacak repo'nun URL'sini veya yolunu girin.")
                return

            # Kullanıcı bilgileri dosyasından oku
            try:

                with open(bilgiler_dosyasi, "r") as f:
                    username, _, token = f.readline().strip().split(",")

                # Token ve kullanıcı adının mevcut olup olmadığını kontrol et
                if not username or not token:
                    messagebox.showerror("Hata", "Lütfen önce kullanıcı bilgilerini girin.")
                    return

                fork_repo(token, username, repo_path)
                messagebox.showinfo("Bilgi", "Repo başarıyla forklandı.")
                fork_repo_entry.delete(0, tk.END)

            except FileNotFoundError:
                messagebox.showerror("Hata", "Kullanıcı bilgileri dosyası bulunamadı.")
            except Exception as e:
                messagebox.showerror("Hata", f"fork_repo_arayuz() Bir hata oluştu: {e}")
        else:
            messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun ve aktif hale getirin.")

    # Pencere oluştur
    fork_pencere = tk.Toplevel(window)
    fork_pencere.title("Repo Forkla")

    fork_repo_label = ttk.Label(fork_pencere, text="Repo URL'si:")
    fork_repo_label.grid(row=0, column=0, padx=5, pady=5)
    fork_repo_entry = ttk.Entry(fork_pencere)
    fork_repo_entry.grid(row=0, column=1, padx=5, pady=5)

    fork_button = ttk.Button(fork_pencere, text="Forkla", command=fork)
    fork_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

def rsaState():
    global statusRSA
    """RSA anahtar durumunu kontrol eder ve label'a yazar."""
    try:
        # SSH bağlantısını test edin
        process = subprocess.run(["ssh", "-T", "git@github.com"], capture_output=True)
        if process.returncode == 1:
            rsa_status_label.config(text="Aktif", foreground="green")
            statusRSA=True
            return "Aktif"
        else:
            rsa_status_label.config(text="Aktif Değil", foreground="red")
            statusRSA=False
            return "Aktif Değil"
    except Exception as e:
        rsa_status_label.config(text="Hata", foreground="red")
        return "Hata"

default = os.path.join(os.path.expanduser("~"), "github")
def update_repo_list(path=default,state=False):
    """GitHub'dan repoları alır ve listbox'a ekler."""
    global bilgiler_dosyasi 
    if True:
        try:
            #get_user_info()
            check_user_info()
            update_rsa_text()
            if not state:
                rsaState()
            
            # Ev dizini ile github klasörünü birleştirin

            with open(bilgiler_dosyasi, "r") as f:
                username, _, token = f.readline().strip().split(",")

            gh = Github(token)
            user = gh.get_user(username)

            repo_listbox.delete(0, tk.END)  # Mevcut listeyi temizle
            if path==default:
                os.chdir(path)			
                for repo in user.get_repos():
                    repo_listbox.insert(tk.END, repo.name)
            else:
                for files in os.listdir(path):
                    repo_listbox.insert(tk.END, files)			    	
        except FileNotFoundError:
            messagebox.showerror("Hata", "bilgiler.txt dosyası bulunamadı. Lütfen dosyayı kontrol edin.")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
    else:
        messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun ve aktif hale getirin.")


# Sağ Tık Menüsü Fonksiyonları
def sil_secilen_repo(secilen_repo):
    """Seçilen repoyu silmek için kullanılır."""
    global bilgiler_dosyasi 
    if statusRSA:
        if secilen_repo:
            # Kullanıcı bilgileri dosyasından oku
            try:
                with open(bilgiler_dosyasi, "r") as f:
                    username, _, token = f.readline().strip().split(",")

                # Token ve kullanıcı adının mevcut olup olmadığını kontrol et
                if not username or not token:
                    messagebox.showerror("Hata", "Lütfen önce kullanıcı bilgilerini girin.")
                    return

                sil_repo(token, username, secilen_repo)
                messagebox.showinfo("Bilgi", f"{secilen_repo} adlı repo başarıyla silindi.")
                repo_listbox.delete(tk.ANCHOR)  # Listbox'tan repoyu sil

            except FileNotFoundError:
                messagebox.showerror("Hata", "Kullanıcı bilgileri dosyası bulunamadı.")
            except Exception as e:
                messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
    else:
        messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun ve aktif hale getirin.")

def kopyala_secilen_repo(secilen_repo):
    if True:
        if secilen_repo:
            pyperclip.copy(secilen_repo)
            messagebox.showinfo("Bilgi", f"{secilen_repo} adlı repo panoya kopyalandı.")
    else:
        messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun ve aktif hale getirin.")

def duzenle_secilen_repo(secilen_repo):
    """Seçilen repoyu düzenlemek için kullanılır."""
    if True:
        if secilen_repo:
            messagebox.showinfo("Bilgi", f"{secilen_repo} adlı repo düzenleniyor...")
    else:
        messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun ve aktif hale getirin.")



def sag_tik_goster(event):
    """Sağ tıklama üzerine menüyü gösterir."""
    try:
        repo_listbox.selection_set(repo_listbox.nearest(event.y))  # En yakın öğeyi seç
    except tk.TclError:
        pass  # Eğer tıklama listbox'ın dışındaysa hata yakala
    sag_tik_menu.post(event.x_root, event.y_root)


def gir_repo(event):
    """Seçilen repo klasörüne girer."""
    if True:
        secilen_repo = repo_listbox.get(tk.ANCHOR)
        print(secilen_repo)
        if secilen_repo:
            bulundugu_dizin=os.getcwd()
            repo_yolu = os.path.join(bulundugu_dizin, secilen_repo)
            if os.path.isdir(repo_yolu):
                os.chdir(repo_yolu)  # Klasöre gir
                print(f"{secilen_repo} adlı klasöre girildi.")
                # Repo listesini güncellemek için update_repo_list'i çağırın
                
                update_repo_list(repo_yolu,True)  
            else:
                messagebox.showerror("Hata", f"{secilen_repo} adlı klasör bulunamadı.")
    else:
        messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun ve aktif hale getirin.")

def geri_al():
	
	os.chdir("..")
	bulundugu_dizin=os.getcwd()
	update_repo_list(bulundugu_dizin,True)
	
	

def show_repo_details():
    """Seçili repo'nun detaylarını gösterir."""
    global bilgiler_dosyasi 
    if statusRSA:
        try:
            selected_repo = repo_listbox.get(tk.ANCHOR)
            if not selected_repo:
                messagebox.showinfo("Bilgi", "Lütfen bir repo seçin.")
                return

            # Ev dizini ile github klasörünü birleştirin
            
            
            with open(bilgiler_dosyasi, "r") as f:
                username, _, token = f.readline().strip().split(",")

            gh = Github(token)
            user = gh.get_user(username)
            repo = user.get_repo(selected_repo)

            # Detayları göster
            details_window = tk.Toplevel(window)
            details_window.title(f"{selected_repo} Detayları")

            # Fork Sayısı
            fork_count_label = ttk.Label(details_window, text=f"Fork Sayısı: {repo.forks_count}")
            fork_count_label.grid(row=0, column=0, padx=5, pady=5)

            # Takipçi Sayısı
            star_count_label = ttk.Label(details_window, text=f"Yıldız Sayısı: {repo.stargazers_count}")
            star_count_label.grid(row=1, column=0, padx=5, pady=5)

            # Takipçiler
            watchers_count_label = ttk.Label(details_window, text=f"İzleyenler: {repo.watchers_count}")
            watchers_count_label.grid(row=2, column=0, padx=5, pady=5)

            # Takipçi Listesi (Ayrıntılı)
            watchers_label = ttk.Label(details_window, text="İzleyenler:")
            watchers_label.grid(row=3, column=0, padx=5, pady=5)
            watchers_list = tk.Listbox(details_window, width=30, height=5)
            watchers_list.grid(row=4, column=0, padx=5, pady=5)
            for watcher in repo.get_stargazers():
                watchers_list.insert(tk.END, watcher.login)

        except FileNotFoundError:
            messagebox.showerror("Hata", "bilgiler.txt dosyası bulunamadı. Lütfen dosyayı kontrol edin.")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
    else:
        messagebox.showerror("Hata", "Lütfen önce RSA anahtarınızı oluşturun ve aktif hale getirin.")





        

calisma_dizini = os.path.join(os.path.expanduser("~"), "github")
bilgiler_dosyasi = os.path.join(os.path.expanduser("~"), "github", "MAIN","Python_OTO_COMMIT", "bilgiler.txt")
os.chdir(calisma_dizini)
# Tkinter Penceresi Oluştur
window = tk.Tk()
window.title("GitHub Proje Oluşturucu")

# Kullanıcı Bilgileri
user_frame = ttk.Frame(window)
user_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

username_label = ttk.Label(user_frame, text="GitHub Kullanıcı Adı:")
username_label.grid(row=0, column=0, padx=5, pady=5)
username_entry = ttk.Entry(user_frame)
username_entry.grid(row=0, column=1, padx=5, pady=5)

email_label = ttk.Label(user_frame, text="E-Posta:")
email_label.grid(row=1, column=0, padx=5, pady=5)
email_entry = ttk.Entry(user_frame)
email_entry.grid(row=1, column=1, padx=5, pady=5)

token_label = ttk.Label(user_frame, text="GitHub Personal Access Token:")
token_label.grid(row=2, column=0, padx=5, pady=5)
token_entry = ttk.Entry(user_frame, show="*")
token_entry.grid(row=2, column=1, padx=5, pady=5)

save_button = ttk.Button(user_frame, text="Kaydet", command=get_user_info)
save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Kontrol Durumunu Gösteren Label'lar
username_status_label = ttk.Label(user_frame, text="", foreground="black")
username_status_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

email_status_label = ttk.Label(user_frame, text="", foreground="black")
email_status_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

token_status_label = ttk.Label(user_frame, text="", foreground="black")
token_status_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Proje Oluşturma
project_frame = ttk.Frame(window)
project_frame.grid(row=7, column=0, padx=5, pady=5, sticky="nw")

repo_name_label = ttk.Label(project_frame, text="Repo Adı:")
repo_name_label.grid(row=0, column=0, padx=5, pady=5)
repo_name_entry = ttk.Entry(project_frame)
repo_name_entry.grid(row=0, column=1, padx=5, pady=5)

create_button = ttk.Button(project_frame, text=" Proje Oluştur ", command=create_project)
create_button.grid(row=1, column=1,columnspan=1, padx=5, pady=10)

# Repo Silme
sil_button = ttk.Button(project_frame, text="Repo Sil", command=sil_repo_arayuz)
sil_button.grid(row=1, column=0, columnspan=1,padx=5, pady=5)

# Repo Forklama
fork_button = ttk.Button(project_frame, text="Repo Forkla", command=fork_repo_arayuz)
fork_button.grid(row=1, column=2, padx=5, pady=5)

# Download All Repos butonu
download_button = ttk.Button(project_frame, text="Download All Repos", command=download_repos)
download_button.grid(row=0, column=2, padx=5, pady=5)

# RSA Anahtarı Bölümü
rsa_frame = ttk.Frame(window)
rsa_frame.grid(row=8, column=0, padx=5, pady=5, sticky="nw")

rsa_label = tk.Text(rsa_frame, wrap=tk.WORD, height=2, width=30)  # Boyutu küçült
rsa_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Scrollbar oluşturma
scrollbar = tk.Scrollbar(rsa_frame, command=rsa_label.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

# Label'ın scrollbar'ı kullanmasını sağlama
rsa_label.config(yscrollcommand=scrollbar.set)

copy_button = ttk.Button(rsa_frame, text="Kopyala", command=copy_rsa)
copy_button.grid(row=1, column=0,columnspan=2, padx=5, pady=5)

generate_button = ttk.Button(rsa_frame, text="Generate RSA", command=generate_rsa)
generate_button.grid(row=1, column=1, columnspan=2,padx=5, pady=10)



# Başlangıçta RSA değerini güncelle
update_rsa_text()



# Repo Listesi Bölümü
repo_listbox = tk.Listbox(window, width=30, height=10)
repo_listbox.grid(row=0, column=2, rowspan=10, padx=5, pady=5, sticky="nsew")

# Scrollbar oluşturma
repo_scrollbar = tk.Scrollbar(window, command=repo_listbox.yview)
repo_scrollbar.grid(row=0, column=3, rowspan=10, sticky="ns")

# Listbox'ın scrollbar'ı kullanmasını sağlama
repo_listbox.config(yscrollcommand=repo_scrollbar.set)


# Sağ Tık Menüsü
sag_tik_menu = tk.Menu(repo_listbox, tearoff=0)
sag_tik_menu.add_command(label="Sil", command=lambda: sil_secilen_repo(repo_listbox.get(tk.ANCHOR)))
sag_tik_menu.add_command(label="Kopyala", command=lambda: kopyala_secilen_repo(repo_listbox.get(tk.ANCHOR)))
sag_tik_menu.add_command(label="Düzenle", command=lambda: duzenle_secilen_repo(repo_listbox.get(tk.ANCHOR)))


# Repo listbox'ına sağ tıklama işlemini bağla
repo_listbox.bind("<Button-3>", sag_tik_goster)
# Repo listbox'ına çift tıklama işlemini bağla
repo_listbox.bind("<Double-Button-1>", gir_repo)


# Repo Detayları
details_button = tk.Button(window, text="Repo Detayları", command=show_repo_details, width=15)
details_button.grid(row=0, column=1, padx=5, pady=5)

# Güncelleme butonu
update_button = ttk.Button(window, text="Güncelle", command=update_repo_list)
update_button.grid(row=10, column=2, padx=5, pady=5)

# Geri alma butonu
geri_button = ttk.Button(window, text="Geri", command=geri_al)
geri_button.grid(row=10,column=1, padx=5, pady=5)

# RSA Durum Label'ı
rsa_status_label = tk.Label(user_frame, text="", foreground="black", bg="#f0f0f0")
rsa_status_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Başlangıçta repo listesini güncelle
update_repo_list()

# Başlangıçta kontrol et
check_user_info()

window.mainloop()
