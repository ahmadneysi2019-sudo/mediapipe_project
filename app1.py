import cv2
import mediapipe as mp
import sounddevice as sd
import time


mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

finger_list = [8, 12, 16, 20]

last_number = 0
countdown = []
microphone_on = False


while True:

    _, frame = cap.read()

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_hands.process(frameRGB)

    counter = 0

    if result.multi_hand_landmarks:

        for hand in result.multi_hand_landmarks:

            landmark = hand.landmark

            
            for tip in finger_list:
                if landmark[tip].y < landmark[tip - 2].y:
                    counter += 1

            
            if landmark[4].x > landmark[3].x:
                counter += 1

    
    if counter in [1, 2, 3]:

        if counter != last_number:
            countdown.append(counter)
            last_number = counter
      
    if len(countdown) >= 3:

        if countdown[-3:] == [3, 2, 1]:

            microphone_on = True

            
            print("Microphone Activated!")

            countdown = []

    
    if microphone_on:
        text = "MIC ON"
    else:
        text = "MIC OFF"

    cv2.putText(
        frame,
        str(counter),
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        3,
        (0, 255, 0),
        3
    )

    cv2.putText(
        frame,
        text,
        (50, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        3
    )

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
