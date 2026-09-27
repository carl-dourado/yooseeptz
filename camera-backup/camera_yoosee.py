import cv2
import tkinter as tk
from PIL import Image, ImageTk
from onvif import ONVIFCamera
import threading

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        # --- CONFIGURACOES DA CAMERA ---
        self.ip = "192.168.0.2"  # COLOQUE O IP DA SUA CAMERA AQUI
        self.port = 5000           # PORTA DO ONVIF (Tente 5000 ou 8899)
        self.user = "admin"        # USUARIO PADRAO
        self.password = "cnvasco54"      # SENHA DO NVR/ONVIF DEFINIDA NO APP
        self.rtsp_url = f"rtsp://{self.user}:{self.password}@{self.ip}:554/onvif1"
        
        # --- CONEXAO ONVIF ---
        try:
            self.cam = ONVIFCamera(self.ip, self.port, self.user, self.password, wsdl_dir='/home/carl/.local/lib/python3.11/site-packages/wsdl')
            self.media = self.cam.create_media_service()
            self.ptz = self.cam.create_ptz_service()
            self.media_profile = self.media.GetProfiles()[0]
            print("Conectado ao ONVIF com sucesso!")
        except Exception as e:
            print("Erro ao conectar no ONVIF (verifique IP, senha e porta):", e)
            self.ptz = None
            
        # --- INTERFACE ---
        self.video_label = tk.Label(window)
        self.video_label.pack()
        
        # Botões de movimento
        btn_frame = tk.Frame(window)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="⬅️ Esquerda", command=lambda: self.move(-1, 0)).pack(side=tk.LEFT, padx=5, expand=True)
        tk.Button(btn_frame, text="⬆️ Cima", command=lambda: self.move(0, 1)).pack(side=tk.LEFT, padx=5, expand=True)
        tk.Button(btn_frame, text="⬇️ Baixo", command=lambda: self.move(0, -1)).pack(side=tk.LEFT, padx=5, expand=True)
        tk.Button(btn_frame, text="➡️ Direita", command=lambda: self.move(1, 0)).pack(side=tk.LEFT, padx=5, expand=True)
        tk.Button(btn_frame, text="⏹️ Parar", command=self.stop, bg="red", fg="white").pack(side=tk.LEFT, padx=5, expand=True)

        # Inicia captura de vídeo
        print(f"Tentando abrir RTSP: {self.rtsp_url}")
        self.cap = cv2.VideoCapture(self.rtsp_url)
        
        self.update_frame()
        self.window.mainloop()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (800, 600))
            img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.video_label.imgtk = img
            self.video_label.configure(image=img)
        self.window.after(30, self.update_frame)
        
    def move(self, x, y):
        if not self.ptz: 
            print("ONVIF não conectado!")
            return
            
        try:
            request = self.ptz.create_type('ContinuousMove')
            request.ProfileToken = self.media_profile.token
            request.Velocity = {
                'PanTilt': {'x': x, 'y': y}
            }
            self.ptz.ContinuousMove(request)
        except Exception as e:
            print("Erro ao mover:", e)

    def stop(self):
        if not self.ptz: return
        try:
            self.ptz.Stop({'ProfileToken': self.media_profile.token})
        except Exception as e:
            print("Erro ao parar:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root, "Câmera Yoosee - RTSP + Controle PTZ")
