from datetime import timedelta, datetime


class OrdenProduccion:
    def __init__(self, id, id_fb, sku, planta_primaria, nombre_producto, nombre_abreviado, 
                 ean, destino_primaria, version_primaria, nb_primaria, dias_caducidad, 
                 id_path, familia_path, familia_path_colos, descripcion_linea_1, 
                 descripcion_linea_2, descripcion_linea_3, proteina, humedad, ceniza, 
                 grasa, fibra, ingredientes_linea_1, ingredientes_linea_2, ingredientes_linea_3, 
                 ingredientes_linea_4, ingredientes_linea_5, registro_sanitario, fabricado_para, 
                 direccion_fabricante, ruc_fabricante, version_secundaria, cantidad_terciaria, 
                 peso_neto_terciaria, fecha_creacion, estado, fecha_final, planta, prensa, 
                 prensa_numero, linea, lote_completo, lote_numeros, turno, inicio_contador_general, 
                 sscc_inicio , inicio_contador, id_producto, id_fb_producto,fin_contador_general, fin_contador, 
                 fecha_caducidad_string, subido_a_firebase, inicio_contador_string

):
        self.id = id
        self.id_fb = id_fb
        self.sku = sku
        self.planta_primaria = planta_primaria
        self.nombre_producto = nombre_producto
        self.nombre_abreviado = nombre_abreviado
        self.ean = ean
        self.destino_primaria = destino_primaria
        self.version_primaria = version_primaria
        self.nb_primaria = nb_primaria
        self.dias_caducidad = dias_caducidad
        self.id_path = id_path
        self.familia_path = familia_path
        self.familia_path_colos = familia_path_colos
        self.descripcion_linea_1 = descripcion_linea_1
        self.descripcion_linea_2 = descripcion_linea_2
        self.descripcion_linea_3 = descripcion_linea_3
        self.proteina = proteina
        self.humedad = humedad
        self.ceniza = ceniza
        self.grasa = grasa
        self.fibra = fibra
        self.ingredientes_linea_1 = ingredientes_linea_1
        self.ingredientes_linea_2 = ingredientes_linea_2
        self.ingredientes_linea_3 = ingredientes_linea_3
        self.ingredientes_linea_4 = ingredientes_linea_4
        self.ingredientes_linea_5 = ingredientes_linea_5
        self.registro_sanitario = registro_sanitario
        self.fabricado_para = fabricado_para
        self.direccion_fabricante = direccion_fabricante
        self.ruc_fabricante = ruc_fabricante
        self.version_secundaria = version_secundaria
        self.cantidad_terciaria = cantidad_terciaria
        self.peso_neto_terciaria = peso_neto_terciaria
        self.fecha_creacion = fecha_creacion
        self.estado = estado
        self.fecha_final = fecha_final
        self.planta = planta
        self.prensa = prensa
        self.prensa_numero = prensa_numero
        self.linea = linea
        self.lote_completo = lote_completo
        self.lote_numeros = lote_numeros
        self.turno = turno
        self.inicio_contador_general = inicio_contador_general
        self.sscc_inicio = sscc_inicio
        self.inicio_contador = inicio_contador
        self.id_producto = id_producto
        self.id_fb_producto = id_fb_producto
        self.fin_contador_general = fin_contador_general
        self.fin_contador = fin_contador
        self.fecha_caducidad_string = fecha_caducidad_string
        self.subido_a_firebase = subido_a_firebase, 
        self.inicio_contador_string = inicio_contador_string

    def to_dict(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "planta_primaria": self.planta_primaria,
            "nombre_producto": self.nombre_producto,
            "nombre_abreviado": self.nombre_abreviado,
            "ean": self.ean,
            "destino_primaria": self.destino_primaria,
            "version_primaria": self.version_primaria,
            "nb_primaria": self.nb_primaria,
            "dias_caducidad": self.dias_caducidad,
            "id_path": self.id_path,
            "familia_path": self.familia_path,
            "familia_path_colos": self.familia_path_colos,
            "descripcion_linea_1": self.descripcion_linea_1,
            "descripcion_linea_2": self.descripcion_linea_2,
            "descripcion_linea_3": self.descripcion_linea_3,
            "proteina": self.proteina,
            "humedad": self.humedad,
            "ceniza": self.ceniza,
            "grasa": self.grasa,
            "fibra": self.fibra,
            "ingredientes_linea_1": self.ingredientes_linea_1,
            "ingredientes_linea_2": self.ingredientes_linea_2,
            "ingredientes_linea_3": self.ingredientes_linea_3,
            "ingredientes_linea_4": self.ingredientes_linea_4,
            "ingredientes_linea_5": self.ingredientes_linea_5,
            "registro_sanitario": self.registro_sanitario,
            "fabricado_para": self.fabricado_para,
            "direccion_fabricante": self.direccion_fabricante,
            "ruc_fabricante": self.ruc_fabricante,
            "version_secundaria": self.version_secundaria,
            "cantidad_terciaria": self.cantidad_terciaria,
            "peso_neto_terciaria": self.peso_neto_terciaria,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "estado": self.estado,
            "fecha_final": self.fecha_final.isoformat() if self.fecha_final else None,
            "planta": self.planta,
            "prensa": self.prensa,
            "prensa_numero": self.prensa_numero,
            "linea": self.linea,
            "lote_completo": self.lote_completo,
            "lote_numeros": self.lote_numeros,
            "turno": self.turno,
            "inicio_contador_general": self.inicio_contador_general,
            "sscc_inicio": self.sscc_inicio,
            "inicio_contador": self.inicio_contador,
            "id_producto": self.id_producto,
            "id_fb_producto": self.id_fb_producto,
            "fin_contador_general": self.fin_contador_general,
            "fin_contador": self.fin_contador,
            "fecha_caducidad_string": self.fecha_caducidad_string,
            "subido_a_firebase": self.subido_a_firebase,
            "inicio_contador_string": self.inicio_contador_string
        }
    
   
    @classmethod
    def default(cls):
        return cls(
            id=1,
            id_fb = 'new',
            sku='1',
            planta_primaria='',
            nombre_producto='',
            nombre_abreviado='',
            ean='',
            destino_primaria='',
            version_primaria='',
            nb_primaria='',
            dias_caducidad=0,
            id_path='',
            familia_path='',
            familia_path_colos='',
            descripcion_linea_1='',
            descripcion_linea_2='',
            descripcion_linea_3='',
            proteina=0.0,
            humedad=0.0,
            ceniza=0.0,
            grasa=0.0,
            fibra=0.0,
            ingredientes_linea_1='',
            ingredientes_linea_2='',
            ingredientes_linea_3='',
            ingredientes_linea_4='',
            ingredientes_linea_5='',
            registro_sanitario='',
            fabricado_para='',
            direccion_fabricante='',
            ruc_fabricante='',
            version_secundaria='',
            cantidad_terciaria='',
            peso_neto_terciaria='',
            fecha_creacion=datetime.now(),
            estado='',
            fecha_final=None,
            planta='',
            prensa='',
            prensa_numero='',
            linea='',
            lote_completo='',
            lote_numeros='',
            turno=0,
            inicio_contador_general=0,
            sscc_inicio='',
            inicio_contador=0,
            id_producto=1,
            id_fb_producto='',
            fin_contador_general=0,
            fin_contador=0,
            fecha_caducidad_string='',
            subido_a_firebase = False, 
            inicio_contador_string = '0001'
        )
    
    def from_new__orden(self, turno, inicio_contador_general ):
            #TODO: Corregir Inicio CONTADOR 
            fecha_creacion = datetime.now()
            fecha_actual = fecha_creacion.strftime("%y%m%d")
            fecha_futura = (fecha_creacion + timedelta(days=self.dias_caducidad)).strftime("%d/%m/%y")
            print("🚀 ~ fecha_futura:", fecha_futura)
            sscc_inicio = f'{self.planta}{self.linea}{self.prensa_numero}{turno}{self.version_primaria}{fecha_actual}{str(self.id_producto).zfill(4)}'
            lote_completo = f'{self.destino_primaria}{fecha_actual}{self.prensa}{self.version_primaria}'
            
            orden = OrdenProduccion(self.id,
                                    'new',
                                    self.sku,
                                    self.planta_primaria,
                                    self.nombre_producto,
                                    self.nombre_abreviado,
                                    self.ean,
                                    self.destino_primaria,
                                    self.version_primaria,
                                    self.nb_primaria,
                                    self.dias_caducidad,
                                    self.id_path,
                                    self.familia_path,
                                    self.familia_path_colos,
                                    self.descripcion_linea_1,
                                    self.descripcion_linea_2,
                                    self.descripcion_linea_3,
                                    self.proteina,
                                    self.humedad,
                                    self.ceniza,
                                    self.grasa,
                                    self.fibra,
                                    self.ingredientes_linea_1,
                                    self.ingredientes_linea_2,
                                    self.ingredientes_linea_3,
                                    self.ingredientes_linea_4,
                                    self.ingredientes_linea_5,
                                    self.registro_sanitario,
                                    self.fabricado_para,
                                    self.direccion_fabricante,
                                    self.ruc_fabricante,
                                    self.version_secundaria,
                                    self.cantidad_terciaria,
                                    self.peso_neto_terciaria,
                                    fecha_creacion,
                                    'INICIO',
                                    fecha_creacion,
                                    self.planta,
                                    self.prensa,
                                    self.prensa_numero,
                                    self.linea,
                                    lote_completo,
                                    fecha_actual,
                                    turno,
                                    inicio_contador_general,
                                    sscc_inicio,
                                    0,
                                    self.id_producto,
                                    self.id_fb_producto,
                                    inicio_contador_general,
                                    inicio_contador_general,
                                    fecha_futura, False,
                                    str(inicio_contador_general).zfill(4))
            return orden
