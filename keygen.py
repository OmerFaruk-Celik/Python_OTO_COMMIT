import subprocess
import os

def generate_ssh_key(key_filename="id_rsa"):
  """SSH anahtar çiftini oluşturur ve kamu anahtarını bir dosyaya kaydeder.

  Args:
    key_filename: Özel anahtarın dosya adı. Kamu anahtarı otomatik olarak aynı isimle ".pub" uzantılı olarak oluşturulur.
  """
  try:
    subprocess.run(["ssh-keygen", "-t", "rsa", "-f", key_filename, "-N", ""])
    # Sadece kamu anahtarını kopyala ve kaydet
    with open(key_filename + ".pub", "r") as pub_file:
      public_key = pub_file.read()
    with open(key_filename, "w") as key_file:
      key_file.write(public_key)
    print(f"SSH anahtar çifti oluşturuldu. Kamu anahtar {key_filename} dosyasına kaydedildi.")
  except FileNotFoundError:
    print("ssh-keygen komutu bulunamadı. Lütfen SSH keygen'in kurulu olduğundan emin olun.")
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
  os.rename(source_file, destination_file)

  source_file = "id_rsa.pub"
  destination_file = os.path.join(ssh_dir, source_file)
  os.rename(source_file, destination_file)
