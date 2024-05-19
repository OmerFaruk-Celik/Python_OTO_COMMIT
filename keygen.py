import subprocess
import os

def generate_ssh_key(key_filename="id_rsa"):
  """SSH anahtar çiftini oluşturur ve kamu anahtarını bir dosyaya kaydeder.
  
  Args:
    key_filename: Özel anahtarın dosya adı. Kamu anahtarı otomatik olarak aynı isimle ".pub" uzantılı olarak oluşturulur.
  """
  try:
	bilgiler_dosyasi = os.path.join(os.path.expanduser("~"), "github","Python_OTO_COMMIT", "bilgiler.txt")
    with open(bilgiler_dosyasi, "r") as f:
      username, email, token = f.readline().strip().split(",")
      
      print(email)
    subprocess.run(["ssh-keygen", "-t", "rsa", "-f", key_filename, "-N", "", "-C", email])
    # Sadece kamu anahtarını kopyala ve kaydet
    with open(key_filename + ".pub", "r") as pub_file:
      public_key = pub_file.read()
    with open(key_filename, "w") as key_file:
      key_file.write(public_key)
    print(f"SSH anahtar çifti oluşturuldu. Kamu anahtar {key_filename} dosyasına kaydedildi.")
  except FileNotFoundError:
    print("bilgiler.txt dosyası bulunamadı. Lütfen dosyanın var olduğundan emin olun.")
  except IndexError:
    print("bilgiler.txt dosyasında e-posta adresi bulunamadı. Lütfen dosyayı kontrol edin.")
  except Exception as e:
    print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
  # varsayılan dosya adı kullanarak anahtarı oluştur
  generate_ssh_key() 

  # .ssh dizini yoksa oluştur
  ssh_dir = os.path.expanduser("~/.ssh")
  if not os.path.exists(ssh_dir):
      os.makedirs(ssh_dir)

  # anahtar dosyasını .ssh dizinine taşı
  source_file = "id_rsa"
  destination_file = os.path.join(ssh_dir, source_file)
  if os.path.exists(source_file):
    os.rename(source_file, destination_file)
    source_file = "id_rsa.pub"
    destination_file = os.path.join(ssh_dir, source_file)
    os.rename(source_file, destination_file)
