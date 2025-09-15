class Parser:
    def __init__(self):
        self.buffer = b''

    def addByteData(self, data: bytes):
        self.buffer += data

    def extract_command(self):

        if not self.buffer.startswith(b"$"):
            dollar = self.buffer.find(b"$")
            if dollar == -1:
                self.buffer = b''
                return []
            self.buffer = self.buffer[dollar:]

        if self.buffer.upper()[1:5] == b"PING":
            dash_pos = self.buffer.find(b"~")
            self.buffer = self.buffer[dash_pos+1:]

            return [b"PING",b'']
        
        if len(self.buffer) < 4 : return []

        idx = 5
        cmd_type = self.buffer[1:4]     
        cmd = [cmd_type,]

        if b"~" not in self.buffer[idx:] : return []

        hash_pos = self.buffer.find(b"#")
        dash_pos = self.buffer.find(b"~")
        cmd.extend(self.buffer[hash_pos+1:dash_pos].split(b"#"))

        self.buffer = self.buffer[dash_pos+1:]

        return cmd

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

def decode_response(sock):
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