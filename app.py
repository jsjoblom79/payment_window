import webview, threading, json
from screeninfo import get_monitors
from flask import Flask, request
import webbrowser

from assets.data.data_api import DataAPI

app = Flask(__name__)
window = None

class Api:
    def __init__(self):
       self.data = DataAPI()

    def display_data(self, content):
        print(content)

api = Api()

@app.route("/data_import")
def data_import():
    data = request.args.to_dict()
    api.display_data(data)
    # window.evaluate_js(f"window.onTableauData({json.dumps(data)})")
    # window.show()
    cur_window = webview.windows[0]
    if cur_window:
        borrowerName = cur_window.dom.get_element('#pay-Name')
        address = cur_window.dom.get_element('#pay-address')
        city = cur_window.dom.get_element('#pay-city')
        state = cur_window.dom.get_element('#pay-state')
        zip = cur_window.dom.get_element('#pay-zip')
        ssn = cur_window.dom.get_element('#pay-SSN_ACCOUNT')
        system = cur_window.dom.get_element('#pay-system')
        email = cur_window.dom.get_element('#pay-email')

        borrowerName.value = data["Name"]
        address.value = data["Addr1"] + " " + data["Addr2"]
        city.value = data["City"]
        state.value = data["State"]
        zip.value = data["ZipCode"]
        ssn.value = data["SSN"]
        email.value = data["EmailAdress"]
        system.value = data["SourceSystem"]

    return "<h2>Data Received, Processing will continue on Payment Window app</h2><p>You may close this window</p>"

def run_server():
    app.run(port=5050)


def start_payment_window():
    monitors = get_monitors()
    totalWidth = 0
    totalHeight = 0
    # avgWidth = 0
    # avgHeight = 0

    for monitor in monitors:
        totalWidth += monitor.width
        totalHeight += monitor.height

    avgWidth = totalWidth / len(monitors)
    avgHeight = totalHeight / len(monitors)

    threading.Thread(target=run_server, daemon=True).start()


    window = webview.create_window(
        title="Payment Window",
        url="pindex.html",
        js_api=api,
        width=avgWidth / 2,
        height=avgHeight - 50/.25, )

    webview.start(debug=True)


if "__main__" == __name__:
    try:
        webbrowser.open("http://nmpr-tableau.nmeaf.org/#/signin?externalRedirect=/views/PaymentWindowAccountLookup/Dashboard1?:showAppBanner%3Dfalse%26:display_couhttp://nmpr-tableau.nmeaf.org/views/PaymentWindowAccountLookup/Dashboard1?:embed%3Dyes%26:toolbar%3Dno&site=")
        start_payment_window()
    except webview.errors.JavascriptException as e:
        print("There was an error.")