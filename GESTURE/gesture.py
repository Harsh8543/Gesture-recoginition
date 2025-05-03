import cv2
import mediapipe as mp
import pyautogui  # For controlling Chrome actions
import time

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Video Capture
cap = cv2.VideoCapture(0)

def detect_gesture(landmarks):
    # Extract key landmarks
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    pinky_tip = landmarks[20]
    
    # Gesture: Play/Pause (Thumb + Index Together)
    if abs(thumb_tip.x - index_tip.x) < 0.05 and abs(thumb_tip.y - index_tip.y) < 0.05:
        return "play_pause"

    # Gesture: Volume Up (Index and Middle Finger Straight Up)
    if index_tip.y < landmarks[6].y and middle_tip.y < landmarks[10].y:
        return "volume_up"

    # Gesture: Volume Down (Index and Middle Finger Downward)
    if index_tip.y > landmarks[6].y and middle_tip.y > landmarks[10].y:
        return "volume_down"

    # Gesture: Mute (Index Finger Straight and Thumb Pointing Down)
    if index_tip.y < landmarks[6].y and thumb_tip.y > landmarks[3].y:
        return "mute"

    # Gesture: Next Video (Thumb and Index forming a "V")
    if abs(thumb_tip.x - index_tip.x) > 0.1 and abs(thumb_tip.y - index_tip.y) < 0.05:
        return "next_video"

    # Gesture: Previous Video (Thumb and Pinky forming a "V")
    if abs(thumb_tip.x - pinky_tip.x) > 0.1 and abs(thumb_tip.y - pinky_tip.y) < 0.05:
        return "previous_video"

    return None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(hand_landmarks.landmark)

            if gesture == "play_pause":
                pyautogui.press("space")  # Play/Pause in most video players
                cv2.putText(frame, "Play/Pause", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif gesture == "volume_up":
                pyautogui.press("volumeup")  # Increase volume
                cv2.putText(frame, "Volume Up", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif gesture == "volume_down":
                pyautogui.press("volumedown")  # Decrease volume
                cv2.putText(frame, "Volume Down", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif gesture == "mute":
                pyautogui.press("volumemute")  # Mute volume
                cv2.putText(frame, "Mute", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif gesture == "next_video":
                pyautogui.hotkey("ctrl", "tab")  # Switch to next tab (Next video)
                cv2.putText(frame, "Next Video", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                time.sleep(0.5)  # Wait a bit to avoid multiple detections
            elif gesture == "previous_video":
                pyautogui.hotkey("ctrl", "shift", "tab")  # Switch to previous tab (Previous video)
                cv2.putText(frame, "Previous Video", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                time.sleep(0.5)  # Wait a bit to avoid multiple detections

    cv2.imshow("Gesture-Controlled Chrome", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()                     