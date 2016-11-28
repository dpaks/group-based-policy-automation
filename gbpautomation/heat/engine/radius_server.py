import socket
from subprocess import call


class RadiusAgent(object):
    def __init__(self):
        pass

    @staticmethod
    def configure_radius(data):
        cmd = ("sed -e 's/\(server = \).*/\1\"poda\"/' -e 's/\(password = "
               "\).*/\1\"poda\"/' -e 's/\(login = \).*/\1\"poda\"/' "
               "-e 's/\(database = \).*/\1\"poda\"/' /etc/freeradius/sql.conf")
        call(cmd.split())
        cmd = ("service freeradius restart")
        call(cmd.split())
s = socket.socket()
host = socket.gethostname()
port = 12345

s.bind((host, port))

s.listen(5)
while True:
    c, addr = s.accept()
    data = c.recv(1024)
    print 'Got data: %s' % data
    c.send('Thank you for connecting to RADIUS. Data: %s' % data)
    RadiusAgent.configure_radius(data)
    c.close()
