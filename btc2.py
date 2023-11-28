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

sc_ver = "CLAIMBTC.ONLINE v5"

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
        self.service_solver = None
        self.active_auto_wd = False
        self.live_roll = False

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
                    self.login()
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
        def curl(url, data=None):
            while True:
                try:
                    if data is None:
                        r = requests.get(url)
                    else:
                        r = requests.post(url, data=data)
                    if r.status_code == 200:
                        return r.text
                    if r.status_code >= 500:
                        self.carousel_msg(f"{self.service_solver.capitalize()} is down now")
                except requests.ConnectionError:
                    self.carousel_msg(f"Reconnecting to {self.service_solver.capitalize()}")
                except requests.Timeout:
                    self.carousel_msg("Too many requests")
                    self.carousel_msg("Plase wait a few seconds")
                self.wait(randint(10,30))

        def get_id_task(method, pageurl):
            self.carousel_msg("Getting id task")
            key = self.mkey if self.service_solver.lower() == "multibot" else self.xkey
            payload = {"key": key, "method": method, "pageurl": pageurl}
            if self.service_solver.lower() == "multibot":
                payload['googlekey'] = sitekey
            if self.service_solver.lower() == "xevil":
                payload['sitekey'] = sitekey
            while True:
                r = curl(f"{url_base}/in.php", payload)
                if '|' in r:
                    self.carousel_msg("Succes created id task")
                    return r.split("|")[1]
                else:
                    self.carousel_msg(f"Error creating {method} id task")
                time.sleep(1)

        def get_solved(method, pageurl, id_task):
            self.carousel_msg("Getting token captcha")
            def get_url_task(id_task):
                key = self.mkey if self.service_solver.lower() == "multibot" else self.xkey
                expar = "action=get&" if self.service_solver == "multibot" else ""
                return f"{url_base}/res.php?key={key}&{expar}id={id_task}"

            method = method
            pageurl = pageurl
            url = get_url_task(id_task)
            while True:
                r = curl(url)
                if 'CAPCHA_NOT_READY' in r:
                    self.cicles += 1
                    self.t_cicles += 1
                    self.carousel_msg(f"Captcha not ready  ●  Attemps: [ {self.cicles}/{self.t_cicles} ]")
                    time.sleep(0.1)
                    if self.cicles >= 50:
                        self.cicles = 0
                        task = get_id_task(method, pageurl)
                        url = get_url_task(task)
                elif '|' in r:
                    self.carousel_msg("Success get captcha")
                    return r.split("|")[1]
                else:
                    self.cicles = 0
                    self.carousel_msg("Error requesting captcha")
                    time.sleep(1)
                    task = get_id_task(method, pageurl)
                    url = get_url_task(task)

        def get_balance():
            self.carousel_msg(f"Getting balance {self.service_solver.lower()}")
            key = self.mkey if self.service_solver.lower() == "multibot" else self.xkey
            action = "userinfo" if self.service_solver.lower() == "multibot" else "getbalance"
            while True:
                userinfo = curl(f"{url_base}/res.php?action={action}&key={key}")
                if self.service_solver.lower() == "multibot":
                    if userinfo == "[]":
                        print(f"{red}Bad {self.service_solver.lower()} api key{res}{end}")
                        exit()
                    userinfo = json.loads(userinfo)
                    if userinfo['balance']:
                        balance = userinfo['balance']
                        if int(balance) <= 0:
                            print(f"{red}Dont have balance in {self.service_solver.lower()}{res}{end}")
                            exit()
                        elif int(balance) > 0:
                            return userinfo['balance']
                if self.service_solver.lower() == "xevil":
                    balance = userinfo
                    if float(balance) <= 0:
                        print(f"{red}Dont have balance in {self.service_solver.lower()}{res}{end}")
                        exit()
                    if float(balance) > 0:
                        return userinfo
                self.carousel_msg("Error getting balance")
                time.sleep(1)

        sitekey = "24f7fecd-2a96-4b03-89d1-7b417eefc12a"
        pageurl = "https://claimbtc.online/"
        method = "hcaptcha"

        url_base = "http://api.multibot.in" if self.service_solver.lower() == "multibot" else "http://goodxevilpay.pp.ua"
        self.t_cicles, self.cicles = 0, 0

        balance = get_balance()
        id_task = get_id_task(method, pageurl)
        id_captcha= get_solved(method, pageurl, id_task)
        return id_captcha, balance
    
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
            roll_min = 1
            roll_max = 9000
            live = 'OFF'
            try:
                with open('config.json', 'r') as f:
                    obj = json.load(f)
                    live_roll = obj.get('Live Roll', {})
                    toggle = live_roll.get('Toggle')
                    min_max = live_roll.get('Min/Max')
                    if toggle.lower() == 'on' and isinstance(min_max, list) and len(min_max) == 2:
                        live = 'ON'
                        roll_min, roll_max = min_max
                        if roll_min > roll_max:
                            roll_min = roll_max
                            roll_max = roll_min
            except (json.JSONDecodeError, FileNotFoundError, ValueError):
                if randint(1, 100) % 2 == 0:
                    roll_min = 9987
                    roll_max = 9999
            next_roll = randint(roll_min, roll_max)
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
                captcha, bal_solver = self.solver()
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
                    print(f" {red}# {white}Live: {red}{live}{res}{end}")
                    print(f" {red}# {white}Range: {white}{roll_min}-{roll_max}{res}{end}")
                    print(f" {red}# {white}Reward: {green}{reward}{res} BTC{end}")
                    print(f" {red}# {white}Balance: {green}{balance}{res} BTC{end}")
                    print(f" {red}# {white}Balance Multibot: {green}{bal_solver}{res}{end}")
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
                captcha, bal_solver = self.solver()
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
            config = {
                'Username': '', 
                'Password': '', 
                'User-Agent': '', 
                'Multibot Key': '', 
                'Auto Wd': {
                    'Toggle': '', 
                    'Faucetpay Btc': ''
                },
                'Live Roll': {
                    'Toggle': 'ON',
                    'Min/Max': [9997,9999]
                }
            }

        keywords = ['Username', 'Password', 'User-Agent', 'Multibot Key', 'Xevil Key']

        for key in keywords:
            while key not in config or len(config[key]) < 5:
                config[key] = input(f"\n{yellow}{key}{red}:{res} ")

        if 'Auto Wd' not in config:
            config['Auto Wd'] = {'Toggle': '', 'Faucetpay Btc': ''}

        auto_wd_choice = "y"
        while auto_wd_choice not in ["y", "n"]:
            print("Please enter a valid choice ('y' or 'n').")
            auto_wd_choice = input(f"\n{yellow}Do you want to activate 'auto withdraw'? (y/n):{res} ").lower()

        config['Auto Wd']['Toggle'] = "on" if auto_wd_choice == "y" else "off"

        if auto_wd_choice == "y":
            while 'Faucetpay Btc' not in config['Auto Wd'] or len(config['Auto Wd']['Faucetpay Btc']) < 10:
                config['Auto Wd']['Faucetpay Btc'] = input(f"\n{yellow}Faucetpay Btc{red}:{res} ")
            self.active_auto_wd = True
        
        if 'Live Roll' not in config:
            config['Live Roll'] = {'Toggle': 'off', 'Min/Max': [9997,9999]}

        os.system("clear" if os.name == "posix" else "cls")
        option = '1'
        if option.isdigit() and 1 <= int(option) <= 2:
            if str(option) == "1":
                self.service_solver = "multibot"
            else:
                self.service_solver = "xevil"
    
        self.write_file(config)
        self.username = config['Username']
        self.password = config['Password']
        self.user_agent = config['User-Agent']
        self.mkey = config['Multibot Key']
        self.xkey = config['Xevil Key']
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
