import tkinter as tk
import subprocess
import threading

class FloatingPTZ:
    def __init__(self, window):
        self.window = window
        self.window.title("Controle (ADB)")
        self.window.attributes('-topmost', True)
        self.window.geometry("180x120")
        
        self.status_var = tk.StringVar(value="🟢 Pronto (Emulador)")
        tk.Label(window, textvariable=self.status_var, font=("Arial", 8)).pack(pady=2)
        
        btn_frame = tk.Frame(window)
        btn_frame.pack()
        
        tk.Button(btn_frame, text="⬆️", command=lambda: self.move("UP"), width=3).grid(row=0, column=1)
        tk.Button(btn_frame, text="⬅️", command=lambda: self.move("LEFT"), width=3).grid(row=1, column=0)
        tk.Button(btn_frame, text="➡️", command=lambda: self.move("RIGHT"), width=3).grid(row=1, column=2)
        tk.Button(btn_frame, text="⬇️", command=lambda: self.move("DOWN"), width=3).grid(row=2, column=1)
        
    def move(self, direction):
        threading.Thread(target=self._send_move, args=(direction,), daemon=True).start()

    def _send_move(self, direction):
        adb = "/home/carl/Android/Sdk/platform-tools/adb"
        # Deslizar no vídeo (y=600, x=540 é o centro aproximado)
        if direction == "LEFT":
            cmd = f"{adb} -s emulator-5556 shell input swipe 800 600 200 600 300"
        elif direction == "RIGHT":
            cmd = f"{adb} -s emulator-5556 shell input swipe 200 600 800 600 300"
        elif direction == "UP":
            # Para olhar para cima, geralmente desliza o dedo para baixo
            cmd = f"{adb} -s emulator-5556 shell input swipe 540 400 540 800 300"
        elif direction == "DOWN":
            cmd = f"{adb} -s emulator-5556 shell input swipe 540 800 540 400 300"
            
        try:
            subprocess.run(cmd.split(), check=True)
            self.status_var.set(f"Moveu {direction}")
        except Exception as e:
            self.status_var.set("Erro no Emulador")
            print("Erro ADB:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingPTZ(root)
    root.mainloop()
