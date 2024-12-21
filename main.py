# main.py
import cv2
import time
from enhanced_hand_tracker import EnhancedHandTracker

def main():
    # Initialize camera with higher resolution for wider view
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Increased from 1280
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Increased from 720
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    tracker = EnhancedHandTracker()
    
    # Mode selection
    modes = ['mouse', 'draw', 'media']
    current_mode = 0
    
    # FPS calculation
    fps_start_time = time.time()
    fps_counter = 0
    fps = 0
    
    while True:
        success, img = cap.read()
        if not success:
            break
            
        # Optional: Resize if the frame is too large for display
        # img = cv2.resize(img, (1280, 720))
            
        img = cv2.flip(img, 1)
        img, hands = tracker.find_hands(img)
        
        # Mode indicator
        cv2.putText(img, f"Mode: {modes[current_mode]}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if hands:
            # Process based on current mode
            if modes[current_mode] == 'mouse':
                img, is_clicking = tracker.virtual_mouse(hands[0], img)
                
            elif modes[current_mode] == 'draw':
                img = tracker.air_drawing(hands[0], img)
                img = tracker.draw_control_panel(img)
                
            elif modes[current_mode] == 'media':
                action = tracker.media_controls(hands[0])
                if action != "none":
                    cv2.putText(img, f"Media Action: {action}", (10, 70),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Check for mode change gesture (closed fist)
            gesture = tracker.get_gesture(hands[0])
            if gesture == "Fist":
                current_mode = (current_mode + 1) % len(modes)
                time.sleep(0.5)  # Prevent multiple switches
        
        # Calculate and display FPS
        fps_counter += 1
        if time.time() - fps_start_time > 1:
            fps = fps_counter
            fps_counter = 0
            fps_start_time = time.time()
            
        cv2.putText(img, f"FPS: {fps}", (10, 670),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display in fullscreen
        cv2.namedWindow("Enhanced Hand Tracker", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Enhanced Hand Tracker", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Enhanced Hand Tracker", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()