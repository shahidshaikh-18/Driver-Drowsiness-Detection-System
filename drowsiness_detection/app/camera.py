import cv2
from app.utils.detection import detect_drowsiness 

def gen_frames():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError("Could not start camera.")

    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            frame = detect_drowsiness(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        camera.release()
