import selectors
import socket
import time
import types
import DangerLevel as dl

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024

speed = 0
situation = 0
start = time.time()
seconds = 0
result = 0.0
dataInn = ""


def startTime(val):
    global start
    global seconds
    global situation
    valueChanged = situation != val
    if valueChanged:
        start = time.time()
        situation = val
        seconds = 0
    else:
        stop = time.time()
        seconds = stop - start


def resultToByte(result):
    resultInBytes = str(result).encode('utf-8')
    return resultInBytes


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr, sock)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        try:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb = recv_data
                data.outb = data.outb.decode('utf-8')
            else:
                print('closing connection to', data.addr)
                sel.unregister(sock)
                sock.close()
        except Exception as e:
            print(e)
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        try:
            if data.outb:
                global situation
                global speed
                global dataInn
                global seconds
                dataInn = str(data.outb)
                if dataInn.startswith("CNN"):
                    dataInn = dataInn[3]
                    startTime(int(dataInn))
                else:
                    speed = int(dataInn)
                seconds = round(seconds)
                print(speed, seconds, situation)
                result = dl.Chief_Danger_Acquisition_Officer(situation, seconds, speed)
                result = round(result, 1)
                sock.send(resultToByte(result))
                print("Danger level: ", result)
        except Exception as e:
            print(e)
        time.sleep(0.5)


sel = selectors.DefaultSelector()
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((TCP_IP, TCP_PORT))
lsock.listen()
print('listening on', (TCP_IP, TCP_PORT))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)
