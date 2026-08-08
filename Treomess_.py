# -*- coding: utf-8 -*-
import os, sys, time, json, random, threading, subprocess, re, gc
from datetime import datetime
import requests

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    clear()
    print(f"{CYAN}{'═'*50}{RESET}")
    print(f"{WHITE}  KENSI TREO MESSENGER v1.0{RESET}")
    print(f"{CYAN}{'═'*50}{RESET}\n")

class TreoMessenger:
    def __init__(self):
        self.cookies = []
        self.boxes = []
        self.msg = ""
        self.delays = []
        self.running = True
        self.threads = []

    def load_cookies(self):
        try:
            with open("cookies.txt", "r") as f:
                self.cookies = [l.strip() for l in f if l.strip()]
            print(f"{GREEN}✓ Loaded {len(self.cookies)} cookies{RESET}")
        except:
            print(f"{RED}✘ No cookies.txt{RESET}")
            return False
        return True

    def load_boxes(self):
        try:
            with open("boxes.txt", "r") as f:
                self.boxes = [l.strip() for l in f if l.strip()]
            print(f"{GREEN}✓ Loaded {len(self.boxes)} boxes{RESET}")
        except:
            print(f"{RED}✘ No boxes.txt{RESET}")
            return False
        return True

    def load_msg(self):
        try:
            with open("msg.txt", "r") as f:
                self.msg = f.read().strip()
            print(f"{GREEN}✓ Loaded message{RESET}")
        except:
            print(f"{RED}✘ No msg.txt{RESET}")
            return False
        return True

    def get_uid(self, cookie):
        try:
            for part in cookie.split(';'):
                if 'c_user' in part:
                    return part.split('=')[1].strip()
        except:
            pass
        return None

    def get_xs(self, cookie):
        try:
            for part in cookie.split(';'):
                if 'xs' in part:
                    return part.split('=')[1].strip()
        except:
            pass
        return None

    def send_message(self, cookie, box, msg):
        try:
            uid = self.get_uid(cookie)
            xs = self.get_xs(cookie)
            if not uid or not xs:
                return False
            
            url = "https://www.facebook.com/messages/send/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 14) Chrome/120.0.0.0 Mobile",
                "Cookie": cookie,
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://www.facebook.com",
                "Referer": "https://www.facebook.com/"
            }
            data = {
                "message": msg,
                "thread_id": box,
                "thread_fbid": box,
                "recipients": box,
                "fb_dtsg": "AQF..."
            }
            r = requests.post(url, headers=headers, data=data, timeout=10)
            return r.status_code == 200
        except:
            return False

    def worker(self, cookie, boxes, msg, delay):
        count = 0
        while self.running:
            try:
                for box in boxes:
                    if not self.running:
                        break
                    if self.send_message(cookie, box, msg):
                        print(f"{GREEN}✓ OK → {box}{RESET}")
                    else:
                        print(f"{RED}✘ FAIL → {box}{RESET}")
                    time.sleep(random.uniform(0.5, 1.5))
                count += 1
                if count % 5 == 0:
                    gc.collect()
                time.sleep(delay)
            except:
                time.sleep(5)

    def run(self):
        banner()
        print(f"{CYAN}◈ KENSI TREO MESSENGER{RESET}\n")
        
        if not self.load_cookies():
            return
        if not self.load_boxes():
            return
        if not self.load_msg():
            return
        
        print(f"{CYAN}◈ Starting...{RESET}\n")
        
        for i, cookie in enumerate(self.cookies):
            delay = random.randint(20, 60)
            self.delays.append(delay)
            print(f"  CK {i+1}: delay {delay}s")
        
        print()
        for i, cookie in enumerate(self.cookies):
            t = threading.Thread(target=self.worker, args=(cookie, self.boxes, self.msg, self.delays[i]))
            t.daemon = True
            t.start()
            self.threads.append(t)
            time.sleep(0.5)
        
        print(f"{GREEN}✓ Started {len(self.threads)} threads{RESET}")
        print(f"{YELLOW}Press Ctrl+C to stop{RESET}")
        
        try:
            while self.running:
                time.sleep(60)
        except KeyboardInterrupt:
            self.running = False
            print(f"\n{YELLOW}Stopped{RESET}")

def main():
    treo = TreoMessenger()
    treo.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Exit{RESET}")
