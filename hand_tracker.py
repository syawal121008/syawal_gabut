# hand_tracker.py
import cv2
import mediapipe as mp
import numpy as np
import math
from typing import List, Tuple, Dict

class ModernHandTracker:
    def __init__(self, 
                 static_mode=False,
                 max_hands=2,
                 detection_confidence=0.7,
                 tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles
        
        self.custom_connections_style = {
            (0, 1): (245, 117, 66),  # Wrist to thumb base (orange)
            (1, 2): (245, 117, 66),  # Thumb connections
            (2, 3): (245, 117, 66),
            (3, 4): (245, 117, 66),
            (0, 5): (117, 245, 16),  # Index finger base (green)
            (5, 6): (117, 245, 16),  # Index finger connections
            (6, 7): (117, 245, 16),
            (7, 8): (117, 245, 16),
            (0, 9): (66, 117, 245),  # Middle finger base (blue)
            (9, 10): (66, 117, 245), # Middle finger connections
            (10, 11): (66, 117, 245),
            (11, 12): (66, 117, 245),
            (0, 13): (245, 66, 230), # Ring finger base (pink)
            (13, 14): (245, 66, 230), # Ring finger connections
            (14, 15): (245, 66, 230),
            (15, 16): (245, 66, 230),
            (0, 17): (245, 233, 66), # Pinky base (yellow)
            (17, 18): (245, 233, 66), # Pinky connections
            (18, 19): (245, 233, 66),
            (19, 20): (245, 233, 66)
        }

    def find_hands(self, img, draw_fancy=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        all_hands = []
        h, w, c = img.shape
        
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                hand_points = []
                
                for lm in hand_landmarks.landmark:
                    px, py, pz = int(lm.x * w), int(lm.y * h), lm.z
                    hand_points.append({'x': px, 'y': py, 'z': pz})
                
                all_hands.append(hand_points)
                
                if draw_fancy:
                    for connection in self.mp_hands.HAND_CONNECTIONS:
                        start_idx = connection[0]
                        end_idx = connection[1]
                        
                        start_pos = hand_points[start_idx]
                        end_pos = hand_points[end_idx]
                        
                        color = self.custom_connections_style.get(connection, (255, 255, 255))
                        
                        cv2.line(img, 
                                (start_pos['x'], start_pos['y']),
                                (end_pos['x'], end_pos['y']),
                                color, 2, cv2.LINE_AA)
                        
                    for point in hand_points:
                        cv2.circle(img, (point['x'], point['y']), 6, (255, 255, 255), -1)
                        cv2.circle(img, (point['x'], point['y']), 4, (75, 75, 75), -1)
                        
        return img, all_hands

    def get_gesture(self, hand_points):
        if not hand_points:
            return "No Hand"
            
        angles = self.calculate_finger_angles(hand_points)
        
        if all(angle > 150 for angle in angles.values()):
            return "Open Palm"
        elif all(angle < 90 for angle in angles.values()):
            return "Fist"
        elif angles['index'] > 150 and all(angle < 90 for finger, angle in angles.items() if finger != 'index'):
            return "Pointing"
        elif angles['index'] > 150 and angles['middle'] > 150 and all(angle < 90 for finger, angle in angles.items() if finger not in ['index', 'middle']):
            return "Peace"
        elif angles['thumb'] > 150 and all(angle < 90 for finger, angle in angles.items() if finger != 'thumb'):
            return "Thumbs Up"
        
        return "Unknown"

    def calculate_finger_angles(self, hand_points):
        if not hand_points:
            return {}
            
        angles = {}
        finger_bases = {
            'thumb': [0, 1, 2],
            'index': [0, 5, 6],
            'middle': [0, 9, 10],
            'ring': [0, 13, 14],
            'pinky': [0, 17, 18]
        }
        
        for finger, points in finger_bases.items():
            p1 = hand_points[points[0]]
            p2 = hand_points[points[1]]
            p3 = hand_points[points[2]]
            
            angle = math.degrees(math.atan2(p3['y'] - p2['y'], p3['x'] - p2['x']) -
                               math.atan2(p1['y'] - p2['y'], p1['x'] - p2['x']))
            
            angle = abs(angle)
            if angle > 180:
                angle = 360 - angle
                
            angles[finger] = angle
            
        return angles

