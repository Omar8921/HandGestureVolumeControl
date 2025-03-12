import mediapipe as mp

class HandTracker:
    def __init__(self, static_image_mode=False, max_num_hands=2, model_complexity= 1, detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.detection_confidence = detection_confidence
        self.model_complexity = model_complexity
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.static_image_mode, self.max_num_hands, self.model_complexity, self.detection_confidence, self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.result = None

    def findHands(self, image, draw=True):
        self.result = self.hands.process(image)

        if self.result.multi_hand_landmarks:
            for hand_landmarks in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, hand_landmarks, self.mpHands.HAND_CONNECTIONS)

    def findPosition(self, image, handNum=0):
        lmList= []
        self.findHands(image, False)
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNum]
            for id, landmark in enumerate(myHand.landmark):
                h, w, c = image.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                lmList.append((id, cx, cy))

        return lmList
    
    def fingersUp(self, image):
        fingers = set()
        lmList = []
        if self.result.multi_hand_landmarks:
            for id, landmark in enumerate(self.result.multi_hand_landmarks[0].landmark):
                h, w, c = image.shape
                cx, cy = (landmark.x * w), (landmark.y * h)
                lmList.append((id, cx, cy))
            
        if lmList:
            for landmark in lmList:
                if lmList[4][2] < lmList[3][2]:
                    fingers.add('thumb')
                    
                if lmList[8][2] < lmList[7][2]:
                    fingers.add('index')
                    
                if lmList[12][2] < lmList[11][2]:
                    fingers.add('middle')
                    
                if lmList[16][2] < lmList[15][2]:
                    fingers.add('ring')
                    
                if lmList[20][2] < lmList[19][2]:
                    fingers.add('pinky')
                    
        return fingers
    