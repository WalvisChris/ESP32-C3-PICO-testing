import network
import socket

# Wi-Fi verbinden
SSID = "SSID"
PASSWORD = "PASSWORD"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    pass

print("Connected! IP:", wlan.ifconfig()[0])

# Webserver starten
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

# Bestand inlezen
with open('snake.html', 'r') as f:
    html = f.read()

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    cl.send(b'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(html)
    cl.close()