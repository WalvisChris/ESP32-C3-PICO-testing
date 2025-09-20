import network
import socket
import time

SSID = "SSID"
PASSWORD = "PASSWORD"

# Wi-Fi verbinden
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Verbinden met Wi-Fi...")
while not wlan.isconnected():
    time.sleep(1)

ip = wlan.ifconfig()[0]
print("Verbonden! IP:", ip)

# Webserver starten
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Luisterend op', addr)

# HTML bestand inlezen
with open('cube.html', 'r') as f:
    html = f.read()

while True:
    conn, addr = s.accept()
    print('Nieuwe verbinding van', addr)
    request = conn.recv(1024)  # HTTP request lezen

    # Stuur HTTP headers
    conn.send(b"HTTP/1.1 200 OK\r\n")
    conn.send(b"Content-Type: text/html\r\n")
    conn.send(b"Connection: close\r\n\r\n")

    # Stuur HTML in stukjes
    for i in range(0, len(html), 512):
        conn.send(html[i:i+512].encode('utf-8'))

    conn.close()