## Daemon:

This app uses TCP Socket to receive dicts from multiple Clients and store them in redis:
- Authentication by SSL
- Port: 1191. It can be changed in **conf/daemon.conf**


## Getting Started

### 1. Authentication Setup:

1. Generate certificates and key for server and client:
```
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt
```

**Note**: Common name for server you declare when generating the certificate must be your server hostname (ex: example.com).

2. Put **server.crt** and **server.key** in /src
3. Create a file name **client_certs.crt** and put all clients' certificate in there with the format:

```
-----BEGIN CERTIFICATE-----
client 1's certificate
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
client 2's certificate
-----END CERTIFICATE-----
```

### 2. Run the server
In **src/**:

```
python main.py
```

The server is waiting for connections from Clients on port 1191.


### 3. Client Side
This server only handles and stores type a **dict** or a **simple nested dict**.

The data must be processed by **json.dumps()** and **encode()** before sent.

In your client's code:
```
data = {
    "key_1": "value_1",
    "key_2": "value_2",
}

nested_dic = {
    "key_1": {
        "field_1": "value",
        "field_2": "value",
    }
}

client.send(json.dumps(data).encode())
```

## Requirements
- \>= Python 3.7.0
- asyncio

## Limit
The tested upper limit of load handling for the server is 100 payloads for 0.9s:
- All payload is sent by a Client.
- Minimum interval between payload is 0.008

## Development
To run test:
1. Make sure test server's credentials (server.crt, server.key, client_certs.crt) are in **test/creds/**

    Make sure common name for server when creating certicate is **localhost**

2. Make sure you have the following files in **test/creds**:
- Credentials for allowed client: **client.crt** and **client.key**
- Credentials for unallowed client: **unallowed_client.crt** and **unallowed_client.key**


3. Run tests. In **test/**:
```
pytest --disable-warnings
```

## To Do:
- Use logging instead of print
