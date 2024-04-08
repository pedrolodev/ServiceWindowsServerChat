import win32serviceutil 
import win32service
import win32event
from server import serverroom
import threading
import sys,servicemanager,time
import logging
import config

logging.basicConfig(
    filename = 'c:\\Temp\\chatservice.log',
    level = logging.DEBUG, 
    format = time.strftime("%I:%M:%S")+' %(levelname)-7.7s %(message)s'
)

class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = config.SERVICE_NAME
    _svc_display_name_ = config.SERVICE_DISPLAY_NAME
    _svc_description_ = config.SERVICE_DESCRIPTION

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Evento que se usara para detener el servicio
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        logging.info("STOPPING SERVICE")
        # Se informa al SMC que se esta deteniendo el servicio
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # Establece el evento de parada
        win32event.SetEvent(self.hWaitStop)
        logging.info("STOPPED SERVICE")

    def SvcDoRun(self):
        logging.info("RUNNING SERVICE...")
        lock = threading.Lock()
        s = serverroom.Server(lock)
        s.setDaemon = True
        s.start()
        # El servicio no hace nada, simplemente esperar al evento de detencion
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__=='__main__':
    if len(sys.argv) == 1:
        "pyinstaller"
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(Service)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        "command line"
        win32serviceutil.HandleCommandLine(Service)

