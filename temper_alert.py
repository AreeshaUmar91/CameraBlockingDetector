import cv2
import numpy as np
import winsound
import requests #getting location
from twilio.rest import Client

# === Config ===
BRIGHTNESS_THRESHOLD = 30
ALERT_SOUND = "alert.wav"
TO_PHONE = "Your number"  
FROM_PHONE = "Twilio number"  

# === Location Fetch ===
def get_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
       
        return 'PGC Okara'
    except Exception as e:
        return f"Location not found. Error: {e}"

# === Send SMS via Twilio ===
def send_sms(message, to_number=TO_PHONE):
    account_sid = "Your SID : Twilio account"         
    auth_token = "Your auth token"   

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message,
            from_=FROM_PHONE,
            to=to_number
        )
        print("📩 SMS sent. SID:", message.sid)
    except Exception as e:
        print("⚠️ Error sending SMS:", e)

# === Tamper Detection ===
def is_tampered(gray_frame):
    avg_brightness = np.mean(gray_frame)
    return avg_brightness < BRIGHTNESS_THRESHOLD

# === Webcam Setup ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Error: Could not access webcam.")
    exit()

print("✅ Monitoring webcam... Press 'q' to quit.")
alert_triggered = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Frame not captured.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if is_tampered(gray):
        if not alert_triggered:
            print("🚨 Tamper detected! Camera view is blocked.")
            try:
                winsound.PlaySound(ALERT_SOUND, winsound.SND_FILENAME)
            except Exception as e:
                print("⚠️ Sound error:", e)

            location = get_location()
            msg = f"🚨 Tamper Alert! Camera is blocked. Possible theft at {location}"
            send_sms(msg)
            alert_triggered = True
    else:
        alert_triggered = False

    cv2.imshow("Webcam Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
