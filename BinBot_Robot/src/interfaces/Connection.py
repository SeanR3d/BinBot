# Author: Sean DiGirolamo
# Date: 10/30/2019
import socket


JAVA_INT_BYTES = 1
ACK = b'\x01'
ACK_BYTES = 1
ENDIAN = "big"


class Connection:
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setblocking(True)
        self.__sock.connect((ip, port))

    def send(self, msg):
        self.__sock.sendall(str.encode(msg + "\n"))
        self.__receive_ack()

    def receive(self):
        length = self.__receive_length()
        retval = self.__sock.recv(length).decode("utf-8")
        # self.__send_ack()
        return retval

    def close(self):
        self.__sock.close()

    def __receive_length(self):
        retval = int.from_bytes(self.__sock.recv(JAVA_INT_BYTES), ENDIAN)
        return retval

    def __send_ack(self):
        self.__sock.sendall(ACK)
        self.__sock.sendall(str.encode("\n"))

    def __receive_ack(self):
        data = self.__sock.recv(ACK_BYTES)