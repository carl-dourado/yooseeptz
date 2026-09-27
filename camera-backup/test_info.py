from onvif import ONVIFCamera
cam = ONVIFCamera("192.168.0.2", 5000, "admin", "cnvasco54")
print("Info:", cam.devicemgmt.GetDeviceInformation())
