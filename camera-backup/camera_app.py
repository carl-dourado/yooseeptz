import tkinter as tk
import cv2
import threading
import subprocess
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Câmera Yoosee")
        self.window.geometry("800x600")
        self.window.configure(bg="#222")
        
        self.video_label = tk.Label(window, bg="black")
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        self.status_var = tk.StringVar(value="🟢 Conectando RTSP...")
        tk.Label(window, textvariable=self.status_var, font=("Arial", 10), bg="#222", fg="white").pack(pady=2)
        
        btn_frame = tk.Frame(window, bg="#222")
        btn_frame.pack(pady=10)
        
        btn_style = {"font": ("Arial", 14), "width": 4, "height": 1, "bg": "#444", "fg": "white", "activebackground": "#666"}
        
        tk.Button(btn_frame, text="⬆️", command=lambda: self.move("UP"), **btn_style).grid(row=0, column=1, padx=5, pady=2)
        tk.Button(btn_frame, text="⬅️", command=lambda: self.move("LEFT"), **btn_style).grid(row=1, column=0, padx=5, pady=2)
        tk.Button(btn_frame, text="➡️", command=lambda: self.move("RIGHT"), **btn_style).grid(row=1, column=2, padx=5, pady=2)
        tk.Button(btn_frame, text="⬇️", command=lambda: self.move("DOWN"), **btn_style).grid(row=2, column=1, padx=5, pady=2)
        
        self.rtsp_url = "rtsp://admin:cnvasco54@192.168.0.2:554/onvif1"
        self.running = True
        
        # Thread para ler o vídeo sem travar a interface
        threading.Thread(target=self.video_loop, daemon=True).start()

    def video_loop(self):
        # Configurações para reduzir latência no OpenCV
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp|fflags;nobuffer|flags;low_delay"
        cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
        
        if not cap.isOpened():
            self.status_var.set("🔴 Falha ao abrir vídeo")
            return
            
        self.status_var.set("🟢 Online")
        
        while self.running:
            ret, frame = cap.read()
            if ret:
                # Redimensiona mantendo proporção
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (800, 450))
                img = ImageTk.PhotoImage(image=Image.fromarray(frame))
                
                # Atualiza na thread principal
                self.video_label.imgtk = img
                self.video_label.configure(image=img)
            else:
                cap.release()
                cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
                
    def move(self, direction):
        threading.Thread(target=self._send_move, args=(direction,), daemon=True).start()

    def _send_move(self, direction):
        adb = "/home/carl/Android/Sdk/platform-tools/adb"
        if direction == "LEFT":
            cmd = f"{adb} -s emulator-5556 shell input swipe 800 600 200 600 300"
        elif direction == "RIGHT":
            cmd = f"{adb} -s emulator-5556 shell input swipe 200 600 800 600 300"
        elif direction == "UP":
            cmd = f"{adb} -s emulator-5556 shell input swipe 540 400 540 800 300"
        elif direction == "DOWN":
            cmd = f"{adb} -s emulator-5556 shell input swipe 540 800 540 400 300"
            
        try:
            subprocess.run(cmd.split(), check=True)
            self.status_var.set(f"🟢 Moveu {direction}")
        except Exception as e:
            self.status_var.set("🔴 Erro ADB")

    def on_close(self):
        self.running = False
        self.window.destroy()

import os
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
