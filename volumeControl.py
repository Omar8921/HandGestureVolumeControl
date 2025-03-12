import cv2
import time
import handTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    volume.SetMasterVolumeLevelScalar(level / 100, None)

def normalize(value, minimum, maximum):
    return (value - minimum) / (maximum - minimum)

cap = cv2.VideoCapture(0)

cTime, pTime = 0, 0

handTracker = htm.HandTracker(max_num_hands=1)
minimum, maximum = 0, 100

# Coordinates of the top-left and bottom-right corners of the sound volume rectangle
rectangle_bbox = (50,100), (120, 400)

while cv2.waitKey(10) != 27:
    success, image = cap.read()
    height, width, c = image.shape

    if not success:
        break

    image = cv2.flip(image, 1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

    handTracker.findHands(image, draw=False)
    lmList = handTracker.findPosition(image)
    cv2.rectangle(image, rectangle_bbox[0], rectangle_bbox[1], (0,255,0), 3)

    if lmList: 
        x1, y1 = lmList[4][1], lmList[4][2] 
        x2, y2 = lmList[8][1], lmList[8][2] 

        cv2.circle(image, (x1, y1), 10, (255,0,255), -1)
        cv2.circle(image, (x2, y2), 10, (255,0,255), -1)
        cv2.line(image, (x1, y1), (x2, y2), (255,0,255), 5)

        distance = math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
        normalized_distance = normalize(distance, minimum, maximum)
        minimum, maximum = min(minimum, distance), max(maximum, distance)

        normalized_distance *= 100
        normalized_distance = int(normalized_distance)
        normalized_distance = max(normalized_distance, 0)
        normalized_distance = min(normalized_distance, 100)
        cv2.rectangle(image, (rectangle_bbox[0][0], rectangle_bbox[1][1] - int(normalized_distance / 100 * (rectangle_bbox[1][1] - rectangle_bbox[0][1]))), rectangle_bbox[1], (0,255,0), -1)
        cv2.putText(image, f'{normalized_distance}', (rectangle_bbox[0][0], rectangle_bbox[1][1] + 50), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
        set_volume(normalized_distance)


    cv2.imshow('Camera Preview', image)

cap.release()