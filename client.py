import socket
from util.config import Config
from util.parser import encode_command, decode_response

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
                print(decode_response(s))
            except Exception as e:
                print("Error:", e)
            
if __name__ == "__main__":
    main()
