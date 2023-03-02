import wifi
from httpserver import Request, response, run as run_server, send_text_file
from machine import Pin
wifi.debug = True

ip = wifi.connect("YOUR WIFI NAME", "YOUR WIFI PASSWORD")
print(f"running on ip {ip}")


led = Pin("LED", Pin.OUT)

def callback(req: Request) -> str:
    if req.path == "/led":
        return send_text_file("led.html")
    if req.path == "/led_action":
        if "action" in req.parameters:
            action = req.parameters["action"]

            if action == "toggle":
                led.toggle()
            elif action == "on":
                led.on()
            elif action == "off":
                led.off()

            return response("", 200, "text/plain")


    return response("<h1>not found</h1><br>see: <a href='/led'>LED Controls</a>", 404)

run_server(callback)
