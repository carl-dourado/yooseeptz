from onvif import ONVIFCamera
import sys

print("Conectando...", flush=True)
try:
    cam = ONVIFCamera("192.168.0.2", 5000, "admin", "cnvasco54")
    media = cam.create_media_service()
    ptz = cam.create_ptz_service()
    media_profile = media.GetProfiles()[0]
    print("Sucesso! Token do profile:", media_profile.token, flush=True)
except Exception as e:
    print("Erro ONVIF:", e, flush=True)
