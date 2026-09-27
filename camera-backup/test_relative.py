from onvif import ONVIFCamera
cam = ONVIFCamera("192.168.0.2", 5000, "admin", "cnvasco54")
media = cam.create_media_service()
ptz = cam.create_ptz_service()
profile = media.GetProfiles()[0]

try:
    req = ptz.create_type('RelativeMove')
    req.ProfileToken = profile.token
    req.Translation = {'PanTilt': {'x': 0.1, 'y': 0.0}}
    ptz.RelativeMove(req)
    print("Moveu relativo direita!")
except Exception as e:
    print("Erro mover relativo:", e)
