## Daemon:

Receive a dict from Clients and store them in redis along with the updated time.
Other apps who wants to use the data will need to fetch them from redis.


## Getting Started

### 1. Authentication Setup:

1. Generate certificates and key for server and client:
```
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt
```

**Note**: Common name for server must be your server hostname (ex: example.com)

2. Put server.crt and server.key in /src
3. Create a file name "client_certs.crt" and put all clients' certificate in there with the format:

```
-----BEGIN CERTIFICATE-----
client 1's certificate
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
client 2's certificate
-----END CERTIFICATE-----
```

### 2. Run the server

```
python src/main.py
```

The server is waiting for connections from Clients on port 1191.


### 3. Server API
This server only handle and store type **dictionary**.

In your client code:
```
data = {
    "key_1": "value_1",
    "key_2": "value_2",
}

client.send(pickle.dumps(data))
```

## Done criterias:

- Daemon must be able to handle authentication.
- Daemon must be able to receive dummy payload and store into Redis.
- Must be able to handle at least 100 payload/second.

## Requirements
- \>= Python 3.7.0
- asyncio

## Commands:
See all connected clients:\
lsof -i -n | grep python3
