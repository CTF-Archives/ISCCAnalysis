import requests
from bs4 import BeautifulSoup
import json
from retrying import retry


def get_usercount():
    html = requests.get(url="https://iscc.isclab.org.cn/scoreboard").text
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    return soup.div.table.th.string.split("：")[1]


@retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=2000)
def get_userinfo(id):
    html = requests.get(url="https://iscc.isclab.org.cn/team/" + str(id)).text
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    username = soup.div.h1.string
    score = soup.div.h3.string.split(":")[1].split(",")[0]
    if score == "":
        score = 0
    rank = soup.div.h3.string.split("在")[1].split("位")[0]
    if rank == "":
        rank = 0
    print(str(id).ljust(8, " ") + str(username).ljust(25, " "), str(score).ljust(8, " "), str(rank))
    data[id] = {"name": username, "score": score, "friends": {}}


if __name__ == "__main__":
    # data_cuttent = {}
    with open("./user.json", "r", encoding="utf8") as f:
        data_cuttent = json.load(f)
    last_userid = list(data_cuttent.keys())[-1]

    data = data_cuttent
    print("当前用户id区间:", int(last_userid), int(get_usercount()))
    for i in range(int(last_userid), int(get_usercount())):
        get_userinfo(i)

    print(data)
    print(json.dumps(data, ensure_ascii=False))
    with open("./user.json", "w+", encoding="utf-8") as f:
        f.truncate(0)
        f.write(json.dumps(data, ensure_ascii=False))
