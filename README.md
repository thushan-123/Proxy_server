# SOCKS5 Proxy Server

## Run the Proxy Server

```bash
./run.sh
```

When you run this command, you should see:

```
Proxy SERVER Listening on Port 1080
```

---

## Test with a Client (cURL)

Use the `curl` command with the SOCKS5 proxy option:

```bash
curl -x socks5://127.0.0.1:1080 http://httpbin.org/ip
```

### Example Output

```
thush@thushans-MacBook-Air proxy_server % ./run.sh

Proxy SERVER Listening on Port 1080
Client Accept Connection From 127.0.0.1 - 55833

Received request via SOCKS5:

curl -x socks5://127.0.0.1:1080 http://httpbin.org/ip
```

**Response:**

```json
{
  "origin": "175.157.142.225"
}
```

---

## Notes
- The proxy runs on **port 1080** by default.
- You can test with any HTTP/HTTPS destination using `curl -x socks5://127.0.0.1:1080 <URL>`.
