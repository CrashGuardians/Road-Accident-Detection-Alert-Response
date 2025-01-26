import cv2
from detection import AccidentDetectionModel
import numpy as np
import os
import winsound
import threading
import time
import tkinter as tk
from twilio.rest import Client
from PIL import Image, ImageTk  # Import PIL modules for image handling

emergency_timer = None
alarm_triggered = False  # Flag to track if an alarm has been triggered

model = AccidentDetectionModel("model.json", "model_weights.keras")
font = cv2.FONT_HERSHEY_SIMPLEX

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
        account_sid = "ACf48d2c173f53f55c724731b2d643674b"
        auth_token = "70a460a17636460c1fe5d6f5c04e43b2"
        client = Client(account_sid, auth_token)

        call = client.calls.create(
            url="https://aakashvinod.github.io/twimlfiles/twiml_response.xml",  # Sample TwiML URL
            to="+918129927118",  # add verified ambulance number
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
        alert_window.destroy()

    # Play the beep sound
    frequency = 2500
    duration = 2000
    winsound.Beep(frequency, duration)

    alert_window = tk.Tk()
    alert_window.title("Alert")
    alert_window.geometry("500x300")  # Adjust window size to fit the GIF and message box
    alert_label = tk.Label(alert_window, text="Alert: Accident Detected!\n\nIs the Accident Critical?", fg="black", font=("Helvetica", 16))
    alert_label.pack()

    # Load and display the GIF
    gif_path = "Wow-gif.gif"  # Replace with the actual path to your GIF
    gif = Image.open(gif_path)
    resized_gif = gif.resize((150, 100), Image.BICUBIC)  # Use Image.BICUBIC for resizing

    try:
        global gif_image  # Create a global variable to hold the reference to the image object
        gif_image = ImageTk.PhotoImage(resized_gif)
        gif_label = tk.Label(alert_window, image=gif_image)
        gif_label.pack()
    except Exception as e:
        print(f"Error loading GIF: {e}")

    call_ambulance_button = tk.Button(alert_window, text="Call Ambulance", command=on_call_ambulance)
    call_ambulance_button.pack()

    # Add a button to open the folder
    open_folder_button = tk.Button(alert_window, text="Open Accident Photos Folder", command=open_accident_folder)
    open_folder_button.pack()

    cancel_button = tk.Button(alert_window, text="Cancel", command=alert_window.destroy)
    cancel_button.pack()

    alert_window.mainloop()

def start_alert_thread():
    alert_thread = threading.Thread(target=show_alert_message)
    alert_thread.daemon = True  # Set the thread as daemon so it doesn't block the main thread
    alert_thread.start()

def startapplication(): #FOR UPLOADED VIDEO OR DOWNLOADED VIDEO
    global alarm_triggered  # Use global variable for tracking alarm status
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
                alarm_triggered = True  # Set the alarm_triggered flag to True
                start_alert_thread()  # Start the alert message thread

            cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
            cv2.putText(frame, pred + " " + str(prob), (20, 30), font, 1, (255, 255, 0), 2)

        if cv2.waitKey(33) & 0xFF == ord('q'):
            return
        cv2.imshow('Video', frame)


# def startapplication():  #FOR LIVE FEED / CCTV
#     global alarm_triggered  # Use global variable for tracking alarm status
#
#     # Change the video source to the camera feed
#     video = cv2.VideoCapture(0)  # Use 0 for the default camera (or another number for other cameras)
#
#     while True:
#         ret, frame = video.read()
#         if not ret:
#             print("Failed to grab frame from the camera")
#             break
#
#         # Process the frame (convert to RGB, resize, and use model for prediction)
#         gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         roi = cv2.resize(gray_frame, (250, 250))
#
#         pred, prob = model.predict_accident(roi[np.newaxis, :, :])
#
#         if pred == "Accident" and not alarm_triggered:
#             prob = round(prob[0][0] * 100, 2)
#
#             if prob > 99:
#                 save_accident_photo(frame)
#                 alarm_triggered = True  # Set the alarm_triggered flag to True
#                 start_alert_thread()  # Start the alert message thread
#
#             cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
#             cv2.putText(frame, pred + " " + str(prob), (20, 30), font, 1, (255, 255, 0), 2)
#
#         if cv2.waitKey(33) & 0xFF == ord('q'):
#             return
#
#         # Show the frame in a window
#         cv2.imshow('Live Feed', frame)


if __name__ == '__main__':
    startapplication()
