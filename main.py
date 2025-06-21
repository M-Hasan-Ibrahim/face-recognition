# main.py

import cv2
from create_oneCamera import addNewUser
from detect import recognizeFaces
import threading

def enroll_user_thread(cap):
    name = input("Enter name for new user: ")
    addNewUser(name, cap)

def main():
    cap = cv2.VideoCapture(0)
    print("[INFO] Press 'a' to add a new user, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Get face locations and names
        faces = recognizeFaces(frame)

        # Draw boxes and labels
        for (top, right, bottom, left, name) in faces:
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

        cv2.imshow("Face Recognition", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        if key & 0xFF == ord('a'):
            t = threading.Thread(target=enroll_user_thread, args=(cap, ))
            t.start()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
