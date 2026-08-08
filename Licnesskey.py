#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, time, requests, json, hashlib, base64, os, subprocess, threading, gc, uuid, platform, random
from datetime import datetime
from urllib.parse import quote

RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'
MAGENTA = '\033[1;35m'
CYAN = '\033[1;36m'
WHITE = '\033[1;37m'
RESET = '\033[0m'

VIP_SERVER = "http://fi6.bot-hosting.net:20805"
SECRET = "kensitool2024xsecret"
LINK4M_API = "6a707ce6f64fc169420e2a7a"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def gradient_text(text, colors):
    result = ""
    for i, char in enumerate(text):
        if char != ' ':
            result += colors[i % len(colors)] + char + RESET
        else:
            result += char
    return result

def banner():
    clear()
    grad = [RED, MAGENTA, CYAN, BLUE, CYAN, MAGENTA, RED]
    title = "KENSI TOOL PRO v9.0"
    subtitle = "Tool Cha Akai Kensi"
    
    print(f"\n{gradient_text(title, grad)}")
    print(f"{gradient_text(subtitle, grad)}\n")

def show_contact():
    print(f"{CYAN}┌{'─'*38}┐{RESET}")
    print(f"{CYAN}│{RESET} {BLUE}●{RESET} {CYAN}Admin{RESET}: {GREEN}Kensi{RESET}")
    print(f"{CYAN}│{RESET} {BLUE}●{RESET} {CYAN}Zalo{RESET}: {GREEN}zalo.me/rwic5s{RESET}")
    print(f"{CYAN}│{RESET} {BLUE}●{RESET} {CYAN}FB{RESET}: {GREEN}fb.com/1GrJbs8{RESET}")
    print(f"{CYAN}└{'─'*38}┘{RESET}\n")

def show_status(key="---", ktype="---", exp="---"):
    print(f"{BLUE}┌{'─'*38}┐{RESET}")
    print(f"{BLUE}│{RESET} {GREEN}🔑 Key{RESET}: {CYAN}{key[:20]:<20}{RESET}")
    print(f"{BLUE}│{RESET} {GREEN}📋 Type{RESET}: {MAGENTA}{ktype:<20}{RESET}")
    print(f"{BLUE}│{RESET} {GREEN}⏳ Expire{RESET}: {YELLOW}{exp:<19}{RESET}")
    print(f"{BLUE}└{'─'*38}┘{RESET}\n")

def menu_license():
    print(f"{BLUE}╔{'═'*36}╗{RESET}")
    print(f"{BLUE}║{RESET} {WHITE}CHON LOAI KEY{RESET}{' '*21}{BLUE}║{RESET}")
    print(f"{BLUE}╠{'═'*36}╣{RESET}")
    print(f"{BLUE}║{RESET} {GREEN}◈{RESET} {CYAN}[1]{RESET}  Free Key (23:59){' '*10}{BLUE}║{RESET}")
    print(f"{BLUE}║{RESET} {GREEN}◈{RESET} {CYAN}[2]{RESET}  VIP Key (Mua){' '*13}{BLUE}║{RESET}")
    print(f"{BLUE}║{RESET} {GREEN}◈{RESET} {RED}[0]{RESET}  Exit{' '*20}{BLUE}║{RESET}")
    print(f"{BLUE}╚{'═'*36}╝{RESET}\n")

def menu_main():
    print(f"{BLUE}╔{'═'*36}╗{RESET}")
    print(f"{BLUE}║{RESET} {WHITE}MENU CHINH{RESET}{' '*24}{BLUE}║{RESET}")
    print(f"{BLUE}╠{'═'*36}╣{RESET}")
    print(f"{BLUE}║{RESET} {GREEN}◈{RESET} {CYAN}[1]{RESET}  Messenger{' '*19}{BLUE}║{RESET}")
    print(f"{BLUE}║{RESET} {GREEN}◈{RESET} {CYAN}[2]{RESET}  Settings{' '*20}{BLUE}║{RESET}")
    print(f"{BLUE}║{RESET} {GREEN}◈{RESET} {CYAN}[3]{RESET}  Statistics{' '*18}{BLUE}║{RESET}")
    print(f"{BLUE}║{RESET} {GREEN}◈{RESET} {CYAN}[4]{RESET}  Account{' '*20}{BLUE}║{RESET}")
    print(f"{BLUE}║{RESET} {GREEN}◈{RESET} {RED}[0]{RESET}  Exit{' '*22}{BLUE}║{RESET}")
    print(f"{BLUE}╚{'═'*36}╝{RESET}\n")

class KeySystemMobile:
    def __init__(self):
        self.auth_dir = os.path.join(os.path.expanduser("~"), ".local/share/.kensi")
        os.makedirs(self.auth_dir, exist_ok=True)
        self.auth_file = os.path.join(self.auth_dir, "vip")
        self.ip_key_file = os.path.join(self.auth_dir, "free")
        self.current_key = None
        self.session_id = None
        self.key_type = None
        self.expire_time = 0
        self.hwid = self.get_hwid()

    def xor_enc(self, data):
        k = (SECRET * (len(data) // len(SECRET) + 1)).encode()
        return bytes(a ^ b for a, b in zip(data.encode(), k))

    def make_token(self, key, hwid):
        return base64.urlsafe_b64encode(self.xor_enc(f"{key}|{hwid}")).decode()

    def read_token(self, token):
        try:
            xored = base64.urlsafe_b64decode(token.encode())
            k = (SECRET * (len(xored) // len(SECRET) + 1)).encode()
            raw = bytes(a ^ b for a, b in zip(xored, k)).decode()
            return raw.split("|")
        except:
            return None, None

    def get_hwid(self):
        try:
            r = subprocess.check_output(["settings", "get", "secure", "android_id"], stderr=subprocess.DEVNULL).decode().strip()
            if r and r != "null":
                return hashlib.sha256(r.encode()).hexdigest()[:16]
        except:
            pass
        try:
            mac = uuid.getnode()
            return hashlib.sha256(str(mac).encode()).hexdigest()[:16]
        except:
            return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:16]

    def get_ip(self):
        try:
            return requests.get("https://api.ipify.org", timeout=5).text.strip()
        except:
            return None

    def gen_free_key(self, ip=None):
        chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        key = "".join(random.choice(chars) for _ in range(16))
        return "-".join([key[i:i+4] for i in range(0, 16, 4)])

    def short_url(self, url):
        try:
            api = f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url={quote(url)}"
            r = requests.get(api, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get("status") == "success":
                    return data.get("shortenedUrl", url)
        except:
            pass
        return url

    def save_vip(self, key, hwid):
        token = self.make_token(key, hwid)
        with open(self.auth_file, "w") as f:
            f.write(token)

    def load_vip(self):
        try:
            if os.path.exists(self.auth_file):
                with open(self.auth_file) as f:
                    return self.read_token(f.read().strip())
        except:
            pass
        return None, None

    def save_free(self, ip, key):
        exp = datetime.now().replace(hour=23, minute=59, second=0).isoformat()
        data = base64.b64encode(json.dumps({ip: {"key": key, "exp": exp}}).encode()).decode()
        with open(self.ip_key_file, "w") as f:
            f.write(data)

    def load_free(self, ip):
        try:
            if os.path.exists(self.ip_key_file):
                data = json.loads(base64.b64decode(open(self.ip_key_file).read().encode()).decode())
                if ip in data:
                    exp = datetime.fromisoformat(data[ip]["exp"])
                    if exp > datetime.now():
                        return data[ip]["key"]
        except:
            pass
        return None

    def verify_vip(self, key):
        try:
            token = self.make_token(key, self.hwid)
            r = requests.post(f"{VIP_SERVER}/verify", json={"token": token}, timeout=10)
            data = r.json()
            if data.get("valid"):
                self.session_id = data.get("session_id")
                self.current_key = key
                self.key_type = "vip"
                self.save_vip(key, self.hwid)
                return True, data.get("expire", "N/A")
            return False, data.get("error", "Invalid")
        except Exception as e:
            return False, str(e)

    def check_free(self):
        banner()
        show_contact()
        show_status()
        
        ip = self.get_ip()
        if not ip:
            print(f"{RED}✘ No IP{RESET}\n")
            input(f"{CYAN}[Enter]{RESET}")
            return False

        saved = self.load_free(ip)
        if saved:
            print(f"{GREEN}✓ Key still valid!{RESET}")
            show_status(key=saved, ktype="FREE", exp="23:59")
            self.current_key = saved
            self.key_type = "free"
            self.expire_time = datetime.now().replace(hour=23, minute=59).timestamp()
            input(f"{CYAN}[Enter]{RESET}")
            return True

        print(f"{CYAN}Generating key...{RESET}")
        key = self.gen_free_key(ip)
        url = f"https://www.webkey.x10.mx/?ma={key}"
        short = self.short_url(url)

        print(f"\n{BLUE}{'═'*40}{RESET}")
        print(f"{WHITE}FREE KEY{RESET}")
        print(f"{BLUE}{'═'*40}{RESET}\n")
        print(f"{GREEN}{short}{RESET}\n")
        print(f"1. Open link")
        print(f"2. Copy key")
        print(f"3. Paste below\n")

        while True:
            uk = input(f"{CYAN}Key: {RESET}").strip()
            if not uk:
                print(f"{RED}Empty!{RESET}")
                continue
            if uk.upper() == key.upper():
                self.save_free(ip, key)
                self.current_key = key
                self.key_type = "free"
                self.expire_time = datetime.now().replace(hour=23, minute=59).timestamp()
                show_status(key=key, ktype="FREE", exp="23:59")
                input(f"{CYAN}[Enter]{RESET}")
                return True
            else:
                print(f"{RED}Wrong! Use link.{RESET}")

    def check_vip(self):
        banner()
        show_contact()
        show_status()
        print(f"{MAGENTA}VIP KEY{RESET}\n")
        print(f"Contact: {GREEN}zalo.me/rwic5s{RESET}\n")
        print(f"{BLUE}{'═'*40}{RESET}\n")

        saved_k, saved_h = self.load_vip()
        if saved_k and saved_h == self.hwid:
            cont = input(f"{CYAN}Resume {saved_k[:6]}***? (y/n): {RESET}").strip().lower()
            if cont == "y":
                ok, exp = self.verify_vip(saved_k)
                if ok:
                    show_status(key=saved_k, ktype="VIP", exp=exp)
                    input(f"{CYAN}[Enter]{RESET}")
                    return True

        key = input(f"{CYAN}Key: {RESET}").strip()
        if not key:
            print(f"{RED}Empty!{RESET}\n")
            input(f"{CYAN}[Enter]{RESET}")
            return False

        print(f"{CYAN}Verifying...{RESET}")
        ok, result = self.verify_vip(key)
        if ok:
            show_status(key=key, ktype="VIP", exp=result)
            input(f"{CYAN}[Enter]{RESET}")
            return True
        else:
            print(f"{RED}✘ {result}{RESET}\n")
            input(f"{CYAN}[Enter]{RESET}")
            return False

    def monitor(self):
        while True:
            try:
                if self.key_type == "free" and self.expire_time:
                    if time.time() > self.expire_time:
                        print(f"\n{RED}✘ Expired!{RESET}")
                        os._exit(1)
            except:
                pass
            time.sleep(5)

    def auth(self):
        while True:
            banner()
            show_contact()
            show_status()
            menu_license()
            ch = input(f"{CYAN}> {RESET}").strip()
            if ch == "0":
                print(f"\n{RED}Bye!{RESET}\n")
                sys.exit(0)
            elif ch == "1":
                if self.check_free():
                    return True
            elif ch == "2":
                if self.check_vip():
                    return True

    def main_loop(self):
        while True:
            banner()
            show_contact()
            show_status(key=self.current_key[:16] if self.current_key else "---",
                       ktype=self.key_type.upper() if self.key_type else "---")
            menu_main()
            ch = input(f"{CYAN}> {RESET}").strip()
            if ch == "0":
                print(f"\n{RED}Exit{RESET}\n")
                break
            elif ch in ["1", "2", "3", "4"]:
                print(f"\n{YELLOW}Coming soon{RESET}\n")
                time.sleep(1)
            else:
                print(f"{RED}Invalid{RESET}\n")
                time.sleep(1)

def main():
    try:
        ks = KeySystemMobile()
        if not ks.auth():
            print(f"{RED}Failed{RESET}\n")
            sys.exit(1)
        threading.Thread(target=ks.monitor, daemon=True).start()
        ks.main_loop()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Stop{RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}Error: {e}{RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
