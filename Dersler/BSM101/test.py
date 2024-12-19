import os
from datetime import datetime

# Test klasörü ve log dosyası yolları
test_dir = r'C:\Dersler\BSM101\Ödevler'
log_file = r'C:\Dersler\BSM101\changes.json'

# Klasörleri oluştur
os.makedirs(test_dir, exist_ok=True)

# Log dosyasına test yazısı yaz
with open(log_file, 'w', encoding='utf-8') as f:
    f.write(f'Test zamanı: {datetime.now()}')

print(f"Test klasörü oluşturuldu: {test_dir}")
print(f"Log dosyası oluşturuldu: {log_file}")