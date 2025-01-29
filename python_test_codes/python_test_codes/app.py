from flask import Flask, render_template, Response, jsonify
import cv2
from keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet import preprocess_input
from collections import Counter

app = Flask(__name__)

model = load_model("best_model.keras")
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
emotion_labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}
emotion_history = []
video_writer = None


def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
    for (x, y, w, h) in faces:
        face_img = frame[y:y + h, x:x + w]
        face_img = cv2.resize(face_img, (224, 224))
        face_img = img_to_array(face_img)
        face_img = np.expand_dims(face_img, axis=0)
        face_img = preprocess_input(face_img)

        emotion_index = np.argmax(model.predict(face_img))
        emotion = emotion_labels[emotion_index]
        emotion_history.append(emotion)

        color = {
            'happy': (0, 200, 0),
            'neutral': (0, 200, 200),
            'sad': (255, 0, 0),
            'angry': (0, 0, 255),
            'surprise': (200, 0, 200)
        }.get(emotion, (100, 200, 200))

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 3)

    return frame


def generate_frames():
    global video_writer
    video = cv2.VideoCapture(0)

    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            frame = detect_emotion(frame)

            if video_writer is not None:
                video_writer.write(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    video.release()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_emotion_data')
def get_emotion_data():
    emotion_counts = Counter(emotion_history)
    return jsonify(dict(emotion_counts))


@app.route('/start_recording')
def start_recording():
    global video_writer
    if video_writer is None:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    return "Recording started"


@app.route('/stop_recording')
def stop_recording():
    global video_writer
    if video_writer is not None:
        video_writer.release()
        video_writer = None
    return "Recording stopped"


if __name__ == "__main__":
    app.run(debug=True)
