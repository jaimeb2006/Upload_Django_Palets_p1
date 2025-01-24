import threading
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import firebase_admin
from firebase_admin import credentials, firestore
from django_manager import DjangoManager
from palet import Palet

class FirebaseManager:
    def __init__(self, django_manager: DjangoManager, linea: str, retry_interval: int = 60):
        # self.cred = credentials.Certificate("./vitapro-40650.json")
        # cred = credentials.Certificate("./vitaproapp.json")
        self.cred = credentials.Certificate("C:/ProgramData/Inbalnor/vitaproapp.json")
        self.upload_in_progress = False
        self.django_manager = django_manager
        self.linea = linea
        # Bandera para controlar si una carga está en progreso
        # Intervalo de reintento en segundos
        self.retry_interval = retry_interval
        self.db = None
        self.is_initialized = False
        self.initialize_firebase(self.cred)
        


    def initialize_firebase(self, cred):
        time_retry_init = 5
        if not self.django_manager.check_real_internet_connection():
            print("No internet connection. Retrying in 5 seconds...")
            self.schedule_function(self.initialize_firebase, time_retry_init, cred)
            return
        try:
            firebase_admin.initialize_app(cred)
            print('Firebase initialized successfully')
            self.is_initialized = True
            self.db = firestore.client()
            self.set_palet_in_firebase()
            
        except Exception as e:
            print(f'Failed to initialize Firebase: {e}')
            print('Retrying in 5 seconds...')
            self.schedule_function(self.initialize_firebase, time_retry_init, cred) 

    def schedule_function(self, func, interval, *args, **kwargs):
        """
        Schedule a function to be called after a specific interval.
        """
        print(f"Scheduling function '{func.__name__}' to run in {interval} seconds...")
        threading.Timer(interval, func, args=args, kwargs=kwargs).start()

    def set_palet_in_firebase(self):
        """Sube palets pendientes en lotes de 5 y evita nuevas subidas hasta que termine."""

        if not self.is_initialized:
            print("Firebase is not already initialized.")
            return
        
        if self.upload_in_progress:
            print("Upload already in progress. Please wait until it finishes.")
            return

        self.upload_in_progress = True
        threading.Thread(target=self._upload_pending_palets, daemon=True).start()

    def _upload_pending_palets(self):
        """Busca los palets pendientes y los sube a Firebase en lotes de 5."""
        
        try:
            pending_palets = self.django_manager.get_palets_pendientes_mas_bajos(self.linea)
            if not pending_palets:
                print("No more pending palets to upload.")
                self.upload_in_progress = False
                return

            time_retry_upload = 30
            for palet in pending_palets:
                if not self.django_manager.check_real_internet_connection():
                    print("No internet connection. Retrying ...")
                    self.upload_in_progress = False
                    self.schedule_function(self.set_palet_in_firebase, time_retry_upload)
                    return
                    
                result_firebase = self._upload_single_palet(palet)
                if not result_firebase:
                    print("Failed to upload palet. Retrying ...")
                    self.upload_in_progress = False
                    self.schedule_function(self.set_palet_in_firebase, time_retry_upload)
                    return
                    # Pausa breve entre subidas para evitar saturar la conexión
            self.upload_in_progress = False    
            self.set_palet_in_firebase()

        except Exception as e:
            print(f"Error during upload process: {e}")
            self.upload_in_progress = False
            self.schedule_function(self.set_palet_in_firebase, time_retry_upload)
        
        


    def _upload_single_palet(self, palet: Palet):
        """Sube un único palet a Firebase y actualiza su estado en Django."""
        try:
            palets_ref = self.db.collection(u'Palets')
            palet_data = palet.to_dict_firebase()
            palet_data['time_stamp_create'] = firestore.SERVER_TIMESTAMP
            ref = palets_ref.add(palet_data)
            
            # Actualiza el estado del palet en Django
            self.django_manager.update_palet_firebase(palet.id, ref[1].id)
            print(f"Palet {palet.id} uploaded successfully with Firebase ID: {ref[1].id} sscc: {palet.sscc}")
            return True

        except Exception as e:
            print(f"Failed to upload palet {palet.id}: {e}")
            return False
