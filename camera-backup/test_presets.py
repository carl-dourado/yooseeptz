from onvif import ONVIFCamera
cam = ONVIFCamera("192.168.0.2", 5000, "admin", "cnvasco54")
media = cam.create_media_service()
ptz = cam.create_ptz_service()
profile = media.GetProfiles()[0]
try:
    req = ptz.create_type('GetPresets')
    req.ProfileToken = profile.token
    presets = ptz.GetPresets(req)
    print("Presets:", presets)
except Exception as e:
    print("Erro presets:", e)
