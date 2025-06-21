# detect.py

import cv2
import face_recognition
import pickle
import os
import numpy as np

DATA_FILE = "faces.dat"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            known_face_encodings, known_face_names = pickle.load(f)
    else:
        known_face_encodings = []
        known_face_names = []
    return known_face_encodings, known_face_names

def recognizeFaces(frame):
    known_face_encodings, known_face_names = load_data()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    names_found = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        for i, person_encodings in enumerate(known_face_encodings):
            if len(person_encodings) == 0:
                continue
            if isinstance(person_encodings, np.ndarray) and person_encodings.ndim == 1:
                person_encodings = [person_encodings]  # wrap in a list
            matches = face_recognition.compare_faces(person_encodings, face_encoding, tolerance=0.5)
            if True in matches:
                name = known_face_names[i]
                break
        names_found.append((top, right, bottom, left, name))
    return names_found
