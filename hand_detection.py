import cv2
import mediapipe as mp
import math
import numpy as np

class HandDetector:
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.7, trackCon=0.7):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            model_complexity=self.modelComplex,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.prev_positions = []

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        self.handTypes = []
        
        if self.results.multi_hand_landmarks:
            for handType in self.results.multi_handedness:
                self.handTypes.append(handType.classification[0].label)
            
            if draw:
                for handLms in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=False):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy, lm.z])
        return lmList

    def fingersUp(self, lmList):
        fingers = []
        if not lmList:
            return []

        # Thumb
        if self.handTypes and self.handTypes[0] == "Right":
            fingers.append(1 if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0]-1][1] else 0)
        else:
            fingers.append(1 if lmList[self.tipIds[0]][1] < lmList[self.tipIds[0]-1][1] else 0)

        # 4 fingers
        for id in range(1, 5):
            fingers.append(1 if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id]-2][2] else 0)

        return fingers

    def detectGesture(self, lmList):
        if not lmList:
            return "No Hand"
            
        fingers = self.fingersUp(lmList)
        
        if sum(fingers) == 0:
            return "Fist"
        elif sum(fingers) == 5:
            return "Open Hand"
        elif fingers == [0,1,0,0,0]:
            return "Point"
        elif fingers == [0,1,1,0,0]:
            return "Peace"
        elif self.isHandPinching(lmList):
            return "Pinch"
        
        return "Unknown"

    def isHandPinching(self, lmList, threshold=30):
        if len(lmList) < 20:
            return False
        distance = self.calculateDistance(lmList, 8, 4)
        return distance < threshold

    def calculateDistance(self, lmList, point1, point2):
        if len(lmList) > max(point1, point2):
            x1, y1 = lmList[point1][1], lmList[point1][2]
            x2, y2 = lmList[point2][1], lmList[point2][2]
            return math.hypot(x2 - x1, y2 - y1)
        return 0