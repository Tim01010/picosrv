import wifi
from httpserver import Request, response, run as run_server, send_text_file, redirect
import json
import random

def random_string():
    chars = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    txt = ""
    for i in range(8):
        txt += random.choice(chars)

    return txt

wifi.debug = True

ip = wifi.connect("YOUR WIFI NAME", "YOUR WIFI PASSWORD")
print(f"running on ip {ip}")

urls = {}
try:
    with open("shortener_urls.json", "r") as f:
        urls = json.load(f)
except:
    pass

def callback(req: Request) -> str:
    if(req.path == "/"):
        return send_text_file("shortener.html")
    
    elif(req.path == "/submit"):
        if("url" not in req.parameters or len(req.parameters["url"]) > 500):
            return response("<h1>invalid request</h1>", 400)
        
        name = random_string()
        
        urls["/"+name] = req.parameters["url"]

        with open("shortener_urls.json", "w") as f:
            json.dump(urls, f)

        url = f"http://{ip}/{name}"

        return response(f"Shortened URL: <a href='{url}'>{url}</a><br><a href='/'><button>Shorten another one</button></a>")
    elif(req.path in urls):
        return redirect(urls[req.path])



    return response("<h1>not found</h1><br>see: <a href='/'>URL Shortener</a>", 404)

run_server(callback)