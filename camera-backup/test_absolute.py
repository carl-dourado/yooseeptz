from onvif import ONVIFCamera
cam = ONVIFCamera("192.168.0.2", 5000, "admin", "cnvasco54")
media = cam.create_media_service()
ptz = cam.create_ptz_service()
profile = media.GetProfiles()[0]

try:
    req = ptz.create_type('AbsoluteMove')
    req.ProfileToken = profile.token
    req.Position = {'PanTilt': {'x': 0.5, 'y': 0.5}}
    ptz.AbsoluteMove(req)
    print("Moveu absoluto!")
except Exception as e:
    print("Erro absoluto:", e)
