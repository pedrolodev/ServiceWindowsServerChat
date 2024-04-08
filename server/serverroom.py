import socket, threading,time
import logging
import config

sockets = {}

class Cliente(threading.Thread):

    def __init__(self,sc,nombre,lock):
        threading.Thread.__init__(self)
        self.nombre = nombre
        self.sc = sc
        self.lock = lock

    def run(self):
        global sockets
        self.broadcast(time.strftime("%I:%M:%S")+' se ha conectado '+self.nombre)
        while True:
            try:
                waiting_for_message = self.sc.recv(1024)
                message = waiting_for_message.decode('utf-8')
                with self.lock:
                    self.broadcast(self.nombre+': '+str(message))
                logging.info(self.nombre+' | '+str(message))
            except Exception as e:
                logging.info("ERROR WAITING FOR MESSAGE OR DESCONNECTED")
                logging.info(e)
                break
        with self.lock:
            del sockets[str(self.nombre)]
        self.broadcast(time.strftime("%I:%M:%S")+' se ha desconectado '+self.nombre)
        logging.info('Se ha desconectado '+self.nombre)

    def broadcast(self,msg):
        global sockets
        try:
            for usu,sock in sockets.items():
                sock.send(msg.encode())
        except Exception as e:
            logging.info("ERROR BROADCASTING")
            logging.info(e)

class Server(threading.Thread):

    def __init__(self,lock):
        threading.Thread.__init__(self)
        logging.info('\nServicio iniciado '+time.strftime("%d/%m/%Y")+' a las '+time.strftime("%I:%M:%S")+'\n')
        self.lock = lock

    def run(self):
        global sockets
        while True:
            try:
                s = socket.socket()
                s.bind(('', config.SERVER_PORT))
                s.listen(5)
                sc, addr = s.accept()
                ip = addr[0]
                logging.info("CONECTADO "+ip)
                waiting_name = sc.recv(1024)
                name = str(waiting_name.decode('utf-8'))
                logging.info(addr[0]+" se le asigna el nombre "+name)
                with self.lock:
                    sockets[name] = sc
                logging.info("LISTA DE USUARIOS/SOCKETS CONECTADOS")
                logging.info(sockets)
                t = Cliente(sc,name,self.lock)
                t.setDaemon = True
                t.start()
                
            except Exception as e:
                logging.info("ERROR IN SERVER WAITING FOR CONEXIONS")
                logging.info(str(e)+"\n")
                logging.info("LISTA DE USUARIOS/SOCKETS CONECTADOS")
                logging.info(sockets)




