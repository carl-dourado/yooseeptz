import tkinter as tk
import subprocess
import time

root = tk.Tk()
root.geometry("640x480")

frame = tk.Frame(root, width=640, height=360, bg="black")
frame.pack()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Esquerda").pack(side=tk.LEFT)
tk.Button(btn_frame, text="Direita").pack(side=tk.LEFT)

root.update()
wid = frame.winfo_id()

# Start mpv
cmd = f"mpv --wid={wid} --profile=low-latency --rtsp-transport=udp --no-osc rtsp://admin:cnvasco54@192.168.0.2:554/onvif1"
mpv_process = subprocess.Popen(cmd.split())

def on_close():
    mpv_process.terminate()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
