import re
import os
import sys
import json
import time
import requests
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime
from json.decoder import JSONDecodeError
from random import randint, choice, uniform
from colorama import Fore, Back, Style, init
from requests.exceptions import RequestException, ConnectionError, Timeout

s = requests.Session()

init(autoreset=True)

sc_ver = "WORKPAID v2"
host = 'workpaid.net'

end = "\033[K"
res = Style.RESET_ALL
red = Style.BRIGHT+Fore.RED
bg_red = Back.RED
white = Style.BRIGHT+Fore.WHITE
green = Style.BRIGHT+Fore.GREEN
yellow = Style.BRIGHT+Fore.YELLOW
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

def clean_screen():
    os.system("clear" if os.name == "posix" else "cls")

class Bot:
    def __init__(self):
        self.rolls_claimed = 0
        self.previousbal = 0
        self.wd_amount = None
        self.active_auto_wd = False
        self.live_roll = False

    def curl(self, method, url, headers=None, data=None):
        base_headers = {
            'keep-alive': 'timeout=5, max=100',
            'connection': 'keep-alive',
            'user-agent': self.user_agent,
        }
        if headers:
            base_headers.update(headers)
        while True:
            try:
                r = s.request(method, url, headers=base_headers, data=data, timeout=10)
                if r.status_code == 200:
                    return r
                elif r.status_code == 403:
                    self.carousel_msg("Access denied")
                    return None
                elif 500 <= r.status_code < 600:
                    self.carousel_msg(f"Server {host} down.")
                else:
                    self.carousel_msg(f"Unexpected response code: {r.status_code}")
                    return None
            except ConnectionError:
                self.carousel_msg(f"Reconnecting to {host}")
            except Timeout:
                self.carousel_msg("Too many requests")
            self.wait(5)

    def wait(self, x):
        for i in range(x, -1, -1):
            col = yellow if i%2 == 0 else white
            animation = "⫸" if i%2 == 0 else "⫸⫸"
            m, s = divmod(i, 60)
            t = f"[00:{m:02}:{s:02}]"
            sys.stdout.write(f"\r  {white}Please wait {col}{t} {animation}{res}{end}\r")
            sys.stdout.flush()
            sleep(1)

    def carousel_msg(self, message):
        def first_part(message, wait):
            animated_message = message.center(48)
            msg_effect = ""
            for i in range(len(animated_message) - 1):
                msg_effect += animated_message[i]
                sys.stdout.write(f"\r {msg_effect}{res} {end}")
                sys.stdout.flush()
                sleep(0.03)
            if wait:
                sleep(1)

        msg_effect = message[:47]
        wait = True if len(message) <= 47 else False
        first_part(msg_effect, wait)
        if len(message) > 47:
            for i in range(50, len(message)):
                msg_effect = msg_effect[1:] + message[i]
                if i > 1:
                    sys.stdout.write(f"\r {msg_effect} {res}{end}")
                    sys.stdout.flush()
                sleep(0.1)
        sleep(1)
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
        if (amount >= rand_amount or 
            self.wd_amount and isinstance(self.wd_amount, int) and self.wd_amount >= 10):
            while True:
                self.carousel_msg("Go to withdraw section")
                min_wd, max_wd, emtoken = None, None, None
                while True:
                    url = f"https://{host}/em-assets/themes/default/fund/withdraw/"
                    payload = {'api_key': self.em_key}
                    headers = {'x-requested-with': 'XMLHttpRequest'}
                    r = self.curl('POST', url, headers, payload)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    try:
                        max_wd = soup.select_one('#fund_fp input[type="text"]').get('value', '')
                        elements_type = soup.find_all('div', {'class': 'type'})
                    except (TypeError, ValueError, AttributeError):
                        self.carousel_msg("Invalid cookies or em-key")
                        self.carousel_msg("Redirect to login...")
                        self.wait(5)
                        self.login()
                        break
                    if elements_type:
                        for element_type in elements_type:
                            if 'faucetpay.png' in str(element_type):
                                element_min = element_type.find_next('div', {'class': 'min'})
                                if element_min is not None:
                                    min_wd = element_min.find('span').text
                                    element_data = element_type.find_next('div', {'class': 'data'})
                                    if element_data is not None:
                                        emtoken = element_data.get('id')
                                        param = emtoken.split('/')[0]
                                        emtoken = emtoken.split('/')[1]
                                        break
                    if min_wd and max_wd and emtoken:
                        break

                if 'Pending' in r.text:
                    self.carousel_msg("Pending withdrawals in queue")
                    break

                if int(min_wd) <= amount <= int(max_wd) and self.wallet:
                    url = f"https://{host}/em-apc/u/{param}"
                    payload = {
                        'emtoken': emtoken,
                        'wd_value': str(amount),
                        'wd_addr': self.wallet,
                        'usr_curpass': self.password
                    }
                    self.carousel_msg("Creating request withdraw")
                    r = self.curl('POST', url, headers, payload)
                    try:
                        r = json.loads(r.text)
                    except Exception as e:
                        self.carousel_msg("Error")
                        self.carousel_msg(str(e))
                        sleep(5)
                        break
                    if 'success' in r and r['success']:
                        self.carousel_msg("Withdraw success")
                        amount = self.formating(amount)
                        self.msg_action("WITHDRAW")
                        print(f" {red}# {white}Status: {yellow}Pending{res}{end}")
                        print(f" {red}# {white}Amount: {green}{amount}{res} BTC{end}")
                        print(f" {red}# {white}Address BTC: {yellow}{self.wallet}{res}{end}")
                        self.msg_line()
                    elif 'balance is not enough' in r.text.lower():
                        self.carousel_msg("Not have min autowd amount")
                else:
                    self.carousel_msg("Not have min autowd amount")
                break

    def claim(self):
        while True:
            self.carousel_msg("Go to faucet section")
            roll_min, roll_max = 9986,9999
            live = 'OFF'
            headers = {'x-requested-with': 'XMLHttpRequest'}
            try:
                with open('config.json', 'r') as f:
                    obj = json.load(f)
                    auto_wd = obj.get('Auto Wd', {})
                    if auto_wd:
                        toggle_auto_wd = auto_wd.get('Toggle')
                        if toggle_auto_wd.lower() == 'on':
                            self.active_auto_wd = True
                            wd_amount = auto_wd.get("Amount")
                            if wd_amount and isinstance(wd_amount, list) and all(isinstance(value, int) for value in wd_amount):
                                self.wd_amount = choice(wd_amount)
                                if self.wd_amount < 10:
                                    self.wd_amount = None
                            else:
                                self.wd_amount = None
                            self.wallet = auto_wd.get("Faucetpay Btc")
                            if self.wallet:
                                if len(self.wallet) <= 10:
                                    self.wallet = None
                            else:
                                self.wallet = None
                        else:
                            self.active_auto_wd = False
                    live_roll = obj.get('Live Roll')
                    if live_roll:
                        toggle = live_roll.get('Toggle')
                        min_max = live_roll.get('Min/Max')
                        if toggle.lower() == 'on' and isinstance(min_max, list) and len(min_max) == 2:
                            live = 'ON'
                            roll_min = min(min_max)
                            roll_max = max(min_max)
            except Exception:
                if randint(1, 100) % 2 == 0:
                    roll_min = 9987
                    roll_max = 9999
            next_roll = randint(roll_min, roll_max)
            while True:
                emtoken = None
                url = f"https://{host}/em-assets/themes/default/earn/faucet/"
                payload = {'api_key': self.em_key}
                r = self.curl('POST', url, headers, payload)
                soup = BeautifulSoup(r.text, 'html.parser')
                try:
                    emtoken = soup.find('button', class_='btn')['id']
                except (TypeError, ValueError, AttributeError):
                    if str(self.username).lower() in r.text.lower():
                        self.carousel_msg("Faucet not available now")
                        self.carousel_msg("Checking faucet roll later")
                        self.wait(120)
                    else:
                        self.carousel_msg("Invalid cookies or em-key")
                        self.carousel_msg("Redirect to login...")
                        self.wait(5)
                        self.login()
                    break
                url = f"https://{host}/em-apc/u/Fc7R1l"
                payload = {
                    'emtoken': emtoken,
                    'roll_num': next_roll
                }
                headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
                self.carousel_msg("Claiming roll faucet")
                r = self.curl('POST', url, headers, payload)
                try:
                    r = json.loads(r.text)
                except Exception as e:
                    self.carousel_msg("Request error format")
                    self.carousel_msg(str(e))
                    sleep(5)
                    break
                if 'success' in r and r['success']:
                    v = self.data_account()
                    if 'Satoshi have been added to your account' in v[2]:
                        reward = v[2].split(' ')[0]
                    else:
                        reward = v[1] - self.previousbal
                    self.previousbal = v[1]
                    self.rolls_claimed += 1
                    balance = self.formating(v[1])
                    reward = self.formating(reward)
                    self.msg_action("FAUCET")
                    print(f" {red}# {white}Roll: {green}{next_roll}{res}{end}")
                    print(f" {red}# {white}Live: {red}{live}{res}{end}")
                    print(f" {red}# {white}Range: {white}{roll_min}-{roll_max}{res}{end}")
                    print(f" {red}# {white}Reward: {green}{reward}{res} BTC{end}")
                    print(f" {red}# {white}Balance: {green}{balance}{res} BTC{end}")
                    self.msg_line()
                    if self.active_auto_wd:
                        amount = self.wd_amount if self.wd_amount else v[1]
                        self.auto_wd(amount)
                    last_time_claim = time.time()
                    while True:
                        self.wait(5 * 60)
                        current_time = time.time()
                        if current_time >= last_time_claim + 60 * 60:
                            break
                        self.data_account(False)
                else:
                    self.carousel_msg("Claim failed")
                    self.wait(60)
                break
                
    def write_file(self, data):
        with open('config.json', 'w') as f:
            json.dump(data, f, indent=4)

    def formating(self, num):
        value = float(num) / 10**8
        return "{:.8f}".format(value)

    def data_account(self, show=True):
        username, balance = None, None
        while True:
            if show:
                self.carousel_msg("Getting user info")
            url = f"https://{host}/dash/"
            headers = {}
            r = self.curl('GET', url, headers)
            match = re.search(r"var apiKey = '([^']*)'", r.text)
            if match and match.group(1):
                self.em_key = match.group(1)
                if not show:
                    self.carousel_msg("Success updated cookies")
                    self.carousel_msg("Success updated em-key")
                    
            url = f"https://{host}/em-assets/themes/default/dash/"
            payload = {'api_key': self.em_key}
            headers = {'x-requested-with': 'XMLHttpRequest'}
            r = self.curl('POST', url, headers, payload)
            soup = BeautifulSoup(r.text, 'html.parser')
            success = soup.find('div', class_='msg success')
            if success:
                success = success.text.strip()
            try:
                username = soup.find('a', {'href': 'https://workpaid.net/user/settings/'}).get('title')
                balance = soup.find('div', class_='balance')
                balance = balance.find('div', class_='num').find('span').text.strip()
                balance = balance.replace(',', '').replace('.', '')
                break
            except (TypeError, ValueError, AttributeError):
                self.carousel_msg("Invalid cookies or em-key")
                self.carousel_msg("Redirect to login...")
                self.wait(5)
                self.login()
        return username, int(balance), success

    def start(self):
        v = self.data_account()
        username = v[0]
        self.previousbal = v[1]
        balance = self.formating(v[1])
        print(f"\n{bg_red}{white} ๏ {res} {yellow}〔 USERNAME 〕.: {res}{username}{end}")
        print(f"{bg_red}{white} ๏ {res} {yellow}〔 BALANCE 〕..: {res}{balance} BTC{end}")
        print(f"{res}{end}")
        self.msg_line()
        self.auto_wd(v[1])
    
    def login(self):
        while True:
            s.close()
            self.carousel_msg("Login processing...")
            while True:
                url = f"https://{host}/login/"
                headers = {}
                r = self.curl('GET', url, headers)
                match = re.search(r"var apiKey = '([^']*)'", r.text)
                if match and match.group(1):
                    api_key = match.group(1)
                    self.carousel_msg("Success found Api-Key")
                    self.em_key = api_key
                    url = f"https://{host}/em-assets/themes/default/auth/login/"
                    payload = {'api_key': api_key}
                    headers['x-requested-with'] = 'XMLHttpRequest'
                    r = self.curl('POST', url, headers, payload)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    id_em = soup.find('div', {'class': 'data'})
                    if id_em:
                        self.carousel_msg("Success found Em-Key")
                        param = id_em.get('id').split('/')[0]
                        emtoken = id_em.get('id').split('/')[1]
                        url = f"https://{host}/em-apc/u/{param}"
                        payload = f"emtoken={emtoken}&user_identity={self.username}&user_pass={self.password}&user_2fa=&user_remember=on"
                        headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
                        r = self.curl('POST', url, headers, payload)
                        try:
                            r = json.loads(r.text)
                        except Exception as e:
                            self.carousel_msg("Error")
                            self.carousel_msg(str(e))
                            sleep(5)
                            break
                        if 'success' in r and r['success']:
                            v = self.data_account()
                            self.carousel_msg(v[2])
                            return
                        else:
                            self.carousel_msg("Login failed")
                            self.wait(10)
                    else:
                        print("Em-Key not found")
                else:
                    self.carousel_msg("Api-Key not found")
                break
    
    def config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}
        except json.JSONDecodeError:
            print(f"{red}Check your config file")
            exit()

        keywords = ['Username', 'Password', 'User-Agent']

        for key in keywords:
            while key not in config or len(config[key]) < 5:
                config[key] = input(f"\n{yellow}{key}{red}:{res} ")

        if 'Auto Wd' not in config:
            config['Auto Wd'] = {'Toggle': 'Off', 'Amount': [], 'Faucetpay Btc': ''}

        auto_wd_choice = "y"
        while auto_wd_choice not in ["y", "n"]:
            print("Please enter a valid choice ('y' or 'n').")
            auto_wd_choice = input(f"\n{yellow}Do you want to activate 'auto withdraw'? (y/n):{res} ").lower()

        config['Auto Wd']['Toggle'] = "on" if auto_wd_choice == "y" else "off"

        if auto_wd_choice == "y":
            if 'Amount' not in config['Auto Wd']:
                config['Auto Wd']['Amount'] = []
            while 'Faucetpay Btc' not in config['Auto Wd'] or len(config['Auto Wd']['Faucetpay Btc']) < 10:
                config['Auto Wd']['Faucetpay Btc'] = input(f"\n{yellow}Faucetpay Btc{red}:{res} ")
            
            self.active_auto_wd = True
        
        if 'Live Roll' not in config:
            config['Live Roll'] = {'Toggle': 'off', 'Min/Max': [9997,9999]}

        os.system("clear" if os.name == "posix" else "cls")

        self.write_file(config)
        self.username = config['Username']
        self.password = config['Password']
        self.user_agent = config['User-Agent']
        self.wallet = config['Auto Wd']['Faucetpay Btc']

bot = Bot()
bot.config()

clean_screen()
bot.msg_line()
print(f"{green}{sc_ver.center(50, ' ')}")
bot.msg_line()

bot.login()
bot.start()
bot.claim()
