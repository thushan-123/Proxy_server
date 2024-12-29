# Run The Proxy Server

cmd :   ./run.sh

thush@Mac Proxy_server % ./run.sh

after running this cmd shows

Proxy SERVER Listening on Port <PORT_NUMBER>

# Http Client 

curl --proxy "<PROXY_SERVER_URL>" "<DESTINATION_SERVER_URL>"

run this command terminal shows 

Proxy SERVER Listening on Port 8080
Client Accept Connection From 127.0.0.1 - 55833

# Example

thush@Mac Proxy_server % ./run.sh

Proxy SERVER Listening on Port 8080

Client Accept Connection From 127.0.0.1 - 55833

Recived request:

GET http://httpbin.org/ip HTTP/1.1

Host: httpbin.org

User-Agent: curl/8.7.1

Accept: */*

Proxy-Connection: Keep-Alive

Recived Response

HTTP/1.1 200 OK

Date: Sun, 29 Dec 2024 13:02:14 GM

Content-Type: application/json

Content-Length: 33

Connection: keep-alive

Server: gunicorn/19.9.0

Access-Control-Allow-Origin: *

Access-Control-Allow-Credentials: true


{
  "origin": "175.157.141.19"
}
