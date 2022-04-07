import datetime
import mysql.connector
from mysql.connector import errorcode
import config as cfg
import sys
import requests

traducciones = {
    'Monday': 'L',  
    'Tuesday': 'M',
    'Wednesday': 'I',
    'Thursday': 'J',
    'Friday': 'V',
    'Saturday': 'S',
    'Sunday': 'D',
}

def enviar_notificacion(codigo_usuario, nombre_programa, horario):
    """Esta función se encargará de enviar la notificación al usuario"""
    url = "https://onesignal.com/api/v1/notifications"
    carga = {
	"app_id": "51c63cff-c83b-405e-927b-a9ce3234ec65",
	"include_player_ids": [codigo_usuario],
	"contents": {"en": f"The program {nombre_programa} starts at {horario}", "es": f"El programa {nombre_programa} comienza a la{'s' if horario != '01:00' else ''} {horario}"},
	"headings": {"en": "Program Notification", "es": "Notificación de Programa"}
    }
    respuesta = requests.post(url, headers={"Content-Type": "application/json; charset=utf-8", "Authorization": "Basic YTQzM2RiOTQtYzUxYy00MTlmLWE3NTQtODhiYWJiYmFhYTBm"}, json=carga)

def consultar_notificaciones(fecha_actual, cnx):
    """Esta función checará si existe alguna notificación que se tiene que mandar"""
    #TODO: Hacer que el comando seleccione los programas que empiezan en la siguiente hora
    #TODO: Checar si solo vamos a generar una notificación para una hora antes
    
    comando = ("SELECT codigo_usuario, nombre_programa, horario FROM radiocucei.notificaciones WHERE horario = %s AND dia = %s")
    cursor = cnx.cursor()
    dia = traducciones[fecha_actual.strftime("%A")]
    hora = fecha_actual.hour
    valores = (f"{hora}:00", dia)
    cursor.execute(comando, valores)
    for (codigo, nombre_programa, horario) in cursor:
        enviar_notificacion(codigo, nombre_programa, horario)

def main():
    try:
        cnx = mysql.connector.connect(**cfg.mysql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            sys.exit(1)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            sys.exit(1)
        else:
            print(err)
            sys.exit(1)
    consultar_notificaciones(datetime.datetime.now(), cnx)
    cnx.close()
    sys.exit(0)

if __name__ == "__main__":
    main()