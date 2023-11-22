import re
import os
import sys
import json
import time
import requests
from random import randint, choice, uniform
from datetime import datetime
from bs4 import BeautifulSoup
from json.decoder import JSONDecodeError
from colorama import Fore, Back, Style, init

s = requests.Session()

init(autoreset=True)

sc_ver = "CLAIMBTC.ONLINE v4"

end = "\033[K"
res = Style.RESET_ALL
red = Style.BRIGHT+Fore.RED
bg_red = Back.RED
white = Style.BRIGHT+Fore.WHITE
green = Style.BRIGHT+Fore.GREEN
yellow = Style.BRIGHT+Fore.YELLOW
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

class Bot:
    def __init__(self):
        self.file = 'config.json'
        self.active_auto_wd = False

    def curl(self, url, headers, data=None):
        while True:
            try:
                if data is None:
                    r = s.get(url=url, headers=headers)
                else:
                    r = s.post(url=url, headers=headers, data=data)
                if r.status_code == 200:
                    return r.text
                elif r.status_code == 403:
                    self.login(True)
                elif r.status_code >= 500:
                    self.carousel_msg("Website error, try in few moment")
                    self.wait(randint(5,10) * 60)
                else:
                    self.update_cookies_emkkey()
            except requests.ConnectionError:
                self.carousel_msg("Reconnecting to claimbtc.online")
            except requests.Timeout:
                self.carousel_msg("Too many requests")
            except requests.Exception as e:
                self.carousel_msg(f"Unexpected requests, Error: {e}")
            self.carousel_msg("Plase wait a few minutos")
            self.wait(randint(1,5))

    def wait(self, x):
        for i in range(x, -1, -1):
            col = yellow if i%2 == 0 else white
            animation = "⫸" if i%2 == 0 else "⫸⫸"
            m, s = divmod(i, 60)
            t = f"[00:{m:02}:{s:02}]"
            sys.stdout.write(f"\r  {white}Please wait {col}{t} {animation}{res}{end}\r")
            sys.stdout.flush()
            time.sleep(1)

    def carousel_msg(self, msg):
        left_spaces = (50 - len(msg)) // 2
        right_spaces = 50 - len(msg) - left_spaces
        animated_message = f"{' ' * left_spaces}{msg}{' ' * right_spaces}"
        msg_effect = ""
        for i in range(len(animated_message)-1):
            msg_effect += animated_message[i]
            sys.stdout.write(f"\r{msg_effect}{res}{end}")
            sys.stdout.flush()
            time.sleep(0.03)
        time.sleep(2)
        sys.stdout.write(f"\r{res}{end}\r")
        sys.stdout.flush()

    def msg_line(self):
        print(f"{green}{'━' * 50}")

    def msg_action(self, action):
        now = datetime.now()
        now = now.strftime("%d/%b/%Y %H:%M:%S")
        total_length = len(action) + len(now) + 5
        space_count = 50 - total_length
        msg = f"[{action.upper()}] {now}{' ' * space_count}"
        print(f"{bg_red} {white}{msg}{res}{red}⫸{res}{end}")

    def auto_wd(self, amount):
        rand_amount = randint(50,100)
        if amount >= rand_amount:
            while True:
                self.carousel_msg("Go to withdraw section")
                min_wd, max_wd, emtoken = None, None, None
                while True:
                    payload = {"api_key": self.em_key}
                    headers = {
                        "User-Agent": self.user_agent,
                        "X-Requested-With": "XMLHttpRequest",
                        "Accept": "*/*",
                        "cookie": self.cookie_str
                    }
                    r = self.curl("https://claimbtc.online/em-assets/themes/default/fund/withdraw/", headers, payload)
                    soup = BeautifulSoup(r, 'html.parser')
                    try:
                        max_wd = soup.select_one('#fund_fp input[type="text"]').get('value', '')
                        elements_type = soup.find_all('div', {'class': 'type'})
                    except (TypeError, ValueError, AttributeError):
                        self.carousel_msg("Invalid cookies or Em-key")
                        self.carousel_msg("Redirect to login...")
                        self.wait(10)
                        self.login()
                        break
                    for element_type in elements_type:
                        if 'faucetpay.png' in str(element_type):
                            element_min = element_type.find_next('div', {'class': 'min'})
                            if element_min is not None:
                                min_wd = element_min.find('span').text
                                element_data = element_type.find_next('div', {'class': 'data'})
                                if element_data is not None:
                                    emtoken = element_data.get('id')
                                    emtoken = emtoken.split('/')[1]
                                    break
                    if min_wd and max_wd and emtoken :
                        break
                    self.wait(5)
                if 'Pending' in r:
                    self.carousel_msg("Pending withdrawals in queue")
                    break
                if int(min_wd) <= amount <= int(max_wd):
                    payload = {
                        "emtoken": emtoken,
                        "wd_value": str(amount),
                        "wd_addr": self.wallet,
                        "usr_curpass": self.password
                    }
                    while True:
                        self.carousel_msg("Creating request withdraw")
                        r = self.curl("https://claimbtc.online/em-apc/u/W7DFpY", headers, payload)
                        time.sleep(0.1)
                        v = self.data_account()
                        if 'Your withdrawal request has been successfully sent' in v[2]:
                            self.carousel_msg("Withdraw success")
                            amount = self.formating(amount)
                            self.msg_action("WITHDRAW")
                            print(f" {red}# {white}Status: {yellow}Pending{res}{end}")
                            print(f" {red}# {white}Amount: {green}{amount}{res} BTC{end}")
                            print(f" {red}# {white}Address BTC: {yellow}{self.wallet}{res}{end}")
                            self.msg_line()
                        else:
                            if 'balance is not enough' in r.lower() or v[2] == '':
                                self.carousel_msg("Not have min autowd amount")
                        break
                else:
                    self.carousel_msg("Not have min autowd amount")
                break

    def solver(self):
        while True:
            url = "http://api.multibot.in/in.php"
            sitekey = "24f7fecd-2a96-4b03-89d1-7b417eefc12a"
            while True:
                payload = {
                    "key": self.mkey,
                    "method": "hcaptcha",
                    "googlekey": sitekey,
                    "pageurl": "https://claimbtc.online/"
                }
                try:
                    r = requests.post(url=url, data=payload)
                    if 'OK' in r.text:
                        id_task = r.text.split("OK|")[1]
                        break
                except requests.ConnectionError:
                    self.carousel_msg("Reconnecting to multibot.in")
                    self.carousel_msg("Connection timeout")
                except requests.Timeout:
                    self.carousel_msg("Too many requests")
                    self.carousel_msg("Plase wait a few seconds")
                self.wait(randint(20,40))
            
            cicles = 0
            while True:
                url = f"http://api.multibot.in/res.php?key={self.mkey}&action=get&id={id_task}"
                try:
                    r = requests.get(url)
                    if r.status_code == 200:
                        if 'CAPCHA_NOT_READY' in r.text:
                            cicles += 1
                            self.carousel_msg(f"H-captcha not ready  ●  Attemps:  [ {cicles} ]")
                            time.sleep(0.1)
                        else:
                            if 'OK' in r.text:
                                self.carousel_msg("Success get h-captcha")
                                captcha = r.text.split("OK|")[1]
                                return captcha
                            cicles = 0
                            self.carousel_msg("Error requesting captcha")
                            break
                except requests.ConnectionError:
                    self.carousel_msg("Reconnecting to multibot.in")
                    self.carousel_msg("Connection timeout")
                except requests.Timeout:
                    self.carousel_msg("Too many requests")
                    self.carousel_msg("Plase wait a few seconds")

    def data_account(self):
        username, balance, success = None, None, ''
        while True:
            payload = {"api_key": self.em_key}
            headers = {
                "User-Agent": self.user_agent,
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "*/*",
                "cookie": self.cookie_str
            }
            r = self.curl("https://claimbtc.online/em-assets/themes/default/dash/", headers, payload)
            soup = BeautifulSoup(r, 'html.parser')
            try:
                success = soup.find('div', class_='msg success')
                username = soup.find('a', {'href': 'https://claimbtc.online/user/settings/'}).get('title')
                balance = soup.find('div', class_='balance')
                balance = balance.find('div', class_='num').find('span').text.strip()
                success = '' if success is None else success.text.strip()
                if username and balance:
                    return username, int(balance), success
            except (TypeError, ValueError, AttributeError):
                self.carousel_msg("Invalid cookies or Em-key")
                self.carousel_msg("Redirect to login...")
                self.wait(10)
                self.login()
                self.claim()

    def claim(self):
        while True:
            self.carousel_msg("Go to faucet section")
            while True:
                emtoken = None
                payload = {"api_key": self.em_key}
                headers = {
                    "User-Agent": self.user_agent,
                    "X-Requested-Whit": "XMLHttpRequest",
                    "Accept": "*/*",
                    "cookie": self.cookie_str
                }
                r = self.curl("https://claimbtc.online/em-assets/themes/default/earn/faucet/", headers, payload)
                soup = BeautifulSoup(r, 'html.parser')
                try:
                    emtoken = soup.find('button', class_='btn')['id']
                except (TypeError, ValueError, AttributeError):
                    if str(self.username).lower() in r.lower():
                        self.carousel_msg("Faucet not available now")
                        self.carousel_msg("Checking faucet roll later")
                        self.wait(120)
                    else:
                        self.carousel_msg("Invalid cookies or Em-key")
                        self.carousel_msg("Redirect to login...")
                        self.wait(10)
                        self.login()
                    break
                if randint(1,1000) % 5 == 0:
                    next_roll = randint(1,9999)
                else:
                    next_roll = randint(9886,9999)
                captcha = self.solver()
                payload = {
                    "emtoken": emtoken,
                    "roll_num": next_roll,
                    "g-recaptcha-response": captcha,    
                    "h-captcha-response": captcha
                }
                headers = {
                    "User-Agent": self.user_agent,
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "cookie": self.cookie_str
                }
                self.carousel_msg("Claiming roll faucet")
                r = self.curl("https://claimbtc.online/em-apc/u/Fc7R1l", headers, payload)
                time.sleep(0.1)
                v = self.data_account()
                if 'Satoshi have been added to your account' in v[2]:
                    self.carousel_msg("Claim roll success")
                    self.carousel_msg("Getting user info")
                    reward = v[2].split(' ')[0]
                    bal = v[1]
                    balance = self.formating(bal)
                    reward = self.formating(reward)
                    self.msg_action("FAUCET")
                    print(f" {red}# {white}Roll: {green}{next_roll}{res}{end}")
                    print(f" {red}# {white}Reward: {green}{reward}{res} BTC{end}")
                    print(f" {red}# {white}Balance: {green}{balance}{res} BTC{end}")
                    self.msg_line()
                    time.sleep(1)
                    if self.active_auto_wd:
                        self.auto_wd(bal)
                    self.wait(60 * 60)
                else:
                    self.carousel_msg("Claim failed")
                    self.wait(60)
                break
                
    
    def write_file(self, data):
        with open(self.file, 'w') as f:
            json.dump(data, f, indent=4)

    def login(self):
        self.carousel_msg("Login proccessing...")
        self.cookie_str = {}
        while True:
            while True:
                url = "https://claimbtc.online/login/"
                payload = {}
                headers = {
                  'authority': 'claimbtc.online',
                  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                  'referer': 'https://claimbtc.online/',
                  'user-agent': self.user_agent
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                match = re.search(r"var apiKey = '([^']*)'", response.text)
                if match:
                    self.carousel_msg("Success found Api-Key")
                    api_key = match.group(1)
                    self.em_key = api_key
                    self.cookie_str = '; '.join([f"{name}={value}" for name, value in response.cookies.items()])
                    break
                else:
                    self.carousel_msg("Api-Key not found")
                    break
            
            while True:
                url = "https://claimbtc.online/em-assets/themes/default/auth/login/"
                payload = {'api_key': api_key}
                files=[
                    
                ]
                headers = {
                  'authority': 'claimbtc.online',
                  'accept': '*/*',
                  'cookie': self.cookie_str,
                  'origin': 'https://claimbtc.online',
                  'referer': 'https://claimbtc.online/login/',
                  'user-agent': self.user_agent,
                  'x-requested-with': 'XMLHttpRequest'
                }
                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                soup = BeautifulSoup(response.text, 'html.parser')
                id_em = soup.find('div', {'class': 'data'})
                if id_em:
                    id_em = id_em.get('id').split('/')[1]
                    self.carousel_msg("Success found Em-Key")
                    break
                else:
                    print("Em-Key not found")
                    break
                self.wait(5)
            
            while True:
                url = "https://claimbtc.online/em-apc/u/ULo91N"
                captcha = self.solver()
                payload = f"emtoken={id_em}&user_identity={self.username}&user_pass={self.password}&user_2fa=&user_remember=on&g-recaptcha-response={captcha}&h-captcha-response={captcha}"
                headers = {
                  'authority': 'claimbtc.online',
                  'accept': 'application/json, text/javascript, */*; q=0.01',
                  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  'cookie': self.cookie_str,
                  'origin': 'https://claimbtc.online',
                  'referer': 'https://claimbtc.online/login/',
                  'user-agent': self.user_agent,
                  'x-requested-with': 'XMLHttpRequest'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                self.cookie_str = '; '.join([f"{name}={value}" for name, value in response.cookies.items()])
                time.sleep(0.1)
                v = self.data_account()
                if 'Successfully login to your account' in v[2]:
                    self.carousel_msg(v[2])
                    return
                else:
                    self.carousel_msg("Login failed")
                    self.wait(10)
                    break

    def formating(self, num):
        value = float(num) / 10**8
        return "{:.8f}".format(value)

    def start(self):
        self.carousel_msg("Getting user info")
        v = self.data_account()
        username = v[0]
        bal = v[1]
        balance = self.formating(bal)
        print(f"\n{bg_red}{white} ๏ {res} {yellow}〔 USERNAME 〕.: {res}{username}{end}")
        print(f"{bg_red}{white} ๏ {res} {yellow}〔 BALANCE 〕..: {res}{balance} BTC{end}")
        print(f"{res}{end}")
        self.msg_line()
        if self.active_auto_wd:
            self.auto_wd(bal)

    def config(self):
        try:
            with open(self.file, 'r') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {'Username': '', 'Password': '', 'User-Agent': '', 'Multibot Key': '', 'Auto Wd': {'Toggle': '','Faucetpay Btc': ''}}

        keywords = ['Username', 'Password', 'User-Agent', 'Multibot Key']

        for key in keywords:
            while key not in config or len(config[key]) < 5:
                config[key] = input(f"\n{yellow}{key}{red}:{res} ")

        if 'Auto Wd' not in config:
            config['Auto Wd'] = {'Toggle': '', 'Faucetpay Btc': ''}

        auto_wd_choice = "y" #input(f"\n{yellow}Do you want to activate 'auto withdraw'? (y/n):{res} ").lower()
        while auto_wd_choice not in ["y", "n"]:
            print("Please enter a valid choice ('y' or 'n').")
            auto_wd_choice = input(f"\n{yellow}Do you want to activate 'auto withdraw'? (y/n):{res} ").lower()

        config['Auto Wd']['Toggle'] = "on" if auto_wd_choice == "y" else "off"

        if auto_wd_choice == "y":
            while 'Faucetpay Btc' not in config['Auto Wd'] or len(config['Auto Wd']['Faucetpay Btc']) < 10:
                config['Auto Wd']['Faucetpay Btc'] = input(f"\n{yellow}Faucetpay Btc{red}:{res} ")
            self.active_auto_wd = True
    
        self.write_file(config)
        self.username = config['Username']
        self.password = config['Password']
        self.user_agent = config['User-Agent']
        self.mkey = config['Multibot Key']
        self.wallet = config['Auto Wd']['Faucetpay Btc']

        os.system("clear" if os.name == "posix" else "cls")
        self.msg_line()
        print(f"{green}{sc_ver.center(50, ' ')}")
        self.msg_line()
        self.login()
        self.start()
        self.claim()

bot = Bot()
bot.config()
