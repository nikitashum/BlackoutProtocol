import selectors
import socket
import time
import types
import DangerLevel as dl

# socket settings
TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024

# creating variables
speed = 0
situation = 0
start = time.time()
seconds = 0
result = 0.0
dataInn = ""


# starts time counter if the situation has changed
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


# encodes result to bytes so it can be sent over tcp
def resultToByte(result):
    resultInBytes = str(result).encode('utf-8')
    return resultInBytes


# socket connections listener, accepts new connections
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr, sock)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


# this is main method, it receives data from the connection, processes it and replies with result
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    # read socket
    if mask & selectors.EVENT_READ:
        try:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                # if data received decode from bytes to string
                data.outb = recv_data
                data.outb = data.outb.decode('utf-8')
            else:
                # close connection to socket if no data received
                print('closing connection to', data.addr)
                sel.unregister(sock)
                sock.close()
        except Exception as e:
            # close socket connection if failed to receive data
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
                # if data starts with CNN process it as situation
                if dataInn.startswith("CNN"):
                    dataInn = dataInn[3]
                    startTime(int(dataInn))
                # else process it as speed
                else:
                    speed = int(dataInn)
                # round seconds to integers and send it to fuzzy logic where it will calculate danger level
                seconds = round(seconds)
                result = dl.Chief_Danger_Acquisition_Officer(situation, seconds, speed)
                # send the result back to simulator
                sock.send(resultToByte(result))
        except Exception as e:
            print(e)
            # half second pause
        time.sleep(0.5)


# initialize selector
sel = selectors.DefaultSelector()
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((TCP_IP, TCP_PORT))
# listen to socket connections
lsock.listen()
print('listening on', (TCP_IP, TCP_PORT))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

# main loop
while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            # accept new connection
            accept_wrapper(key.fileobj)
        else:
            # service connection
            service_connection(key, mask)
