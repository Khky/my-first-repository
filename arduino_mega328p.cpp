#include <Ethernet.h>

// Arduino MAC address
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };  // Replace with your Arduino's MAC address

// Arduino IP address and port
IPAddress arduino_ip(192, 168, 1, 200);  // Replace with the desired IP address
unsigned int arduino_port = 8888;  // Replace with the desired port number

// Raspberry Pi IP address and port
IPAddress rpi_ip(192, 168, 1, 100);  // Replace with your Raspberry Pi's IP address
unsigned int rpi_port = 5005;  // Replace with the desired port number

EthernetUDP udp;

void setup() {
  Ethernet.begin(mac, arduino_ip);
  udp.begin(arduino_port);
}

void loop() {
  // Send a message to the Raspberry Pi
  udp.beginPacket(rpi_ip, rpi_port);
  udp.print("Hello from Arduino!");
  udp.endPacket();

  // Receive a response from the Raspberry Pi
  int packetSize = udp.parsePacket();
  if (packetSize) {
    char buffer[UDP_TX_PACKET_MAX_SIZE];
    int len = udp.read(buffer, UDP_TX_PACKET_MAX_SIZE);
    if (len > 0) {
      buffer[len] = '\0';
      Serial.print("Received response from Raspberry Pi: ");
      Serial.println(buffer);
    }
  }

  delay(1000);
}
