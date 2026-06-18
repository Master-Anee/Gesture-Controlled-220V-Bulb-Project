#include <WiFi.h>

// Replace with your network credentials
const char* ssid = "ANEES";
const char* password = "AMAN1234";

WiFiServer server(80);

int ledPin = 2; // GPIO pin connected to LED

void setup() {
  Serial.begin(115200);

  // Initialize the LED pin as an output
  pinMode(ledPin, OUTPUT);

  // Connect to Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
  
  Serial.println("Connected to Wi-Fi");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());  // Print the IP address to the Serial Monitor
  
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  
  if (client) {
    String request = client.readStringUntil('\r');
    client.flush();
    
    // Check if the request is to turn the LED on
    if (request.indexOf("/LED=ON") != -1) {
      digitalWrite(ledPin, HIGH);  // Turn LED on
    }

    // Check if the request is to turn the LED off
    if (request.indexOf("/LED=OFF") != -1) {
      digitalWrite(ledPin, LOW);   // Turn LED off
    }

    // Send a response back to the client
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println("");
    client.println("<!DOCTYPE HTML>");
    client.println("<html>");
    client.println("LED is now " + String(digitalRead(ledPin) ? "ON" : "OFF"));
    client.println("</html>");
    
    delay(1);
    client.stop();
  }
}
