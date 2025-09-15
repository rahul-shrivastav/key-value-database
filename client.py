import socket
from util.config import Config

def encode_command(*args):
    cmd_type = args[0].upper()
    match cmd_type:
        case "SET":
            cmd = "$set"
            if len(args) != 3:
                raise ValueError("SET command requires key and value") 
        case "GET":
            if len(args) != 2:
                raise ValueError("GET command requires a key")
            cmd = "$get"
        case "PING":
            if len(args) != 1:
                raise ValueError("PING command takes no arguments")
            cmd = "$ping"
        case "DEL":
            if len(args) != 2:
                raise ValueError("DEL command requires a key")
            cmd = "$del"
        case _:
            raise ValueError("Unsupported command")

    for arg in args[1:]:
        cmd += f"{'#'+arg}"
    cmd += '~'

    return cmd.encode()

def read_reply(sock):
    buf = b""
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            raise ConnectionError("Server closed connection")
        buf += chunk
        if b"~" in buf:
            break
    reply = buf.decode()
    if not reply.startswith('$'):
        raise ValueError(f"Invalid reply: {reply}")
    return reply[1:-1]

def main(): 
    with socket.create_connection((Config.host, Config.port)) as s:
      while True:
            try:
                line = input(">> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExited.")
                break

            if not line : continue
            
            if line.upper() in {"EXIT", "QUIT"}:
                print("Closing connection.")
                break

            parts = line.split()
            try:
                s.sendall(encode_command(*parts))
                print(read_reply(s))
            except Exception as e:
                print("Error:", e)
            

if __name__ == "__main__":
    main()
