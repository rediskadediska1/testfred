from threading import Thread
import pyfiglet
from colorama import Fore

communityLink = "http://aminoapps.com/p/lfr1vx"

from binascii import hexlify
from uuid import UUID
import hmac
from _sha1 import sha1
from base64 import b64encode
import aminofix
import os
import time
import json
import random
import requests
from flask import Flask, logging
from json_minify import json_minify

flask_app = Flask('')

colors = {
    '[red]': Fore.RED,
    '[cyan]': Fore.CYAN,
    '[magenta]': Fore.MAGENTA,
    '[green]': Fore.GREEN,
    '[blue]': Fore.BLUE,
    '[black]': Fore.BLACK,
    '[reset]': Fore.RESET,
    '[yellow]': Fore.YELLOW
}


def colorify(data):
    for elem in colors.keys():
        if elem in data:
            data = data.replace(elem, colors[elem])
    return data


@flask_app.route('/')
def home(): return " ~~8:> \n\t\t~~8:>"


def run(): flask_app.run(host='0.0.0.0', port=random.randint(2000, 9000))


Thread(target=run).start()


def timers():
    return [{'start': int(time.time()), 'end': int(time.time()) + 300} for _ in range(50)]


def tzFilter():
    localhour = time.strftime("%H", time.gmtime())
    localminute = time.strftime("%M", time.gmtime())
    UTC = {"GMT0": '+0', "GMT1": '+60', "GMT2": '+120', "GMT3": '+180', "GMT4": '+240', "GMT5": '+300', "GMT6": '+360',
           "GMT7": '+420', "GMT8": '+480', "GMT9": '+540', "GMT10": '+600', "GMT11": '+660', "GMT12": '+720',
           "GMT13": '+780', "GMT-1": '-60', "GMT-2": '-120', "GMT-3": '-180', "GMT-4": '-240', "GMT-5": '-300',
           "GMT-6": '-360', "GMT-7": '-420', "GMT-8": '-480', "GMT-9": '-540', "GMT-10": '-600', "GMT-11": '-660'};
    hour = [localhour, localminute]
    if hour[0] == "00": tz = UTC["GMT-1"];return int(tz)
    if hour[0] == "01": tz = UTC["GMT-2"];return int(tz)
    if hour[0] == "02": tz = UTC["GMT-3"];return int(tz)
    if hour[0] == "03": tz = UTC["GMT-4"];return int(tz)
    if hour[0] == "04": tz = UTC["GMT-5"];return int(tz)
    if hour[0] == "05": tz = UTC["GMT-6"];return int(tz)
    if hour[0] == "06": tz = UTC["GMT-7"];return int(tz)
    if hour[0] == "07": tz = UTC["GMT-8"];return int(tz)
    if hour[0] == "08": tz = UTC["GMT-9"];return int(tz)
    if hour[0] == "09": tz = UTC["GMT-10"];return int(tz)
    if hour[0] == "10": tz = UTC["GMT13"];return int(tz)
    if hour[0] == "11": tz = UTC["GMT12"];return int(tz)
    if hour[0] == "12": tz = UTC["GMT11"];return int(tz)
    if hour[0] == "13": tz = UTC["GMT10"];return int(tz)
    if hour[0] == "14": tz = UTC["GMT9"];return int(tz)
    if hour[0] == "15": tz = UTC["GMT8"];return int(tz)
    if hour[0] == "16": tz = UTC["GMT7"];return int(tz)
    if hour[0] == "17": tz = UTC["GMT6"];return int(tz)
    if hour[0] == "18": tz = UTC["GMT5"];return int(tz)
    if hour[0] == "19": tz = UTC["GMT4"];return int(tz)
    if hour[0] == "20": tz = UTC["GMT3"];return int(tz)
    if hour[0] == "21": tz = UTC["GMT2"];return int(tz)
    if hour[0] == "22": tz = UTC["GMT1"];return int(tz)
    if hour[0] == "23": tz = UTC["GMT0"];return int(tz)


class Farm:
    def __init__(self, session, device):
        self.session = session
        self.api = "http://service.narvii.com/api/v1"
        self.comId = aminofix.Client().get_from_code(communityLink).comId
        self.objectId = aminofix.Client().get_from_code(communityLink).objectId
        self.device_Id = device
        self.coin = None
        self.headers = {"NDCDEVICEID": self.device_Id, "SMDEVICEID": "b89d9a00-f78e-46a3-bd54-6507d68b343c",
                        "Accept-Language": "ru-RU", "Content-Type": "application/json; charset=utf-8",
                        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.4.33562)",
                        "Host": "service.narvii.com", "Accept-Encoding": "gzip", "Connection": "Keep-Alive"}
        self.sid, self.auid = None, None

    def generate_device(self):
        identifier = os.urandom(20)
        return ("42" + identifier.hex() + hmac.new(bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F"),
                                                   b"\x42" + identifier, sha1).hexdigest()).upper()

    def generate_signature(self, data):
        data = data if isinstance(data, bytes) else data.encode("utf-8")
        return b64encode(bytes.fromhex("42") + hmac.new(bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93"), data,
                                                        sha1).digest()).decode("utf-8")

    def generate_headers(self, data=None, content_type=None, sig=None):
        headers = {
            'NDCDEVICEID': self.device_Id,
            'Accept-Language': 'en-US',
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 9 Pro Build/QQ3A.200805.001; com.narvii.amino.master/3.4.33585)',
            'Host': 'service.narvii.com',
            'Accept-Encoding': 'gzip',
            'Connection': 'Keep-Alive'
        }
        if data:
            headers['Content-Length'] = str(len(data))
            if sig:
                headers['NDC-MSG-SIG'] = sig
        if self.sid:
            headers['NDCAUTH'] = f'sid={self.sid}'
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def login(self, email: str, password: str, device_Id: str):
        data = json.dumps({"email": email, "secret": f"0 {password}", "deviceID": device_Id, "clientType": 100,
                           "action": "normal", "timestamp": (int(time.time() * 1000))})
        self.headers["ndc-msg-sig"] = self.generate_signature(data=data)
        request = self.session.post(f"{self.api}/g/s/auth/login", data=data, headers=self.headers)
        try:
            self.sid, self.auid = request.json()["sid"], request.json()["auid"]
        except:
            pass
        return request.json()

    def join_community(self, comId, inviteId: str = None):
        data = {"timestamp": int(time.time() * 1000)}
        if inviteId: data["invitationId"] = inviteId
        data = json.dumps(data)
        self.headers["ndc-msg-sig"] = self.generate_signature(data=data)
        request = self.session.post(f"{self.api}/x{comId}/s/community/join?sid={self.sid}", data=data,
                                    headers=self.headers)
        return request.json()

    def send_active_object(self, comId, start_time: int = None, end_time: int = None, timers: list = None,
                           tz: int = -time.timezone // 1000):
        data = {"userActiveTimeChunkList": [{"start": start_time, "end": end_time}],
                "timestamp": int(time.time() * 1000), "optInAdsFlags": 2147483647, "timezone": tz}
        if timers: data["userActiveTimeChunkList"] = timers
        data = json_minify(json.dumps(data))
        self.headers["ndc-msg-sig"] = self.generate_signature(data=data)
        request = self.session.post(f"{self.api}/x{comId}/s/community/stats/user-active-time?sid={self.sid}", data=data,
                                    headers=self.headers)
        return request.json()

    def send_my_coins(self):
        with self.session.get(f'{self.api}/g/s/wallet', headers=self.generate_headers()) as response:
            response = response.json()
            if response["api:statuscode"] == 0:
                pass
            else:
                raise Exception(response['api:message'])
            coins = int(response['wallet']['totalCoins'])
            if not coins:
                return coins
            data = json.dumps(
                {'coins': coins % 500,
                 'tippingContext': {"transactionId": str(UUID(hexlify(os.urandom(16)).decode('ascii')))},
                 'timestamp': int(time.time() * 1000)})
            with self.session.post(f'{self.api}/x{self.comId}/s/blog/{self.objectId}/tipping',
                                   headers=self.generate_headers(data=data, sig=self.generate_signature(data)),
                                   data=data) as response:
                response = response.json()
                if response["api:statuscode"] == 0:
                    pass
                else:
                    raise Exception(response['api:message'])
            for _ in range(coins // 500):
                data = json.dumps(
                    {'coins': 500,
                     'tippingContext': {"transactionId": str(UUID(hexlify(os.urandom(16)).decode('ascii')))},
                     'timestamp': int(time.time() * 1000)})
                with self.session.post(f'{self.api}/x{self.comId}/s/blog/{self.objectId}/tipping',
                                       headers=self.generate_headers(data=data, sig=self.generate_signature(data)),
                                       data=data) as response:
                    response = response.json()
                    if response["api:statuscode"] == 0:
                        pass
                    else:
                        raise Exception(response['api:message'])
            return coins

    def main(self, email, password, deviceId):
        print(colorify(
            f"[yellow]> [reset]ЛОГИН [yellow]{email.upper()}[reset] >>[yellow] {self.login(email=email, password=password, device_Id=deviceId)['api:message']}"))
        print(colorify(
            f"[yellow]> [reset]ВХОД В СОО [yellow]{email.upper()}[reset] >>[yellow] {self.join_community(comId=self.comId)['api:message']}"))
        for _ in range(24):
            sobj = self.send_active_object(comId=self.comId, timers=timers(), tz=tzFilter())['api:message']
            print(colorify(
                f"[yellow]> [reset]SOBJ [yellow]{email.upper()}[reset] >>[yellow] {sobj}"))
            if sobj != 'OK':
                break
            time.sleep(2.4)
        print((colorify(f"[yellow]> [reset]МОНЕТЫ [yellow]{email.upper()}[reset] >>[yellow] {self.send_my_coins()}")))


class App:
    def __init__(self, session, file):
        self.session = session
        self.invitationId = None
        self.file = file

    def run(self):
        accountlines = [elem.replace('\n', '') for elem in open(file=self.file).readlines()]
        print(colorify(f'[yellow]{pyfiglet.figlet_format("Arisen", font="slant").rstrip()}'))
        print(colorify(f'[reset]{pyfiglet.figlet_format("FarmBot", font="slant")}'))
        while True:
            for accountline in accountlines:
                account = accountline.split()
                Farm(session=self.session, device=account[2]).main(email=account[0], password=account[1],
                                                                   deviceId=account[2])


def main():
    session = requests.Session()
    App(session, "accounts.txt").run()


if __name__ == "__main__":
    main()
