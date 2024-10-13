import json
import requests
from datetime import datetime

endpoint = "https://api.takasumibot.com/v1"
gifturl = "https://gift.takasumibot.com/"

def load(req: requests.models.Response) -> dict:
    ## requests.getをdict型に変換する関数
    return json.loads(req.content)["data"]

def d_time(i: dict) -> datetime:
    ## i["time"]をdatetime型に変換する関数
    return datetime.strptime(i["time"], "%Y-%m-%d %H:%M:%S")

def all_int(data: dict, int_list: list) -> dict:
    ## dataのint_listがある項目をintに変換する関数
    for i in int_list:
        data[i] = int(data[i])
    return data

def strange(count: int) -> list:
    ## strのrangeを生成する関数
    return [str(i) for i in range(count)]

class user:
    def __init__(self, id: int):
        self.id = id
        req = requests.get(f"{endpoint}/discord/user.php?id={self.id}")
        data = load(req)
        if not json.loads(req.content)["success"]:
            raise ValueError("IDが見つからない")
        ac = data["accentColor"]
        data["accentColor"] = int(ac) if ac is not None else ac
        data = all_int(data, ["id", "discriminator"])
        self.user = data

    def money(self) -> dict[str, int | datetime]:
        """ユーザーの所持しているものを取得

        Returns
        -------
        dict[str, int | datetime]
            ユーザーの所持しているもの
        """
        req = requests.get(f"{endpoint}/money.php")
        for i in load(req):
            if int(i["id"]) == self.id:
                for j in  strange(9):
                    i.pop(j)
                i = all_int(i, ["id", "amount", "roll", "yellow", "red", "blue", "random", "stock"])
                i["time"] = d_time(i)
                return i
                

    def rank(self) -> int:
        """ユーザーの所持金の順位を取得

        Returns
        -------
        int
            ユーザーの所持金の順位
        """
        req = requests.get(f"{endpoint}/money.php")
        data = sorted(load(req), key=lambda x: int(x["amount"]))
        for i, _ in enumerate(data[::-1]):
            if int(_["id"]) == self.id:
                return i+1
        return 0
    
    def is_mute(self) -> dict | None:
        """ユーザーがミュートされているかどうかを取得

        Returns
        -------
        dict | None
            ミュート情報もしくはNone
        """
        req = requests.get(f"{endpoint}/mute_user.php")
        data = load(req)
        for i in data:
            if int(i["id"]) == self.id:
                for j in strange(3):
                    i.pop(j)
                i["id"] = int(i["id"])
                i["time"] = d_time(i)
                return i
        return None
    
    def history(self) -> list:
        """ユーザーのhistoryを取得

        Returns
        -------
        list
            ユーザーのhistory
        """
        req = requests.get(f"{endpoint}/history.php?id={self.id}")
        data = load(req)
        out = []
        for i in data:
            for j in strange(5):
                i.pop(j)
            i = all_int(i, ["amount", "user"])
            i["time"] = d_time(i)
            out += [i]
        return out

class guild:
    def __init__(self, id: int):
        self.id = id
    
    def fetch(self) -> dict | None:
        """ギルドの情報を取得

        Returns
        -------
        dict | None
            ギルドの情報

        Raises
        ------
        ValueError
            ギルドが無効な場合
        """
        req = requests.get(f"{endpoint}/discord/guild.php?id={self.id}")
        if not json.loads(req.content)["success"]:
            if json.loads(req.content)["message"] == "Unknown Guild":
                return None
            else:
                raise ValueError("IDが見つからない")
        data = load(req)
        data = all_int(data, ["id", "ownerId"])
        return data

class gift:
    def __init__(self, id: str):
        self.id = id
        if id.startswith(gifturl):
            self.id = id[len(gifturl):]
        if id.endswith("/"):
            self.id = id[:1]
        req = requests.get(f"{endpoint}/gift.php?id={self.id}")
        if not json.loads(req.content)["success"]:
            raise ValueError("なんか取得できない")
        data = load(req)
        for i in strange(4):
            data.pop(i)
        data = all_int(data, ["type"])
        data["time"] = d_time(data)
        try:
            data["user"] = user(int(data["user"]))
        except ValueError:
            data["user"] = int(data["userr"])
        self.data = data


def count() -> dict:
    req = requests.get(f"{endpoint}/count.php")
    data = load(req)[0]
    for i in strange(7):
        data.pop(i)
    data = all_int(data, ["id", "message", "command", "stock", "buy", "sell", "treasury"])
    return data

def trade() -> list:
    req = requests.get(f"{endpoint}/trade.php")
    data = load(req)
    out =  []
    for i in data:
        for j in strange(4):
            i.pop(j)
        i = all_int(i, ["price", "buy", "sell"])
        i["time"] = d_time(i)
        out += [i]
    return out

def trade_get(time: datetime) -> dict | None:
    data = trade()
    for i in range(len(data)):
        if i == len(data) - 1:
            continue
        if data[i]["time"] <= time <= data[i + 1]["time"]:
            return data[i+1]
    return None

def server() -> list:
    req = requests.get(f"{endpoint}/server.php")
    data = load(req)
    out = []
    for i in data:
        for j in strange(8):
            i.pop(j)
        i = all_int(i, ["id", "count", "owner"])
        i["time"] = d_time(i)
        out += [(i, guild(i["id"]))]
    return out

def status() -> list:
    req = requests.get(f"{endpoint}/status.php")
    data = load(req)
    out = []
    for i in data:
        for j in strange(8):
            i.pop(j)
        i = all_int(i, ["ping", "user", "guild", "message", "command", "ram"])
        i["time"] = d_time(i)
        i["cpu"] = float(i["cpu"])
        out += [i]
    return out
