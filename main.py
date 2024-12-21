#!/usr/bin/env python3
"""
Hand Gesture Control System
Author: Syawal Mods
Created: 12 12 2024
"""

import cv2
import time
import sys
from enhanced_hand_tracker import EnhancedHandTracker

def print_banner():
    banner = """
  _    _                 _    _____           _                  _____            _             _ 
 | |  | |               | |  / ____|         | |                / ____|          | |           | |
 | |__| | __ _ _ __   __| | | |  __  ___  ___| |_ _   _ _ __  | |     ___  _ __ | |_ _ __ ___ | |
 | |  | |/ _` | '_ \ / _` | | | |_ |/ _ \/ __| __| | | | '__| | |    / _ \| '_ \| __| '__/ _ \| |
 | |  | | (_| | | | | (_| | | |____| (__/\__ \ |_| |_| | |    | |___| (_) | | | | |_| | | (_) | |
 |_|  |_|\__,_|_| |_|\__,_|  \_____|\___||___/\__|\__,_|_|     \_____\___/|_| |_|\__|_|  \___/|_|
                                                                                By: SyawalMods
    """
    print(banner)
    print("\nMemulai Hand Gesture Control System...")
    print("Tekan 'q' untuk keluar\n")

def initialize_camera():
    """Inisialisasi kamera dengan pengaturan optimal."""
    cap = cv2.VideoCapture(0)
    
    # Pengaturan kamera untuk performa optimal
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    if not cap.isOpened():
        raise Exception("Tidak dapat mengakses kamera!")
    
    return cap

def main():
    try:
        print_banner()
        
        # Inisialisasi kamera
        cap = initialize_camera()
        
        # Inisialisasi hand tracker
        tracker = EnhancedHandTracker()
        
        # Pengaturan mode
        modes = ['mouse', 'draw', 'media']
        current_mode = 0
        
        # Pengaturan FPS
        fps_start_time = time.time()
        fps_counter = 0
        fps = 0
        
        # Mode indikator warna
        mode_colors = {
            'mouse': (0, 255, 0),    # Hijau
            'draw': (255, 0, 0),     # Biru
            'media': (0, 0, 255)     # Merah
        }
        
        while True:
            # Baca frame dari kamera
            success, img = cap.read()
            if not success:
                print("Gagal membaca frame dari kamera!")
                break
                
            # Flip gambar horizontal untuk tampilan mirror
            img = cv2.flip(img, 1)
            
            # Deteksi tangan
            img, hands = tracker.find_hands(img)
            
            # Tampilkan mode aktif
            current_color = mode_colors[modes[current_mode]]
            cv2.putText(img, f"Mode: {modes[current_mode].upper()}", 
                       (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                       current_color, 2)
            
            if hands:
                # Proses berdasarkan mode aktif
                if modes[current_mode] == 'mouse':
                    img, is_clicking = tracker.virtual_mouse(hands[0], img)
                    
                elif modes[current_mode] == 'draw':
                    img = tracker.air_drawing(hands[0], img)
                    img = tracker.draw_control_panel(img)
                    
                elif modes[current_mode] == 'media':
                    action = tracker.media_controls(hands[0])
                    if action != "none":
                        cv2.putText(img, f"Media: {action.replace('_', ' ').title()}", 
                                  (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                                  (0, 255, 0), 2)
                
                # Deteksi pergantian mode
                gesture = tracker.get_gesture(hands[0])
                if gesture == "Fist":
                    current_mode = (current_mode + 1) % len(modes)
                    print(f"Mode berubah ke: {modes[current_mode].upper()}")
                    time.sleep(0.5)  # Delay untuk mencegah multiple switch
            
            # Hitung dan tampilkan FPS
            fps_counter += 1
            if time.time() - fps_start_time > 1:
                fps = fps_counter
                fps_counter = 0
                fps_start_time = time.time()
                
            cv2.putText(img, f"FPS: {fps}", 
                       (20, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (255, 255, 255), 2)
            
            # Tampilkan frame
            cv2.namedWindow("Hand Gesture Control", cv2.WINDOW_NORMAL)
            cv2.imshow("Hand Gesture Control", img)
            
            # Cek input keyboard
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\nMenutup aplikasi...")
                break
                
    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")
        sys.exit(1)
        
    finally:
        # Bersihkan resources
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()
        print("Aplikasi ditutup dengan aman.")

if __name__ == "__main__":
    main()
