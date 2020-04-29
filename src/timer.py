import time
import datetime
import requests
import argparse

white_lists = ["10:00", "11:00", "12:00", "14:00", "15:00", "16:00",
               "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]


def next_point():
    now = time.localtime()
    for i, s in enumerate(white_lists):
        t = time.strptime(s, "%H:%M")
        if now.tm_hour < t.tm_hour:
            d = datetime.timedelta(
                hours=t.tm_hour-now.tm_hour, minutes=t.tm_min-now.tm_min)
            return d.seconds


def notify(key, content):
    print(requests.post(
        url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=%s" % key,
        json={
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
    ))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("KEY", type=str, help='key of web hook')
    parser.add_argument("--file", type=str,
                        help='content for post', default="assets/drink.md")

    args = parser.parse_args()

    while True:
        time.sleep(next_point())
        with open(args.param.file) as file:
            content = file.read()
        notify(args.param.KEY, content)
