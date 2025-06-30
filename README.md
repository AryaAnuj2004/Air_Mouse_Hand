# 🖱️ Air_Mouse_Hand Introduction
## Introduction
This Python project enables you to control your computer's mouse cursor using only hand gestures, captured via a webcam. It uses OpenCV and MediaPipe for hand tracking, providing real-time gesture recognition.

---

## ✨ Features
- Move cursor with hand movement
- Left click using gesture
- Right click using gesture 
- Scroll and drag support 
- Real-time performance with minimal latency

---

## 🛠️ Tech Stack
- Python
- OpenCV (`cv2`)
- MediaPipe
- Autopy
- Pyautogui
- Math and Time (standard libraries)

---

## 📦 Requirements
Install the required Python packages with:

```bash
pip install -r requirement.txt
```

---

## 📸 Hand Gestures Used
### Gesture	- Action
- Index finger up	- Move Cursor
- Index + Middle fingers up (close together)	- Right Click
- Index + Thumb fingers up (close together)	- Left Click
- Index + Thumb fingers up (close together and holds more than 0.5 sec)	- Holding Cursor for Dragging
- All fingers up (except thumb) - Scrolling

---

## 🚀 How to Run
1. Clone the repository or download the script.

   ```
   $ git clone https://github.com/AryaAnuj2004/Air_Mouse_Hand
   ```
2. Install all the requirements.
   ```
   pip install -r requirement.txt
   ```
3. Ensure your webcam is connected or all the permissions of the camera are given to the system.

4. Run the script (in the Hand_Mouse directory):
   ```
   python .\FullHandVirtualMouse.py
   ```

---

## 🧠 How It Works
- Captures frames using your webcam.
- Detects hand landmarks using MediaPipe.
- Maps the index finger position to your screen resolution.
- Triggers mouse events like move, click, drag and scrolling using gesture conditions

---

#### ⚠️ This project requires **Python 3.7 to 3.12**. Python 3.13 is not supported due to `mediapipe` compatibility issues.

---

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE-MIT) file for details.

