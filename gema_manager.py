import threading
import time
from datetime import datetime
import psycopg2
from psycopg2 import sql
from django_manager import DjangoManager
from palet import Palet
from zoneinfo import ZoneInfo

# Credenciales de PostgreSQL (constantes)
DB_HOST = "34.138.202.114"
DB_PORT = 5432
DB_NAME = "db-gema-matriz-dev"
DB_USER = "user_colos"
DB_PASSWORD = "5zZh0uuECz0M"


class GemaManager:
    def __init__(self, django_manager: DjangoManager, linea: str, retry_interval: int = 60):
        self.db_config = {
            "host": DB_HOST,
            "port": DB_PORT,
            "dbname": DB_NAME,
            "user": DB_USER,
            "password": DB_PASSWORD
        }
        self.retry_interval = retry_interval
        self.upload_in_progress = False
        self.connection = None
        self.django_manager = django_manager
        self.linea = linea
        self._connect_to_database()

    def _connect_to_database(self):
        """Inicializa la conexión a la base de datos."""
        while True:
            try:
                self.connection = psycopg2.connect(**self.db_config)
                print("PostgreSQL connection established successfully.")
                self.upload_pending_palets()
                break
            except Exception as e:
                print(f"Failed to connect to PostgreSQL: {e}")
                print(f"Retrying in {self.retry_interval} seconds...")
                time.sleep(self.retry_interval)

    def get_finished_product_data(self, sku_code: str, id_factory: int):
        """
        Obtiene `id_finished_product` basado en `sku_code` e `id_factory`.
        Si no existe, devuelve `None`.

        Args:
            sku_code (str): Código SKU del producto.
            id_factory (int): ID de la fábrica asociada.

        Returns:
            dict: Diccionario con `id_finished_product` e `id_factory`, o `None` si no se encuentra.
        """
        try:
            cursor = self.connection.cursor()
            query_select = sql.SQL("""
                SELECT id_finished_product, id_factory
                FROM general.finished_product
                WHERE sku_code = %s AND id_factory = %s
            """)
            cursor.execute(query_select, (sku_code, id_factory))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return {"id_finished_product": result[0], "id_factory": result[1]}
            else:
                print(f"No data found for SKU Code: {sku_code} and Factory ID: {id_factory}.")
                return None
        except Exception as e:
            print(f"Error retrieving data for SKU Code {sku_code} and Factory ID {id_factory}: {e}")
            return None

    def insert_finished_product(self, sku_code: str, finished_product_detail: str, id_factory: int):
        """
        Inserta un nuevo registro en la tabla `general.finished_product`.

        Args:
            sku_code (str): Código SKU del producto.
            finished_product_detail (str): Detalle del producto terminado.
            id_factory (int): ID de la fábrica asociada.

        Returns:
            dict: Diccionario con `id_finished_product` e `id_factory` del registro recién creado.
        """
        try:
            cursor = self.connection.cursor()
            query_insert = sql.SQL("""
                INSERT INTO general.finished_product (sku_code, finished_product_detail, id_factory)
                VALUES (%s, %s, %s)
                RETURNING id_finished_product, id_factory
            """)
            cursor.execute(query_insert, (sku_code, finished_product_detail, id_factory))
            self.connection.commit()
            new_result = cursor.fetchone()
            cursor.close()

            print(f"New finished product inserted with ID: {new_result[0]}")
            return {"id_finished_product": new_result[0], "id_factory": new_result[1]}
        except Exception as e:
            print(f"Error inserting new finished product for SKU Code {sku_code} and Factory ID {id_factory}: {e}")
            return None

    def insert_conforming_product_quantity(self, data: dict):
        """Inserta un registro en la tabla `production.conforming_product_quantity`."""
        try:
            cursor = self.connection.cursor()
            query = sql.SQL("""
                INSERT INTO production.conforming_product_quantity (
                    date, "time", id_packaging_line, id_production_line,
                    id_finished_product, batch, bags_quantity,
                    id_shift_report, sscc, pallet_number, unit_of_measurement
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """)
            cursor.execute(query, (
                data["date"], data["time"], data["id_packaging_line"],
                data["id_production_line"], data["id_finished_product"],
                data["batch"], data["bags_quantity"], data.get("id_shift_report"),
                data.get("sscc"), data.get("pallet_number"), data["unit_of_measurement"]
            ))
            self.connection.commit()
            print(f"Record for batch {data['batch']} inserted successfully.")
            cursor.close()
        except Exception as e:
            print(f"Failed to insert record for batch {data['batch']}: {e}")

    def upload_pending_palets(self):
        """Verifica y sube los palets con `subido_a_vitacontrol=False`."""
        if self.upload_in_progress:
            print("Upload already in progress. Please wait until it finishes.")
            return

        self.upload_in_progress = True
        threading.Thread(target=self._process_pending_palets, daemon=True).start()

    def _process_pending_palets(self):
        """Sube los palets pendientes a PostgreSQL."""
        try:
            while True:
                pending_palets = self.django_manager.get_palets_pendientes_mas_bajos_gema(self.linea)
                if not pending_palets:
                    print("No more pending palets to upload.")
                    break

                for palet in pending_palets:
                    # Buscar `id_finished_product` por SKU e ID de fábrica
                    #Planta 1 = id = 2 y planta 2 = id = 3
                    product_data = self.get_finished_product_data(palet.sku, 2)
                    if not product_data:
                        # Si no existe, insertar un nuevo registro
                        print(f"Inserting new finished product for SKU {palet.sku} and Factory ID {2}.")
                        product_data = self.insert_finished_product(
                            sku_code=palet.sku,
                            finished_product_detail=palet.nombre_producto,
                            id_factory=2
                        )
                        if not product_data:
                            print(f"Skipping Palet {palet.id}: Unable to insert finished product.")
                            continue

                    # Obtener fecha y hora local desde fecha_creacion
                    fecha_hora = self.get_fecha_hora_local(palet.fecha_creacion)

                    record = {
                        "date": fecha_hora["fecha"],
                        "time": fecha_hora["hora"],
                        "id_packaging_line": palet.linea,
                        "id_production_line": palet.prensa_numero,
                        "id_finished_product": product_data["id_finished_product"],
                        "batch": palet.lote_completo,
                        "bags_quantity": palet.cantidad,
                        "id_shift_report": None,
                        "sscc": palet.sscc,
                        "pallet_number": palet.numero_palet,
                        "unit_of_measurement": 'UND'
                    }
                    result = self.insert_conforming_product_quantity(record)
                    if result is None:
                        print(f"Error inserting record for Palet {palet.id} marked as uploaded.")
                    else:
                        # Marca el palet como subido
                        self.django_manager.update_palet_gema(palet.id)
                        print(f"Palet {palet.id} marked as uploaded.")
                    time.sleep(1)  # Pausa breve entre subidas para evitar saturar la conexión

                # time.sleep(self.retry_interval)
        except Exception as e:
            print(f"Error during palet upload: {e}")
        finally:
            self.upload_in_progress = False

    def close_connection(self):
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
            print("PostgreSQL connection closed.")

    @staticmethod
    def get_fecha_hora_local(fecha_creacion: str) -> dict:
        """
        Convierte una fecha y hora con zona horaria UTC-5 a la fecha y hora local de Guayaquil.

        Args:
            fecha_creacion (str): Fecha en formato ISO con zona horaria.

        Returns:
            dict: Diccionario con la fecha y la hora local separadas.
        """
        try:
            # Parsear la fecha y hora directamente
            fecha, hora = fecha_creacion.split("T")
            hora = hora.split("-")[0]  # Eliminar la parte de la zona horaria si está presente
            return {
                "fecha": fecha,
                "hora": hora
            }
        except Exception as e:
            print(f"Error parsing fecha_creacion: {e}")
            return {"fecha": None, "hora": None}
