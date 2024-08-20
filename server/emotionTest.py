import requests

url = "http://127.0.0.1:8000/api/detect-mood"
data = {
    "ticket_body": "We love Sentry and explored the user feedback feature, it has the advantage to bring the user info, trace, ... However, we are planning to implement Intercom for overall client integration. It would be fantastic if you provide a native integration with Intercom, so users initiating a recording on Intercom will have all relevant info directly on Sentry."
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)
print(response.json())
