from onvif import ONVIFCamera
cam = ONVIFCamera("192.168.0.2", 5000, "admin", "cnvasco54")
media = cam.create_media_service()
ptz = cam.create_ptz_service()

# OVERRIDE THE BROKEN URL!
ptz.xaddr = "http://192.168.0.2:5000/onvif/ptz_service"
# Media is also probably wrong! Let's check media xaddr
print("Original Media URL:", media.xaddr)
media.xaddr = "http://192.168.0.2:5000/onvif/media_service"

profile = media.GetProfiles()[0]

try:
    req = ptz.create_type('ContinuousMove')
    req.ProfileToken = profile.token
    req.Velocity = {'PanTilt': {'x': 1.0, 'y': 0.0}}
    ptz.ContinuousMove(req)
    print("Moveu direita via URL corrigida!")
except Exception as e:
    print("Erro corrigido:", e)
