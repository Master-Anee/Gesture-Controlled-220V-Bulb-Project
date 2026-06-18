import cv2
import mediapipe as mp
import requests

# ESP32 IP address, replace with the actual IP address of your ESP32
esp_ip = "http://192.168.0.104"

# Function to send command to ESP32
def send_command_to_esp(command):
    url = f"{esp_ip}/LED={command}"
    try:
        response = requests.get(url)
        print(f"Sent {command} command to ESP32. Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send command: {e}")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Initialize camera
cap = cv2.VideoCapture(0)

def detect_gesture(hand_landmarks):
    if not hand_landmarks:
        return None

    # Get key landmarks for gesture detection
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

    # Measure distances from each fingertip to its respective MCP joint
    def distance(a, b):
        return ((a.x - b.x)**2 + (a.y - b.y)**2 + (a.z - b.z)**2)**0.5

    index_finger_dist = distance(index_tip, index_mcp)
    middle_finger_dist = distance(middle_tip, middle_mcp)
    ring_finger_dist = distance(ring_tip, ring_mcp)
    pinky_finger_dist = distance(pinky_tip, pinky_mcp)

    # Simple logic: if all fingertip distances are small, hand is closed
    if (index_finger_dist < 0.1 and
        middle_finger_dist < 0.1 and
        ring_finger_dist < 0.1 and
        pinky_finger_dist < 0.1):
        return "CLOSED"
    else:
        return "OPEN"

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the image color to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame to detect hands
    results = hands.process(rgb_frame)
    
    # Draw the hand annotations on the frame
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(hand_landmarks)
            cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # Send the gesture result to the ESP32
            if gesture == "OPEN":
                send_command_to_esp("OFF")
            elif gesture == "CLOSED":
                send_command_to_esp("ON")
    
    # Display the frame
    cv2.imshow("Hand Gesture Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
