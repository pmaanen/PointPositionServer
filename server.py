import numpy as np
import matplotlib.pyplot as plt
import socket
from threading import Thread,Event
from collections import deque
from time import sleep


class Draggable:
    def __init__(self,point,position):
        self.point = point
        self.press = None
        self.q=position
        self.update_pos()

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.point.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.point.axes: return

        contains, attrd = self.point.contains(event)
        if not contains: return

        xdata,ydata=self.point.get_data()
        x=xdata[0]
        y=ydata[0]
        #x0, y0 = self.point.xy
        self.press = x, y, event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the point if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.point.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.point.set_data([x0+dx],[y0+dy])
        self.point.figure.canvas.draw()
        self.update_pos()

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.point.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.point.figure.canvas.mpl_disconnect(self.cidpress)
        self.point.figure.canvas.mpl_disconnect(self.cidrelease)
        self.point.figure.canvas.mpl_disconnect(self.cidmotion)

    def update_pos(self):
        x,y=self.point.get_data()
        self.q.append((int(x[0]),int(y[0])))

class Server:
    def __init__(self,q,stop_event):
        self.stop_event=stop_event
        self.pos=(0,0)
        self.q=q
        self.s = socket.socket()         # Create a socket object
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setblocking(0)
        self.s.settimeout(10)
        host = socket.gethostname() # Get local machine name
        port = 5551
        try:
            self.s.bind(('',port))
        except Exception as e:
            print "Error: " + str(e)
            #self.s.shutdown()
            raise

    def sendpos(self):
        self.s.listen(5)
        print "Waiting for connections..."
        c, addr = self.s.accept()     # Establish connection with client.
        print 'Got connection from', addr
        while True:
            sleep(1)
            try:
                self.pos=self.q.pop()
                c.send(str(self.pos)+"\n")
            except IndexError:
                c.send(str(self.pos)+"\n")
            if self.stop_event.is_set():
                c.send("Closing Connection...\n")
                print "Closing Connection..."
                c.close()
                break
        return

def guiThread(stop_event,position):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    points = ax.plot(1,500,'bo')
    ax.set_xlim(0,20)
    ax.set_ylim(0,2000)
    ax.set_xlabel("#")
    ax.set_ylabel("rate [a.u.]")
    for point in points:
        dr = Draggable(point,position)
        dr.connect()
    plt.show()
    stop_event.set()


def networkThread(stop_event,position):
    try:
        r=Server(position,stop_event)
        while not stop_event.is_set():
            r.sendpos()
    except Exception as e:
        print str(e)
        return

def main():
    stop_event=Event()
    q=deque(maxlen=1)
    thread1 = Thread(target=guiThread,args=(stop_event,q))
    thread2 = Thread(target=networkThread,args=(stop_event,q))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


if __name__=="__main__":
    main()
