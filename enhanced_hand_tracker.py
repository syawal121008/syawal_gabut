from hand_tracker import ModernHandTracker
import cv2
import numpy as np
import pyautogui
import math
from typing import List, Dict, Tuple
import time

class EnhancedHandTracker(ModernHandTracker):
    def __init__(self):
        super().__init__()
        # Screen & Mouse Configuration
        self.screen_width, self.screen_height = pyautogui.size()
        pyautogui.FAILSAFE = False
        
        # Mouse Tracking Parameters
        self.smooth_factor = 0.5
        self.prev_mouse_pos = (0, 0)
        self.mouse_speed_limit = 60
        
        # Expanded Detection Area for wider view
        self.x_min, self.x_max = 50, 590
        self.y_min, self.y_max = 50, 430
        
        # Drawing Mode
        self.drawing_points = []
        self.is_drawing = False
        self.current_color = (0, 255, 0)
        self.current_thickness = 3
        
        # Mouse Stabilization
        self.mouse_positions_buffer = []
        self.buffer_size = 4
        self.last_stable_pos = None
        
        # Mode Control
        self.modes = ['mouse', 'draw', 'media']
        self.current_mode_index = 0
        
        # Stability threshold
        self.stability_threshold = 15

    def calibrate_mouse_area(self, hand_points):
        if not hand_points:
            return
        
        x_values = [point['x'] for point in hand_points]
        y_values = [point['y'] for point in hand_points]
        
        # Wider area calibration with smoothing
        margin = 100
        target_x_min = max(50, min(x_values) - margin)
        target_x_max = min(590, max(x_values) + margin)
        target_y_min = max(50, min(y_values) - margin)
        target_y_max = min(430, max(y_values) + margin)
        
        # Smooth transition for area boundaries
        self.x_min = int(self.x_min * 0.8 + target_x_min * 0.2)
        self.x_max = int(self.x_max * 0.8 + target_x_max * 0.2)
        self.y_min = int(self.y_min * 0.8 + target_y_min * 0.2)
        self.y_max = int(self.y_max * 0.8 + target_y_max * 0.2)

    def air_drawing(self, hand_points, img):
        if not hand_points:
            return img
            
        index_tip = hand_points[8]
        middle_tip = hand_points[12]
        
        if self.check_drawing_mode(hand_points):
            pt = (index_tip['x'], index_tip['y'])
            if not self.is_drawing:
                self.drawing_points.append([])
                self.is_drawing = True
            self.drawing_points[-1].append((pt, self.current_color, self.current_thickness))
        else:
            self.is_drawing = False
            
        for stroke in self.drawing_points:
            for i in range(1, len(stroke)):
                cv2.line(img, stroke[i-1][0], stroke[i][0], 
                        stroke[i][1], stroke[i][2])
                        
        return img

    def media_controls(self, hand_points):
        if not hand_points:
            return "none"
            
        gesture = self.get_gesture(hand_points)
        
        if gesture == "Peace":
            return "play_pause"
        elif gesture == "Open Palm":
            palm_center = hand_points[0]
            if palm_center['x'] < 200:
                return "previous"
            elif palm_center['x'] > 440:
                return "next"
                
        thumb_tip = hand_points[4]
        index_tip = hand_points[8]
        angle = math.atan2(index_tip['y'] - thumb_tip['y'], 
                          index_tip['x'] - thumb_tip['x'])
        angle = math.degrees(angle)
        
        if 45 < angle < 135:
            return "volume_up"
        elif -135 < angle < -45:
            return "volume_down"
            
        return "none"

    def draw_control_panel(self, img):
        h, w, c = img.shape
        
        cv2.rectangle(img, (w-200, 0), (w, 150), (0, 0, 0), -1)
        cv2.rectangle(img, (w-200, 0), (w, 150), (255, 255, 255), 1)
        
        colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]
        for i, color in enumerate(colors):
            cv2.circle(img, (w-180+i*40, 30), 15, color, -1)
            if color == self.current_color:
                cv2.circle(img, (w-180+i*40, 30), 17, (255, 255, 255), 2)
                
        for i in range(3):
            thickness = i*2 + 2
            y_pos = 70 + i*20
            cv2.line(img, (w-180, y_pos), (w-100, y_pos), 
                    (255, 255, 255), thickness)
            if thickness == self.current_thickness:
                cv2.circle(img, (w-190, y_pos), 5, (0, 255, 0), -1)
                
        return img

    def check_drawing_mode(self, hand_points):
        index_up = hand_points[8]['y'] < hand_points[7]['y']
        middle_down = hand_points[12]['y'] > hand_points[11]['y']
        return index_up and middle_down

    def advanced_mouse_smoothing(self, new_pos):
        self.mouse_positions_buffer.append(new_pos)
        
        if len(self.mouse_positions_buffer) > self.buffer_size:
            self.mouse_positions_buffer.pop(0)
        
        # Weighted average with more weight to recent positions
        weights = np.linspace(1, 2, len(self.mouse_positions_buffer))
        weights = weights / np.sum(weights)
        
        avg_x = int(sum(pos[0] * w for pos, w in zip(self.mouse_positions_buffer, weights)))
        avg_y = int(sum(pos[1] * w for pos, w in zip(self.mouse_positions_buffer, weights)))
        
        # Stability check
        if self.last_stable_pos is not None:
            dx = avg_x - self.last_stable_pos[0]
            dy = avg_y - self.last_stable_pos[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.stability_threshold:
                return self.last_stable_pos
            
        self.last_stable_pos = (avg_x, avg_y)
        return (avg_x, avg_y)

    def virtual_mouse(self, hand_points, img):
        if not hand_points:
            return img, False
        
        self.calibrate_mouse_area(hand_points)
        
        index_tip = hand_points[8]
        thumb_tip = hand_points[4]
        
        # Smoother interpolation
        screen_x = np.interp(index_tip['x'], 
                           [self.x_min, self.x_max], 
                           [0, self.screen_width])
        screen_y = np.interp(index_tip['y'], 
                           [self.y_min, self.y_max], 
                           [0, self.screen_height])
        
        # Calculate movement with speed limit
        dx = screen_x - self.prev_mouse_pos[0]
        dy = screen_y - self.prev_mouse_pos[1]
        
        # Apply speed limits
        dx = np.clip(dx, -self.mouse_speed_limit, self.mouse_speed_limit)
        dy = np.clip(dy, -self.mouse_speed_limit, self.mouse_speed_limit)
        
        # Apply smooth factor
        curr_mouse_x = int(self.prev_mouse_pos[0] + dx * self.smooth_factor)
        curr_mouse_y = int(self.prev_mouse_pos[1] + dy * self.smooth_factor)
        
        # Apply advanced smoothing
        curr_mouse_x, curr_mouse_y = self.advanced_mouse_smoothing((curr_mouse_x, curr_mouse_y))
        
        is_clicking = self.check_pinch(thumb_tip, index_tip)
        
        try:
            if not is_clicking:  # Only move if not clicking
                pyautogui.moveTo(curr_mouse_x, curr_mouse_y, duration=0.01)
            else:
                pyautogui.click()
        except Exception as e:
            print(f"Mouse movement error: {e}")
        
        self.prev_mouse_pos = (curr_mouse_x, curr_mouse_y)
        
        # Visual feedback
        cv2.circle(img, (index_tip['x'], index_tip['y']), 10, (255, 0, 255), cv2.FILLED)
        if is_clicking:
            cv2.circle(img, (index_tip['x'], index_tip['y']), 12, (0, 255, 0), 2)
        
        return img, is_clicking

    def check_pinch(self, p1, p2, threshold=30):
        distance = math.hypot(p1['x'] - p2['x'], p1['y'] - p2['y'])
        return distance < threshold