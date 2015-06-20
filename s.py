import time

import uinput

import socket
import sys

from thread import *
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string

    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data = conn.recv(1024)
        print data
        reply = 'OK...' + data
        if not data:
            break

        conn.sendall(reply)


    #came out of loop
    conn.close()

def main():
    events = (
        uinput.REL_X,
        uinput.REL_Y,
        uinput.BTN_LEFT,
        uinput.BTN_RIGHT,
        uinput.KEY_W,
        uinput.KEY_A,
        uinput.KEY_S,
        uinput.KEY_D,
        uinput.KEY_J,
        uinput.KEY_K
        )

    device =  uinput.Device(events)
    # for i in range(20):
    #     # syn=False to emit an "atomic" (5, 5) event.
    #     device.emit(uinput.REL_X, 5, syn=False)
    #     device.emit(uinput.REL_Y, 5)
    #     # Just for demonstration purposes: shows the motion. In real
    #     # application, this is of course unnecessary.
    #     time.sleep(0.01)

    time.sleep(2)
    # device.emit_click(uinput.KEY_H)
    # device.emit_click(uinput.KEY_E)
    # device.emit_click(uinput.KEY_L)
    # device.emit_click(uinput.KEY_L)
    # device.emit_click(uinput.KEY_O)

    # device.emit(uinput.KEY_D,1)
    # time.sleep(5)
    # device.emit(uinput.KEY_D,0)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'

    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    print 'Socket bind complete'

    #Start listening on socket
    s.listen(10)
    print 'Socket now listening'

    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        start_new_thread(clientthread ,(conn,))

    s.close()
if __name__ == "__main__":
    main()