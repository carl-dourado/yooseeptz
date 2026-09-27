from onvif import ONVIFCamera
cam = ONVIFCamera("192.168.0.2", 5000, "admin", "cnvasco54")
media = cam.create_media_service()
ptz = cam.create_ptz_service()
ptz.xaddr = "http://192.168.0.2:5000/onvif/ptz_service"
media.xaddr = "http://192.168.0.2:5000/onvif/media_service"

profiles = media.GetProfiles()

try:
    req = ptz.create_type('ContinuousMove')
    req.ProfileToken = "IPCProfilesToken1"
    req.Velocity = {'PanTilt': {'x': 1.0, 'y': 0.0}}
    ptz.ContinuousMove(req)
    print("Moveu direita no token 1!")
except Exception as e:
    print("Erro:", e)
