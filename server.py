from operator import itemgetter
import requests
import json
from flask import Flask, request


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def ping_url():
    f = open('carriers.json')
    urls = json.load(f)

    response = ""
    result_dict = {}
    result_list = []

    for rec in urls:
        test_url(rec, response, result_list)

    result = sorted(result_list, key=itemgetter('msg'), reverse=False)
    response = ""
    # try:
    #     token = request.form["token"]
    #     if token != "K2AuO1ZvEt2GYcVfiz1ObDh7":
    #         return "Invalid Slack Token"
    # except ValueError as err:
    #     return "Missing Slack Token"

    try:
        if request.form["command"] == '/serp-uptime':
            for rec in result:
                response += rec["msg"] + " " + rec["status"] + " " + rec["carrier"] + " " + rec["url"] + '\r\n'
            response += "https://n3uutmqmdv.us-west-2.awsapprunner.com/"
            return response

    except KeyError as err:
        response = response

    table = format_html(result)
    response = table

    return response


def test_url(rec, response, result_list):
    carrier = rec["carrier"]
    status = ""
    url = rec['url']
    try:
        response = requests.get(rec["url"])
        response.raise_for_status()
        msg = "UP  "

    except requests.exceptions.HTTPError as error:
        if response.status_code == 405 or response.status_code == 401:
            msg = "UP  "
        else:
            msg = "DOWN"
    except requests.exceptions.RequestException as error:
        msg = "ERROR: " + {error}
    result_dict = {"status": str(response.status_code), "carrier": carrier, "url": url, "msg": msg}
    result_list.append(result_dict)


def format_html(result):
    table = "<table>\n"
    table += "<tr><th>Status</th><th>Code</th><th>Carrier</th><th>URL</th></tr>\n"
    for rec in result:
        msg = rec["msg"]
        status = rec["status"]
        carrier = rec["carrier"]
        url = rec["url"]
        table += f"<tr><td>{msg}</td><td>{status}</td><td>{carrier}</td><td>{url}</td></tr>\n"
    # table += f"<tr><td span=4><a href=https://n3uutmqmdv.us-west-2.awsapprunner.com/>Check Up Time</a></td></tr>\n"
    table += "</table>"
    return table


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

