from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# ChromeDriver yolunu belirt
service = Service(executable_path="C:/Users/fafli/Desktop/chromedriver-win64/chromedriver.exe")

# Chrome'un yüklü olduğu binary yolunu belirt
chrome_options = Options()
chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"

# Tarayıcıyı başlat
driver = webdriver.Chrome(service=service, options=chrome_options)

# Pinterest sayfasına git
driver.get("https://www.pinterest.com/kiricishop/aesthetic-gadgets/")
time.sleep(5)  # Sayfanın yüklenmesini bekle

# Pinlerin URL'lerini depolamak için bir liste
pin_urls = set()

# Kaydırma döngüsü
last_height = driver.execute_script("return document.body.scrollHeight")
scroll_attempts = 0  # Sonuç almadan yapılan kaydırma denemelerini say
while True:
    # Tüm pinleri al
    pins = driver.find_elements(By.CSS_SELECTOR, "a[href*='/pin/']")
    for pin in pins:
        pin_url = pin.get_attribute("href")
        pin_urls.add(pin_url)
    
    # Küçük adımlarla kaydır
    driver.execute_script("window.scrollBy(0, 1000);")  # Küçük kaydırma adımları
    time.sleep(2)  # Sayfanın yüklenmesini bekle
    
    # Yeni yüksekliği al ve karşılaştır
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    # Sayfa daha fazla kaydırılamıyorsa denemeleri say ve çık
    if new_height == last_height:
        scroll_attempts += 1
        if scroll_attempts >= 5:  # 5 kez kaydırma denemesi sonuçsuz kaldıysa çık
            break
    else:
        scroll_attempts = 0  # Başarılı kaydırma yaptıysak sıfırla
    last_height = new_height

# Pin sayısını yazdır
print(f"Toplam {len(pin_urls)} pin bulundu.")

# Pin linklerini bir dosyaya kaydet
with open("pin_urls.txt", "w") as file:
    for url in pin_urls:
        file.write(url + "\n")
37
# Tarayıcıyı kapat
driver.quit()

