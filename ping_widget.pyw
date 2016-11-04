from tkinter import *
import subprocess
import time
import threading

def ping_pc(ip, encodage="cp850"):
    """envoie un ping à l'ordinateur d'adresse ip, et retourne la réponse
       sous forme d'une liste de lignes unicode
    """
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    commande = ["ping","-n","1", ip]
    try:
        out, _ = subprocess.Popen(commande, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT,
                                  startupinfo=si).communicate()
    except (ValueError, OSError) as err:
        return ("Erreur: %s" % (err.args[0],)).decode(encodage)
    reponse = out.decode(encodage)
    reponse = reponse.splitlines()
    reponse = reponse[2][43:49].split(' ')[0].replace('=','')
    time.sleep(0.5)
    try:
        reponse = int(reponse)
        print('ping:',reponse)
        return reponse
    except:
        print('Aucune réponse ping')
        return 999

def justify(text):
    """ Changes an hexadecimal '5' to '05' to satisfy #color syntax"""
    if len(text) == 2:
        return text
    else:
        text='0'+text
        return text

def pingtohex(ping):
    """ Returns ping to hexadecimal color from green to red """
    if ping < 50:
        couleur='#00ff00'
    elif ping > 150:
        couleur='#ff0000'
    else:
        if ping<100:
            rouge=justify(hex((ping-50)*5).replace('0x',''))
            vert='ff'
            couleur='#'+rouge+vert+'00'
        else:
            rouge='ff'
            # 150->0 100->255
            vert=justify(hex((ping-100)*-5+255).replace('0x',''))
            couleur='#'+rouge+vert+'00'
    print('couleur:',couleur)
    return couleur


class ThreadPingLatency(threading.Thread):
    """Objet mettant à jour la variable ping sans interruption"""
    def __init__(self):
        threading.Thread.__init__(self)
        self.ping = 0
        self.state = True
    def stop(self):
        self.state = False
    def run(self):
        while self.state==True:
            self.ping = ping_pc('google.fr')
            
    
class Application(Tk):
    def __init__(self):
        """Constructeur de la fenêtre principale"""

        # Instanciation de la fenêtre tkinter dans notre objet
        Tk.__init__(self)
        self.title('SysInfo')
        self.call('wm', 'attributes', '.', '-topmost', '1')
        self.configure(background='gold')
        self.resizable(width=False, height=False)
        self.geometry('%dx%d+%d+%d'%(120, 40, 20, 20)) # The last 20 are the placement (x,y) of the window

        self.start = Button(self, text='Lancer', command=self.mainLoop)
        self.start.grid(row=0, column=2, sticky=W)
        self.ping = Label(self, text='', font=("Helvetica", 16))
        self.ping.grid(row=0, column=0)

    def mainLoop(self):
        self.start.destroy()
        self.updatePing()
        self.after(500,self.mainLoop)

    def updatePing(self):
        ping = "   %s ms"%(th_ping.ping)
        color = pingtohex(th_ping.ping)
        self.ping.config(text=ping,background=color)
        self.configure(background=color)    
    
# Programme principal
if __name__ == '__main__':
    th_ping = ThreadPingLatency()
    th_ping.start()
    app = Application()
    app.mainloop()
    th_ping.stop()
