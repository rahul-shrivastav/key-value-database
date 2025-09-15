import time
import asyncio
import collections
from .parser import Parser

class Protocol(asyncio.Protocol):
    def __init__(self,memory ):
        self.response = collections.deque()
        self.parser = Parser()
        self.memory = memory
        self.transport = None 

        self.commands = {
            b"SET": self.setCommand,
            b"GET": self.getCommand,
            b"PING": self.pingCommand,
            b"DEL": self.deleteCommand,
        }
        self.buffer = b''

    def connection_made(self, transport: asyncio.transports.Transport):
        self.transport = transport

    def data_received(self, data: bytes):

        self.parser.addByteData(data)
        while True:
            extracted_command = self.parser.extract_command()
            if extracted_command:
                self.response.append(self.commands[extracted_command[0].upper()](*extracted_command[1:]))
                self.transport.write(self.response.popleft())
                self.response.clear()
            else:
                break

    def get(self, key, default=None):
        return self.memory.get(key, default)
    
    def set(self, key, value):
        self.memory[key] = value

    def setCommand(self, *args) -> bytes:
        key = args[0]
        value = args[1]
        self.set(key, value)
        return b"$OK~"

    def getCommand(self, key: bytes) -> bytes:
        value = self.get(key)
        if not value:
            return b"$Key not found~"
        if not isinstance(value, bytes):
            return b"-WRONGTYPE Operation against a key holding the wrong kind of value"
        return b"$" + value + b"~"

    def deleteCommand(self, key: bytes) -> bytes:
        value = self.memory.pop(key, None)
        if not value:
            return b"$Key not found.~"

        if not isinstance(value, bytes):
            return b"-WRONGTYPE Operation against a key holding the wrong kind of value"

        return b"$" + key + b" deleted with value " + value + b"~"

    def pingCommand(self,*args) -> bytes:
        return b"$PONG~"


 