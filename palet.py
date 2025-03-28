from datetime import datetime

from orden_produccion import OrdenProduccion


class Palet:
    def __init__(self, id, id_fb, sku, nombre_producto, ean13, planta_primaria,
                 linea, llenadora, prensa, prensa_numero, version_primaria, lote_completo,
                 cantidad, sscc, fecha_elaboracion, fecha_caducidad, numero_palet,
                 fecha_creacion, fecha_actualizacion, id_bodega_origen, id_bodega_destino,
                 movimientos_id, movimientos_nombre, fechas_movimientos, usuarios_movimientos,
                 turno, id_usuario, id_orden_produccion, subido_a_firebase, subido_a_vitacontrol,
                 fecha_caducidad_string, peso_neto_terciaria, linea_letra, numero_palet_string, id_vitacontrol, 
                 codigo_bodega_actual ,    id_fb_producto ,    id_producto
                 ):
        self.id = id
        self.id_fb = id_fb
        self.sku = sku
        self.nombre_producto = nombre_producto
        self.ean13 = ean13
        self.planta_primaria = planta_primaria
        self.linea = linea
        self.llenadora = llenadora
        self.prensa = prensa
        self.prensa_numero = prensa_numero
        self.version_primaria = version_primaria
        self.lote_completo = lote_completo
        self.cantidad = cantidad
        self.sscc = sscc
        self.fecha_elaboracion = fecha_elaboracion
        self.fecha_caducidad = fecha_caducidad
        self.numero_palet = numero_palet
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion
        self.id_bodega_origen = id_bodega_origen
        self.id_bodega_destino = id_bodega_destino
        self.movimientos_id = movimientos_id
        self.movimientos_nombre = movimientos_nombre
        self.fechas_movimientos = fechas_movimientos
        self.usuarios_movimientos = usuarios_movimientos
        self.turno = turno
        self.id_usuario = id_usuario
        self.id_orden_produccion = id_orden_produccion
        self.subido_a_firebase = subido_a_firebase
        self.subido_a_vitacontrol = subido_a_vitacontrol
        self.fecha_caducidad_string = fecha_caducidad_string
        self.peso_neto_terciaria = peso_neto_terciaria
        self.linea_letra = linea_letra
        self.numero_palet_string = numero_palet_string
        self.id_vitacontrol = id_vitacontrol
        self.codigo_bodega_actual = codigo_bodega_actual
        self.id_fb_producto = id_fb_producto
        self.id_producto = id_producto


    def to_dict(self):
        return {
            "id": self.id,
            "id_fb": self.id_fb,
            "sku": self.sku,
            "nombre_producto": self.nombre_producto,
            "ean13": self.ean13,
            "planta_primaria": self.planta_primaria,
            "linea": self.linea,
            "llenadora": self.llenadora,
            "prensa": self.prensa,
            "prensa_numero": self.prensa_numero,
            "version_primaria": self.version_primaria,
            "lote_completo": self.lote_completo,
            "cantidad": self.cantidad,
            "sscc": self.sscc,
            "fecha_elaboracion": self.fecha_elaboracion.isoformat() if self.fecha_elaboracion else None,
            "fecha_caducidad": self.fecha_caducidad.isoformat() if self.fecha_caducidad else None,
            "numero_palet": self.numero_palet,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            "id_bodega_origen": self.id_bodega_origen,
            "id_bodega_destino": self.id_bodega_destino,
            "movimientos_id": self.movimientos_id,
            "movimientos_nombre": self.movimientos_nombre,
            "fechas_movimientos": [fecha.isoformat() for fecha in self.fechas_movimientos] if self.fechas_movimientos else [],
            "usuarios_movimientos": self.usuarios_movimientos,
            "turno": self.turno,
            "id_usuario": self.id_usuario,
            "id_orden_produccion": self.id_orden_produccion,
            "subido_a_firebase": self.subido_a_firebase,
            "subido_a_vitacontrol": self.subido_a_vitacontrol,
            "fecha_caducidad_string": self.fecha_caducidad_string, 
            "peso_neto_terciaria": self.peso_neto_terciaria, 
            "linea_letra": self.linea_letra, 
            "numero_palet_string": self.numero_palet_string,
            "id_vitacontrol": self.id_vitacontrol,
            "codigo_bodega_actual": self.codigo_bodega_actual if self.codigo_bodega_actual else '0-0',
            "id_fb_producto": self.id_fb_producto if self.id_fb_producto else '-1',
            "id_producto": self.id_producto if self.id_producto else -1,
            # "planta": self.movimientos_nombre[0],
            # "planta_linea": f'{self.movimientos_nombre[0]}_l{self.linea}',
            # "id_last_session": f'produccion_{self.movimientos_nombre[0]}',
           
        }
    
    def parse_datetime_with_timezone(self, date_string):
        try:
            # Parsear la cadena de fecha con zona horaria
            return datetime.fromisoformat(date_string)  # Maneja fechas en formato ISO 8601
        except ValueError:
            print(f"Formato de fecha inválido: {date_string}")
            return datetime.now()
        

    def to_dict_firebase(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "nombre_producto": self.nombre_producto,
            "ean13": self.ean13,
            "planta_primaria": self.planta_primaria,
            "linea": self.linea,
            "llenadora": self.llenadora,
            "prensa": self.prensa,
            "prensa_numero": self.prensa_numero,
            "version_primaria": self.version_primaria,
            "lote_completo": self.lote_completo,
            "cantidad": self.cantidad,
            "sscc": self.sscc,
            "fecha_elaboracion": self.parse_datetime_with_timezone(self.fecha_elaboracion) ,
            "fecha_caducidad": self.parse_datetime_with_timezone(self.fecha_caducidad ),
            "numero_palet": self.numero_palet,
            "fecha_creacion": self.parse_datetime_with_timezone(self.fecha_creacion ),
            "fecha_recepcion_bodega": self.parse_datetime_with_timezone(self.fecha_creacion ),
            "fecha_actualizacion":  self.parse_datetime_with_timezone(self.fecha_actualizacion ),
            "id_bodega_origen": self.id_bodega_origen,
            "id_bodega_destino": self.id_bodega_destino,
            "movimientos": [
                { 
                    "id_bodega": f'{self.id_bodega_origen}-{self.id_bodega_destino}',
                    "nombre": f'{self.movimientos_nombre[0]}_l{self.linea}', 
                    "email": f'{self.movimientos_nombre[0]}_l{self.linea}',
                    "usuario": self.usuarios_movimientos[0],
                    "fecha":  self.parse_datetime_with_timezone(self.fechas_movimientos[0]),
                    "id_session": f'produccion_{self.movimientos_nombre[0]}',
                }
            ],
            "turno": self.turno,
            "id_usuario": self.id_usuario,
            "id_orden_produccion": self.id_orden_produccion,
            "subido_a_firebase": True,
            "subido_a_vitacontrol": self.subido_a_vitacontrol,
            "fecha_caducidad_string": self.fecha_caducidad_string, 
            "peso_neto_terciaria": self.peso_neto_terciaria, 
            "linea_letra": self.linea_letra, 
            "numero_palet_string": self.numero_palet_string,
            "id_vitacontrol": self.id_vitacontrol, 
            "codigo_bodega_actual": f'{self.id_bodega_origen}-{self.id_bodega_destino}',
            "id_fb_producto": self.id_fb_producto if self.id_fb_producto else '-1',
            "id_producto": self.id_producto if self.id_producto else -1,
            "planta": self.movimientos_nombre[0],
            "planta_linea": f'{self.movimientos_nombre[0]}_l{self.linea}',
            "id_last_session": f'produccion_{self.movimientos_nombre[0]}',
            'fecha_lote_numeros': self.lote_completo[2:8]
        }



    def from_orden_produccion_to_palet( orden_produccion: OrdenProduccion, numero_actual, subido_a_firebase: bool, subido_a_vitacontrol: bool):
        sscc_inicio = f'{orden_produccion.planta}{orden_produccion.linea}{orden_produccion.prensa_numero}{str(orden_produccion.turno).zfill(2)}{orden_produccion.version_primaria}{orden_produccion.lote_numeros}{str(orden_produccion.id_producto).zfill(4)}{str(numero_actual).zfill(4)}'
        ean13 = f"{orden_produccion.sku}@30{orden_produccion.cantidad_terciaria}@10{orden_produccion.lote_completo}"
        print("🚀 ~ ean13:", ean13 , 'sscc_inicio: ', sscc_inicio)
        fecha_caducidad = datetime.strptime(orden_produccion.fecha_caducidad_string, "%d/%m/%y")
        id_usuario = f'produccion_p{orden_produccion.planta}_l{orden_produccion.linea}'
        numero_actual_string = str(numero_actual).zfill(4)
        return Palet(
            id=1,
            id_fb='id_fb',
            sku=orden_produccion.sku,
            nombre_producto=orden_produccion.nombre_producto,
            ean13=ean13,
            planta_primaria=orden_produccion.planta_primaria,
            linea=orden_produccion.linea,
            llenadora=orden_produccion.prensa_numero,
            prensa=orden_produccion.prensa,
            prensa_numero=orden_produccion.prensa_numero,
            version_primaria=orden_produccion.version_primaria,
            lote_completo=orden_produccion.lote_completo,
            cantidad=orden_produccion.cantidad_terciaria,
            sscc=sscc_inicio,
            fecha_elaboracion=orden_produccion.fecha_creacion,
            fecha_caducidad=fecha_caducidad,
            numero_palet=numero_actual,
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now(),
            id_bodega_origen=0,
            id_bodega_destino=0,
            movimientos_id=[0],
            movimientos_nombre=['planta_1'],
            fechas_movimientos=[datetime.now()],
            usuarios_movimientos=[id_usuario],
            turno=orden_produccion.turno,
            id_usuario=id_usuario,
            id_orden_produccion=orden_produccion.id,
            subido_a_firebase=subido_a_firebase,
            subido_a_vitacontrol=subido_a_vitacontrol,
            fecha_caducidad_string=orden_produccion.fecha_caducidad_string, 
            peso_neto_terciaria = orden_produccion.peso_neto_terciaria, 
            linea_letra = orden_produccion.linea,
            numero_palet_string = numero_actual_string,
            id_vitacontrol = ' ',
            codigo_bodega_actual = '0-0',
            id_fb_producto = orden_produccion.id_fb_producto,
            id_producto = orden_produccion.id_producto
            )
            

            
            
