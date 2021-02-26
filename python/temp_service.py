#!/usr/bin/env python3


import http.server
import temp_reader
import threading
import time
import sys

HOST = "127.0.0.1"
PORT = 8500
DEVICE_NAME = "TempBureau"

temp_value = None
keep_looping = True


def read_temperature_loop():
    global temp_value

    r = temp_reader.TempReader(DEVICE_NAME)
    while True:
        temp_value = r.read_temperature()
        print("Read temp:", temp_value)
        if not keep_looping:
            break
        time.sleep(5)


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        if temp_value:
            self.wfile.write(("%.1f°C\n" % (temp_value)).encode("utf8"))


threading.Thread(target=read_temperature_loop).start()

try:
    with http.server.HTTPServer((HOST, PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
except Exception as x:
    print(x)
    keep_looping = False
    sys.exit(1)
