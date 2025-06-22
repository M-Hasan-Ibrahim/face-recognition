# main.py

import cv2
from create_oneCamera import addNewUser
from detect import recognizeFaces
import threading
from dotenv import load_dotenv
import os
from my_bot import MyBot
import time
from PIL import Image
import queue

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = MyBot(TELEGRAM_BOT_TOKEN, CHAT_ID)

sent_names = set()
name_last_sent = {}
RESEND_DELAY = 120
RESEND_DELAY_MODIFIED = RESEND_DELAY

send_queue = queue.Queue()

def telegram_sender_worker():
    while True:
        item = send_queue.get()
        if item is None:
            break
        message, pil_image = item
        try:
            bot.send_message([message])
            bot.send_pil_image(pil_image=pil_image)
        except Exception as e:
            print("[Telegram ERROR]", e)
        send_queue.task_done()


sender_thread = threading.Thread(target=telegram_sender_worker, daemon=True)
sender_thread.start()

def enroll_user_thread(cap):
    name = input("Enter name for new user: ")
    addNewUser(name, cap)
    message = "{name} has been enrolled.".format(name=name)
    send_queue.put((message, None))

def main():
    cap = cv2.VideoCapture(1)
    print("[INFO] Press 'a' to add a new user, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break

        faces = recognizeFaces(frame)

        for (top, right, bottom, left, name) in faces:
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame, name, (left-25, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            img_height, img_width = frame.shape[:2]
            crop_top = max(top - 30, 0)
            crop_bottom = min(bottom, img_height)
            crop_left = max(left - 25, 0)
            crop_right = min(right + 30, img_width)
            face_image = frame[crop_top:crop_bottom, crop_left:crop_right]

            if face_image.size == 0:
                continue

            face_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(face_rgb)

            if name == "Unknown":
                RESEND_DELAY_MODIFIED = 30
                message = "{name} face has been detected.".format(name=name)
            else:
                RESEND_DELAY_MODIFIED = RESEND_DELAY
                message = "{name} has been detected.".format(name=name)
            now = time.time()
            if (name not in sent_names) or (now - name_last_sent.get(name, 0) > RESEND_DELAY_MODIFIED):
                sent_names.add(name)
                name_last_sent[name] = now
                send_queue.put((message, pil_image))

        cv2.imshow("Face Recognition", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        if key & 0xFF == ord('a'):
            t = threading.Thread(target=enroll_user_thread, args=(cap, ))
            t.start()

    cap.release()
    cv2.destroyAllWindows()

    send_queue.put(None)
    sender_thread.join()

if __name__ == "__main__":
    main()
