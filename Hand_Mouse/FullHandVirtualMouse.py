import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui

# Webcam dimensions
wCam, hCam = 640, 480
frameRed = 100
smoothening = 5

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

pinch_time_start = 0
is_dragging = False
click_threshold_time = 0.3   # Time threshold for click vs drag
drag_threshold_time = 0.5   # Time to initiate drag


while True:

    # -------------------- Find the hand landmarks -----------------------
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # ------------------- Get the tip of the index, middle and thumb fingers --------------------------
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]     # Index tip
        x2, y2 = lmList[12][1:]    # Middle tip
        thumb_x, thumb_y = lmList[4][1:]    # Thumb tip

        # ------------------- Check which fingers are up ---------------------
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameRed, 30), (wCam - frameRed, hCam - (70 + frameRed)), (255, 0, 255), 2)


        # -------------- Only index finger : Moving Mode -------------------------

        if (fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0) or is_dragging:
            mx, my = lmList[8][1], lmList[8][2]

            # ---------- Convert coordinates -------------------
            x3 = np.interp(x1, (frameRed, wCam - frameRed), (0, wScr))
            y3 = np.interp(y1, (frameRed - 40, hCam-(80 + frameRed)), (0, hScr))

            # ---------- Smoothen Values ---------------
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # ---------- Move mouse ------------
            autopy.mouse.move(wScr-clocX, clocY)
            cv2.circle(img, (mx, my), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY


        # ----------------- Left Click and Dragging mode ---------------------

        if fingers[1] == 1 and fingers[0] == 1 and fingers[2] == 0:
            length, img, lineInfo = detector.findDistance(4, 8, img)
            is_pinching = length < 30

            if is_pinching:
                if pinch_time_start == 0:
                    pinch_time_start = time.time()
                pinch_duration = time.time() - pinch_time_start

                # Quick pinch for click
                if pinch_duration < click_threshold_time and not is_dragging:
                    # Only register click when pinch is released within click_threshold_time
                    pass  # Wait for release to confirm click
                # Longer pinch for drag
                elif pinch_duration >= drag_threshold_time and not is_dragging:
                    is_dragging = True
                    pyautogui.mouseDown(button='left')
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            else:
                if pinch_time_start != 0:
                    pinch_duration = time.time() - pinch_time_start
                    if pinch_duration < click_threshold_time and not is_dragging:
                        # Perform click only if pinch was short and no drag started
                        pyautogui.click(button='left')
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    elif is_dragging:
                        # Release drag
                        pyautogui.mouseUp(button='left')
                        is_dragging = False
                    pinch_time_start = 0


        # Right click ------------ index finger and middle finger -------------

        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            if length < 30:
                cv2.circle(img,(lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.RIGHT)
                time.sleep(0.2)

            # -------------------- Scrolling using all fingers -------------------------

            elif fingers[1:] == [1, 1, 1, 1]:
                y_scroll = lmList[12][2]  # Y of middle tip
                if y_scroll < (hCam / 3) + 10:
                    pyautogui.scroll(100)       # Scroll Up
                elif y_scroll > (hCam * 2 / 3) - 20:
                    pyautogui.scroll(-100)         # Scroll Down


    # -----------------  Frame rate  ----------------

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:'+str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 1)

    # -----------------  Display the video  ----------------------

    cv2.imshow("Virtual Mouse", img)
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or cv2.getWindowProperty("Virtual Mouse", cv2.WND_PROP_VISIBLE) < 1:
        break


cap.release()
cv2.destroyAllWindows()