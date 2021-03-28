import os
import requests
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ.get('account_sid')
auth_token = os.environ.get('auth_token')
print(os.environ['USER'])
OWM_ENDPOINT = 'https://api.openweathermap.org/data/2.5/onecall'  # or any endpoint of choice
API_KEY = 'YOUR API KEY'
MY_LAT = 'YOUR CURRENT LATITUDE'
MY_LONG = 'YOUR CURRENT LONGITUDE'

FROM_ = 'TWILLO PHONE NUMBER'
TO = 'YOUR PHONE NUMBER'

parameters = {
    'lat': MY_LAT,
    'lon': MY_LONG,
    'exclude': 'current,minutely,daily',
    'appid': API_KEY
}

response = requests.get(OWM_ENDPOINT, params=parameters)
timezone = response.json()['timezone']
weather_ids = [w_id['weather'][0]['id'] for w_id in response.json()['hourly']][:12]
bring_umbrella = False
for code in weather_ids:
    if code < 700:
        bring_umbrella = True

if bring_umbrella:
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body="Hey, Its Going to rain Today. Bring an Umbrella ☔️.",
            from_=FROM_,
            to=TO
        )
    print(message.status)
    print("Bring Umbrella ")

print(timezone, weather_ids)
