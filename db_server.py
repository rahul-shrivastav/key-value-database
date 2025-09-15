import asyncio
from util.config import Config
from util.protocol import Protocol

async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda : Protocol({}), Config.host, Config.port)
    print("\n>> DB Serving on {}".format(server.sockets[0].getsockname()))
    async with server:
        await server.serve_forever()  

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(">> Server exited.")
