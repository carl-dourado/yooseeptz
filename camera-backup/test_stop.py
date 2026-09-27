from onvif import ONVIFCamera
cam = ONVIFCamera("192.168.0.2", 5000, "admin", "cnvasco54")
media = cam.create_media_service()
ptz = cam.create_ptz_service()
profile = media.GetProfiles()[0]

try:
    ptz.Stop({'ProfileToken': profile.token})
    print("Parou com sucesso!")
except Exception as e:
    print("Erro ao parar:", e)
