import cv2
import numpy as np
import serial

arduino = serial.Serial('COM3', 9600)
cap = cv2.VideoCapture(0)
gestures = {
    0: "Open Hand",
    1: "Fist"
}
def detect_hand(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    mask = cv2.GaussianBlur(mask, (5, 5), 100)
    return mask
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    mask = detect_hand(frame)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        contour = max(contours, key=lambda x: cv2.contourArea(x))
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if w > 100 and h > 100:
            gesture = 1
        else:
            gesture = 0
        cv2.putText(frame, gestures[gesture], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        if gesture == 1:
            arduino.write(b'F')
        elif gesture == 0:
            arduino.write(b'O')
    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
arduino.close()
