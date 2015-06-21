import time

import uinput

import socket
import sys

games = ['Mario', 'Contra']
game = games[1]

keysMapperMain = {
    "Contra": {
        "UpLeft": [uinput.KEY_A, uinput.KEY_W],
        "UpRight": [uinput.KEY_D, uinput.KEY_W],
        "DownLeft": [uinput.KEY_S, uinput.KEY_A],
        "DownRight": [uinput.KEY_S, uinput.KEY_D],

        "Up": [uinput.KEY_W],
        "Right": [uinput.KEY_D],
        "Down": [uinput.KEY_S],
        "Left": [uinput.KEY_A],

        "ADown": [uinput.KEY_J],
        "BDown": [uinput.KEY_K],

        "AUp": [uinput.KEY_J],
        "BUp": [uinput.KEY_K],


        "UpLeft2": [uinput.KEY_UP, uinput.KEY_LEFT],
        "UpRight2": [uinput.KEY_UP, uinput.KEY_RIGHT],
        "DownLeft2": [uinput.KEY_DOWN, uinput.KEY_LEFT],
        "DownRight2": [uinput.KEY_DOWN, uinput.KEY_RIGHT],

        "Up2": [uinput.KEY_UP],
        "Right2": [uinput.KEY_RIGHT],
        "Down2": [uinput.KEY_DOWN],
        "Left2": [uinput.KEY_LEFT],

        "ADown2": [uinput.KEY_KP1],
        "BDown2": [uinput.KEY_NUMERIC_2],

        "AUp2": [uinput.KEY_KP1],
        "BUp2": [uinput.KEY_NUMERIC_2],
        }
    }
keysMapper = None


from thread import *
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 9128 # Arbitrary non-privileged port

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
        uinput.KEY_K,
        uinput.KEY_H,
        uinput.KEY_F,
        uinput.KEY_KP1,
        uinput.KEY_NUMERIC_2,
        uinput.KEY_UP,
        uinput.KEY_DOWN,
        uinput.KEY_LEFT,
        uinput.KEY_RIGHT,
        )

# device = uinput.Device(uinput.KEY_NUMLOCK)
# device.emit_click(uinput.KEY_NUMLOCK)-

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
    device =  uinput.Device(events)
    keyspressed = []
    keyspressed2 = []
    

    #infinite loop so that function do not terminate and thread do not end.
    while True:
        #Receiving from client
        data_ = conn.recv(1024).strip()

        for data in data_.split('-'):
            print repr(data)
            # print data_, "====", data
            if data in ["AUp", "BUp", "BDown", "ADown"]:
                if "Down" in data:
                    device.emit(keysMapper[data][0], 1)
                else:
                    device.emit(keysMapper[data][0], 0)

            if data in ["AUp2", "BUp2", "BDown2", "ADown2"]:
                if "Down" in data:
                    device.emit(keysMapper[data][0], 1)
                else:
                    device.emit(keysMapper[data][0], 0)    

            else:
                print data
                if len(keyspressed) > 0:
                            for key in keyspressed:
                                    device.emit(key, 0)
                            keyspressed = []

                if len(keyspressed2) > 0:
                            for key in keyspressed2:
                                    device.emit(key, 0)
                            keyspressed2 = []


                if data in keysMapper:
                            for key in keysMapper[data]:
                                    device.emit(key, 1)
                                    if "2" in data:
                                        keyspressed2.append(key)
                                    else:
                                        keyspressed.append(key)

    #came out of loop
    conn.close()

def main():
    # for i in range(20):
    #     # syn=False to emit an "atomic" (5, 5) event.
    #     device.emit(uinput.REL_X, 5, syn=False)
    #     device.emit(uinput.REL_Y, 5)
    #     # Just for demonstration purposes: shows the motion. In real
    #     # application, this is of course unnecessary.
    #     time.sleep(0.01)

    # time.sleep(2)
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

if len(sys.argv) > 1:
    _ = sys.argv[1].strip()
    if _ not in games: raise Exception("no game")
    game = _
    keysMapper = keysMapperMain[game]

main()