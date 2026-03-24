import cv2
import mediapipe as mp
import pyautogui
import time

print("🎮 Temple Run Finger Control Started...")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
gesture_cooldown = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            x = int(hand_landmarks.landmark[8].x * frame.shape[1])
            y = int(hand_landmarks.landmark[8].y * frame.shape[0])

            cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = x, y

            dx = x - prev_x
            dy = y - prev_y

            if time.time() - gesture_cooldown > 1:

                if abs(dx) > 100:
                    if dx > 0:
                        print("➡ RIGHT")
                        pyautogui.press("right")
                    else:
                        print("⬅ LEFT")
                        pyautogui.press("left")
                    gesture_cooldown = time.time()

                elif abs(dy) > 100:
                    if dy < 0:
                        print("⬆ JUMP")
                        pyautogui.press("up")
                    else:
                        print("⬇ SLIDE")
                        pyautogui.press("down")
                    gesture_cooldown = time.time()

            prev_x, prev_y = x, y

    else:
        prev_x, prev_y = 0, 0

    cv2.imshow("Temple Run Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()