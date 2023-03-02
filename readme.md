# PicoHTTP
A simple library that allows hosting a HTTP Server on a Raspberry Pi Pico W

## Installation

Create 2 files on the pico.
1. A file called `wifi.py` with the content of [wifi.py on this repository](wifi.py) in it.
2. Repeat with [httpserver.py](httpserver.py).

## Usage

### Connecting to the wifi
To use PicoHTTP you must first connect to your wifi.

```py
import wifi
wifi.debug = True # Enable debug mode, this allows us to see what the library is currently doing

ip = wifi.connect("YOUR WIFI NAME", "YOUR WIFI PASSWORD") # Connect to the wifi with the wifi name and password, it will return an ip address

print(f"IP Address: {ip}") # Log the ip address
```

If you run this you should see the device connecting to the wifi and sending its IP Address.

### Creating a http server
Next, let's create a simple server:

1. Import all the neccessary tools
    ```py
    from httpserver import Request, response, run as run_server, send_text_file
    ```

2. Create a callback function
    ```py
    def callback(req: Request) -> str:
        return response("hello world!")
    ```
    This function will automatically be called once a request is received.

3. Run your server, make sure this is at the very end of the file. Code after it will not be executed.
    ```py
    run_server(callback)
    ```

    The code should look something like this once you're done:
    ```py
    import wifi
    from httpserver import Request, response, run as run_server, send_text_file

    wifi.debug = True

    ip = wifi.connect("YOUR WIFI NAME", "YOUR WIFI PASSWORD")

    print(f"IP Address: {ip}")

    def callback(req: Request) -> str:
        return response("hello world!")

    run_server(callback)
    ```
    If you run this code and open the IP address in your browser you should see "hello world!" from the pico.

#### The Request Object
The request object contains all the information the browser has sent to the pico:
+ `.method` is the [request method](https://developer.mozilla.org/docs/Web/HTTP/Methods), and will usually be `GET`

+ `.path` is the path, with `1.2.3.4/a/b` the path will be `/a/b`

+ `.parameters` are the parameters contained within the url as a dictionary

+ `.body` the request body. Only available with `POST` and `PUT` requests.

##### Example
When opening `http://1.2.3.4/hello%20world/start?abc=def&numbers=123` the request object will look something like this:

```yaml
path: "/hello world/start"
parameters: {
    abc: "def"
    numbers: "123" // Note that numbers will not be parsed automatically. be sure to convert them to an int() or float() first.
}
method: "GET" 
```

#### The Response String
Your callback function is supposed to return a http response string, not plain html code. The `response()` function is able to generate proper responses.

`response("<p>hello world</p>")` returns something similar to this:
```
HTTP/1.0 200 OK
Content-Type: text/html

<p>hello world</p>
```
You can also pass in a [status code](https://developer.mozilla.org/docs/Web/HTTP/Status), which defaults to `200` and a [content type](https://developer.mozilla.org/docs/Glossary/MIME_type) which defaults to `text/html`

```py
return response("<h1>404 Not Found!</h1><br>The requested page could not be found.<br>Try something else.", 404)
```

#### send_text_file
The `send_text_file` function allows you to easily send source code like HTML, JavaScript or CSS from a file.
```py
return send_text_file("test.html")
```
sends the content of `test.html` from the pico's storage.


### More Examples
You can view more examples in the [examples directory](/examples) of this repository.
