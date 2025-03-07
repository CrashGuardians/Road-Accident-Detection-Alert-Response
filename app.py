from flask import Flask, render_template, Response, jsonify, send_from_directory
import cv2
import numpy as np
import time
import os
from detection import AccidentDetectionModel
from twilio.rest import Client
import geocoder
import threading
import winsound

app = Flask(__name__)

# Global variables
alarm_triggered = False
video_capture = cv2.VideoCapture("car1.mp4")
model = AccidentDetectionModel("model.json", "model_weights.keras")

def play_beep():
    winsound.Beep(2500, 2000)

def get_location():
    try:
        g = geocoder.ip('me')
        if g.latlng:
            lat, lng = g.latlng
            return f"https://www.google.com/maps?q={lat},{lng}"
        else:
            return "Location not available"
    except Exception as e:
        print("Error fetching location:", e)
        return "Location not available"

def send_sms():
    try:
        account_sid = "ACf48d2c173f53f55c724731b2d643674b"
        auth_token = "9dd61f1e3525f53ace8a4a95ddc5df93"
        client = Client(account_sid, auth_token)
        location = get_location()
        message = client.messages.create(
            body=f"Accident Detected! Location: {location}",
            from_="+15632783597",
            to="+918129927118"
        )
        print("SMS sent:", message.sid)
    except Exception as e:
        print("Error sending SMS:", e)

def call_ambulance():
    try:
        account_sid = "ACf48d2c173f53f55c724731b2d643674b"
        auth_token = "9dd61f1e3525f53ace8a4a95ddc5df93"
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            url="https://raw.githubusercontent.com/AakashVinod/twimlfiles/refs/heads/main/twiml_response.xml",
            to="+918129927118",
            from_="+15632783597"
        )
        print("Call made:", call.sid)
    except Exception as e:
        print("Error calling ambulance:", e)

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

def gen_frames():
    global alarm_triggered, video_capture
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        roi = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (250, 250))
        pred, prob = model.predict_accident(roi[np.newaxis, :, :])
        if pred == "Accident" and not alarm_triggered:
            prob_val = round(prob[0][0] * 100, 2)
            if prob_val > 99:
                # Save screenshot before setting alarm_triggered
                save_accident_photo(frame)
                alarm_triggered = True
                threading.Thread(target=play_beep, daemon=True).start()
                threading.Thread(target=send_sms, daemon=True).start()
                threading.Thread(target=call_ambulance, daemon=True).start()
                cv2.putText(frame, "Accident Detected!", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start-detection')
def start_detection():
    global alarm_triggered, video_capture
    alarm_triggered = False
    # Restart video capture from beginning
    video_capture.release()
    video_capture = cv2.VideoCapture("car1.mp4")
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    return jsonify({'message': 'Accident detection started!'})

@app.route('/stop-detection')
def stop_detection():
    global video_capture
    video_capture.release()
    return jsonify({'message': 'Accident detection stopped!'})

# Routes for screenshot gallery
@app.route('/accident_photos/<filename>')
def accident_photo(filename):
    return send_from_directory('accident_photos', filename)

@app.route('/screenshots')
def screenshots():
    folder = 'accident_photos'
    images = []
    if os.path.exists(folder):
        images = os.listdir(folder)
        images = [img for img in images if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return render_template('screenshots.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
