from onvif import ONVIFCamera
cam = ONVIFCamera("192.168.0.2", 5000, "admin", "cnvasco54")
for service in cam.xaddrs:
    print(service, cam.xaddrs[service])
