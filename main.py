import requests
from datetime import datetime
import time
import smtplib

MY_EMAIl ="" #Enter Your Email
MY_PASSWORD = "" #Enter Your Password
MY_LAT =  # Your latitude
MY_LONG =  # Your longitude

def iss_overhead():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

def sunrise_api():

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()
    hour_now = time_now.hour

    if hour_now >= sunset or hour_now<= sunrise:
        return True

while True:
    time.sleep(60)
    if iss_overhead() and sunrise_api():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIl,MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIl,
            to_addrs=MY_EMAIl,
            msg = "Subject: Look up\n\nLook above in the sky, you will see the International Space Station."
        )

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.