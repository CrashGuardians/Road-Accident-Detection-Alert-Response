import cv2
from detection import AccidentDetectionModel
import numpy as np
import os
import winsound
import threading
import time
import tkinter as tk
from twilio.rest import Client
from PIL import Image, ImageTk
import geocoder  # Import geocoder for location services
import requests  # Import requests for API calls

emergency_timer = None
alarm_triggered = False
model = AccidentDetectionModel("model.json", "model_weights.keras")
font = cv2.FONT_HERSHEY_SIMPLEX

def get_location():
    try:
        g = geocoder.ip('me')
        if g.latlng:
            latitude, longitude = g.latlng
            map_link = f"https://www.google.com/maps?q={latitude},{longitude}"
            return map_link
        else:
            return "Location not available"
    except Exception as e:
        print(f"Error fetching location: {e}")
        return "Location not available"


def send_sms():
    try:
        account_sid = "enter "
        auth_token = "enter "
        client = Client(account_sid, auth_token)
        location = get_location()
        message = client.messages.create(
            body=f"Accident Detected! Emergency Assistance Needed. Location: {location}",
            from_="enter",
            to="enter"
        )
        print(f"SMS sent: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")


def save_accident_photo(frame):
    try:
        current_date_time = time.strftime("%Y-%m-%d-%H%M%S")
        directory = "accident_photos"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = f"{directory}/{current_date_time}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Accident photo saved as {filename}")
    except Exception as e:
        print(f"Error saving accident photo: {e}")


def call_ambulance():
    try:
        account_sid = "enter"
        auth_token = "enter"
        client = Client(account_sid, auth_token)

        call = client.calls.create(
            url="enter",
            to="+enter",
            from_="(563) 278-3597"
        )
        print(call.sid)
    except Exception as e:
        print(f"Error calling ambulance: {e}")


def open_accident_folder():
    try:
        folder_path = "accident_photos"
        os.startfile(folder_path)
    except Exception as e:
        print(f"Error opening folder: {e}")


def show_alert_message():
    def on_call_ambulance():
        call_ambulance()
        send_sms()
        alert_window.destroy()

    frequency = 2500
    duration = 2000
    winsound.Beep(frequency, duration)

    alert_window = tk.Tk()
    alert_window.title("Alert")
    alert_window.geometry("500x300")
    alert_label = tk.Label(alert_window, text="Alert: Accident Detected!\n\nIs the Accident Critical?", fg="black", font=("Helvetica", 16))
    alert_label.pack()

    gif_path = "Wow-gif.gif"
    gif = Image.open(gif_path)
    resized_gif = gif.resize((150, 100), Image.BICUBIC)

    try:
        global gif_image
        gif_image = ImageTk.PhotoImage(resized_gif)
        gif_label = tk.Label(alert_window, image=gif_image)
        gif_label.pack()
    except Exception as e:
        print(f"Error loading GIF: {e}")

    call_ambulance_button = tk.Button(alert_window, text="Call Ambulance", command=on_call_ambulance)
    call_ambulance_button.pack()

    open_folder_button = tk.Button(alert_window, text="Open Accident Photos Folder", command=open_accident_folder)
    open_folder_button.pack()

    cancel_button = tk.Button(alert_window, text="Cancel", command=alert_window.destroy)
    cancel_button.pack()

    alert_window.mainloop()


def start_alert_thread():
    alert_thread = threading.Thread(target=show_alert_message)
    alert_thread.daemon = True
    alert_thread.start()


def startapplication():
    global alarm_triggered
    video = cv2.VideoCapture("car1.mp4")
    while True:
        ret, frame = video.read()
        if not ret:
            print("No more frames to read")
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(gray_frame, (250, 250))

        pred, prob = model.predict_accident(roi[np.newaxis, :, :])
        if pred == "Accident" and not alarm_triggered:
            prob = round(prob[0][0] * 100, 2)

            if prob > 99:
                save_accident_photo(frame)
                alarm_triggered = True
                start_alert_thread()

            cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
            cv2.putText(frame, pred + " " + str(prob), (20, 30), font, 1, (255, 255, 0), 2)

        if cv2.waitKey(33) & 0xFF == ord('q'):
            return
        cv2.imshow('Video', frame)


if __name__ == '__main__':
    startapplication()
