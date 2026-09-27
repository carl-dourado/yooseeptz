from onvif import ONVIFCamera

try:
    cam = ONVIFCamera("192.168.0.2", 5000, "admin", "cnvasco54")
    ptz = cam.create_ptz_service()
    
    print("Methods available in PTZ:", dir(ptz))
    
    req = ptz.create_type('GetNodes')
    nodes = ptz.GetNodes()
    print("Nodes:", nodes)
    
except Exception as e:
    print("Error:", e)
