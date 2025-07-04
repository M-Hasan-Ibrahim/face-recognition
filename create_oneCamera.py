# create.py

import cv2
import face_recognition
import pickle
import os
import time
import winsound


DATA_FILE = "faces.dat"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            known_face_encodings, known_face_names = pickle.load(f)
    else:
        known_face_encodings = []
        known_face_names = []
    return known_face_encodings, known_face_names

def save_data(encodings, names):
    with open(DATA_FILE, "wb") as f:
        pickle.dump((encodings, names), f)

def addNewUser(name, cap):
    print(f"[INFO] Adding new user: {name}")
    encodings = []
    images = []
    count = 0
    print("[INFO] Please slowly turn your head left and right. Press 'q' to abort.")
    while count < 10:
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_encodings(rgb_frame)
        if faces:
            encodings.append(faces[0])
            images.append(frame.copy())
            count += 1
            print(f"[INFO] Captured {count}/10")
            winsound.Beep(1000, 200)
            time.sleep(1)
        cv2.imshow("Add New User", frame)
        key = cv2.waitKey(100)
        if key & 0xFF == ord('q'):
            print("[WARN] User add aborted!")
            break
    cv2.destroyWindow("Add New User")
    if count >= 8:
        known_face_encodings, known_face_names = load_data()
        known_face_names.append(name)
        known_face_encodings.append(encodings)
        save_data(known_face_encodings, known_face_names)
        print("[INFO] User added and data saved!")
        if images:
            return images[0]
        return None
    else:
        print("[ERROR] Not enough images captured. User not added.")
        return None