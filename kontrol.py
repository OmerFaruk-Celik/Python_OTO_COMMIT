import os
import time
import subprocess
from datetime import datetime

# GitHub deponuzun kök dizinine giden yolu ayarlayın
github_dizin = os.path.join(os.path.expanduser("~"), "github")


# Zaman damgası dosyası yolu
zaman_d = os.path.join(github_dizin, "MAIN","Python_OTO_COMMIT", "zaman_damgasi.txt")
kaydet=True
def update(repo):
    global kaydet
    """
    GitHub deponuzun kök dizinine geçerek commit ve push işlemleri yapar.
    """
    # Kilit dosyası kontrolü
    os.chdir(repo)
    if os.path.exists(".yukleniyor"):
        print("Yuklenen Dosya :",os.getcwd())		
        print("Yükleme işlemi devam ediyor, çıkılıyor...")
        kaydet=False
        return

    try:
        # Kilit dosyası oluştur
        
        with open(".yukleniyor", "w") as f:
            pass

        # Mevcut dizini kaydet
        original_directory = os.getcwd()

        try:
            # GitHub deponuzun kök dizinine geç
             
            
            # Git add, commit ve push işlemleri
            subprocess.run(["git", "fetch", "origin"])  # En son değişiklikleri indir
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "python oto commit"])
            result = subprocess.run(["git", "push", "-u", "origin", "main"])
            kaydet=True
            if result.returncode != 0:
                print("Git push işlemi başarısız oldu.")
                kaydet=False

        finally:
            # Başlangıç dizinine geri dön
            os.chdir(original_directory)
    finally:
        # Kilit dosyasını sil
        os.remove(".yukleniyor")
       

def en_son_değişiklik_zamanı(dosya_yolu):
    """Dosyanın son değiştirilme, oluşturulma ve erişim zamanlarından en büyük olanını döndürür."""
    try:
        stat = os.stat(dosya_yolu)
        son_degisiklik = datetime.fromtimestamp(stat.st_mtime)
        olusturma = datetime.fromtimestamp(stat.st_ctime)
        erisim = datetime.fromtimestamp(stat.st_atime)

        # En büyük zamanı bul
        en_buyuk = max(son_degisiklik, olusturma, erisim)
        return en_buyuk
    except FileNotFoundError:
        print(f"Hata: {dosya_yolu} dosyası bulunamadı.")
        return None

# Bu script'in çalıştığı dizini al
script_dizin = os.path.dirname(os.path.abspath(__file__))

# Zaman damgası dosyasını oku
try:
    with open(zaman_d, "r") as f:
        zaman_damgasi = f.readline().strip()
        zaman_damgasi = datetime.strptime(zaman_damgasi, "%a %b %d %H:%M:%S %Y")
except FileNotFoundError:
    zaman_damgasi = None  # Dosya yoksa None ata
except ValueError:
    print("Zaman damgası dosyasında geçersiz veri bulundu.")
    zaman_damgasi = None

# Başlangıçta max_zaman'ı zaman_damgasi olarak ata
max_zaman = zaman_damgasi 

# Dizindeki dosyaları al
for root, dirs, files in os.walk(github_dizin):
    dirs[:] = [d for d in dirs if d != ".git"]  # .git dizinini filtrele
    dirs[:] = [d for d in dirs if d != ".gitingore"]
    dirs[:] = [d for d in dirs if d != "MAIN"]
    dirs[:] = [d for d in dirs if ".git" not in d] 
    for dosya in files:	
        # Gizli dosyaları ve belirli dosyaları atla
        if  dosya=="zaman_damgasi.txt" or dosya=="bilgiler.txt" or dosya=="output.log" or dosya==".yukleniyor":
		
            continue
            

        dosya_yolu = os.path.join(root, dosya)
        

        # Dosyanın en son değişiklik zamanını al
        z = en_son_değişiklik_zamanı(dosya_yolu)
        try:
            saniye = int(z.second)
        except:
            saniye=0			
        z = datetime(z.year, z.month, z.day, z.hour, z.minute, saniye)

        if z is not None:
            # En son değiştirilme zamanını max_zaman ile karşılaştır
            if max_zaman is not None:
                try:
                    if z > max_zaman:
                        print(f"{dosya_yolu}: True, {z}")
                        max_zaman = z  # En büyük zaman damgasını güncelle
                        update(root)  # Update fonksiyonunu çağır
                except ValueError:
                    print(f"Hata: {dosya_yolu} için geçersiz zaman damgası.")

# Zaman damgası dosyasını güncelle
if max_zaman is not None and kaydet:
    with open(zaman_d, "w") as f:
        f.write(max_zaman.strftime("%a %b %d %H:%M:%S %Y"))  # Zaman damgasını dosyaya kaydet
