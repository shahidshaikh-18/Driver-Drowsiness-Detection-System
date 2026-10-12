import cv2
import dlib
import os
from scipy.spatial import distance
import pygame
import threading

# EAR calculation function
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Constants
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 15

# Eye landmark indices
LEFT_EYE_IDX = list(range(42, 48))
RIGHT_EYE_IDX = list(range(36, 42))

# Load dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
model_path = os.path.join(os.path.dirname(__file__), "shape_predictor_68_face_landmarks.dat")
predictor = dlib.shape_predictor(model_path)

# Alarm sound setup
alarm_path = os.path.join(os.path.dirname(__file__), "music.WAV.wav")
pygame.mixer.init()
pygame.mixer.music.load(alarm_path)

frame_counter = 0
alarm_on = False

def play_alarm():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()

def stop_alarm():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

def detect_drowsiness(frame):
    global frame_counter, alarm_on

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        left_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in LEFT_EYE_IDX]
        right_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in RIGHT_EYE_IDX]

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        avg_ear = (left_ear + right_ear) / 2.0

        for (x, y) in left_eye + right_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        if avg_ear < EAR_THRESHOLD:
            frame_counter += 1
            if frame_counter >= CONSEC_FRAMES:
                cv2.putText(frame, "DROWSINESS ALERT!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            1.2, (0, 0, 255), 3)
                if not alarm_on:
                    alarm_on = True
                    threading.Thread(target=play_alarm, daemon=True).start()
        else:
            frame_counter = 0
            if alarm_on:
                alarm_on = False
                stop_alarm()

        cv2.putText(frame, f"EAR: {avg_ear:.2f}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)

    return frame
