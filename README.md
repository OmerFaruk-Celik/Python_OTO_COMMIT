# Python Projem
#!/bin/bash

# 1 İÇERİK

chmod +x "$0"


 1. Gerekli Python paketlerini yükleme

echo "Gerekli Python paketlerini indiriyorum..."

pip install github3 pyperclip tkinter ttk


 2. ~/github dizinini oluşturma

echo "~/github dizinini oluşturuyorum..."

mkdir -p ~/github


 3. Repo'yu indirme

echo "Repo'yu indiriyorum..."

git clone https://github.com/OmerFaruk-Celik/Python_OTO_COMMIT.git ~/github/Python_OTO_COMMIT


 4. repo.py dosyasını /usr/bin/repo'ya kopyalama

echo "repo.py dosyasını kopyalıyorum..."

sudo cp ~/github/Python_OTO_COMMIT/repo.py /usr/bin/repo


 5. Crontab'a komut ekleme

echo "Crontab'a komut ekliyorum..."

echo "* * * * * /usr/bin/python3 ~/github/Python_OTO_COMMIT/kontrol.py > ~/github/Python_OTO_COMMIT/output.log 2>&1" | sudo tee -a /etc/crontab


 6. Bilgiler.txt dosyasını düzenleme

echo "bilgiler.txt dosyasını düzenleyin..."

echo "Kullanıcı Adı,E-Posta,GITHUB_TOKEN" > ~/github/Python_OTO_COMMIT/bilgiler.txt

echo "Lütfen bilgiler.txt dosyasını düzenleyin ve bilgilerinizi ekleyin."

echo "Token'ı GitHub'dan oluşturun."

echo "Daha sonra script'i çalıştırın."

echo "INSTALL işlemi tamamlandı!"




# 2 YUKLEME ADIMLARI

git clone https://github.com/OmerFaruk-Celik/Python_OTO_COMMIT.git

cd Python_OTO_COMMIT

chmod +x ./INSTALL

./INSTALL

