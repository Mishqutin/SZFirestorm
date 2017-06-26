# For use with sockets! They're essential.

class sNet:
    def send(s, data):
        """Data is converted to bytes and send to socket s."""
        s.send(str(data).encode())
    def recv(s, bytes=4096):
        """Receives string from socket s."""
        data = s.recv(bytes)
        return str(data)[2:-1]