from onvif import ONVIFCamera
cam = ONVIFCamera("192.168.0.2", 5000, "admin", "cnvasco54")
media = cam.create_media_service()
media.xaddr = "http://192.168.0.2:5000/onvif/media_service"
profiles = media.GetProfiles()
for p in profiles:
    print(p.token)
