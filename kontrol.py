import os
import shutil
import subprocess
from datetime import datetime

# GitHub deponuzun kök dizinine giden yolu ayarlayın
github_dizin = os.path.join(os.path.expanduser("~"), "github")

# Zaman damgası dosyası yolu
zaman_d = os.path.join(github_dizin, "MAIN", "Python_OTO_COMMIT", "zaman_damgasi.txt")
kaydet = True
TEMP_DIZIN = os.path.join(github_dizin, "MAIN", "TEMP")
os.makedirs(TEMP_DIZIN, exist_ok=True)

def git_command(command, repo):
    process = subprocess.run(command, cwd=repo, text=True, capture_output=True)
    if process.returncode != 0:
        print(process.stderr)
        return False
    return True

def update(repo):
    global kaydet
    os.chdir(repo)
    if os.path.exists(".yukleniyor"):
        print("Yükleme işlemi devam ediyor, çıkılıyor...")
        kaydet = False
        return

    try:
        with open(".yukleniyor", "w") as f:
            pass

        original_directory = os.getcwd()
        try:
            commit_message = "oto commit " + str(datetime.now())
            git_command(["git", "add", "."], repo)
            git_command(["git", "commit", "-m", commit_message], repo)

            # Dal adı belirleme
            branch = subprocess.run(["git", "branch", "--show-current"], cwd=repo, text=True, capture_output=True).stdout.strip()
            if not branch:
                branch = "main"

            # Git push işlemi
            result = git_command(["git", "push", "-u", "origin", branch], repo)
            if not result:
                print("Git push işlemi başarısız oldu.")

            kaydet = True
        except Exception as e:
            print(f"Git işlemi sırasında hata: {e}")
            try:
                commit_message = "oto commit --rebase " + str(datetime.now())
                git_command(["git", "add", "."], repo)
                git_command(["git", "commit", "-m", commit_message], repo)
                git_command(["git", "pull", "--rebase"], repo) 
                result = git_command(["git", "push", "-u", "origin", branch], repo)
            except Exception as e:
                kaydet = False
                print(f"Git rebase işlemi sırasında hata: {e}")
                
        finally:
            os.chdir(original_directory)
    finally:
        os.remove(".yukleniyor")

def en_son_değişiklik_zamanı(dosya_yolu):
    try:
        stat = os.stat(dosya_yolu)
        son_degisiklik = datetime.fromtimestamp(stat.st_mtime)
        olusturma = datetime.fromtimestamp(stat.st_ctime)
        erisim = datetime.fromtimestamp(stat.st_atime)
        en_buyuk = max(son_degisiklik, olusturma, erisim)
        return en_buyuk
    except FileNotFoundError:
        print(f"Hata: {dosya_yolu} dosyası bulunamadı.")
        return None

def klasor_boyutunu_hesapla(klasor):
    toplam_boyut = 0
    for root, dirs, files in os.walk(klasor):
        for dosya in files:
            dosya_yolu = os.path.join(root, dosya)
            toplam_boyut += os.path.getsize(dosya_yolu)
    return toplam_boyut

def klasoru_tasi_ve_parcala(klasor_yolu):
    ana_klasor_adi = os.path.basename(klasor_yolu)
    hedef_klasor_yolu = os.path.join(TEMP_DIZIN, ana_klasor_adi)
    shutil.move(klasor_yolu, hedef_klasor_yolu)

    parca_boyutu = 100 * 1024 * 1024  # 100 MB
    parca_numarasi = 0
    parcalar = []
    for root, dirs, files in os.walk(hedef_klasor_yolu):
        for dosya in files:
            dosya_yolu = os.path.join(root, dosya)
            with open(dosya_yolu, 'rb') as f:
                while True:
                    parca = f.read(parca_boyutu)
                    if not parca:
                        break
                    parca_dosya_adi = f"{ana_klasor_adi}.parca{parca_numarasi}"
                    parca_dosya_yolu = os.path.join(TEMP_DIZIN, parca_dosya_adi)
                    with open(parca_dosya_yolu, 'wb') as pf:
                        pf.write(parca)
                    parcalar.append(parca_dosya_yolu)
                    parca_numarasi += 1
            os.remove(dosya_yolu)
    shutil.rmtree(hedef_klasor_yolu)
    return parcalar

def parcalari_push_etme(parcalar, repo, klasor_yolu):
    ana_klasor_adi = os.path.basename(klasor_yolu)
    yeni_klasor_yolu = os.path.join(os.path.dirname(klasor_yolu), ana_klasor_adi)
    os.makedirs(yeni_klasor_yolu, exist_ok=True)

    for parca_dosya_yolu in parcalar:
        parca_dosya_adi = os.path.basename(parca_dosya_yolu)
        hedef_dosya_yolu = os.path.join(yeni_klasor_yolu, parca_dosya_adi)
        shutil.move(parca_dosya_yolu, hedef_dosya_yolu)
        update(repo)
        os.remove(hedef_dosya_yolu)
    shutil.rmtree(yeni_klasor_yolu)

script_dizin = os.path.dirname(os.path.abspath(__file__))

try:
    with open(zaman_d, "r") as f:
        zaman_damgasi = f.readline().strip()
        zaman_damgasi = datetime.strptime(zaman_damgasi, "%a %b %d %H:%M:%S %Y")
except FileNotFoundError:
    zaman_damgasi = None
except ValueError:
    print("Zaman damgası dosyasında geçersiz veri bulundu.")
    zaman_damgasi = None

max_zaman = zaman_damgasi 

for root, dirs, files in os.walk(github_dizin):
    if root == github_dizin:
        for dir_name in dirs:
            klasor_yolu = os.path.join(root, dir_name)
            klasor_boyutu = klasor_boyutunu_hesapla(klasor_yolu)
            if klasor_boyutu > 500 * 1024 * 1024:  # 500 MB
                parcalar = klasoru_tasi_ve_parcala(klasor_yolu)
                parcalari_push_etme(parcalar, root, klasor_yolu)
                continue

    for dosya in files:
        if dosya in ["zaman_damgasi.txt", "bilgiler.txt", "output.log", ".yukleniyor"]:
            continue

        dosya_yolu = os.path.join(root, dosya)
        z = en_son_değişiklik_zamanı(dosya_yolu)
        if z is None:
            continue  # Zaman damgası yoksa dosyayı atla
        try:
            saniye = int(z.second)
        except:
            saniye = 0
        z = datetime(z.year, z.month, z.day, z.hour, z.minute, saniye)

        if z is not None:
            if max_zaman is not None:
                try:
                    if z > max_zaman:
                        print(f"{dosya_yolu}: True, {z}")
                        max_zaman = z
                        update(root)
                except ValueError:
                    print(f"Hata: {dosya_yolu} için geçersiz zaman damgası.")

if max_zaman is not None and kaydet:
    with open(zaman_d, "w") as f:
        f.write(max_zaman.strftime("%a %b %d %H:%M:%S %Y"))
