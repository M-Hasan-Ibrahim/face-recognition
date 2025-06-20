import cv2
import face_recognition
import os
import pickle

if os.path.exists("faces.dat"):
    with open("faces.dat", "rb") as f:
        known_face_encodings, known_face_names = pickle.load(f)
else:
    known_face_encodings = []
    known_face_names = []

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            idx = matches.index(True)
            name = known_face_names[idx]
        else:
            # Ask for name only once per unknown face
            cv2.imshow("camera", frame)
            cv2.waitKey(1)
            print("New face detected! Please type name in the terminal and press Enter:")
            name = input("Enter name: ")
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)
            # Save updated faces
            with open("faces.dat", "wb") as f:
                pickle.dump((known_face_encodings, known_face_names), f)

        # Draw box and label
        cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
        cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    cv2.imshow("camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
