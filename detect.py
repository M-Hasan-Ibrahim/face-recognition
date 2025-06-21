# detect.py

import cv2
import face_recognition
import pickle
import os
import numpy as np
from jsonschema.exceptions import best_match

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

    tolerance = 0.5

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        best_match_name = "Unknown"
        best_match_distance = float("inf")
        for i, person_encodings in enumerate(known_face_encodings):
            if len(person_encodings) == 0:
                continue
            if isinstance(person_encodings, np.ndarray) and person_encodings.ndim == 1:
                person_encodings = [person_encodings]  # wrap in a list

            distances = face_recognition.face_distance(person_encodings, face_encoding)
            min_distance = min(distances)

            if min_distance < best_match_distance and min_distance <= tolerance:
                best_match_distance = min_distance
                best_match_name = known_face_names[i]
        names_found.append((top, right, bottom, left, best_match_name))
    return names_found
