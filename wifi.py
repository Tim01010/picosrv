# allows you to use your Pico W's wifi capabilities

import network
import utime

debug = False


def connect_with_secrets(secrets, static_ip=None) -> str:
    return connect(secrets.SSID, secrets.PASSWORD, static_ip)


def connect(name: str, password: str, static_ip=None) -> str:
    print("wifi.connect called")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if static_ip is not None:
        if debug:
            print("applying static ip")
        ifconfig = wlan.ifconfig()
        wlan.ifconfig((static_ip, ifconfig[1], ifconfig[2], ifconfig[3]))
    wlan.connect(name, password)

    if debug:
        print("waiting for connection")

    for i in range(15):
        if(debug):
            print("...")
        if(wlan.status() < 0 or wlan.status() >= 3):
            break
        utime.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError(f"connection failed with status {wlan.status()}.\ntry powering off your pico for ~10 seconds.")
    else:
        if debug:
            print("connected")
        return wlan.ifconfig()[0]