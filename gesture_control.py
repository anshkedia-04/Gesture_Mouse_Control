import streamlit as st
import cv2
# import mediapipe as mp
import pyautogui
import time
import threading
from collections import deque
from cvzone.HandTrackingModule import HandDetector


running = False  # Flag to control loop
thread = None    # To store thread reference
stframe = None   # Streamlit placeholder for video frames

# Gesture loop now updates Streamlit image instead of cv2 window
def gesture_loop():
    global running, stframe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    screen_width, screen_height = pyautogui.size()
    cam = cv2.VideoCapture(0)

    buffer_length = 5
    x_buffer = deque(maxlen=buffer_length)
    y_buffer = deque(maxlen=buffer_length)

    last_click_time = 0
    click_delay = 0.5

    stframe = st.empty()  # placeholder for video

    while running:
        success, img = cam.read()
        if not success:
            continue

        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand_landmark in result.multi_hand_landmarks:
                lm_list = []
                for lm in hand_landmark.landmark:
                    lm_x, lm_y = int(lm.x * w), int(lm.y * h)
                    lm_list.append((lm_x, lm_y))

                mp_draw.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)

                if len(lm_list) >= 9:
                    index_finger = lm_list[8]
                    thumb = lm_list[4]

                    raw_x = int(index_finger[0] * screen_width / w)
                    raw_y = int(index_finger[1] * screen_height / h)

                    x_buffer.append(raw_x)
                    y_buffer.append(raw_y)

                    avg_x = int(sum(x_buffer) / len(x_buffer))
                    avg_y = int(sum(y_buffer) / len(y_buffer))

                    pyautogui.moveTo(avg_x, avg_y, duration=0.01)

                    distance = ((index_finger[0] - thumb[0]) ** 2 + (index_finger[1] - thumb[1]) ** 2) ** 0.5
                    current_time = time.time()
                    if distance < 40 and (current_time - last_click_time > click_delay):
                        pyautogui.click()
                        last_click_time = current_time
                        cv2.circle(img, index_finger, 10, (0, 255, 0), cv2.FILLED)

        # Convert BGR to RGB for Streamlit
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        stframe.image(img_rgb, channels="RGB")

    cam.release()

# Start and stop functions
def start_control():
    global running, thread
    if not running:
        running = True
        thread = threading.Thread(target=gesture_loop)
        thread.start()

def stop_control():
    global running, thread
    running = False
    if thread and thread.is_alive():
        thread.join()
