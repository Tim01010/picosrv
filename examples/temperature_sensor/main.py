import wifi
from httpserver import Request, response, run as run_server, send_text_file
from machine import ADC
wifi.debug = True
sensor = ADC(4)

ip = wifi.connect("YOUR WIFI NAME", "YOUR WIFI PASSWORD")
print(f"running on ip {ip}")


def callback(req: Request) -> str:
    if req.path == "/sensor":
        voltage = sensor.read_u16() * (3.3 / (65535))
        temp = 27 - (voltage - 0.706)/0.00172
        return response(f"Temparature: {temp}&deg;C<script>setTimeout(()=>location.reload(),2000);</script>")

    return response("<h1>not found</h1><br>see: <a href='/sensor'>Temperature Sensor</a>", 404)

run_server(callback)
