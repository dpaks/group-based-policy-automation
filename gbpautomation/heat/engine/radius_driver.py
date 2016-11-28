import socket


class RadiusDriver():
    def __init__(self):
        pass

    def configure_radius(self, data):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        s.connect('/var/run/nfp_socket')
        s.sendall(data)
        print s.recv(1024)
        s.close
