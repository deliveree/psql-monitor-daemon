## Daemon:

Receive figures from Clients and store them in redis along with the updated time.

Other apps who wants to use the data will need to fetch them from redis. Updated time is used by other app to check if the data is still valid. (No APIs are required at this point)

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

## Referemce
https://medium.com/@pgjones/an-asyncio-socket-tutorial-5e6f3308b8b0

https://www.electricmonk.nl/log/2018/06/02/ssl-tls-client-certificate-verification-with-python-v3-4-sslcontext/
