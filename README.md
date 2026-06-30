# Gesture-Controlled 220V Bulb Project



![Status](https://img.shields.io/badge/Status-Completed-success)
![Platform](https://img.shields.io/badge/Platform-NodeMCU%20%7C%20ESP32-blue)
![Language](https://img.shields.io/badge/Programming-Arduino%20%7C%20Python-orange)
![Computer Vision](https://img.shields.io/badge/Computer%20Vision-OpenCV-green)

A smart gesture-based automation project that controls a **220V bulb** using hand gestures detected by a webcam. The system uses **Python OpenCV** for gesture recognition and sends control commands wirelessly to a **NodeMCU / ESP32**, which switches the bulb ON or OFF in real time.

---

## Project Overview

This project demonstrates a practical combination of **computer vision**, **microcontroller programming**, and **IoT-style wireless control**.  
The core idea is simple and powerful:

- **open hand** → bulb ON

<img width="929" height="991" alt="image" src="https://github.com/user-attachments/assets/99c4f0df-8b1c-462d-a9ee-ab54654489ea" />


- **closed hand** → bulb OFF


<img width="745" height="711" alt="image" src="https://github.com/user-attachments/assets/7de15331-02f4-469f-ac57-0a81272cdd03" />



Instead of using a physical switch, the user controls the bulb through hand gestures detected by the camera.

---

## Project Objectives

- Detect hand gestures using a webcam.
- Classify the hand state as open or closed.
- Send the detected command from Python to the microcontroller over Wi-Fi.
- Control a 220V bulb wirelessly in real time.
- Demonstrate a clean and practical smart-home automation concept.

---

## Technologies Used

### Hardware
- NodeMCU / ESP32
- Relay module
- 220V bulb
- Webcam / laptop camera
- Power supply

### Software
- Arduino IDE
- Python
- OpenCV
- HTTP-based communication
- Wi-Fi networking

---

## How It Works

1. A webcam captures the user’s hand in front of the camera.
2. A Python script processes the video using **OpenCV**.
3. The script detects whether the hand is **open** or **closed**.
4. Based on the detected gesture, Python sends an HTTP request to the NodeMCU / ESP32.
5. The microcontroller receives the command.
6. The relay switches the **220V bulb ON or OFF** accordingly.

---

## Main Features

- Touch-free bulb control
- Real-time gesture recognition
- Wireless communication over Wi-Fi
- Simple and practical smart automation
- Combination of Python and embedded systems
- Good foundation for smart home applications

---

## System Workflow

### Open Hand
- Gesture detected as open
- Python sends ON command
- Microcontroller activates relay
- Bulb turns ON

### Closed Hand
- Gesture detected as closed
- Python sends OFF command
- Microcontroller deactivates relay
- Bulb turns OFF

---

## Communication Method

The Python script communicates with the microcontroller using **HTTP requests over Wi-Fi**.

This makes the system:
- fast
- easy to implement
- suitable for local automation
- easy to expand in future projects

---

## Project Demo

LinkedIn Video Demo:  
[Gesture-Controlled 220V Bulb Project](https://www.linkedin.com/feed/update/urn:li:activity:7254236279024799744/?originTrackingId=RORgDKfSTBumCledLlcwUQ%3D%3D)

---
## Files
ESP Code :
[ESP_code.DOCX](https://github.com/user-attachments/files/29085339/ESP_code.DOCX)

Python Code :
[Uploading Hanimport cv2
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
d_Gesture_Detection_Using_Laptop_Camera.py…]()

---

## Future Improvements

- Add multiple gestures
- Control more appliances
- Add mobile app integration
- Improve gesture accuracy
- Add voice control
- Build a full smart-home dashboard

---

## Conclusion

This project successfully shows how **computer vision** and **microcontroller-based IoT control** can be combined to create a touch-free automation system.  
It is a strong demonstration of real-time gesture recognition, wireless communication, and practical smart-device control.

---

## Author

**Anees Ur Rehman**  
Email: eng.aneesrehman@gmail.com
