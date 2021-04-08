import threading
class Intervallometre(threading.Thread):
    
    def __init__(self, duree, fonction):
        threading.Thread.__init__(self)
        self.duree = duree
        self.fonction = fonction
        self.encore = True  # pour permettre l'arret a la demande
 
    def run(self):
        while self.encore:
            self.timer = threading.Timer(self.duree, self.fonction)
            self.timer.setDaemon(True)
            self.timer.start()
            self.timer.join()
 
    def stop(self):
        self.encore = False  # pour empecher un nouveau lancement de Timer et terminer le thread