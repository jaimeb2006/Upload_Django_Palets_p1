from datetime import datetime
import socket

from orden_produccion import OrdenProduccion
from palet import Palet


def subir_palet(orden_produccion: OrdenProduccion, numero_actual):
    palet = Palet.from_orden_produccion_to_palet(orden_produccion, numero_actual, False, False)
    result = UtilidadGeneral.datos_compartidos["django_manager"].set_palet(palet)
    if(result =='SSCC_EXISTS' ):
        print("Error: Un palet con este SSCC ya existe.")
        return None
    if result is None:
        print(f"Error al subir palet")
        return None
    
    return result

def check_orden_and_update(orden: OrdenProduccion,nuevo_contador, contador_actual, fin_contador_genetal):
    print("🚀 ~ orden.id>4 and orden.inicio_contador< nuevo_contador:", orden.id>4 and orden.inicio_contador< nuevo_contador, orden.id>4 , orden.inicio_contador< nuevo_contador)
    if orden.id>4 and orden.inicio_contador< nuevo_contador and contador_actual!=-1:
        try:
            print("🚀 ~ nuevo_contador > contador_actual:", nuevo_contador > contador_actual, nuevo_contador , contador_actual)
            if nuevo_contador > contador_actual:
                for palet_numero in range(contador_actual+1, nuevo_contador+1):
                    palet:Palet = subir_palet(orden, palet_numero)
                    if palet != None:
                        print("🚀 ~ palet id:", palet.id, palet.sscc)
                        try:
                            UtilidadGeneral.datos_compartidos['django_manager'].update_counter_orden_produccion_async(orden.id,fin_contador_genetal,palet_numero)
                        except Exception as e:
                            print(f'😵‍💫Error al actualizar orden produccion', e)

        except Exception as e:
            print(f'😵‍💫Erroooooooooooor crear palet', e)

    # if val != None and orden.inicio_contador_general != None :
    #     actual = val - orden.inicio_contador_general
    #     if actual == 0 and tigger == orden.id:
    #             print(f'Inicio id:{orden.id} tigger:{tigger} val:{val} actual:{actual} ')
    #     elif tigger != orden.id:
    #             print(f'Error Tigger y orden distinto id:{orden.id} tigger:{tigger} val:{val} actual:{actual} ')
    #     elif orden.id>4 and actual>0:
    #         palet_numero = actual + orden.inicio_contador
    #         palet = subir_palet(orden, palet_numero)
            # change_turno = UtilidadGeneral.calcular_turno(orden)
            # if change_turno:
            #     try:
            #         fin_contador_general = val
            #         fin_contador = palet_numero
            #         fecha_actual = datetime.now()
            #         orden_update = UtilidadGeneral.datos_compartidos['django_manager'].update_orden_produccion(orden.id,fecha_actual,fin_contador_general,fin_contador,'FINALIZADO')
            #         print("🚀 ~ orden_update:", orden_update.id)
            #         turno_new =calcular_turno_con_hora(fecha_actual)
            #         orden_new = orden.from_new__orden(turno_new,fin_contador_general)
            #         result_new_order = UtilidadGeneral.datos_compartidos["django_manager"].set_orden_produccion(orden_new)
            #         print("🚀 ~ result_new_order:", result_new_order)
            #         print("🚀 ~ addres_job_trigger:", addres_job_trigger)

            #         UtilidadGeneral.datos_compartidos["opc_manager"].set_node_value(str(result_new_order.id), addres_job_trigger) 
                    
            #     except Exception as e:
            #         print(f"Error al actualizar orden {e}")

        # else:
        #     print(f'Printer sin etiqueta final id:{orden.id} tigger:{tigger} val:{val} actual:{actual} ')
                
                    

def calcular_turno_con_hora(fecha_actual: datetime):
    
    hora_actual = fecha_actual.hour
    if(fecha_actual.minute >= 44):
        hora_actual = 23

    if hora_actual < 7:
        turno = 10
    elif hora_actual < 15:
        turno = 30
    elif hora_actual < 23:
        turno = 50
    else:
        turno = 70
    return turno

def convertir_id_string_a_int(id):
    try:
        id = int(id)
    except Exception as e:
        print(f"Error al convertir a entero {e}")
        id = 1
    return id




class UtilidadGeneral:
    datos_compartidos = {
        "opc_manager": None,
        "django_manager": None,
        'opc_addresses' : {
            'actualizar_productos': "ns=2;s=Inbalnor_OPC.generales.p1_actualizar_productos",
            # 'job_trigger_l1': f'ns=2;s=Inbalnor_OPC.generales.p1_l1_job_trigger',
            # 'job_trigger_l2': f'ns=2;s=Inbalnor_OPC.generales.p1_l2_job_trigger',
            # 'job_trigger_l3': f'ns=2;s=Inbalnor_OPC.generales.p1_l3_job_trigger',
            # 'job_trigger_l4': f'ns=2;s=Inbalnor_OPC.generales.p1_l4_job_trigger',
            # 'job_trigger_l5': f'ns=2;s=Inbalnor_OPC.generales.p1_l5_job_trigger',
            # Agrega más direcciones según sea necesario
        },
        'opc_addresses_subcription' :{
            'job_trigger_l1': f'ns=2;s=Inbalnor_OPC.generales.p1_l1_job_trigger',
            'turno_l1': f'ns=2;s=Inbalnor_OPC.generales.p1_l1_turno',
            'terciaria_status_l1': f'ns=2;s=Printers_Inbalnor.p1_l1_terciaria.Devices.p1_l1_terciaria.Status',
            'terciaria_counter1_l1': f'ns=2;s=Printers_Inbalnor.p1_l1_terciaria.Devices.p1_l1_terciaria.Counter1',
            'terciaria_counter_total_l1': f'ns=2;s=Printers_Inbalnor.p1_l1_terciaria.Devices.p1_l1_terciaria.TotalCount',
            'terciaria_job_id_l1': "ns=2;s=Printers_Inbalnor.p1_l1_terciaria.Devices.p1_l1_terciaria.CurrentProduct",

            'job_trigger_l2': f'ns=2;s=Inbalnor_OPC.generales.p1_l2_job_trigger',
            'turno_l2': f'ns=2;s=Inbalnor_OPC.generales.p1_l2_turno',
            'terciaria_status_l2': f'ns=2;s=Printers_Inbalnor.p1_l2_terciaria.Devices.p1_l2_terciaria.Status',
            'terciaria_counter1_l2': f'ns=2;s=Printers_Inbalnor.p1_l2_terciaria.Devices.p1_l2_terciaria.Counter1',
            'terciaria_counter_total_l2': f'ns=2;s=Printers_Inbalnor.p1_l2_terciaria.Devices.p1_l2_terciaria.TotalCount',
            'terciaria_job_id_l2': "ns=2;s=Printers_Inbalnor.p1_l2_terciaria.Devices.p1_l2_terciaria.CurrentProduct",


            'job_trigger_l3': f'ns=2;s=Inbalnor_OPC.generales.p1_l3_job_trigger',
            'turno_l3': f'ns=2;s=Inbalnor_OPC.generales.p1_l3_turno',
            'terciaria_status_l3': f'ns=2;s=Printers_Inbalnor.p1_l3_terciaria.Devices.p1_l3_terciaria.Status',
            'terciaria_counter1_l3': f'ns=2;s=Printers_Inbalnor.p1_l3_terciaria.Devices.p1_l3_terciaria.Counter1',
            'terciaria_counter_total_l3': f'ns=2;s=Printers_Inbalnor.p1_l3_terciaria.Devices.p1_l3_terciaria.TotalCount',
            'terciaria_job_id_l3': "ns=2;s=Printers_Inbalnor.p1_l3_terciaria.Devices.p1_l3_terciaria.CurrentProduct",

            'job_trigger_l4': f'ns=2;s=Inbalnor_OPC.generales.p1_l4_job_trigger',
            'turno_l4': f'ns=2;s=Inbalnor_OPC.generales.p1_l4_turno',
            'terciaria_status_l4': f'ns=2;s=Printers_Inbalnor.p1_l4_terciaria.Devices.p1_l4_terciaria.Status',
            'terciaria_counter1_l4': f'ns=2;s=Printers_Inbalnor.p1_l4_terciaria.Devices.p1_l4_terciaria.Counter1',
            'terciaria_counter_total_l4': f'ns=2;s=Printers_Inbalnor.p1_l4_terciaria.Devices.p1_l4_terciaria.TotalCount',
            'terciaria_job_id_l4': "ns=2;s=Printers_Inbalnor.p1_l4_terciaria.Devices.p1_l4_terciaria.CurrentProduct",

            'job_trigger_l5': f'ns=2;s=Inbalnor_OPC.generales.p1_l5_job_trigger',
            'turno_l5': f'ns=2;s=Inbalnor_OPC.generales.p1_l5_turno',
            'terciaria_status_l5': f'ns=2;s=Printers_Inbalnor.p1_l5_terciaria.Devices.p1_l5_terciaria.Status',
            'terciaria_counter1_l5': f'ns=2;s=Printers_Inbalnor.p1_l5_terciaria.Devices.p1_l5_terciaria.Counter1',
            'terciaria_counter_total_l5': f'ns=2;s=Printers_Inbalnor.p1_l5_terciaria.Devices.p1_l5_terciaria.TotalCount',
            'terciaria_job_id_l5': "ns=2;s=Printers_Inbalnor.p1_l5_terciaria.Devices.p1_l5_terciaria.CurrentProduct",

        }, 
        'job_trigger_l1':-1,
        'turno_l1':-1,
        'terciaria_status_l1':'Error',
        'terciaria_counter1_l1':-1,
        'terciaria_counter_total_l1':-1,
        'terciaria_job_id_l1':-1,

        'job_trigger_l2':-1,
        'turno_l2':-1,
        'terciaria_status_l2':'Error',
        'terciaria_counter1_l2':-1,
        'terciaria_counter_total_l2':-1,
        'terciaria_job_id_l2':-1,

        'job_trigger_l3':-1,
        'turno_l3':-1,
        'terciaria_status_l3':'Error',
        'terciaria_counter1_l3':-1,
        'terciaria_counter_total_l3':-1,
        'terciaria_job_id_l3':-1,

        'job_trigger_l4':-1,
        'turno_l4':-1,
        'terciaria_status_l4':'Error',
        'terciaria_counter1_l4':-1,
        'terciaria_counter_total_l4':-1,
        'terciaria_job_id_l4':-1,

        'job_trigger_l5':-1,
        'turno_l5':-1,
        'terciaria_status_l5':'Sin impresora',
        'terciaria_counter1_l5':0,
        'terciaria_counter_total_l5':-1,
        'terciaria_job_id_l5': -1,

        'orden_produccion_actual_l1': OrdenProduccion.default(),
        'orden_produccion_actual_l2': OrdenProduccion.default(),
        'orden_produccion_actual_l3': OrdenProduccion.default(),
        'orden_produccion_actual_l4': OrdenProduccion.default(),
        'orden_produccion_actual_l5': OrdenProduccion.default(),
    }

    suscriptores = []

    

    @staticmethod
    def inicializar_managers(django_manager, opc_manager):
        UtilidadGeneral.datos_compartidos["django_manager"] = django_manager
        UtilidadGeneral.datos_compartidos["opc_manager"] = opc_manager
        UtilidadGeneral.datos_compartidos["opc_manager"].init_opcua()

    @staticmethod
    def notificar_suscriptores():
        for objeto in UtilidadGeneral.suscriptores:
            objeto.actualizar_con_datos()

    @staticmethod
    def notificar_suscriptores_por_cambio(tipo_cambio):
        for objeto in UtilidadGeneral.suscriptores:
            if hasattr(objeto, 'actualizar_por_tipo'):
                objeto.actualizar_por_tipo(tipo_cambio)

    @staticmethod
    def suscribir(objeto):
        UtilidadGeneral.suscriptores.append(objeto)

    @staticmethod
    def calcular_turno( orden_produccion: OrdenProduccion ):
        if orden_produccion.id<5:
            return False
        fecha_actual = datetime.now()
        turno_calculado = calcular_turno_con_hora(fecha_actual)
        turno_actual = orden_produccion.turno
        print(f'Linea: {orden_produccion.linea} Turno calculado: {turno_calculado} Turno actual: {turno_actual} Turno calculado > Turno actual: {turno_calculado > turno_actual}')
        return turno_calculado > turno_actual

    

    @staticmethod
    def on_data_changed_opc_manager(name, val):
        if name == 'job_trigger_l1':
            UtilidadGeneral.datos_compartidos["job_trigger_l1"] = val
            
        if name == 'job_trigger_l2':
            UtilidadGeneral.datos_compartidos["job_trigger_l2"] = val

        if name == 'job_trigger_l3':
            UtilidadGeneral.datos_compartidos["job_trigger_l3"] = val

        if name == 'job_trigger_l4':
            UtilidadGeneral.datos_compartidos["job_trigger_l4"] = val

        if name == 'job_trigger_l5':
            UtilidadGeneral.datos_compartidos["job_trigger_l5"] = val
        
        if name == 'turno_l1':
            UtilidadGeneral.datos_compartidos["turno_l1"] = val

        if name == 'turno_l2':
            UtilidadGeneral.datos_compartidos["turno_l2"] = val

        if name == 'turno_l3':
            UtilidadGeneral.datos_compartidos["turno_l3"] = val

        if name == 'turno_l4':
            UtilidadGeneral.datos_compartidos["turno_l4"] = val

        if name == 'turno_l5':
            UtilidadGeneral.datos_compartidos["turno_l5"] = val

        if name == 'terciaria_status_l1':
            UtilidadGeneral.datos_compartidos["terciaria_status_l1"] = val

        if name == 'terciaria_status_l2':
            UtilidadGeneral.datos_compartidos["terciaria_status_l2"] = val

        if name == 'terciaria_status_l3':
            UtilidadGeneral.datos_compartidos["terciaria_status_l3"] = val

        if name == 'terciaria_status_l4':
            UtilidadGeneral.datos_compartidos["terciaria_status_l4"] = val
            
        if name == 'terciaria_status_l5':
            UtilidadGeneral.datos_compartidos["terciaria_status_l5"] = val

        
        if name == 'terciaria_counter1_l1':
            contador_actual = UtilidadGeneral.datos_compartidos["terciaria_counter1_l1"]
            UtilidadGeneral.datos_compartidos["terciaria_counter1_l1"] = val
            if val != None:
                orden = UtilidadGeneral.datos_compartidos["orden_produccion_actual_l1"]
                nuevo_contador = val
                fin_contador_genetal = UtilidadGeneral.datos_compartidos["terciaria_counter_total_l1"]
                check_orden_and_update(orden,nuevo_contador, contador_actual, fin_contador_genetal)
                

        if name == 'terciaria_counter1_l2':
            contador_actual = UtilidadGeneral.datos_compartidos["terciaria_counter1_l2"]
            UtilidadGeneral.datos_compartidos["terciaria_counter1_l2"] = val
            if val != None:
                orden = UtilidadGeneral.datos_compartidos["orden_produccion_actual_l2"]
                nuevo_contador = val
                fin_contador_genetal = UtilidadGeneral.datos_compartidos["terciaria_counter_total_l2"]
                print("🚀 ~ nuevo_contador, contador_actual:", nuevo_contador, contador_actual)
                check_orden_and_update(orden,nuevo_contador, contador_actual, fin_contador_genetal)

        if name == 'terciaria_counter1_l3':
            contador_actual = UtilidadGeneral.datos_compartidos["terciaria_counter1_l3"]
            UtilidadGeneral.datos_compartidos["terciaria_counter1_l3"] = val
            if val != None:
                orden = UtilidadGeneral.datos_compartidos["orden_produccion_actual_l3"]
                nuevo_contador = val
                fin_contador_genetal = UtilidadGeneral.datos_compartidos["terciaria_counter_total_l3"]
                check_orden_and_update(orden,nuevo_contador, contador_actual, fin_contador_genetal)

        if name == 'terciaria_counter1_l4':
            contador_actual = UtilidadGeneral.datos_compartidos["terciaria_counter1_l4"]
            UtilidadGeneral.datos_compartidos["terciaria_counter1_l4"] = val
            if val != None:
                orden = UtilidadGeneral.datos_compartidos["orden_produccion_actual_l4"]
                nuevo_contador = val
                fin_contador_genetal = UtilidadGeneral.datos_compartidos["terciaria_counter_total_l4"]
                check_orden_and_update(orden,nuevo_contador, contador_actual, fin_contador_genetal)


        if name == 'terciaria_job_id_l1':
            UtilidadGeneral.datos_compartidos["terciaria_job_id_l1"] = val
            val = convertir_id_string_a_int(val)
            orden = UtilidadGeneral.datos_compartidos["django_manager"].get_orden_produccion(val)
            UtilidadGeneral.datos_compartidos["orden_produccion_actual_l1"] = orden

        if name == 'terciaria_job_id_l2':
            UtilidadGeneral.datos_compartidos["terciaria_job_id_l2"] = val
            val = convertir_id_string_a_int(val)
            orden = UtilidadGeneral.datos_compartidos["django_manager"].get_orden_produccion(val)
            UtilidadGeneral.datos_compartidos["orden_produccion_actual_l2"] = orden

        if name == 'terciaria_job_id_l3':
            UtilidadGeneral.datos_compartidos["terciaria_job_id_l3"] = val
            val = convertir_id_string_a_int(val)
            orden = UtilidadGeneral.datos_compartidos["django_manager"].get_orden_produccion(val)
            UtilidadGeneral.datos_compartidos["orden_produccion_actual_l3"] = orden

        if name == 'terciaria_job_id_l4':
            UtilidadGeneral.datos_compartidos["terciaria_job_id_l4"] = val
            val = convertir_id_string_a_int(val)
            orden = UtilidadGeneral.datos_compartidos["django_manager"].get_orden_produccion(val)
            UtilidadGeneral.datos_compartidos["orden_produccion_actual_l4"] = orden

        if name == 'terciaria_job_id_l5':
            UtilidadGeneral.datos_compartidos["terciaria_job_id_l5"] = val
            val = convertir_id_string_a_int(val)
            orden = UtilidadGeneral.datos_compartidos["django_manager"].get_orden_produccion(val)
            UtilidadGeneral.datos_compartidos["orden_produccion_actual_l5"] = orden


        if name == 'terciaria_counter_total_l1':
            UtilidadGeneral.datos_compartidos["terciaria_counter_total_l1"] = val

        if name == 'terciaria_counter_total_l2':
            UtilidadGeneral.datos_compartidos["terciaria_counter_total_l2"] = val

        if name == 'terciaria_counter_total_l3':
            UtilidadGeneral.datos_compartidos["terciaria_counter_total_l3"] = val

        if name == 'terciaria_counter_total_l4':
            UtilidadGeneral.datos_compartidos["terciaria_counter_total_l4"] = val

        if name == 'terciaria_counter_total_l5':
            UtilidadGeneral.datos_compartidos["terciaria_counter_total_l5"] = val
        
        
        UtilidadGeneral.notificar_suscriptores()

