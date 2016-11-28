import socket


class HttpClient(object):
    def client(self, data):
        s = socket.socket()

        host = '172.16.2.1'
        port = 12345                # Reserve a port for your service.

        s.connect((host, port))
        s.sendall(data)
        resp = s.recv(1024)
        s.close                     # Close the socket when done
        return resp


class UdsServer(object):
    def server(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        s.bind('/var/run/nfp_socket')
        s.listen(5)

        while True:
            c, addr = s.accept()
            print 'Got connection from', addr
            data = c.recv(1024)
            if data:
                resp = HttpClient().client(data)
                c.send(resp)
            c.close()
UdsServer().server()
