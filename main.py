import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 32.556599  # Your latitude
MY_LONG = 76.124702  # Your longitude
MY_EMAIL = "suwetayuvraj777@gmail.com"
MY_PASSWORD = "ywsi mrnr inwi cggo"
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


# Your position is within +5 or -5 degrees of the ISS position.
def is_isis_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def send_email():
    """Send email and said to look up"""
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="suwetayuvraj9411417@gmail.com",
                            msg="Subject: Hey Look Up \n\n The ISS is in the sky")


def is_night():
    """This function check is the night or not and return true if is night"""
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now <= sunrise or time_now >= sunset:
        return True


# This loop will run code in every 60 seconds
while True:
    time.sleep(60)
    if is_isis_overhead() and is_night():
        send_email()
