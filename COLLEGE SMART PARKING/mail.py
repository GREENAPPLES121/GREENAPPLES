import cv2
import pickle
import cvzone
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48

def send_email(free_spaces):
    sender_email = "freefireoff2020@gmail.com"
    receiver_email = "muthiahkyz@gmail.com"
    password = "freefire123="

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Free Parking Spaces"

    body = f"There are {free_spaces} free parking spaces available."
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Rest of your code remains unchanged...


def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            spaceCounter += 1

    return spaceCounter

# ... (previous code remains unchanged)

start_time = time.time()
while True:
    if time.time() - start_time > 60:
        free_spaces = checkParkingSpace(imgDilate)
        send_email(free_spaces)
        start_time = time.time()

    # ... (previous code remains unchanged)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # Capture the result of checkParkingSpace
    free_spaces = checkParkingSpace(imgDilate)

    # ... (previous code remains unchanged)

# ... (remaining code remains unchanged)


    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    cv2.waitKey(10)