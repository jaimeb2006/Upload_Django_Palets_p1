import threading
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import firebase_admin
from firebase_admin import credentials, firestore
from django_manager import DjangoManager
from palet import Palet

class FirebaseManager:
    def __init__(self, django_manager: DjangoManager, linea: str):
        cred = credentials.Certificate("./vitapro-40650.json")
        # cred = credentials.Certificate("./vitaproapp.json")
        # cred = credentials.Certificate("C:/ProgramData/Inbalnor/vitaproapp.json")
        self.upload_in_progress = False
        self.django_manager = django_manager
        self.linea = linea
        # Bandera para controlar si una carga está en progreso
        # Intervalo de reintento en segundos
        self.retry_interval = 60
        
        self.initialize_firebase(cred)
        self.db = firestore.client()
        


    def initialize_firebase(self, cred):
        while True:
            try:
                firebase_admin.initialize_app(cred)
                print('Firebase initialized successfully')
                self.set_palet_in_firebase()
                break
            except Exception as e:
                print(f'Failed to initialize Firebase: {e}')
                print('Retrying in 5 seconds...')
                time.sleep(5)

    def set_palet_in_firebase(self):
        """Sube palets pendientes en lotes de 5 y evita nuevas subidas hasta que termine."""
        if self.upload_in_progress:
            print("Upload already in progress. Please wait until it finishes.")
            return

        self.upload_in_progress = True
        threading.Thread(target=self._upload_pending_palets, daemon=True).start()

    def _upload_pending_palets(self):
        """Busca los palets pendientes y los sube a Firebase en lotes de 5."""
        while True:
            try:
                pending_palets = self.django_manager.get_palets_pendientes_mas_bajos(self.linea)
                if not pending_palets:
                    print("No more pending palets to upload.")
                    break

                for palet in pending_palets:
                    self._upload_single_palet(palet)
                    time.sleep(1)  # Pausa breve entre subidas para evitar saturar la conexión

            except Exception as e:
                print(f"Error during upload process: {e}")

            # Esperar antes de reintentar si no hay más palets pendientes
            time.sleep(self.retry_interval)

        self.upload_in_progress = False

    def _upload_single_palet(self, palet: Palet):
        """Sube un único palet a Firebase y actualiza su estado en Django."""
        try:
            palets_ref = self.db.collection(u'Palets')
            palet_data = palet.to_dict_firebase()
            palet_data['time_stamp_create'] = firestore.SERVER_TIMESTAMP
            ref = palets_ref.add(palet_data)
            
            # Actualiza el estado del palet en Django
            self.django_manager.update_palet_firebase(palet.id, ref[1].id)
            print(f"Palet {palet.id} uploaded successfully with Firebase ID: {ref[1].id}")

        except Exception as e:
            print(f"Failed to upload palet {palet.id}: {e}")
