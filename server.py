from operator import itemgetter
import requests
import json
from flask import Flask


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def ping_url():
    f = open('carriers.json')
    urls = json.load(f)

    msg = ""
    carrier = ""
    status = ""
    url = ""
    response = ""
    result_dict = {}
    result_list = []

    for rec in urls:

        carrier = rec["carrier"]
        status = ""
        url = rec['url']
        try:
            response = requests.get(rec["url"])
            response.raise_for_status()
            msg = "UP and running"

        except requests.exceptions.HTTPError as error:
            if response.status_code == 405:
                msg = "UP and running"
            else:
                msg = "Not Available"
        except requests.exceptions.RequestException as error:
            msg = "ERROR: " + {error}

        result_dict = {"status": str(response.status_code), "carrier": carrier, "url": url, "msg": msg}

        result_list.append(result_dict)

    result = sorted(result_list, key=itemgetter('status'), reverse=True)
    response = ""
    for rec in result:
        response += rec["status"] + " " + rec["carrier"] + " " + rec["url"] + " " + rec["msg"] + '</br>'

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

