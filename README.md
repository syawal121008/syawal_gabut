```
  _    _                 _    _____           _                  _____            _             _ 
 | |  | |               | |  / ____|         | |                / ____|          | |           | |
 | |__| | __ _ _ __   __| | | |  __  ___  ___| |_ _   _ _ __  | |     ___  _ __ | |_ _ __ ___ | |
 | |  | |/ _` | '_ \ / _` | | | |_ |/ _ \/ __| __| | | | '__| | |    / _ \| '_ \| __| '__/ _ \| |
 | |  | | (_| | | | | (_| | | |____| (__/\__ \ |_| |_| | |    | |___| (_) | | | | |_| | | (_) | |
 |_|  |_|\__,_|_| |_|\__,_|  \_____|\___||___/\__|\__,_|_|     \_____\___/|_| |_|\__|_|  \___/|_|
                                                                                                    
                                                                                By: SyawalMods
```

# Hand Gesture Control System 🖐️

Sebuah sistem kontrol komputer berbasis gerakan tangan yang memungkinkan Anda mengontrol mouse, menggambar di udara, dan mengontrol media player menggunakan gerakan tangan.

## ✨ Fitur Utama

- 🖱️ **Mode Mouse Virtual**: Kontrol kursor menggunakan gerakan tangan
- 🎨 **Mode Menggambar**: Menggambar di udara dengan gerakan jari
- 🎵 **Mode Media**: Kontrol media player (play/pause, next/previous, volume)
- 🔄 **Multi-Mode**: Beralih antar mode dengan mudah menggunakan gesture
- 📊 **Real-time FPS Display**: Monitor performa sistem
- 🎯 **Tracking Presisi**: Deteksi tangan yang akurat dengan MediaPipe

## 🛠️ Persyaratan Sistem

- Python 3.8+
- Webcam
- Sistem Operasi: Windows/Linux/MacOS

## 📦 Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/syawal12102008/syawal_gabut/hand-gesture-control.git
cd hand-gesture-control
```

2. Install dependensi yang diperlukan:
```bash
pip install -r requirements.txt
```

## 🚀 Cara Penggunaan

1. Jalankan program:
```bash
python main.py
```

2. Gunakan gesture tangan untuk mengontrol sistem:
   - 👊 **Gesture Tinju**: Ganti mode
   - ✌️ **Gesture Peace**: Play/Pause di mode media
   - 🤚 **Telapak Terbuka**: Previous/Next track di mode media
   - 👆 **Jari Telunjuk**: Kontrol mouse di mode mouse
   - 🤏 **Gesture Pinch**: Klik mouse di mode mouse

## 📝 Mode dan Gesture

### 1. Mode Mouse
- Gunakan telunjuk untuk menggerakkan kursor
- Gesture pinch (ibu jari dan telunjuk) untuk klik
- Tracking halus dengan stabilisasi gerakan

### 2. Mode Menggambar
- Angkat telunjuk untuk mulai menggambar
- Turunkan telunjuk untuk berhenti menggambar
- Panel kontrol untuk memilih warna dan ketebalan garis

### 3. Mode Media
- ✌️ Peace: Play/Pause
- 🤚 Telapak ke kiri: Previous track
- 🤚 Telapak ke kanan: Next track
- 👆 Telunjuk ke atas: Volume up
- 👆 Telunjuk ke bawah: Volume down

## 🔍 Penjelasan Kode

Proyek ini terdiri dari beberapa modul utama:
- `main.py`: Program utama dan loop aplikasi
- `hand_detection.py`: Deteksi tangan menggunakan MediaPipe
- `hand_tracker.py`: Tracking dan analisis gerakan tangan
- `enhanced_hand_tracker.py`: Implementasi fitur kontrol

## 🤝 Kontribusi

Kontribusi selalu diterima! Silakan:
1. Fork repository
2. Buat branch fitur baru (`git checkout -b fitur-baru`)
3. Commit perubahan (`git commit -m 'Menambah fitur baru'`)
4. Push ke branch (`git push origin fitur-baru`)
5. Buat Pull Request

## 📄 Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 🙏 Credit

- MediaPipe untuk teknologi hand tracking
- OpenCV untuk image processing
- PyAutoGUI untuk kontrol mouse

## 📞 Kontak

- GitHub: syawal121008
- Email: syawalduinalhabsy2@gmail.com

---

Made with ❤️ in Indonesia
