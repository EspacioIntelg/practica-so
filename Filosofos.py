import threading
import time
import random

# Número de filósofos y tenedores
NUM_FILOSOFOS = 5
TIEMPO_PENSAR = (1, 3)  
TIEMPO_COMER = (2, 4)   

class Filosofo(threading.Thread):
    def __init__(self, id, tenedor_izquierdo, tenedor_derecho, stop_event):
        threading.Thread.__init__(self)
        self.id = id
        self.tenedor_izquierdo = tenedor_izquierdo
        self.tenedor_derecho = tenedor_derecho
        self.stop_event = stop_event  

    def pensar(self):
        tiempo = random.uniform(*TIEMPO_PENSAR)
        print(f"Filósofo {self.id} está pensando por {tiempo:.2f} segundos.")
        time.sleep(tiempo)

    def comer(self):
        tiempo = random.uniform(*TIEMPO_COMER)
        print(f"Filósofo {self.id} está comiendo por {tiempo:.2f} segundos.")
        time.sleep(tiempo)

    def run(self):
        while not self.stop_event.is_set():
            self.pensar()

            print(f"Filósofo {self.id} intenta tomar los tenedores.")

            
            if self.id == NUM_FILOSOFOS - 1:
                
                primero, segundo = self.tenedor_derecho, self.tenedor_izquierdo
            else:
                
                primero, segundo = self.tenedor_izquierdo, self.tenedor_derecho

            acquired = primero.acquire(timeout=1)  
            if not acquired or self.stop_event.is_set():
                continue  

            try:
                acquired = segundo.acquire(timeout=1)
                if not acquired or self.stop_event.is_set():
                    continue  

                try:
                    print(f"Filósofo {self.id} ha tomado ambos tenedores y empieza a comer.")
                    self.comer()
                finally:
                    segundo.release()
            finally:
                primero.release()

            print(f"Filósofo {self.id} ha terminado de comer y suelta los tenedores.")


tenedores = [threading.Semaphore(1) for _ in range(NUM_FILOSOFOS)]

stop_event = threading.Event()


filosofos = []
for i in range(NUM_FILOSOFOS):
    filosofo = Filosofo(i, tenedores[i], tenedores[(i + 1) % NUM_FILOSOFOS], stop_event)
    filosofos.append(filosofo)
    filosofo.start()


try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Interrupción recibida. Terminando la simulación.")
    stop_event.set()  


for filosofo in filosofos:
    filosofo.join()

print("Simulación terminada.")