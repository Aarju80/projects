import cv2
import mediapipe as mp
import pygame

pygame.init()
pygame.mixer.init()
chords = {
    "index": pygame.mixer.Sound("chords/Em.wav"),   # Index finger
    "middle": pygame.mixer.Sound("chords/d.wav"),   # Middle finger
    "ring": pygame.mixer.Sound("chords/c.wav"),     # Ring finger
}

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()


def fingers_up(hand_landmarks):
    """Returns a list of boolean values indicating which fingers are up"""
    return [
        hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y,  # Index
        hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y,  # Middle
        hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y,  # Ring
    ]

last_played = None  # To avoid repeat play

def process_frame(img):
    """Process and return the processed frame (flipped and with hand landmarks)"""
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Draw landmarks and detect fingers if hands are detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            fingers = fingers_up(handLms)
 
            # Check if any finger is raised and play the corresponding chord
            if fingers[0] and last_played != "index":
                chords["index"].play()
                print("🎵 Playing: Em chord")
                return "index"
            elif fingers[1] and last_played != "middle":
                chords["middle"].play()
                print("🎵 Playing: D chord")
                return "middle"
            elif fingers[2] and last_played != "ring":
                chords["ring"].play()
                print("🎵 Playing: C chord")
                return "ring"
            elif not any(fingers):
                return None  # Reset when no fingers are up
    return last_played  # Return previous chord if no new finger is detected

# Main loop
while True:
    success, img = cap.read()
    if not success:
        print("Error: Failed to capture image.")
        break

    # Process the frame (hand landmarks detection and chord playing)
    last_played = process_frame(img)

    # Mirror the image (flip horizontally)
    img = cv2.flip(img, 1)

    # Show the mirrored video
    cv2.imshow("🎹 Air Piano - Hand Chord Player (Mirrored)", img)

    # Quit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 🧹 Cleanup
cap.release()
cv2.destroyAllWindows()
