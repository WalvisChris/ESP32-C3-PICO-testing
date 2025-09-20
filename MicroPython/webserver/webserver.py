import network
import socket
import machine

# WiFi-instellingen
SSID = "SSID"
PASSWORD = "PASSWORD"

# LED pin
led = machine.Pin(2, machine.Pin.OUT)

# Verbinden met WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Verbinden met WiFi...")
while not wlan.isconnected():
    pass
print("Verbonden! IP:", wlan.ifconfig()[0])

# HTML-bestand inladen
def load_html():
    with open("index.html", "r") as f:
        return f.read()

# Webserver starten
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Verbonden met:", addr)
    request = conn.recv(1024).decode()
    print("Request:", request)

    if "/?led=on" in request:
        led.value(1)
    if "/?led=off" in request:
        led.value(0)

    # HTML vullen met de status
    led_state = "ON" if led.value() == 1 else "OFF"
    response = load_html().replace("{{state}}", led_state)

    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()