import socket

debug = False

# HTTP/1.0 methods
ALLOWED_METHODS = ("GET", "POST", "HEAD")

class Request:
    def __init__(self, raw: str):
        lines = raw.splitlines()
        first_line = lines[0].split(" ")
        self.method = first_line[0]
        if self.method not in ALLOWED_METHODS:
            raise Exception(f"method {self.method} not allowed")
        self.path = "" 
        self.parameters = {}


        i = -1
        is_params = False
        is_key = False

        key = ""
        value = ""
        end = len(first_line[1])
        skip = 0
        for c in first_line[1]:
            i += 1
            if skip > 0:
                skip -= 1
                continue
            
            if c == "?":
                is_params = True
                is_key = True
                continue

            char = c
            if c == "%" and i < end - 2:
                try:
                    char = chr(int(first_line[1][i+1:i+3], 16))
                    skip = 2
                except Exception as e:
                    if debug:
                        print("error parsing url-encoded string", e)
                    pass
            
            if is_params:
                if is_key:
                    if char == "=":
                        is_key = False
                        continue

                    key += char
                else:
                    if (char == "&" or i == end - 1) and key != "":
                        is_key = True
                        if i == end - 1:
                            value += char
                        self.parameters[key] = value
                        key = ""
                        value = ""
                        continue
                    value += char

            else:
                self.path += char
            


        self.headers = {}

        i = -1
        end = len(lines)
        for line in lines:
            i += 1
            if(i == 0): continue
            if(self.method == "POST" or self.method == "PUT") and len(line) == 0 and i < end - 1:
                self.body = "\n".join(lines[(i + 1):])
                break


            key = ""
            value = ""
            is_value = 0
            for char in line:
                if char == ":" and is_value == 0:
                    is_value = 1
                    continue
                if char == " " and is_value == 1:
                    is_value = 2
                    continue

                if is_value == 0:
                    key += char.lower()
                elif is_value == 2:
                    value += char

            if len(key) > 0:
                self.headers[key] = value

        
                

def run(callback, port=80):
    if debug:
        print("configuring server")
    addr = socket.getaddrinfo("0.0.0.0", port)[0][-1]
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(1)

    if debug:
        print("waiting for connections")
    while True:
        cl = None
        try:
            cl, addr = sock.accept()
            raw = cl.recv(1024).decode()

            req = Request(raw)

            cl.send(callback(req))
            cl.close()
        except Exception as error:
            print(error)
            if cl != None:
                cl.close()


def response(html: str, status_code: int = 200, content_type: str = "text/html") -> str:
    return f"HTTP/1.0 {status_code} OK\r\nContent-Type: {content_type}\r\n\r\n{html}"


def redirect(url: str, status_code = 302) -> str:
    return f"HTTP/1.0 {status_code} Redirect\r\nLocation: {url}\r\n\r\n"


mimetypes = {
    "html": "text/html",
    "css": "text/css",
    "js": "application/javascript",
    "json": "application/json"
}

"""
[Errno 2] ENOENT most likely means that the file does not exist.
"""
def send_text_file(path: str):
    type = path.split(".")[-1].lower()
    mimetype = mimetypes[type] if type in mimetypes else "text/plain" 

    with open(path, "r") as f:
        return response(f.read(), 200, mimetype)