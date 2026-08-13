#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import os, sys, subprocess, time, re, json, string, hashlib, random, platform, ssl, uuid, socket, gc, threading
from datetime import datetime
from collections import deque
from urllib.parse import urlparse, quote
import requests, paho.mqtt.client as mqtt

R = '\033[1;31m'; G = '\033[1;32m'; Y = '\033[1;33m'; B = '\033[1;34m'; M = '\033[1;35m'; C = '\033[1;36m'; W = '\033[1;37m'; RS = '\033[0m'

OWNER = "Cha Akai Kensi"
TOOL_NAME = "KENSI TOOL PRO v9.0"
STATUS = "FREE"

def loading_animation(text="Loading", duration=3):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start = time.time()
    i = 0
    while time.time() - start < duration:
        sys.stdout.write(f"\r\033[1;36m{frames[i % len(frames)]}\033[1;37m {text}...    ")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()

def progress_bar(text, duration=2):
    bar_len = 30
    for i in range(bar_len + 1):
        pct = int((i / bar_len) * 100)
        filled = i
        empty = bar_len - i
        bar = "█" * filled + "░" * empty
        sys.stdout.write(f"\r\033[1;37m[{bar}] \033[1;33m{pct}%\033[1;32m {text}...    ")
        sys.stdout.flush()
        time.sleep(duration / bar_len)
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()

def auto_install():
    pkgs = ["requests","paho-mqtt","beautifulsoup4","fake-useragent","rich","colorama","bs4"]
    total = len(pkgs)
    os.system("clear")
    print("\033[1;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[1;37m")
    print("  🔧 INSTALLING REQUIRED MODULES...")
    print("\033[1;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[1;32m")
    for i, pkg in enumerate(pkgs, 1):
        pct = int((i / total) * 100)
        bar_len = 20
        filled = int(bar_len * i / total)
        bar = "█" * filled + "░" * (bar_len - filled)
        sys.stdout.write(f"\r\033[1;37m[{bar}] \033[1;33m{pct}%\033[1;32m - Installing {pkg}...    ")
        sys.stdout.flush()
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
    sys.stdout.write(f"\r\033[1;32m[{'█' * bar_len}] \033[1;37m100% - \033[1;32mAll modules installed!\033[0m\n")
    time.sleep(1)
    os.system("clear")

auto_install()

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    loading_animation("Loading KENSI TOOL", 2)
    progress_bar("Initializing", 1.5)
    print(f"""
{R}   ██╗  ██╗███████╗███╗   ██╗███████╗██╗{RS}
{Y}   ██║ ██╔╝██╔════╝████╗  ██║██╔════╝██║{RS}
{G}   █████╔╝ █████╗  ██╔██╗ ██║███████╗██║{RS}
{C}   ██╔═██╗ ██╔══╝  ██║╚██╗██║╚════██║██║{RS}
{B}   ██║  ██╗███████╗██║ ╚████║███████║██║{RS}
{M}   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝{RS}
{W}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RS}
{W}         {TOOL_NAME}{RS}
{W}         {C}OWNER{R}: {G}{OWNER}{RS}
{W}         {C}STATUS{R}: {G}{STATUS}{RS}
{W}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RS}
""")
    time.sleep(0.5)

def linex():
    print(f"{B}─────────────────────────────────────────────────────{RS}")

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_system_info():
    info = {}
    try:
        info['device'] = subprocess.check_output("getprop ro.product.model", shell=True).decode().strip() or "Unknown"
    except:
        info['device'] = "Unknown"
    try:
        info['brand'] = subprocess.check_output("getprop ro.product.brand", shell=True).decode().strip() or "Unknown"
    except:
        info['brand'] = "Unknown"
    try:
        info['android'] = subprocess.check_output("getprop ro.build.version.release", shell=True).decode().strip() or "Unknown"
    except:
        info['android'] = "Unknown"
    info['arch'] = platform.architecture()[0] or "Unknown"
    info['machine'] = platform.machine() or "Unknown"
    try:
        info['processor'] = subprocess.check_output("getprop ro.product.board", shell=True).decode().strip() or platform.processor() or "Unknown"
    except:
        info['processor'] = platform.processor() or "Unknown"
    info['hostname'] = socket.gethostname() or "Unknown"
    try:
        info['ip'] = requests.get("https://api.ipify.org", timeout=3).text.strip()
    except:
        info['ip'] = "Unknown"
    try:
        loc = requests.get("http://ip-api.com/json/", timeout=3).json()
        info['country'] = loc.get('country', 'Unknown')
        info['city'] = loc.get('city', 'Unknown')
        info['region'] = loc.get('regionName', 'Unknown')
        info['isp'] = loc.get('isp', 'Unknown')
        info['timezone'] = loc.get('timezone', 'Unknown')
    except:
        info['country'] = "Unknown"
        info['city'] = "Unknown"
        info['region'] = "Unknown"
        info['isp'] = "Unknown"
        info['timezone'] = "Unknown"
    try:
        info['sim'] = subprocess.check_output("getprop gsm.operator.alpha", shell=True).decode().strip() or "Unknown"
    except:
        info['sim'] = "Unknown"
    try:
        info['network'] = subprocess.check_output("getprop gsm.network.type", shell=True).decode().strip() or "Unknown"
    except:
        info['network'] = "Unknown"
    try:
        info['resolution'] = subprocess.check_output("wm size", shell=True).decode().strip().replace("Physical size: ", "") or "Unknown"
    except:
        info['resolution'] = "Unknown"
    return info

def show_system_info():
    info = get_system_info()
    loading_animation("Fetching system info", 1)
    print(f"{W}┌─────────────────────────────────────────────────────{RS}")
    print(f"{W}│  {C}DEVICE{RS}      : {G}{info['brand']} {info['device']}{RS}")
    print(f"{W}│  {C}ANDROID{RS}     : {G}{info['android']}{RS}")
    print(f"{W}│  {C}ARCH{RS}        : {G}{info['arch']} | {info['machine']}{RS}")
    print(f"{W}│  {C}PROCESSOR{RS}   : {G}{info['processor']}{RS}")
    print(f"{W}│  {C}HOSTNAME{RS}    : {G}{info['hostname']}{RS}")
    print(f"{W}│  {C}IP ADDRESS{RS}  : {G}{info['ip']}{RS}")
    print(f"{W}│  {C}LOCATION{RS}    : {G}{info['city']}, {info['region']}, {info['country']}{RS}")
    print(f"{W}│  {C}TIMEZONE{RS}    : {G}{info['timezone']}{RS}")
    print(f"{W}│  {C}ISP{RS}         : {G}{info['isp']}{RS}")
    print(f"{W}│  {C}SIM{RS}         : {G}{info['sim']}{RS}")
    print(f"{W}│  {C}NETWORK{RS}     : {G}{info['network']}{RS}")
    print(f"{W}│  {C}RESOLUTION{RS}  : {G}{info['resolution']}{RS}")
    print(f"{W}└─────────────────────────────────────────────────────{RS}")

VIP_SERVER = "http://fi6.bot-hosting.net:20805"
SECRET = "kensitool2024xsecret"
LINK4M_API = "6a707ce6f64fc169420e2a7a"
class KeySystem:
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
        self.is_valid = False

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
            parts = raw.split("|")
            if len(parts) == 2:
                return parts[0], parts[1]
        except:
            pass
        return None, None

    def get_hwid(self):
        try:
            r = subprocess.check_output(["settings", "get", "secure", "android_id"], stderr=subprocess.DEVNULL).decode().strip()
            if r and r != "null" and len(r) > 5:
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
                self.is_valid = True
                return True, data.get("expire", "N/A")
            return False, data.get("error", "Invalid")
        except Exception as e:
            return False, str(e)

    def check_free(self):
        banner()
        print(f"\n{C}◈ KEY FREE{RS}\n")
        linex()
        ip = self.get_ip()
        if not ip:
            print(f"{R}✘ No IP{RS}\n")
            input(f"{C}[Enter]{RS}")
            return False

        saved = self.load_free(ip)
        if saved:
            print(f"{G}✓ Key still valid!{RS}")
            self.current_key = saved
            self.key_type = "free"
            self.is_valid = True
            input(f"{C}[Enter]{RS}")
            return True

        print(f"{C}Generating key...{RS}")
        loading_animation("Generating free key", 2)
        key = self.gen_free_key(ip)
        url = f"https://www.webkey.x10.mx/?ma={key}"
        short = self.short_url(url)

        print(f"\n{B}{'═'*40}{RS}")
        print(f"{W}FREE KEY{RS}")
        print(f"{B}{'═'*40}{RS}\n")
        print(f"{G}{short}{RS}\n")
        print(f"1. Open link")
        print(f"2. Copy key")
        print(f"3. Paste below\n")

        while True:
            uk = input(f"{C}Key: {RS}").strip()
            if not uk:
                print(f"{R}Empty!{RS}")
                continue
            if uk.upper() == key.upper():
                self.save_free(ip, key)
                self.current_key = key
                self.key_type = "free"
                self.is_valid = True
                print(f"\n{G}✓ Key valid!{RS}\n")
                input(f"{C}[Enter]{RS}")
                return True
            else:
                print(f"{R}Wrong! Use link.{RS}")

    def check_vip(self):
        banner()
        print(f"\n{M}VIP KEY{RS}\n")
        print(f"Contact: {G}zalo.me/rwic5s{RS}\n")
        print(f"{B}{'═'*40}{RS}\n")

        saved_k, saved_h = self.load_vip()
        if saved_k and saved_h == self.hwid:
            cont = input(f"{C}Resume {saved_k[:6]}***? (y/n): {RS}").strip().lower()
            if cont == "y":
                ok, exp = self.verify_vip(saved_k)
                if ok:
                    self.is_valid = True
                    print(f"\n{G}✓ VIP valid!{RS}\n")
                    input(f"{C}[Enter]{RS}")
                    return True

        key = input(f"{C}Key: {RS}").strip()
        if not key:
            print(f"{R}Empty!{RS}\n")
            input(f"{C}[Enter]{RS}")
            return False

        print(f"{C}Verifying...{RS}")
        loading_animation("Verifying VIP key", 1.5)
        ok, result = self.verify_vip(key)
        if ok:
            self.is_valid = True
            print(f"\n{G}✓ VIP valid!{RS}\n")
            input(f"{C}[Enter]{RS}")
            return True
        else:
            print(f"{R}✘ {result}{RS}\n")
            input(f"{C}[Enter]{RS}")
            return False

    def monitor(self):
        while True:
            try:
                if self.key_type == "free" and self.expire_time:
                    if time.time() > self.expire_time:
                        print(f"\n{R}✘ Expired!{RS}")
                        os._exit(1)
            except:
                pass
            time.sleep(5)

    def auth(self):
        banner()
        loading_animation("Loading license system", 1)
        print(f"{B}╔{'═'*36}╗{RS}")
        print(f"{B}║ {W}SELECT KEY TYPE{RS}{' '*16}{B}║{RS}")
        print(f"{B}╠{'═'*36}╣{RS}")
        print(f"{B}║ {G}◈{RS} {C}[1]{RS}  Free Key{' '*17}{B}║{RS}")
        print(f"{B}║ {G}◈{RS} {C}[2]{RS}  VIP Key{' '*18}{B}║{RS}")
        print(f"{B}║ {G}◈{RS} {R}[0]{RS}  Exit{' '*21}{B}║{RS}")
        print(f"{B}╚{'═'*36}╝{RS}\n")
        ch = input(f"{C}> {RS}").strip()
        if ch == "0":
            sys.exit(0)
        elif ch == "1":
            return self.check_free()
        elif ch == "2":
            return self.check_vip()
        else:
            print(f"{R}Invalid!{RS}")
            return False

def menu():
    banner()
    show_system_info()
    linex()
    print(f"{G} [1] {C}SPAM MESSENGER{RS}")
    print(f"{G} [2] {C}SETTINGS{RS}")
    print(f"{G} [3] {C}STATISTICS{RS}")
    print(f"{G} [4] {C}ACCOUNT{RS}")
    print(f"{R} [0] {C}EXIT{RS}")
    linex()

class SpamMessenger:
    def __init__(self):
        self.running = False
        self.paused = False
        self.total_sent = 0
        self.stats = {}
        self.msg = ""
        self.boxes = []
        self.accounts = []
        self.HW = self.get_hardware_info()
        self.start_time = datetime.now()

    def get_hardware_info(self):
        try:
            result = subprocess.check_output(['free', '-m'], text=True).split('\n')[1].split()
            total = int(result[1])
        except:
            total = 2000
        if total >= 8000:
            return {'level':'HIGH','threads':12,'heartbeat':15,'reconnect':30}
        elif total >= 4000:
            return {'level':'MEDIUM','threads':6,'heartbeat':20,'reconnect':25}
        elif total >= 2000:
            return {'level':'LOW','threads':4,'heartbeat':25,'reconnect':20}
        else:
            return {'level':'VERY_LOW','threads':2,'heartbeat':30,'reconnect':15}

    def get_uid(self, cookie):
        try:
            for part in cookie.split(';'):
                if 'c_user' in part:
                    return part.split('=')[1].strip()
        except:
            pass
        return None

    def get_fb_dtsg(self, cookie):
        try:
            headers = {'Cookie': cookie, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            r = requests.get('https://www.facebook.com', headers=headers, timeout=10)
            match = re.search(r'name="fb_dtsg" value="([^"]+)"', r.text)
            if match:
                return match.group(1)
            return None
        except:
            return None

    def get_last_seq_id(self, cookie):
        try:
            uid = self.get_uid(cookie)
            fb_dtsg = self.get_fb_dtsg(cookie)
            if not uid or not fb_dtsg:
                return None
            form = {
                "queries": json.dumps({
                    "o0": {
                        "doc_id": "3336396659757871",
                        "query_params": {"limit": 1, "tags": ["INBOX"]}
                    }
                }),
                "fb_dtsg": fb_dtsg,
                "__user": uid
            }
            headers = {'Cookie': cookie, 'Content-Type': 'application/x-www-form-urlencoded'}
            r = requests.post("https://www.facebook.com/api/graphqlbatch/", data=form, headers=headers, timeout=10)
            if r.status_code == 200:
                content = r.text.replace('for(;;);', '')
                data = json.loads(content.split('\n')[0])
                if 'o0' in data and 'viewer' in data['o0']['data']:
                    return data['o0']['data']['viewer']['message_threads']['sync_sequence_id']
            return None
        except:
            return None

    def refresh_cookie(self, cookie):
        try:
            session = requests.Session()
            session.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; Android 14) Chrome/120.0.0.0 Mobile'})
            u = re.search(r'c_user=(\d+)', cookie)
            x = re.search(r'xs=([^;]+)', cookie)
            if not u or not x:
                return cookie
            session.cookies.set('c_user', u.group(1), domain='.facebook.com')
            session.cookies.set('xs', x.group(1), domain='.facebook.com')
            r = session.get('https://mbasic.facebook.com/', timeout=15)
            if r.status_code != 200:
                return cookie
            for ck_obj in session.cookies:
                if ck_obj.name == 'c_user':
                    nu = ck_obj.value
                elif ck_obj.name == 'xs':
                    nx = ck_obj.value
            if nu and nx:
                nc = f"c_user={nu}; xs={nx};"
                for ck_obj in session.cookies:
                    if ck_obj.name == 'datr':
                        nc += f" datr={ck_obj.value};"
                        break
                return nc
            return cookie
        except:
            return cookie

    def connect_mqtt(self, cookie, idx):
        try:
            uid = self.get_uid(cookie)
            if not uid:
                return None
            last_seq = self.get_last_seq_id(cookie)
            if not last_seq:
                return None
            session_id = random.randint(1, 2**53)
            user = {
                "u": uid, "s": session_id, "chat_on": "true", "fg": False,
                "d": str(uuid.uuid4()), "ct": "websocket", "aid": 219994525426954,
                "cp": 3, "ecp": 10,
                "st": ["/t_ms", "/messenger_sync_get_diffs", "/messenger_sync_create_queue"]
            }
            client = mqtt.Client(client_id="mqttwsclient", transport="websockets", protocol=mqtt.MQTTv31)
            client.username_pw_set(username=json.dumps(user, separators=(",", ":")), password="")
            client.tls_set(cert_reqs=ssl.CERT_NONE)
            client.tls_insecure_set(True)
            client.ws_set_options(path="/chat", headers={
                "Cookie": cookie,
                "Origin": "https://www.messenger.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 14) Chrome/120.0.0.0 Mobile"
            })
            client.connect("edge-chat.facebook.com", 443, 60)
            client.loop_start()
            time.sleep(2)
            return client
        except:
            return None

    def send_message(self, client, uid, box_id, message):
        try:
            mid = str(int(time.time()*1000)) + str(random.randint(1000,9999))
            payload = {
                "body": message, "msgid": mid,
                "sender_fbid": uid, "to": box_id,
                "offline_threading_id": mid
            }
            client.publish("/send_message2", json.dumps(payload), qos=0)
            return True
        except:
            return False

    def get_boxes_manual(self):
        print(f"\n{C}◈ Enter box IDs (one per line, type 'done' to finish){RS}")
        boxes = []
        while True:
            try:
                box = input(f"  {C}Box ID: {RS}").strip()
                if box.lower() == 'done' or box == '':
                    break
                if box.isdigit():
                    boxes.append(box)
                    print(f"{G}✓ Added: {box}{RS}")
                else:
                    print(f"{R}✘ Invalid ID (must be digits){RS}")
            except:
                break
        return boxes

    def load_new_config(self):
        cookie_file = input(f"  {C}Cookie file (default cookies.txt): {RS}").strip()
        if not cookie_file:
            cookie_file = "cookies.txt"
        try:
            with open(cookie_file, 'r') as f:
                self.accounts = [l.strip() for l in f if l.strip()]
            print(f"{G}✓ Loaded {len(self.accounts)} cookies from {cookie_file}{RS}")
        except:
            print(f"{R}✘ File not found: {cookie_file}!{RS}")
            return False
        
        print(f"\n{C}◈ Enter box IDs (manual){RS}")
        self.boxes = self.get_boxes_manual()
        if not self.boxes:
            print(f"{R}✘ No boxes!{RS}")
            return False
        
        print(f"")
        msg_file = input(f"  {C}Message file (default Ngon.txt): {RS}").strip()
        if not msg_file:
            msg_file = "Ngon.txt"
        try:
            with open(msg_file, 'r') as f:
                self.msg = f.read().strip()
            print(f"{G}✓ Loaded message from {msg_file}{RS}")
        except:
            print(f"{R}✘ File not found: {msg_file}! Enter manually:{RS}")
            self.msg = input(f"  {C}Message content: {RS}").strip()
            if not self.msg:
                print(f"{R}✘ No message!{RS}")
                return False
            save = input(f"  {C}Save to Ngon.txt? (y/n): {RS}").strip().lower()
            if save == 'y':
                with open("Ngon.txt", "w") as f:
                    f.write(self.msg)
                print(f"{G}✓ Saved message to Ngon.txt{RS}")
        return True

    def worker(self, idx, cookie, boxes, message):
        uid = self.get_uid(cookie)
        client = self.connect_mqtt(cookie, idx)
        if not client:
            print(f"{R}✘ C{idx+1} MQTT fail{RS}")
            self.stats[idx] = {'ok': 0, 'fail': 0, 'status': 'failed'}
            return
        self.stats[idx] = {'ok': 0, 'fail': 0, 'status': 'running'}
        print(f"{G}✓ C{idx+1} MQTT connected{RS}")
        delay = random.randint(20, 60)
        count = 0
        hb_time = time.time()
        retry_count = 0
        while self.running:
            try:
                if not client.is_connected():
                    print(f"{Y}⚠ C{idx+1} reconnecting...{RS}")
                    cookie = self.refresh_cookie(cookie)
                    client = self.connect_mqtt(cookie, idx)
                    if not client:
                        retry_count += 1
                        if retry_count >= 3:
                            print(f"{R}✘ C{idx+1} reconnect fail{RS}")
                            self.stats[idx]['status'] = 'failed'
                            return
                        time.sleep(30)
                        continue
                    retry_count = 0
                    print(f"{G}✓ C{idx+1} reconnected{RS}")
                for box in boxes:
                    if not self.running or self.paused:
                        break
                    if self.send_message(client, uid, box, message):
                        self.stats[idx]['ok'] += 1
                        self.total_sent += 1
                        print(f"{C}✓ C{idx+1} → {box}{RS}")
                    else:
                        self.stats[idx]['fail'] += 1
                        print(f"{R}✘ C{idx+1} → {box} fail{RS}")
                    time.sleep(random.uniform(0.5, 1.5))
                count += 1
                if count % 5 == 0:
                    now = time.time()
                    if now - hb_time > self.HW['heartbeat']:
                        try:
                            client.publish("/t_ms", json.dumps({"t": int(now*1000)}), qos=0)
                            hb_time = now
                        except:
                            pass
                if count % 20 == 0:
                    gc.collect()
                time.sleep(delay)
            except:
                time.sleep(5)

    def show_status(self):
        print(f"\n{B}{'═'*50}{RS}")
        print(f"{W}  STATUS{RS}")
        print(f"{B}{'═'*50}{RS}")
        for idx, stat in self.stats.items():
            status = stat.get('status', 'unknown')
            ok = stat.get('ok', 0)
            fail = stat.get('fail', 0)
            color = G if status == 'running' else R
            print(f"{W}  C{idx+1}: {color}{status}{RS} | OK: {ok} | FAIL: {fail}")
        elapsed = datetime.now() - self.start_time
        hours, remainder = divmod(elapsed.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"{W}  Time: {hours}h {minutes}m {seconds}s | Total sent: {self.total_sent}{RS}")
        print(f"{B}{'═'*50}{RS}\n")

    def start_spam(self):
        clear()
        loading_animation("Starting SPAM MESSENGER", 1.5)
        banner()
        print(f"\n{C}◈ SPAM MESSENGER PRO{RS}\n")
        linex()
        
        if not self.load_new_config():
            input(f"\n{C}[Enter] back{RS}")
            return
        
        print(f"\n{C}◈ Hardware: {self.HW['level']} - {self.HW['threads']} threads{RS}\n")
        
        self.running = True
        self.paused = False
        self.start_time = datetime.now()
        
        for i, cookie in enumerate(self.accounts):
            if i >= self.HW['threads']:
                break
            t = threading.Thread(target=self.worker, args=(i, cookie, self.boxes, self.msg))
            t.daemon = True
            t.start()
            print(f"{G}✓ C{i+1} started{RS}")
            time.sleep(0.5)
        
        print(f"\n{C}◈ Type 'help' for commands{RS}\n")
        
        while self.running:
            try:
                cmd = input(f"{C}> {RS}").strip().lower()
                if cmd == 'help':
                    print(f"""
{C}╔═══════════════════════════════════════════════╗
║  COMMANDS:                                  ║
╠═══════════════════════════════════════════════╣
║  start    - Start spam                     ║
║  stop     - Stop spam                      ║
║  pause    - Pause spam                     ║
║  resume   - Resume spam                    ║
║  status   - Show status                    ║
║  q/quit   - Quit                           ║
╚═══════════════════════════════════════════════╝{RS}
""")
                elif cmd == 'start':
                    if not self.running:
                        self.running = True
                        print(f"{G}✓ Started{RS}")
                elif cmd == 'stop':
                    self.running = False
                    print(f"{Y}◈ Stopping...{RS}")
                elif cmd == 'pause':
                    self.paused = True
                    print(f"{Y}◈ Paused{RS}")
                elif cmd == 'resume':
                    self.paused = False
                    print(f"{G}✓ Resumed{RS}")
                elif cmd == 'status':
                    self.show_status()
                elif cmd in ['q', 'quit']:
                    self.running = False
                    break
            except:
                pass

def main():
    loading_animation("Initializing KENSI TOOL", 2)
    key = KeySystem()
    if not key.auth():
        print(f"{R}License failed!{RS}")
        sys.exit(1)
    
    threading.Thread(target=key.monitor, daemon=True).start()
    
    while True:
        menu()
        ch = input(f"{C}> {RS}").strip()
        if ch == "0":
            print(f"{R}Bye!{RS}")
            break
        elif ch == "1":
            spam = SpamMessenger()
            spam.start_spam()
        elif ch in ["2", "3", "4"]:
            print(f"{Y}Coming soon!{RS}")
            time.sleep(1)
        else:
            print(f"{R}Invalid!{RS}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Y}Stopped{RS}")
        gc.collect()
    except Exception as e:
        print(f"\n{R}Error: {e}{RS}")
        gc.collect()