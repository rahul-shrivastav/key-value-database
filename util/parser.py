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
